# web_browser.py
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
    selector: str = None
    text: str = None
    url: str = None
    seconds: int = None
    path: str = None

class WebBrowserTool(BaseTool):
    name: str = "WebBrowser"
    description: str = "Performs full browser automation including page interactions and navigation"
    
    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complete automation workflow from natural language to browser actions"""
        try:
            # Generate task sequence using LLM
            task_spec = self._generate_task_plan(input['query'])
            return self._execute_browser_tasks(task_spec)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_task_plan(self, query: str) -> Dict[str, Any]:
        """Convert natural language query to browser automation plan"""
        prompt = f"""Convert this browser request into automation tasks:
        {query}
        
        Available actions: navigate, click, type, wait, scroll, screenshot
        Response format: JSON with 'tasks' array and 'headless' flag
        Example response for "open youtube and search cats":
        {{
            "tasks": [
                {{"action": "navigate", "url": "https://youtube.com"}},
                {{"action": "type", "selector": "input#search", "text": "cats"}},
                {{"action": "click", "selector": "button#search-icon-legacy"}},
                {{"action": "wait", "seconds": 3}},
                {{"action": "click", "selector": "a#video-title:first-child"}},
                {{"action": "wait", "seconds": 5}}
            ],
            "headless": false
        }}
        """
        
        response = self.llm.generate(prompt=prompt)
        return json.loads(response)

    def _execute_browser_tasks(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser tasks with proper element waiting and error handling"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        
        if task_spec.get("headless", False):
            options.add_argument("--headless")

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
                if result['status'] == 'error':
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
        """Execute individual browser task with robust error handling"""
        try:
            if task.action == "navigate":
                driver.get(task.url)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                return {"action": "navigate", "url": task.url, "status": "success"}

            elif task.action == "type":
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, task.selector))
                )
                element.clear()
                element.send_keys(task.text)
                return {"action": "type", "selector": task.selector, "status": "success"}

            elif task.action == "click":
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, task.selector))
                )
                element.click()
                return {"action": "click", "selector": task.selector, "status": "success"}

            elif task.action == "wait":
                time.sleep(task.seconds)
                return {"action": "wait", "seconds": task.seconds, "status": "success"}

            return {"status": "error", "message": "Unknown action"}
        except Exception as e:
            return {"status": "error", "message": str(e), "action": task.action}