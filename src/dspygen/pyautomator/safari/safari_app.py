import os
import requests
import json
import pyperclip
import time
from html2text import HTML2Text

from dspygen.pyautomator.base_app import BaseApp


class SafariApp(BaseApp):
    def __init__(self):
        super().__init__("Safari")

    def get_current_tab(self):
        script = """
        function getCurrentTab() {
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            return JSON.stringify({
                url: tab.url(),
                name: tab.name()
            });
        }
        getCurrentTab();
        """
        result = self.execute_jxa(script)
        return json.loads(result)

    def open_url(self, url):
        script = f"""
        const Safari = Application('Safari');
        const tab = Safari.windows[0].currentTab();
        tab.url = '{url}';
        """
        self.execute_jxa(script)

    def execute_js_in_tab(self, js_code):
        script = f"""
        function executeInTab() {{
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            return Safari.doJavaScript(`{js_code}`, {{in: tab}});
        }}
        executeInTab();
        """
        return self.execute_jxa(script)

    def get_page_content(self):
        js_code = "document.body.innerHTML;"
        return self.execute_js_in_tab(js_code)

    def get_page_links(self):
        js_code = """
        JSON.stringify(
            Array.from(document.querySelectorAll('a'))
                .map(a => ({href: a.href, text: a.textContent.trim()}))
        );
        """
        result = self.execute_js_in_tab(js_code)
        return json.loads(result)

    def search_google(self, query):
        self.open_url("https://www.google.com")
        js_code = f"""
        document.querySelector('textarea[name="q"]').value = "{query}";
        document.querySelector('form').submit();
        """
        self.execute_js_in_tab(js_code)

    def convert_to_markdown(self, output_file=None):
        script = """
        (() => {
          const Safari = Application('Safari');
          const tab = Safari.windows[0].currentTab();

          const turndownURL = "https://unpkg.com/turndown/dist/turndown.js";
          const nsURL = $.NSURL.URLWithString($(turndownURL));
          const data = $.NSData.dataWithContentsOfURL(nsURL);
          const turndownSrc = $.NSString.alloc.initWithDataEncoding(data, $.NSUTF8StringEncoding).js;

          const scriptSrc = turndownSrc + 
            `
          var turndownService = new TurndownService({
             headingStyle: 'atx',
             codeBlockStyle: 'fenced',
             bullet: '-'
             });
             /* Ignore 'script' and 'nav' elements to keep 
                markdown cleaner */
             turndownService.remove('script');
             turndownService.remove('nav');
             turndownService.turndown(document.body);
        `;
         const result = Safari.doJavaScript(`${scriptSrc}`, {in: tab});
         
         // Copy the result to clipboard
         const app = Application.currentApplication();
         app.includeStandardAdditions = true;
         app.setTheClipboardTo(result);
        })()
        """
        self.execute_jxa(script)
        
        # Give some time for the clipboard to be updated
        time.sleep(0.5)
        
        # Get the result from the clipboard
        markdown_content = pyperclip.paste()
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown content saved to: {output_file}")
        
        return markdown_content

def main():
    safari = SafariApp()
    safari.activate_app()
    
    # Example usage
    current_tab = safari.get_current_tab()
    print(f"Current tab: {current_tab['name']} - {current_tab['url']}")

    # safari.open_url("https://www.linkedin.com/in/seanchatman/")
    content = safari.get_page_content()
    print(content)
    # print(f"Page content length: {len(content)}")

    # links = safari.get_page_links()
    # print(f"Number of links on the page: {len(links)}")

    # safari.search_google("Python programming")
    
    # Convert to Markdown and save to file
    output_file = "converted_page.md"
    markdown = safari.convert_to_markdown(output_file=output_file)
    print(f"Converted Markdown length: {len(markdown)}")
    print(f"Markdown content saved to: {output_file}")

if __name__ == "__main__":
    main()