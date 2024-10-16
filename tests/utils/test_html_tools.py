import pytest
from bs4 import BeautifulSoup
from dspygen.utils.html_tools import replace_div_with_p, extract_relevant_form_tags

# Sample HTML content for testing
html_with_divs = """
<div>
    <div>This is a div containing text.</div>
    <div>
        <table><tr><td>This div contains a table and should not be replaced.</td></tr></table>
    </div>
    <div>This is another div.</div>
</div>
"""

html_with_form_elements = """
<div>
    <form action="/submit">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name">
        <input type="submit" value="Submit">
    </form>
    <div>This div should be ignored.</div>
</div>
"""

@pytest.fixture
def soup_with_divs():
    """Fixture for the sample HTML with divs."""
    return BeautifulSoup(html_with_divs, "html.parser")

@pytest.fixture
def soup_with_form_elements():
    """Fixture for the sample HTML with form elements."""
    return html_with_form_elements


def test_replace_div_with_p_basic(soup_with_divs):
    """Test basic functionality of replacing <div> with <p>."""
    modified_soup = replace_div_with_p(soup_with_divs)

    # Ensure that <div> containing only text is replaced with <p>
    assert len(modified_soup.find_all('p')) == 2  # 3 <p> tags should exist after replacement

    # Ensure that <div> containing a <table> is NOT replaced
    remaining_divs = modified_soup.find_all('div')
    assert len(remaining_divs) == 1  # There should be 1 remaining <div>
    assert remaining_divs[0].find('table') is not None  # The remaining <div> should contain a <table>


def test_replace_div_with_p_does_not_replace_table(soup_with_divs):
    """Test that <div> wrapping <table> elements are not replaced."""
    modified_soup = replace_div_with_p(soup_with_divs)
    assert modified_soup.find('table') is not None  # The table should still be there
    assert modified_soup.find_all('div')  # The <div> containing the <table> should not be replaced


# Tests for the extract_relevant_form_tags function
def test_extract_relevant_form_tags_only_form_elements(soup_with_form_elements):
    """Test that only form-related tags are extracted."""
    cleaned_soup = extract_relevant_form_tags(soup_with_form_elements)
    assert len(cleaned_soup.find_all('form')) == 1  # There should be 1 form tag
    assert len(cleaned_soup.find_all('input')) == 2  # There should be 2 input tags
    assert cleaned_soup.find_all('div') == []  # Divs should not be present


def test_extract_relevant_form_tags_handles_empty_html():
    """Test handling of empty HTML."""
    empty_html = ""
    cleaned_soup = extract_relevant_form_tags(empty_html)
    assert len(cleaned_soup) == 0  # Should return an empty soup


def test_extract_relevant_form_tags_no_form_elements():
    """Test HTML with no form elements."""
    html_no_form = "<div>No forms here!</div>"
    cleaned_soup = extract_relevant_form_tags(html_no_form)
    assert len(cleaned_soup) == 0  # Should return empty soup since no relevant tags are present


def test_extract_relevant_form_tags_complex_form():
    """Test HTML with complex form structure."""
    html_complex = """
    <form action="/complex">
        <fieldset>
            <legend>Personal Information</legend>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name">
            <select id="gender" name="gender">
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>
        </fieldset>
        <button type="submit">Submit</button>
    </form>
    """
    cleaned_soup = extract_relevant_form_tags(html_complex)
    assert len(cleaned_soup.find_all('form')) == 1
    assert len(cleaned_soup.find_all('input')) == 1
    assert len(cleaned_soup.find_all('select')) == 1
    assert len(cleaned_soup.find_all('option')) == 2
    assert len(cleaned_soup.find_all('button')) == 1
