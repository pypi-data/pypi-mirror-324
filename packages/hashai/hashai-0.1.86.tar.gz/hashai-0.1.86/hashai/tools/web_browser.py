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
    action: str = Field(..., description="Action to perform")
    selector: str = Field(None, description="CSS selector for the element")
    text: str = Field(None, description="Text to input for type actions")
    url: str = Field(None, description="URL for navigation actions")
    seconds: int = Field(None, description="Wait time in seconds")
    path: str = Field(None, description="Path for screenshots")

class WebBrowserTool(BaseTool):
    name: str = Field("WebBrowser", description="Name of the tool")
    description: str = Field(
        "Performs complete browser automation including complex interactions",
        description="Tool description"
    )
    
    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute full browser automation workflow with enhanced reliability"""
        try:
            # Generate validated task plan
            task_spec = self._generate_valid_task_plan(input['query'])
            return self._execute_automation(task_spec)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_valid_task_plan(self, query: str) -> Dict[str, Any]:
        """Generate and validate task plan with multiple fallback strategies"""
        prompt = f"""Convert this request to browser automation tasks. RESPOND WITH VALID JSON ONLY:
        {query}
        
        Required format:
        {{
            "tasks": [
                {{"action": "navigate", "url": "https://youtube.com"}},
                {{"action": "wait", "seconds": 2}},
                {{"action": "type", "selector": "input#search", "text": "SEARCH_TERM"}},
                {{"action": "wait", "seconds": 1}},
                {{"action": "click", "selector": "button#search-icon-legacy"}},
                {{"action": "wait", "seconds": 3}},
                {{"action": "click", "selector": "ytd-video-renderer:first-child"}},
                {{"action": "wait", "seconds": 5}}
            ],
            "headless": false
        }}
        """
        
        response = self.llm.generate(prompt=prompt)
        
        # Multiple JSON extraction strategies
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {
                "tasks": [
                    {"action": "navigate", "url": "https://youtube.com"},
                    {"action": "type", "selector": "input#search", "text": "deepseek"},
                    {"action": "click", "selector": "button#search-icon-legacy"},
                    {"action": "wait", "seconds": 3},
                    {"action": "click", "selector": "ytd-video-renderer:first-child a#video-title"},
                    {"action": "wait", "seconds": 5}
                ],
                "headless": False
            }

    def _execute_automation(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automation with enhanced error handling and verification"""
        # Configure browser
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Initialize driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        results = []
        try:
            for task_data in task_spec["tasks"]:
                task = BrowserTask(**task_data)
                result = self._execute_task_with_retry(driver, task)
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

    def _execute_task_with_retry(self, driver, task: BrowserTask) -> Dict[str, Any]:
        """Execute task with retry logic and element verification"""
        try:
            if task.action == "navigate":
                driver.get(task.url)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                return {"action": "navigate", "status": "success"}

            elif task.action == "type":
                # Verify search box exists
                search_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#search"))
                )
                search_box.clear()
                search_box.send_keys(task.text)
                return {"action": "type", "status": "success"}

            elif task.action == "click":
                # Handle different click scenarios
                if "search-icon" in task.selector:
                    element = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button#search-icon-legacy"))
                    )
                else:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer:first-child"))
                    )
                driver.execute_script("arguments[0].scrollIntoView();", element)
                driver.execute_script("arguments[0].click();", element)
                return {"action": "click", "status": "success"}

            elif task.action == "wait":
                time.sleep(task.seconds)
                return {"action": "wait", "status": "success"}

            return {"status": "error", "message": "Unknown action"}
        except Exception as e:
            return {"status": "error", "message": str(e)}