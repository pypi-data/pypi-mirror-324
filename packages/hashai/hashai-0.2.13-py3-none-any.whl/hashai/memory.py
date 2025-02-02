# hashai/memory.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from abc import ABC, abstractmethod

class MemoryEntry(BaseModel):
    role: str                 # "user" or "assistant"
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
        # For simplicity, we ignore the query and return the last "limit" entries.
        return self.history[-limit:]

class Memory:
    def __init__(
        self,
        storage: Optional[BaseMemoryStorage] = None,
        max_context_length: int = 4000,
        summarization_threshold: int = 3000
    ):
        self.storage = storage if storage is not None else InMemoryStorage()
        self.max_context_length = max_context_length
        self.summarization_threshold = summarization_threshold
        self._current_context = ""

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        entry = MemoryEntry(role=role, content=content, metadata=metadata or {})
        self.storage.store(entry)
        self._manage_context()

    def _manage_context(self):
        full_history = "\n".join([entry.content for entry in self.storage.retrieve()])
        if len(full_history) > self.max_context_length:
            self._current_context = full_history[-self.max_context_length:]
        else:
            self._current_context = full_history

    def get_context(self, llm=None) -> str:
        # If the current context is too long, summarize it (if an LLM is provided)
        if len(self._current_context) >= self.summarization_threshold:
            if llm:
                return self.summarize(llm)
            return self._current_context[:self.max_context_length]
        return self._current_context

    def summarize(self, llm) -> str:
        # Create a prompt that asks the LLM to summarize the conversation history.
        history = "\n".join([entry.content for entry in self.storage.retrieve()])
        prompt = f"Summarize the following conversation while keeping all key details:\n{history[-self.summarization_threshold:]}"
        # Note: This assumes your LLM’s generate() method works synchronously.
        self._current_context = llm.generate(prompt)
        return self._current_context

    def clear(self):
        self.storage = InMemoryStorage()
        self._current_context = ""
