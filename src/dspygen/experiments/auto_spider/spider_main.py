
import subprocess
import time
from playwright.sync_api import sync_playwright

def start_browser_with_debugging():
    # Define the command to start the browser with remote debugging enabled
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    user_data_dir = "/Users/sac/Library/Application Support/Google/Chrome/Profile 1"
    remote_debugging_port = 9222
    command = [
        chrome_path,
        f"--remote-debugging-port={remote_debugging_port}",
        f"--user-data-dir={user_data_dir}",
    ]

    print(str(command))

    # Start the browser process
    process = subprocess.Popen(command)
    return process


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Start the browser
    browser_process = start_browser_with_debugging()

    # Give the browser some time to start
    time.sleep(5)

    # Connect Playwright to the running browser
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f'http://localhost:9222')

        # Optionally, list all open pages
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()

        # Navigate to a URL or perform any actions
        page.goto('https://example.com')

        # Example: Take a screenshot to verify the connection
        page.screenshot(path='example.png')

        # Close the page and context if you don't need them anymore
        page.close()
        context.close()

        # Note: Do not close the browser as it is managed externally
        # browser.close()

    # Terminate the browser process if needed
    # browser_process.terminate()


if __name__ == '__main__':
    main()