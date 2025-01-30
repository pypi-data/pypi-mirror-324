# web_browser.py
from typing import Dict, Any
from pydantic import Field
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .base_tool import BaseTool
import json
import time

class WebBrowserTool(BaseTool):
    name: str = "WebBrowser"
    description: str = (
        "A web browsing tool that can open URLs, interact with web pages, "
        "and perform complex browsing tasks with real browser automation."
    )
    
    def execute(self, input: Dict[str, Any]) -> str:
        """
        Execute complex browser automation tasks.
        
        Parameters:
            input (Dict):
                - tasks: List of actions to perform
                - headless: Run browser in background (default: False)
                
        Example input:
        {
            "tasks": [
                {"action": "navigate", "url": "https://youtube.com"},
                {"action": "type", "selector": "input#search", "text": "deepseek"},
                {"action": "click", "selector": "button#search-icon-legacy"},
                {"action": "wait", "seconds": 3},
                {"action": "click", "selector": "a#video-title:first-child"}
            ],
            "headless": False
        }
        """
        try:
            options = Options()
            if input.get("headless", False):
                options.add_argument("--headless")
            else:
                options.add_argument("--start-maximized")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            result = []
            for task in input.get("tasks", []):
                action = task.get("action")
                
                if action == "navigate":
                    driver.get(task["url"])
                    result.append(f"Navigated to {task['url']}")
                    
                elif action == "type":
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, task["selector"]))
                    )
                    element.send_keys(task["text"])
                    result.append(f"Typed '{task['text']}' into {task['selector']}")
                    
                elif action == "click":
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, task["selector"]))
                    )
                    element.click()
                    result.append(f"Clicked {task['selector']}")
                    
                elif action == "wait":
                    time.sleep(task.get("seconds", 2))
                    result.append(f"Waited {task['seconds']} seconds")
                    
                elif action == "screenshot":
                    driver.save_screenshot(task.get("path", "screenshot.png"))
                    result.append("Saved screenshot")
                    
                elif action == "scroll":
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    result.append("Scrolled to bottom")
                    
            driver.quit()
            return json.dumps({"results": result, "status": "success"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})