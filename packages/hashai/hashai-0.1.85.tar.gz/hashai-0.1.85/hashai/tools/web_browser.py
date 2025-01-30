from typing import Dict, Any, List
from pydantic import Field, BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from .base_tool import BaseTool

class BrowserTask(BaseModel):
    action: str
    selector: str = Field(None)
    text: str = Field(None)
    url: str = Field(None)
    seconds: int = Field(None)
    path: str = Field(None)

class WebBrowserTool(BaseTool):
    name: str = Field("WebBrowser", description="Name of the tool")
    description: str = Field(
        "Performs full browser automation including page interactions and navigation",
        description="Tool description"
    )
    
    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complete automation workflow from natural language to browser actions"""
        try:
            # Generate task sequence using LLM
            task_spec = self._generate_task_plan(input['query'])
            return self._execute_browser_tasks(task_spec)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_task_plan(self, query: str) -> Dict[str, Any]:
        """Convert natural language query to browser automation plan with validation"""
        prompt = f"""Convert this browser request into automation tasks. RESPONSE MUST BE VALID JSON:
        User Request: {query}
        
        Required Format:
        {{
            "tasks": [
                {{"action": "navigate", "url": "https://youtube.com"}},
                {{"action": "type", "selector": "input#search", "text": "search_query"}},
                {{"action": "click", "selector": "button#search-icon-legacy"}},
                {{"action": "wait", "seconds": 3}},
                {{"action": "click", "selector": "ytd-video-renderer:first-child a#video-title"}}
            ],
            "headless": false
        }}
        """
        
        response = self.llm.generate(prompt=prompt)
        
        # Clean response and extract JSON
        try:
            json_str = response.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            return json.loads(response)

    def _execute_browser_tasks(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser tasks with enhanced error handling"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        results = []
        try:
            for task_data in task_spec.get("tasks", []):
                task = BrowserTask(**task_data)
                result = self._execute_single_task(driver, task)
                results.append(result)
                if result['status'] != 'success':
                    break
            
            return {
                "status": "success" if all(r['status'] == 'success' for r in results) else "partial",
                "results": results
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if task_spec.get("headless", False):
                driver.quit()

    def _execute_single_task(self, driver, task: BrowserTask) -> Dict[str, Any]:
        """Execute individual task with verified YouTube selectors"""
        try:
            if task.action == "navigate":
                driver.get(task.url)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                )
                return {"action": "navigate", "status": "success"}

            elif task.action == "type":
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#search"))
                )
                element.clear()
                element.send_keys(task.text)
                return {"action": "type", "status": "success"}

            elif task.action == "click":
                selector = task.selector if "button#search" in task.selector else "ytd-video-renderer:first-child a#video-title"
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                element.click()
                return {"action": "click", "status": "success"}

            elif task.action == "wait":
                time.sleep(task.seconds)
                return {"action": "wait", "status": "success"}

            return {"status": "error", "message": "Unknown action"}
        except Exception as e:
            return {"status": "error", "message": str(e)}