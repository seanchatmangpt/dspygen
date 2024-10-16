from bs4 import BeautifulSoup


def replace_div_with_p(soup):
    """
    Replace <div> tags with <p> tags in the soup to reduce tokens,
    but only if the <div> contains inline or textual content.
    """
    for div in soup.find_all('div'):
        # Replace <div> with <p> only if it does not contain block elements
        # like <table>, <ul>, <ol>, etc.
        block_elements = div.find_all(['table', 'ul', 'ol', 'form', 'header', 'footer'])
        if not block_elements:
            div.name = 'p'  # Safely replace <div> with <p>

    return soup


def extract_relevant_form_tags(html_content):
    """
    Extracts only form-related tags (e.g., <form>, <input>, <textarea>, <select>, <option>, <button>, etc.)
    from the HTML content to reduce noise and focus on essential form elements.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <form> tags and their children (inputs, buttons, selects, etc.)
    relevant_tags = soup.find_all(
        ['form', 'input', 'textarea', 'select', 'option', 'button', 'label', 'fieldset', 'legend', 'datalist',
         'optgroup'])

    # Create a new BeautifulSoup object for cleaned content
    cleaned_soup = BeautifulSoup("", "html.parser")

    # Add the relevant form elements back to the cleaned soup
    for tag in relevant_tags:
        cleaned_soup.append(tag)

    return cleaned_soup
