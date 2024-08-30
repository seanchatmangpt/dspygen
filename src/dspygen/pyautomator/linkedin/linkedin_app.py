import json
import pyperclip
import time
from typing import List, Dict

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

    def send_message(self, recipient_url: str, message: str) -> bool:
        """Send a message to a LinkedIn connection."""
        script = f"""
        (() => {{
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            
            // Navigate to recipient's profile
            tab.url = "{recipient_url}";
            delay(3);  // Wait for page to load
            
            // Click on "Message" button
            Safari.doJavaScript(`
                document.querySelector('button[aria-label="Message"]').click();
            `, {{in: tab}});
            delay(1);
            
            // Type and send message
            Safari.doJavaScript(`
                const messageInput = document.querySelector('div[aria-label="Write a message…"]');
                messageInput.textContent = "{message}";
                document.querySelector('button[aria-label="Send"]').click();
            `, {{in: tab}});
            
            return true;
        }})()
        """
        return self.execute_jxa(script)

    def add_message(self, recipient_url: str, message: str) -> bool:
        """Prepare a message to a LinkedIn connection without sending it."""
        script = f"""
        (() => {{
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            
            // Navigate to recipient's profile
            tab.url = "{recipient_url}";
            delay(3);  // Wait for page to load
            
            // Click on "Message" button
            Safari.doJavaScript(`
                document.querySelector('button[aria-label="Message"]').click();
            `, {{in: tab}});
            delay(1);
            
            // Type message without sending
            Safari.doJavaScript(`
                const messageInput = document.querySelector('div[aria-label="Write a message…"]');
                messageInput.textContent = "{message}";
            `, {{in: tab}});
            
            return true;
        }})()
        """
        return self.execute_jxa(script)

    def send_prepared_message(self) -> bool:
        """Send the prepared message."""
        script = """
        (() => {
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            
            // Click the send button
            Safari.doJavaScript(`
                document.querySelector('button[aria-label="Send"]').click();
            `, {in: tab});
            
            return true;
        })()
        """
        return self.execute_jxa(script)

    def get_conversations(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent conversations."""
        script = f"""
        (() => {{
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            
            // Navigate to messaging page
            tab.url = "https://www.linkedin.com/messaging/";
            delay(3);  // Wait for page to load
            
            return Safari.doJavaScript(`
                const conversations = Array.from(document.querySelectorAll('li[data-control-name="conversation_item"]'))
                    .slice(0, {limit})
                    .map(conv => ({{
                        name: conv.querySelector('.msg-conversation-card__participant-names').textContent.trim(),
                        preview: conv.querySelector('.msg-conversation-card__message-snippet-body').textContent.trim(),
                        time: conv.querySelector('time').getAttribute('datetime')
                    }}));
                JSON.stringify(conversations);
            `, {{in: tab}});
        }})()
        """
        result = self.execute_jxa(script)
        return json.loads(result)

    def get_conversation_history(self, conversation_url: str) -> List[Dict]:
        """Retrieve message history for a specific conversation."""
        script = f"""
        (() => {{
            const Safari = Application('Safari');
            const tab = Safari.windows[0].currentTab();
            
            // Navigate to conversation
            tab.url = "{conversation_url}";
            delay(3);  // Wait for page to load
            
            return Safari.doJavaScript(`
                const messages = Array.from(document.querySelectorAll('.msg-s-message-list__event'))
                    .map(msg => ({{
                        sender: msg.querySelector('.msg-s-message-group__profile-link')?.textContent.trim() || 'You',
                        content: msg.querySelector('.msg-s-event-listitem__body')?.textContent.trim(),
                        time: msg.querySelector('time').getAttribute('datetime')
                    }}));
                JSON.stringify(messages);
            `, {{in: tab}});
        }})()
        """
        result = self.execute_jxa(script)
        return json.loads(result)


def main():
    linkedin = LinkedInApp()
    linkedin.activate_app()
    
    # Example usage
    profile_url = "https://www.linkedin.com/in/seanchatman/"
    output_file = "linkedin_profile.md"
    
    markdown = linkedin.get_profile_markdown(profile_url, output_file=output_file)
    print(f"Converted LinkedIn profile length: {len(markdown)}")
    print(f"LinkedIn profile content saved to: {output_file}")

    # Example usage of new methods
    recipient_url = "https://www.linkedin.com/in/example-user/"
    message = "Hello! I hope this message finds you well."
    
    if linkedin.add_message(recipient_url, message):
        print("Message prepared successfully!")
        input("Press Enter to send the message or Ctrl+C to cancel...")
        if linkedin.send_prepared_message():
            print("Message sent successfully!")
    
    conversations = linkedin.get_conversations(limit=5)
    print("Recent conversations:")
    for conv in conversations:
        print(f"- {conv['name']}: {conv['preview']} ({conv['time']})")
    
    conversation_url = "https://www.linkedin.com/messaging/thread/123456789/"
    history = linkedin.get_conversation_history(conversation_url)
    print("\nConversation history:")
    for msg in history:
        print(f"{msg['sender']} ({msg['time']}): {msg['content']}")

if __name__ == "__main__":
    main()