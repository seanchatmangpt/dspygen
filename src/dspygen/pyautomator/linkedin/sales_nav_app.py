import json
import pyperclip
import time
import logging
import pandas as pd

from dspygen.pyautomator.safari.safari_app import SafariApp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SalesNavApp(SafariApp):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/sales"
        self.connections = None

    def login(self, username, password):
        self.open_url(f"{self.base_url}/login")
        time.sleep(3)  # Wait for page to load

        script = f"""
        (() => {{
            document.getElementById('username').value = '{username}';
            document.getElementById('password').value = '{password}';
            document.querySelector('form.login__form').submit();
        }})()
        """
        self.execute_jxa(script)
        time.sleep(5)  # Wait for login to complete

    def search_leads(self, query):
        self.open_url(f"{self.base_url}/search/people")
        time.sleep(3)  # Wait for page to load

        script = f"""
        (() => {{
            const searchInput = document.querySelector('input[placeholder="Search by keyword"]');
            searchInput.value = '{query}';
            searchInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            document.querySelector('button[aria-label="Search"]').click();
        }})()
        """
        self.execute_jxa(script)
        time.sleep(5)  # Wait for search results to load

    def get_search_results(self, num_results=10):
        script = f"""
        (() => {{
            const results = Array.from(document.querySelectorAll('.search-results__result-item')).slice(0, {num_results});
            return JSON.stringify(results.map(result => {{
                const nameElement = result.querySelector('.result-lockup__name');
                const titleElement = result.querySelector('.result-lockup__highlight-keyword');
                const companyElement = result.querySelector('.result-lockup__position-company');
                return {{
                    name: nameElement ? nameElement.textContent.trim() : '',
                    title: titleElement ? titleElement.textContent.trim() : '',
                    company: companyElement ? companyElement.textContent.trim() : ''
                }};
            }}));
        }})()
        """
        result = self.execute_jxa(script)
        return json.loads(result)

    def send_connection_request(self, lead_index):
        script = f"""
        (() => {{
            const connectButtons = document.querySelectorAll('button[aria-label="Connect"]');
            if (connectButtons[{lead_index}]) {{
                connectButtons[{lead_index}].click();
                setTimeout(() => {{
                    const sendButton = document.querySelector('button[aria-label="Send now"]');
                    if (sendButton) {{
                        sendButton.click();
                        return "Connection request sent";
                    }}
                    return "Failed to send connection request";
                }}, 1000);
            }}
            return "Connect button not found";
        }})()
        """
        return self.execute_jxa(script)

    def import_connections(self, file_path):
        try:
            self.connections = pd.read_csv(file_path)
            logger.info(f"Imported {len(self.connections)} connections from {file_path}")
        except Exception as e:
            logger.error(f"Error importing connections: {e}")

    def compare_results_with_connections(self, search_results):
        if self.connections is None:
            logger.warning("Connections not imported. Please import connections first.")
            return search_results

        for result in search_results:
            match = self.connections[self.connections['Full Name'].str.lower() == result['name'].lower()]
            if not match.empty:
                result['connected'] = True
                result['connected_on'] = match.iloc[0]['Connected On']
            else:
                result['connected'] = False
                result['connected_on'] = None

        return search_results

def main():
    sales_nav = SalesNavApp()
    sales_nav.activate_app()

    # Import connections
    connections_file = "/Users/sac/Downloads/Complete_LinkedInDataExport_08-21-2024/21KLinkedInConnections.csv"
    sales_nav.import_connections(connections_file)

    # Example usage
    username = "your_username"
    password = "your_password"
    sales_nav.login(username, password)

    search_query = "Software Engineer"
    sales_nav.search_leads(search_query)

    results = sales_nav.get_search_results(5)
    results_with_connection_status = sales_nav.compare_results_with_connections(results)

    print("Search Results:")
    for i, result in enumerate(results_with_connection_status):
        connection_status = "Connected" if result['connected'] else "Not connected"
        connected_on = f" (Connected on: {result['connected_on']})" if result['connected'] else ""
        print(f"{i+1}. {result['name']} - {result['title']} at {result['company']} - {connection_status}{connected_on}")

    # Uncomment to send a connection request to the first non-connected result
    # for result in results_with_connection_status:
    #     if not result['connected']:
    #         response = sales_nav.send_connection_request(results_with_connection_status.index(result))
    #         print(response)
    #         break

if __name__ == "__main__":
    main()