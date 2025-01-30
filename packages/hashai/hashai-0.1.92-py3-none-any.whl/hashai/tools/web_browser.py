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
from bs4 import BeautifulSoup
import base64
import json
import time
import re
from .base_tool import BaseTool
import validators

class BrowserPlan(BaseModel):
    tasks: List[Dict[str, Any]] = Field(
        ...,
        description="List of automation tasks to execute"
    )

class BrowserState(BaseModel):
    html: str = Field(..., description="Current page HTML")
    url: str = Field(..., description="Current page URL")

class BrowserTask(BaseModel):
    action: str = Field(..., description="Action to perform (navigate, click, type, etc.)")
    target: str = Field(..., description="Natural language description of target element")
    value: Optional[str] = Field(None, description="Input text (if needed)")

class WebBrowserTool(BaseTool):
    name: str = Field("WebBrowser", description="Name of the tool")
    description: str = Field(
        "Advanced web automation tool with dynamic element detection",
        description="Tool description"
    )
    
    def execute(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute dynamic web automation workflow"""
        try:
            driver = self._init_browser(input.get("headless", False))
            state = BrowserState(html="", url="about:blank")
            results = []
            
            # Generate initial plan
            plan = self._generate_plan(input['query'], state)
            
            for task in plan.tasks:
                task_obj = BrowserTask(**task)
                result = self._execute_task(driver, task_obj, state)
                results.append(result)
                
                if not result['success']:
                    break
                    
                # Update state after each action
                state = self._capture_state(driver)
                
            driver.quit()
            return {"status": "success", "results": results}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def _generate_plan(self, query: str, state: BrowserState) -> BrowserPlan:
        """Generate adaptive execution plan using the LLM."""
        prompt = f"""Generate web automation plan for: {query}
    
        Current page: {state.url}
        Available elements: {self._extract_key_elements(state.html)}
    
        Response format:
        {{
            "tasks": [
                {{
                    "action": "navigate|click|type|etc",
                    "target": "element description",
                    "value": "input text (if needed)"
                }}
            ]
        }}
        """
    
        response = self.llm.generate(prompt=prompt)
        return self._parse_plan(response)
    def _parse_plan(self, response: str) -> BrowserPlan:
        """Parse and validate the generated plan."""
        try:
            # Clean response and extract JSON
            json_str = re.search(r'\{.*\}', response, re.DOTALL).group()
            plan_data = json.loads(json_str)
        
            # Validate and return as BrowserPlan
            return BrowserPlan(**plan_data)
    
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            # Fallback plan if parsing fails
            print(f"Error parsing plan: {e}. Using fallback plan.")
            return BrowserPlan(tasks=[{
                "action": "navigate",
                "target": "YouTube homepage",
                "value": "https://www.youtube.com"
            }])
        
    def _init_browser(self, headless: bool) -> webdriver.Chrome:
        """Initialize browser with advanced options."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
        if headless:
            options.add_argument("--headless=new")
    
        # Install ChromeDriver automatically using WebDriverManager
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    

    def _execute_task(self, driver, task: BrowserTask, state: BrowserState) -> Dict[str, Any]:
        """Execute a single browser task."""
        try:
            if task.action == "navigate":
                # Validate the URL
                url = task.value
                if not validators.url(url):
                    return self._create_result(task, success=False, message=f"Invalid URL: {url}")
            
                # Navigate to the specified URL
                driver.get(url)
                return self._create_result(task, success=True, message=f"Navigated to {url}")
        
            elif task.action == "click":
                # Detect the target element and perform a click
                element_info = self._detect_element(task.target, state)
                if element_info:
                    self._perform_click(driver, element_info)
                    return self._create_result(task, success=True, message=f"Clicked on {task.target}")
                else:
                    return self._create_result(task, success=False, message=f"Could not find element: {task.target}")
        
            elif task.action == "type":
                # Detect the target input field and type the value
                element_info = self._detect_element(task.target, state)
                if element_info:
                    selector = element_info.get('selector')
                    if selector:
                        element = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        element.clear()
                        element.send_keys(task.value)
                        return self._create_result(task, success=True, message=f"Typed '{task.value}' into {task.target}")
                    else:
                        return self._create_result(task, success=False, message=f"Could not find element: {task.target}")
                else:
                    return self._create_result(task, success=False, message=f"Could not find element: {task.target}")
        
            else:
                return self._create_result(task, success=False, message=f"Unsupported action: {task.action}")
    
        except Exception as e:
            return self._create_result(task, success=False, message=str(e))
    
    def _detect_element(self, description: str, state: BrowserState) -> Dict[str, Any]:
        """Detect element using HTML analysis."""
        # Analyze HTML structure to find relevant elements
        html_elements = self._analyze_html(description, state.html)
        
        # Select the best matching element
        return self._select_best_element(html_elements)
    
    def _select_best_element(self, elements: List[Dict]) -> Dict[str, Any]:
        """Select the best matching element from the list."""
        if not elements:
            return None
        
        # Simple heuristic: Choose the first element with a valid selector
        for element in elements:
            if element.get("selector"):
                return element
        
        return None
    
    def _analyze_html(self, description: str, html: str) -> List[Dict]:
        """Analyze HTML structure to find relevant elements."""
        prompt = f"""Find CSS selectors matching: {description}
        HTML structure:
        {self._simplify_html(html)}
        
        Return JSON format:
        {{
            "elements": [
                {{
                    "selector": "css selector",
                    "reason": "matching logic"
                }}
            ]
        }}
        """
        
        response = self.llm.generate(prompt=prompt)
        try:
            data = json.loads(response)
            return data.get("elements", [])
        except json.JSONDecodeError:
            return []
    def _extract_key_elements(self, html: str) -> str:
        """Extract key interactive elements from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        elements = []
    
        # Find all interactive elements
        for tag in soup.find_all(['a', 'button', 'input', 'form', 'select', 'textarea']):
            element_info = {
                'tag': tag.name,
                'id': tag.get('id'),
                'class': ' '.join(tag.get('class', [])),
                'text': tag.text.strip()[:50],  # Limit text length
                'type': tag.get('type'),
                'name': tag.get('name')
            }
            elements.append(json.dumps(element_info))
    
        return "\n".join(elements[:15])  # Return top 15 elements
    
    def _simplify_html(self, html: str) -> str:
        """Simplify HTML for LLM processing."""
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style', 'svg', 'img']):
            tag.decompose()
            
        simplified = []
        for element in soup.find_all(True):
            attrs = {
                'id': element.get('id'),
                'class': ' '.join(element.get('class', [])),
                'name': element.get('name'),
                'type': element.get('type'),
                'role': element.get('role'),
                'text': element.text.strip()[:50]
            }
            simplified.append(f"<{element.name} {json.dumps(attrs)}>")
            
        return "\n".join(simplified[:200])  # Limit to first 200 elements
    
    def _capture_state(self, driver) -> BrowserState:
        """Capture current page state."""
        return BrowserState(
            html=driver.page_source,
            url=driver.current_url
        )
    
    def _perform_click(self, driver, element_info: Dict):
        """Smart click implementation."""
        selector = element_info.get('selector')
        if selector:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)
            element.click()
    
    def _create_result(self, task: BrowserTask, success: bool, message: str = "") -> Dict:
        return {
            "action": task.action,
            "target": task.target,
            "success": success,
            "message": message
        }