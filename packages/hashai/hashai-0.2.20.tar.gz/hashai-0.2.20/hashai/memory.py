# hashai/memory.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import json
from abc import ABC, abstractmethod
from .llm.base_llm import BaseLLM

class MemoryEntry(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict = Field(default_factory=dict)

class BaseMemoryStorage(ABC):
    @abstractmethod
    def store(self, entry: MemoryEntry):
        pass
    
    @abstractmethod
    def retrieve(self, query: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        pass

class InMemoryStorage(BaseMemoryStorage):
    def __init__(self):
        self.history: List[MemoryEntry] = []
    
    def store(self, entry: MemoryEntry):
        self.history.append(entry)
    
    def retrieve(self, query: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        return self.history[-limit:]

class Memory:
    def __init__(
        self,
        storage: BaseMemoryStorage = InMemoryStorage(),
        max_context_length: int = 4000,
        summarization_threshold: int = 3000
    ):
        self.storage = storage
        self.max_context_length = max_context_length
        self.summarization_threshold = summarization_threshold
        self._current_context = ""

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        entry = MemoryEntry(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.storage.store(entry)
        self._manage_context()

    def get_context(self, llm: Optional[BaseLLM] = None) -> str:
        if len(self._current_context) < self.summarization_threshold:
            return self._current_context
        
        # Automatic summarization when context grows too large
        if llm:
            return self.summarize(llm)
        return self._current_context[:self.max_context_length]
    def _manage_context(self):
        # Include roles in the conversation history
        full_history = "\n".join([f"{e.role}: {e.content}" for e in self.storage.retrieve()])
        if len(full_history) > self.max_context_length:
            self._current_context = full_history[-self.max_context_length:]
        else:
            self._current_context = full_history

    def summarize(self, llm: BaseLLM) -> str:
        # Include roles in the history for summarization
        history = "\n".join([f"{e.role}: {e.content}" for e in self.storage.retrieve()])
        prompt = f"""
        Summarize this conversation history maintaining key details and references:
        {history[-self.summarization_threshold:]}
        """
        self._current_context = llm.generate(prompt)
        return self._current_context

    def clear(self):
        self.storage = InMemoryStorage()
        self._current_context = ""

class FileStorage(BaseMemoryStorage):
    def __init__(self, file_path: str = "memory.json"):
        self.file_path = file_path
        self.history = self._load_from_file()

    def _load_from_file(self) -> List[MemoryEntry]:
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [MemoryEntry(**entry) for entry in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self):
        with open(self.file_path, "w") as f:
            data = [entry.dict() for entry in self.history]
            json.dump(data, f, default=str)

    def store(self, entry: MemoryEntry):
        self.history.append(entry)
        self._save_to_file()

    def retrieve(self, query: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        return self.history[-limit:]