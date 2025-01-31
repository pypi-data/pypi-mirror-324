# web_browser.py
from typing import Dict, Any, List, Optional
from pydantic import Field, BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
import json
import time
import re
import logging
from .base_tool import BaseTool
import validators
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

class BrowserPlan(BaseModel):
    tasks: List[Dict[str, Any]] = Field(
        ...,
        description="List of automation tasks to execute"
    )

class WebBrowserTool(BaseTool):
    name: str = Field("WebBrowser", description="Name of the tool")
    description: str = Field(
        "Universal web automation tool with enhanced dynamic handling",
        description="Tool description"
    )
    
    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute dynamic web automation workflow"""
        driver = None
        try:
            driver = self._init_browser(input.get("headless", False))
            results = []
            current_url = ""

            # Generate initial plan
            plan = self._generate_plan(input['query'], current_url)
            
            for task in plan.tasks:
                result = self._execute_safe_task(driver, task)
                results.append(result)
                
                if not result['success']:
                    break
                    
                # Update context for next tasks
                current_url = driver.current_url

            return {"status": "success", "results": results}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if driver:
                driver.quit()

    def _init_browser(self, headless: bool) -> webdriver.Chrome:
        """Initialize browser with enhanced options"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-notifications")
        options.add_argument("--force-device-scale-factor=1")
        
        if headless:
            options.add_argument("--headless=new")
            
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def _generate_plan(self, query: str, current_url: str) -> BrowserPlan:
        """Generate adaptive execution plan using LLM with retry mechanism"""
        for attempt in range(3):
            try:
                prompt = f"""Generate browser automation plan for: {query}
                
                Current URL: {current_url or 'No page loaded yet'}
                
                Required JSON format:
                {{
                    "tasks": [
                        {{
                            "action": "navigate|click|type|wait|scroll",
                            "selector": "CSS selector (use # for IDs)",
                            "value": "input text/URL/seconds",
                            "description": "action purpose"
                        }}
                    ]
                }}
                
                Important guidelines:
                - For YouTube search: use selector ".ytSearchboxComponentInput"
                - After navigation: include wait(3)
                - For typing: clear field first
                - For clicks: verify element visibility
                """
                
                response = self.llm.generate(prompt=prompt)
                return self._parse_plan(response)
                
            except Exception as e:
                logger.error(f"Plan generation attempt {attempt+1} failed: {e}")
                time.sleep(1)
                
        return BrowserPlan(tasks=[])

    def _parse_plan(self, response: str) -> BrowserPlan:
        """Enhanced JSON parsing with schema validation"""
        try:
            # Normalize response format
            clean_response = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", response)
            json_str = re.search(r'\{.*\}', clean_response, re.DOTALL).group()
            plan_data = json.loads(json_str)
            
            # Validate task structure
            validated_tasks = []
            for task in plan_data.get("tasks", []):
                if not isinstance(task, dict):
                    continue
                validated_tasks.append({
                    "action": str(task.get("action", "")).lower(),
                    "selector": str(task.get("selector", "")),
                    "value": str(task.get("value", "")),
                    "description": str(task.get("description", ""))
                })
            
            return BrowserPlan(tasks=validated_tasks)
            
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Plan parsing failed: {e}")
            return BrowserPlan(tasks=[])

    def _execute_safe_task(self, driver, task: Dict) -> Dict[str, Any]:
        """Execute task with comprehensive error handling and retries"""
        for attempt in range(3):
            try:
                result = self._execute_task(driver, task)
                if result['success']:
                    return result
                time.sleep(1)  # Wait before retry
            except StaleElementReferenceException:
                logger.warning(f"Stale element reference, retrying {task}")
                
        return self._execute_task(driver, task)  # Final attempt

    def _execute_task(self, driver, task: Dict) -> Dict[str, Any]:
        """Core task execution with enhanced element handling"""
        action = task["action"].lower()
        selector = task.get("selector", "")
        value = task.get("value", "")
        
        try:
            if action == "navigate":
                return self._handle_navigation(driver, value)
                
            elif action == "click":
                return self._handle_click(driver, selector)
                
            elif action == "type":
                return self._handle_typing(driver, selector, value)
                
            elif action == "wait":
                return self._handle_wait(value)
                
            elif action == "scroll":
                return self._handle_scroll(driver, selector)
                
            return {
                "action": action,
                "success": False,
                "message": f"Unsupported action: {action}"
            }
            
        except Exception as e:
            return {
                "action": action,
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def _handle_navigation(self, driver, url: str) -> Dict[str, Any]:
        """Robust navigation handler with enhanced validation"""
        try:
            # Clean and validate URL
            if not url:
                return {
                    "action": "navigate",
                    "success": False,
                    "message": "Empty URL provided"
                }

            # Remove surrounding quotes and whitespace
            clean_url = url.strip(" '\"")
            
            # Add scheme if missing
            if not clean_url.startswith(("http://", "https://")):
                clean_url = f"https://{clean_url}"

            # Validate URL structure
            if not validators.url(clean_url):
                return {
                    "action": "navigate",
                    "success": False,
                    "message": f"Invalid URL format: {clean_url}"
                }

            # Normalize URL path
            parsed = urlparse(clean_url)
            normalized_url = urlunparse(parsed._replace(path=parsed.path.rstrip('/')))

            # Execute navigation
            driver.get(normalized_url)
            
            # Wait for both document readiness and basic content
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for body element
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            return {
                "action": "navigate",
                "success": True,
                "message": f"Navigated to {normalized_url}"
            }
            
        except Exception as e:
            return {
                "action": "navigate",
                "success": False,
                "message": f"Navigation failed: {type(e).__name__} - {str(e)}"
            }

    def _handle_click(self, driver, selector: str) -> Dict[str, Any]:
        """Enhanced click handler for dynamic elements"""
        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            # Ensure element is in view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # Click using JavaScript to avoid overlay issues
            driver.execute_script("arguments[0].click();", element)
            return {
                "action": "click",
                "success": True,
                "message": f"Clicked element: {selector}"
            }
        except Exception as e:
            return {
                "action": "click",
                "success": False,
                "message": f"Click failed: {str(e)}"
            }

    def _handle_typing(self, driver, selector: str, text: str) -> Dict[str, Any]:
        """Enhanced typing handler with element state validation"""
        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            
            # Clear existing text properly
            element.send_keys("\b" * 100)  # Clear using backspaces
            element.clear()  # Standard clear
            
            # Type text with delays to mimic human input
            for char in text:
                element.send_keys(char)
                time.sleep(0.05)
                
            return {
                "action": "type",
                "success": True,
                "message": f"Typed '{text}' into {selector}"
            }
        except Exception as e:
            return {
                "action": "type",
                "success": False,
                "message": f"Typing failed: {str(e)}"
            }

    def _handle_wait(self, seconds: str) -> Dict[str, Any]:
        """Improved wait handler with validation"""
        try:
            wait_time = min(float(seconds), 10)  # Max 10 seconds wait
            time.sleep(wait_time)
            return {
                "action": "wait",
                "success": True,
                "message": f"Waited {wait_time} seconds"
            }
        except ValueError:
            return {
                "action": "wait",
                "success": False,
                "message": "Invalid wait time"
            }

    def _handle_scroll(self, driver, selector: str) -> Dict[str, Any]:
        """Smart scroll handler with element detection"""
        try:
            if selector:
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                    element
                )
            else:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                
            return {
                "action": "scroll",
                "success": True,
                "message": f"Scrolled to {selector or 'page center'}"
            }
        except Exception as e:
            return {
                "action": "scroll",
                "success": False,
                "message": f"Scroll failed: {str(e)}"
            }