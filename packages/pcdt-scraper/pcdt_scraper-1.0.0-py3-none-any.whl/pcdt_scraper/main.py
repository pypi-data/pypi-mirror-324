import PyChromeDevTools
from bs4 import BeautifulSoup, Tag
from typing import Optional, List, Union
from datetime import datetime
from requests.exceptions import ConnectionError

class ElementWrapper:
    def __init__(self, element: Optional[Union[BeautifulSoup, Tag]] = None):
        self.element = element

    def text(self) -> str:
        """Get the text content of the element"""
        try:
            if self.element:
                return self.element.get_text(strip=True)
            return ""
        except Exception as e:
            print(f"Failed to get text: {str(e)}")
            return ""

    def get_attribute(self, attribute: str) -> str:
        """Get the value of specified attribute"""
        try:
            if self.element:
                return self.element.get(attribute, "")
            return ""
        except Exception as e:
            print(f"Failed to get attribute: {str(e)}")
            return ""

    def is_displayed(self) -> bool:
        """Check if element exists"""
        return self.element is not None

    def get_html(self) -> str:
        """Get the HTML content of the element"""
        try:
            if self.element:
                return str(self.element)
            return ""
        except Exception as e:
            print(f"Failed to get HTML: {str(e)}")
            return ""

class Elements:
    def __init__(self, elements: List[Union[BeautifulSoup, Tag]] = None):
        self.elements = [ElementWrapper(elem) for elem in (elements or [])]

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

