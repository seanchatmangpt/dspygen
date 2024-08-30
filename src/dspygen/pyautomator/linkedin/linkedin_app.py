import json
import pyperclip
import time

from dspygen.pyautomator.safari.safari_app import SafariApp


class LinkedInApp(SafariApp):
    def __init__(self):
        super().__init__()

    def get_profile_markdown(self, profile_url, output_file=None):
        self.open_url(profile_url)
        time.sleep(5)  # Wait for the page to load

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
          var turndownService = new TurndownService();
             /* Ignore 'script' and 'nav' elements to keep 
                markdown cleaner */
             turndownService.remove('script');
             turndownService.remove('nav');
             
             var mainContent = document.querySelector('main').innerHTML;
             
             // Convert to Markdown
             var markdown = turndownService.turndown(mainContent);
             markdown;
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
            print(f"LinkedIn profile content saved to: {output_file}")
        
        return markdown_content


def main():
    linkedin = LinkedInApp()
    linkedin.activate_app()
    
    # Example usage
    profile_url = "https://www.linkedin.com/in/seanchatman/"
    output_file = "linkedin_profile.md"
    
    markdown = linkedin.get_profile_markdown(profile_url, output_file=output_file)
    print(f"Converted LinkedIn profile length: {len(markdown)}")
    print(f"LinkedIn profile content saved to: {output_file}")


if __name__ == "__main__":
    main()