from playwright.sync_api import sync_playwright

from dspygen.modules.get_selector_module import get_selector_call
from dspygen.utils.dspy_tools import init_dspy


def find_all_inputs(page):
    """
    Finds all input elements on a given Playwright page.

    Args:
        page: The Playwright page object to search within.

    Returns:
        A list of Playwright element handles representing the input elements.
    """

    input_elements = page.query_selector_all('input')

    # Optional filtering - You can uncomment and adjust any of these:
    # visible_inputs = [el for el in input_elements if el.is_visible()]  # Only visible inputs
    # enabled_inputs = [el for el in input_elements if el.is_enabled()]  # Only enabled inputs
    # specific_types = [el for el in input_elements if el.get_attribute('type') in ['text', 'email', 'password']]  # Filter by type

    return input_elements


def find_all_interactable_elements(page):
    # Get all 'button' elements
    interactable_elements = page.query_selector_all("button, input, textarea, select, a")

    for element in interactable_elements:
        # Further checks for visibility and enabled state
        if element.is_visible() and element.is_enabled():
            print(element.get_attribute('id'), element.tag_name())


def get_attributes(js_handle):
    """Prints attributes of a JSHandle"""
    attributes = js_handle.evaluate("""el => { 
                                      const attrs = {}; 
                                      for (const attrib of el.attributes) {
                                          attrs[attrib.name] = attrib.value;
                                      }
                                      return attrs; 
                                    }""", js_handle)
    print(attributes)
    return attributes


def main(goal):
    init_dspy()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://google.com")

        inputs = find_all_inputs(page)

        selector = get_selector_call(str(inputs), prompt="search box")

        search_box = page.query_selector(selector)

        search_term = "How many storeys are in the castle that David Gregory inherited?"

        search_box.fill(search_term)

        page.keyboard.press("Enter")

        browser.close()


if __name__ == '__main__':
    main("Search for Language Models")
