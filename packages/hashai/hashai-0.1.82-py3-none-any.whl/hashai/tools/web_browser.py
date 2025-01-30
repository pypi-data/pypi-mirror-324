from typing import Dict, Any
from pydantic import Field
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .base_tool import BaseTool
import json

class WebBrowserTool(BaseTool):
    name: str = "WebBrowser"
    description: str = (
        "A web browsing tool that can open URLs, retrieve web content, "
        "interact with web pages, and extract specific information. "
        "Supports both static content and JavaScript-rendered pages."
    )
    
    headers: Dict[str, str] = Field(
        default_factory=lambda: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        description="HTTP headers for web requests"
    )
    
    def execute(self, input: Dict[str, Any]) -> str:
        """
        Execute a web browsing action with support for both static and dynamic content.
        
        Parameters:
            input (Dict):
                - action: "get", "search", "extract", or "interact"
                - url: URL to visit (for get/extract actions)
                - query: Search query (for search action)
                - selector: CSS selector for element extraction
                - interaction: Dictionary describing interaction (type, selector, value)
                - render_js: Whether to use headless browser for JavaScript rendering (default: False)
                
        Returns:
            str: Result of the web browsing operation
        """
        try:
            action = input.get("action", "get")
            render_js = input.get("render_js", False)
            
            if action == "get":
                return self._fetch_content(input["url"], render_js)
            elif action == "search":
                return self._google_search(input["query"])
            elif action == "extract":
                return self._extract_content(input["url"], input["selector"], render_js)
            elif action == "interact":
                return self._interact_with_page(input["url"], input["interaction"], render_js)
            else:
                return f"Invalid action: {action}"
                
        except Exception as e:
            return f"Web browsing error: {str(e)}"

    def _fetch_content(self, url: str, render_js: bool = False) -> str:
        """Fetch web content with optional JavaScript rendering"""
        if render_js:
            return self._fetch_with_selenium(url)
        else:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return self._parse_content(response.text)

    def _fetch_with_selenium(self, url: str) -> str:
        """Use headless Chrome to render JavaScript content"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            return self._parse_content(driver.page_source)

    def _parse_content(self, html: str) -> str:
        """Clean and structure HTML content"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()
            
        # Extract main content
        main_content = soup.find("main") or soup.find("article") or soup.body
        return main_content.get_text(separator="\n", strip=True) if main_content else ""

    def _google_search(self, query: str) -> str:
        """Perform a Google search and return top results"""
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        response = requests.get(search_url, headers=self.headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for result in soup.select("div.g")[:5]:
            link = result.select_one("a")
            if link and link["href"]:
                results.append({
                    "title": link.text,
                    "url": link["href"],
                    "snippet": result.get_text(separator=" ", strip=True)
                })
                
        return json.dumps({"results": results}, indent=2)

    def _extract_content(self, url: str, selector: str, render_js: bool) -> str:
        """Extract specific content using CSS selector"""
        content = self._fetch_content(url, render_js)
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(selector)
        return "\n".join([elem.get_text(strip=True) for elem in elements])

    def _interact_with_page(self, url: str, interaction: Dict, render_js: bool) -> str:
        """Interact with page elements using Selenium"""
        if not render_js:
            return "Page interaction requires JavaScript rendering (set render_js=True)"
            
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        
        try:
            driver.get(url)
            
            # Find element
            element = driver.find_element_by_css_selector(interaction["selector"])
            
            # Perform action
            action_type = interaction["type"]
            if action_type == "click":
                element.click()
            elif action_type == "input":
                element.send_keys(interaction["value"])
            elif action_type == "submit":
                element.submit()
                
            # Wait for page update
            driver.implicitly_wait(2)
            return self._parse_content(driver.page_source)
            
        finally:
            driver.quit()