import subprocess
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

from dspygen.pyautomator.base_app import BaseApp

class MailSearchParams(BaseModel):
    for_: Optional[str] = Field(None, alias="for")
    in_: Optional[List[str]] = Field(None, alias="in")
    from_: Optional[str] = Field(None, alias="from")
    to: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    date_received: Optional[datetime] = None
    date_sent: Optional[datetime] = None
    flagged: Optional[bool] = None
    read: Optional[bool] = None
    replied_to: Optional[bool] = None
    attachment_type: Optional[str] = None

    class Config:
        populate_by_name = True

    def to_jxa_dict(self) -> dict:
        jxa_dict = {}
        for field, value in self.dict(by_alias=True).items():
            if value is not None:
                if isinstance(value, datetime):
                    jxa_dict[field] = value.isoformat()
                elif isinstance(value, list):
                    jxa_dict[field] = ', '.join(value)
                else:
                    jxa_dict[field] = json.dumps(str(value))[1:-1]  # Use json.dumps to properly escape special characters
        return jxa_dict

class MailApp(BaseApp):
    def __init__(self):
        super().__init__("Mail")

    def get_most_recent_email(self) -> Dict[str, Any]:
        """
        Retrieve the most recent email using JXA.
        
        Returns:
            Dict containing email details: subject, sender, date, and body.
        """
        jxa_script = '''
        function run() {
            console.log("run() function called");
            var Mail = Application("Mail");
            Mail.includeStandardAdditions = true;
            
            console.log("Accessing inbox");
            var inbox = Mail.inbox();
            var messages = inbox.messages();
            
            if (messages.length === 0) {
                console.log("No messages found in inbox");
                return JSON.stringify({error: "No messages found in inbox"});
            }
            
            console.log("Retrieving latest message");
            var latestMessage = messages[0];
            
            console.log("Preparing message data");
            var result = {
                subject: latestMessage.subject(),
                sender: latestMessage.sender(),
                date: latestMessage.dateReceived().toISOString(),
                body: latestMessage.content()
            };
            
            console.log("Returning message data");
            return JSON.stringify(result);
        }

        run();
        '''
        
        return self._run_jxa_script(jxa_script)

    def send_email(self, sender: str, recipient: str, subject: str, content: str) -> Dict[str, Any]:
        """
        Send an email using JXA.
        
        Args:
            sender: Email address of the sender
            recipient: Email address of the recipient
            subject: Subject of the email
            content: Body of the email
        
        Returns:
            Dict containing the result of the operation
        """
        jxa_script = f'''
        function run() {{
            console.log("Sending email");
            var Mail = Application("Mail");
            
            var msg = Mail.OutgoingMessage({{
                sender: "{sender}",
                subject: "{subject}"
            }});
            
            Mail.outgoingMessages.push(msg);
            
            var rcpt = Mail.Recipient({{
                address: "{recipient}"
            }});
            
            msg.toRecipients.push(rcpt);
            msg.content = "{content}";
            
            Mail.activate();
            msg.send();
            
            return JSON.stringify({{success: true, message: "Email sent successfully"}});
        }}

        run();
        '''
        
        return self._run_jxa_script(jxa_script)

    def save_attachments(self, target_folder: str, mime_types: List[str]) -> Dict[str, Any]:
        """
        Save attachments from selected emails that match the specified MIME types.
        
        Args:
            target_folder: Path to the folder where attachments will be saved
            mime_types: List of MIME types to save (e.g., ['application/pdf', 'image/.*'])
        
        Returns:
            Dict containing the result of the operation
        """
        jxa_script = f'''
        function run() {{
            var Mail = Application("Mail");
            var curApp = Application.currentApplication();
            curApp.includeStandardAdditions = true;

            var targetFolder = "{target_folder}";
            var desiredTypes = {mime_types};

            var selMsg = Mail.messageViewers[0].selectedMessages();
            var savedAttachments = [];

            selMsg.forEach(function(m) {{
                var src = m.source();
                var boundaries = src.match(/boundary="(.*?)"/g);
                var splitRE = new RegExp("^--(" + boundaries.map(function(b) {{
                    return b.match(/boundary="(.*?)"/)[1];
                }}).join('|') + ")$", "m");

                var msgParts = src.split(splitRE);
                var partInfo = [];

                msgParts.forEach(function(part) {{
                    var disposition = part.match(/Content-Disposition:\\s+(.*?);/);
                    if (disposition && disposition[1] === "attachment") {{
                        var type = part.match(/Content-Type:\\s+(.*?);/);
                        var name = part.match(/name="(.*?)"/);
                        if (type && name) {{
                            partInfo.push({{
                                "type": type[1],
                                "name": name[1]
                            }});
                        }}
                    }}
                }});

                var attachmentRE = new RegExp(desiredTypes.join('|'));
                var attachments = partInfo.filter(function(p) {{
                    return attachmentRE.test(p.type);
                }});

                curApp.doShellScript('mkdir -p "' + targetFolder + '"');

                attachments.forEach(function(a) {{
                    var fileName = targetFolder + "/" + a.name;
                    var attachment = m.mailAttachments[a.name];
                    Mail.save(attachment, {{in: Path(fileName)}});
                    savedAttachments.push(fileName);
                }});
            }});

            return JSON.stringify({{success: true, savedAttachments: savedAttachments}});
        }}

        run();
        '''
        
        return self._run_jxa_script(jxa_script)

    def _run_jxa_script(self, script: str) -> Dict[str, Any]:
        """
        Run a JXA script and return the result.
        
        Args:
            script: The JXA script to run
        
        Returns:
            Dict containing the result of the script execution
        """
        print("Executing JXA script:")
        print(script)
        try:
            result = subprocess.run(['osascript', '-l', 'JavaScript', '-e', script], 
                                    capture_output=True, text=True, check=True)
            print("JXA Script Output:", result.stdout)
            print("JXA Script Error Output:", result.stderr)
            return json.loads(result.stdout)  # Use json.loads to parse the JSON string
        except subprocess.CalledProcessError as e:
            print(f"Error executing JXA script: {e}")
            print("Error Output:", e.stderr)
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Raw output:", result.stdout)
            return {"error": f"JSON decode error: {str(e)}"}

    def search_emails(self, search_params: MailSearchParams, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search emails using JXA and return a specified number of results.
        
        Args:
            search_params: MailSearchParams object containing search criteria
            max_results: Maximum number of results to return (default: 10)
        
        Returns:
            List of dictionaries containing email details: subject, sender, date, and body snippet
        """
        jxa_search_params = search_params.to_jxa_dict()
        jxa_search_params_str = ', '.join([f'{k}: "{v}"' for k, v in jxa_search_params.items()])

        jxa_script = f'''
        function run() {{
            console.log("Starting email search");
            try {{
                var Mail = Application("Mail");
                Mail.includeStandardAdditions = true;
                
                console.log("Mail application initialized");
                
                // Check if Mail.search exists
                if (typeof Mail.search !== 'function') {{
                    throw new Error("Mail.search method does not exist");
                }}
                
                console.log('Search parameters: {jxa_search_params_str}');
                
                var searchParams = {{{jxa_search_params_str}}};
                var searchResults = Mail.search(searchParams);
                console.log("Search completed. Number of results: " + searchResults.length);
                
                var results = [];
                
                for (var i = 0; i < Math.min(searchResults.length, {max_results}); i++) {{
                    var message = searchResults[i];
                    try {{
                        results.push({{
                            subject: message.subject(),
                            sender: message.sender(),
                            date: message.dateReceived().toISOString(),
                            bodySnippet: message.content().substring(0, 100)
                        }});
                    }} catch (err) {{
                        console.log("Error processing message " + i + ": " + err);
                    }}
                }}
                
                console.log("Processed " + results.length + " messages");
                return JSON.stringify(results);
            }} catch (err) {{
                console.log("Error in JXA script: " + err);
                return JSON.stringify({{ error: err.toString() }});
            }}
        }}

        run();
        '''
        
        try:
            result = self._run_jxa_script(jxa_script)
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and 'error' in result:
                print(f"Error in JXA script: {result['error']}")
                return []
            else:
                print(f"Unexpected result type: {type(result)}")
                return []
        except Exception as e:
            print(f"Error in search_emails: {e}")
            return []

    def check_mail_accessibility(self) -> Dict[str, bool]:
        jxa_script = '''
        function run() {
            try {
                var Mail = Application("Mail");
                Mail.includeStandardAdditions = true;
                
                var result = {
                    mailAccessible: true,
                    searchMethodExists: typeof Mail.search === 'function'
                };
                
                return JSON.stringify(result);
            } catch (err) {
                return JSON.stringify({
                    mailAccessible: false,
                    searchMethodExists: false,
                    error: err.toString()
                });
            }
        }

        run();
        '''
        
        return self._run_jxa_script(jxa_script)

def main():
    app = MailApp()
    
    # Check Mail accessibility
    accessibility_check = app.check_mail_accessibility()
    print("Mail Accessibility Check:")
    if "error" in accessibility_check:
        print(f"Error checking Mail accessibility: {accessibility_check['error']}")
        return

    print(f"Mail Accessible: {accessibility_check.get('mailAccessible', False)}")
    print(f"Search Method Exists: {accessibility_check.get('searchMethodExists', False)}")
    
    if not accessibility_check.get('mailAccessible', False) or not accessibility_check.get('searchMethodExists', False):
        print("Cannot proceed with email search due to Mail accessibility issues.")
        return

    search_params = MailSearchParams(
        from_="my@remarkable.com",
    )
    max_results = 5
    print(f"\nSearching for emails from: {search_params.from_}")
    search_results = app.search_emails(search_params, max_results)
    
    print(f"\nSearch Results (max {max_results} results):")
    if not search_results:
        print("No results found or an error occurred.")
    else:
        for idx, email in enumerate(search_results, 1):
            print(f"\nEmail {idx}:")
            print(f"Subject: {email.get('subject', 'N/A')}")
            print(f"From: {email.get('sender', 'N/A')}")
            print(f"Date: {email.get('date', 'N/A')}")
            print(f"Body Snippet: {email.get('bodySnippet', 'N/A')}")

if __name__ == "__main__":
    main()
