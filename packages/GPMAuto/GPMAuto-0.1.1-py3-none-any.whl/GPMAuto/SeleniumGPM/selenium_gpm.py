# -*- coding: utf-8 -*-
import random
from time import sleep, time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome import service
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options

from .pointer import Pointer
from selenium import webdriver

class SeleniumGPM(webdriver.Chrome):
    def __init__(self, service : service.Service, options : Options) -> None:
        super().__init__(service = service, options=options)
        self._pointer = Pointer(self)
        self.current_handles = []
    def hasCdcProps(self):
        return self.execute_script(
            """
            let objectToInspect = window,
                result = [];
            while(objectToInspect !== null)
            { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
              objectToInspect = Object.getPrototypeOf(objectToInspect); }
            return result.filter(i => i.match(/.+_.+_(Array|Promise|Symbol)/ig))
            """
        )

    def removeCdcProps(self):
        self.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            },
        )

        if self.hasCdcProps():
            self.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                        let objectToInspect = window,
                            result = [];
                        while(objectToInspect !== null) 
                        { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
                        objectToInspect = Object.getPrototypeOf(objectToInspect); }
                        result.forEach(p => p.match(/.+_.+_(Array|Promise|Symbol)/ig)
                                            &&delete window[p]&&console.log('removed',p))
                        """
                },
            )
    def get(self, url):
        self.removeCdcProps()
        super().get(url)
    def quit(self):
        try:
            for h in self.window_handles:
                self.switch_to.window(h)
                self.close()
            self.quit()
        except: pass
    def close_only_tab(self):
        try:
            for i in range(3):
                if len(self.window_handles) > 1:
                    handles = self.window_handles
                    handles.reverse()
                    for win in handles:
                        self.switch_to.window(win)
                        if len(self.window_handles) == 1: return
                        self.close()
                    break
                sleep(1)
        except: return 
    def wait_open_window(self, second=20):
        start = time()+second
        while time() < start:
            if len(self.window_handles) > len(self.current_handles): return True
            sleep(0.5)
        return False
    def wait_close_window(self, handles_current):
        while len(self.window_handles) == len(handles_current): sleep(1)

    def choose_window_url(self, url):
        # handles = 
        current_url = self.current_url
        start = time()+20
        while url not in current_url and time() < start:
            for i in self.window_handles:
                self.switch_to.window(i)
                current_url = self.current_url
                if url in current_url: return
    def set_size(self, size: float=0.5):
        self.get('chrome://settings/')
        self.execute_script('chrome.settingsPrivate.setDefaultZoom(%s);'%size)
    def get_location_element(self, element):
        reduceBox = 0.1
        random_x = element.size['width'] * 0.1 + int(random.uniform(0, int(element.size['width']) * (1 - 2 * reduceBox)))
        random_y = element.size['height'] * 0.1  + int(random.uniform(0, int(element.size['height']) * (1 - 2 * reduceBox)))
        x = element.location['x'] + random_x
        y = element.location['y'] + random_y
        return (x, y)
    def paste_content(self, el, content):
        self.execute_script(
            f'''
                const text = `{content}`;
                const dataTransfer = new DataTransfer();
                dataTransfer.setData('text', text);
                const event = new ClipboardEvent('paste', {{
                clipboardData: dataTransfer,
                bubbles: true
                }});
                arguments[0].dispatchEvent(event)
                ''',
            el)
    def click_js(self, by: By, value: str, text: str=None, timeout: int=30, check_enable=False):
        try:
            ignored_exceptions=(StaleElementReferenceException, NoSuchElementException)
            your_element = WebDriverWait(self, timeout,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((by, value)))
            while not self.is_element(by, value) and check_enable: sleep(1)
            self.scroll_element(your_element)
            self.execute_script('arguments[0].click();', your_element)
            if text != None:
                your_element.clear()
                your_element.send_keys(text)
        except StaleElementReferenceException: return  self.click_js(by, value, text, timeout)
    def wait_element(self,by, value, check_enable=True, timeout=30):
        start = time()+timeout
        while not self.is_element(by, value) and check_enable and time() < start: sleep(1)
        return time() < start
    def click_js_element(self, el):
        self.scroll_element(el)
        self.execute_script('arguments[0].click();', el)
    def scroll_amount_js(self, step):
        self.execute_script('''document.documentElement.scroll({top: %s, behavior: 'smooth'});'''%step)
    def is_element(self, by, value, check_display=True, check_enable=True, index=0):
        try:
            self.implicitly_wait(0.5)
            element =  self.find_elements(by, value)[index]
            if check_display:
                if element.is_displayed():
                    if check_enable: return element.is_enabled()
                    return True
                else: return False
            else: return True
        # except NoSuchWindowException: 
        #     raise NoSuchWindowException("Đéo có window này!")
        except: return False
    
    def click_send_keys(self, by: By, value: str, text: str=None, index: int=0, timeout: int=30):
        driver = self
        driver.implicitly_wait(timeout)
        el = driver.find_elements(by, value)[index]
        ActionChains(driver).click(el).perform()
        if text: 
            # el.clear()
            # el.send_keys(text)
            ActionChains(self).send_keys(text).perform()
    def send_keys_no_element(self, key):
        ActionChains(self).send_keys(key).perform()
    @property
    def is_full_page(self):
        try:
            return self.execute_script('function isPageFullyScrolled() { const windowHeight = window.innerHeight; const body = document.body;const html = document.documentElement; const documentHeight = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight); const scrollY = window.scrollY;return (windowHeight + scrollY+5) >= documentHeight;} return isPageFullyScrolled();')
        except: return False
    def scroll_element(self, element):
        script = '''
            var element = arguments[0];
            var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
            var elementTop = element.getBoundingClientRect().top;
            var currentY = window.scrollY || window.pageYOffset;
            var targetY = elementTop - (viewPortHeight / 2) + currentY;
            
            window.scroll({
                top: targetY,
                behavior: 'smooth'
            });
        '''
        self.execute_script(script, element)
    def send_keys(self, element, text, duration=1000):
        ActionChains(self, duration).send_keys_to_element(element, text).perform()