class WebScraper:
    def __init__(self, parser: str = 'html.parser'):
        try:
            self.chrome = PyChromeDevTools.ChromeInterface()
        except ConnectionError:
            print("Error: Got ConnectionError, it seems your chrome remote instance is not running.")
            return
        self.parser = parser
        self.setup_browser()

    def setup_browser(self):
        try:
            self.chrome.Network.enable()
            self.chrome.Page.enable()
            self.chrome.DOM.enable()
            
            self.chrome.Network.setUserAgentOverride(
                userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"
            )
        except Exception as e:
            print(f"Failed to setup browser: {str(e)}")
            raise

    def get(self, url: str, timeout: int = 60) -> bool:
        """Navigate to a webpage (Selenium-style)"""
        return self.navigate_to_page(url, timeout)

    def navigate_to_page(self, url: str, timeout: int = 60) -> bool:
        try:
            self.chrome.Page.navigate(url=url)
            try:
                self.chrome.wait_event("Page.loadEventFired", timeout=timeout)
                return True
            except TimeoutError:
                print(f"Page load timed out after {timeout} seconds")
                return False
        except Exception as e:
            print(f"Navigation failed: {str(e)}")
            return False

    def get_page_source(self) -> Optional[BeautifulSoup]:
        """Get page source (Selenium-style)"""
        return self.get_page_content()

    def get_page_content(self) -> Optional[BeautifulSoup]:
        try:
            root = self.chrome.DOM.getDocument()
            
            if isinstance(root, tuple):
                root_data = root[0]
            else:
                root_data = root

            node_id = root_data['result']['root']['nodeId']
            html = self.chrome.DOM.getOuterHTML(nodeId=node_id)
            
            if isinstance(html, tuple):
                html_data = html[0]
            else:
                html_data = html

            return BeautifulSoup(html_data['result']['outerHTML'], self.parser)
        except Exception as e:
            print(f"Failed to get page content: {str(e)}")
            return None

    # Selenium-style element finding methods
    def find_element_by_id(self, id_: str) -> ElementWrapper:
        """Find element by ID (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return ElementWrapper(soup.find(id=id_))
            return ElementWrapper()
        except Exception as e:
            print(f"Failed to find element by ID: {str(e)}")
            return ElementWrapper()

    def find_element_by_class_name(self, class_name: str) -> ElementWrapper:
        """Find element by class name (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return ElementWrapper(soup.find(class_=class_name))
            return ElementWrapper()
        except Exception as e:
            print(f"Failed to find element by class: {str(e)}")
            return ElementWrapper()

    def find_elements_by_class_name(self, class_name: str) -> Elements:
        """Find elements by class name (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return Elements(soup.find_all(class_=class_name))
            return Elements()
        except Exception as e:
            print(f"Failed to find elements by class: {str(e)}")
            return Elements()

    def find_element_by_tag_name(self, tag_name: str) -> ElementWrapper:
        """Find element by tag name (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return ElementWrapper(soup.find(tag_name))
            return ElementWrapper()
        except Exception as e:
            print(f"Failed to find element by tag: {str(e)}")
            return ElementWrapper()

    def find_elements_by_tag_name(self, tag_name: str) -> Elements:
        """Find elements by tag name (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return Elements(soup.find_all(tag_name))
            return Elements()
        except Exception as e:
            print(f"Failed to find elements by tag: {str(e)}")
            return Elements()

    def find_element_by_name(self, name: str) -> ElementWrapper:
        """Find element by name attribute (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return ElementWrapper(soup.find(attrs={"name": name}))
            return ElementWrapper()
        except Exception as e:
            print(f"Failed to find element by name: {str(e)}")
            return ElementWrapper()

    def find_elements_by_name(self, name: str) -> Elements:
        """Find elements by name attribute (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return Elements(soup.find_all(attrs={"name": name}))
            return Elements()
        except Exception as e:
            print(f"Failed to find elements by name: {str(e)}")
            return Elements()

    def find_element_by_css_selector(self, css_selector: str) -> ElementWrapper:
        """Find element by CSS selector (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return ElementWrapper(soup.select_one(css_selector))
            return ElementWrapper()
        except Exception as e:
            print(f"Failed to find element by CSS selector: {str(e)}")
            return ElementWrapper()

    def find_elements_by_css_selector(self, css_selector: str) -> Elements:
        """Find elements by CSS selector (Selenium-style)"""
        try:
            soup = self.get_page_content()
            if soup:
                return Elements(soup.select(css_selector))
            return Elements()
        except Exception as e:
            print(f"Failed to find elements by CSS selector: {str(e)}")
            return Elements()

    def find_element_by_xpath(self, xpath: str) -> ElementWrapper:
        """Find element by XPath (limited support)"""
        print("Warning: XPath support is limited with BeautifulSoup")
        return self.find_element_by_css_selector(self._xpath_to_css(xpath))

    def close(self):
        try:
            self.chrome.close()
        except Exception as e:
            print(f"Failed to close browser: {str(e)}")

    def quit(self):
        """Quit browser (Selenium-style)"""
        self.close()

def main():
    scraper = WebScraper()
    
    try:
        # Navigate to page (Selenium-style)
        scraper.get("https://httpbin.org/")

        # Find single element by class name
        header = scraper.find_element_by_class_name("heading")
        if header.is_displayed():
            print("Header text:", header.text())

        # Find all elements by class name
        links = scraper.find_elements_by_class_name("nav-link")
        for link in links:
            print(f"Link text: {link.text()}, URL: {link.get_attribute('href')}")

        # Find element by ID
        main_content = scraper.find_element_by_id("main")
        print("Main content:", main_content.text())

        # Find elements by tag name
        paragraphs = scraper.find_elements_by_tag_name("p")
        for p in paragraphs:
            print("Paragraph:", p.text())

        # Find element by CSS selector
        nav_menu = scraper.find_element_by_css_selector("nav.menu")
        print("Navigation menu:", nav_menu.text())

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        scraper.quit()

# if __name__ == "__main__":
#     main()

def main():
    scraper = WebScraper()
    url = "https://www.flipkart.com/triggr-ultrabuds-n1-neo-enc-40hr-playback-13mm-drivers-rich-bass-fast-charging-bluetooth/p/itm8085df018e710?pid=ACCGZRZ2SSCF6Y4Y&lid=LSTACCGZRZ2SSCF6Y4YAJYUWV&marketplace=FLIPKART&store=0pm%2Ffcn&srno=b_1_1&otracker=browse&fm=organic&iid=en_3K-Bmc2jQZHOzPkaLmAo0NgbUzXoy8i6mjtZwcPnKUbm2Dl1EanNmUZDlLgDQQw3vIHGdBA5MYasS4yJrijM6g%3D%3D&ppt=browse&ppn=browse&ssid=og6i03g6w00000001738074701012"
    try:
        # Navigate to a page
        if scraper.get(url):
            # Get page content
            content = scraper.get_page_content()

            # Extract all links
            # links = scraper.extract_elements(".Nx9bqj")
            price = scraper.find_by_class('Nx9bqj CxhGGd').text()
            print(price)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()