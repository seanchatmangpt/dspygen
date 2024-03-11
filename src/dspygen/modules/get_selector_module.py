"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


import dspy

class SelectSingleElement(dspy.Signature):
    """
    Selects a single element from a list of elements that best matches the given prompt.
    """
    elements = dspy.InputField(desc="A list of elements.")
    prompt = dspy.InputField(desc="A prompt used to match the most relevant element.")

    selected_element = dspy.OutputField(desc="The css selector to use with Selenium.")




class GetSelectorModule(dspy.Module):
    """GetSelectorModule"""

    def forward(self, elements, prompt):
        pred = dspy.ChainOfThought(SelectSingleElement)
        result = pred(elements=elements, prompt=prompt).selected_element
        return result


def get_selector_call(elements, prompt):
    get_selector = GetSelectorModule()
    return get_selector.forward(elements=elements, prompt=prompt)


@app.command()
def call(elements, prompt):
    """GetSelectorModule"""
    init_dspy()
    
    print(get_selector_call(elements=elements, prompt=prompt))


from fastapi import APIRouter
router = APIRouter()

@router.post("/get_selector/")
async def get_selector_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return get_selector_call(**data)


def main():
    init_dspy()
    element_dicts = """{'type': 'checkbox', 'id': 'vector-main-menu-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-main-menu-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Main menu'}
{'type': 'checkbox', 'id': 'vector-main-menu-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-main-menu-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Main menu'}
{'class': 'cdx-text-input__input', 'type': 'search', 'name': 'search', 'placeholder': 'Search Wikipedia', 'aria-label': 'Search Wikipedia', 'autocapitalize': 'sentences', 'title': 'Search Wikipedia [ctrl-option-f]', 'accesskey': 'f', 'id': 'searchInput', 'autocomplete': 'off'}
{'class': 'cdx-text-input__input', 'type': 'search', 'name': 'search', 'placeholder': 'Search Wikipedia', 'aria-label': 'Search Wikipedia', 'autocapitalize': 'sentences', 'title': 'Search Wikipedia [ctrl-option-f]', 'accesskey': 'f', 'id': 'searchInput', 'autocomplete': 'off'}
{'type': 'hidden', 'name': 'title', 'value': 'Special:Search'}
{'type': 'hidden', 'name': 'title', 'value': 'Special:Search'}
{'type': 'checkbox', 'id': 'vector-user-links-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-user-links-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Personal tools'}
{'type': 'checkbox', 'id': 'vector-user-links-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-user-links-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Personal tools'}
{'type': 'checkbox', 'id': 'p-variants-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-p-variants', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Change language variant'}
{'type': 'checkbox', 'id': 'p-variants-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-p-variants', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Change language variant'}
{'type': 'checkbox', 'id': 'vector-page-tools-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-page-tools-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Tools'}
{'type': 'checkbox', 'id': 'vector-page-tools-dropdown-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-vector-page-tools-dropdown', 'class': 'vector-dropdown-checkbox ', 'aria-label': 'Tools'}
{'type': 'checkbox', 'id': 'p-lang-btn-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-p-lang-btn', 'class': 'vector-dropdown-checkbox mw-interlanguage-selector', 'aria-label': 'Go to an article in another language. Available in 48 languages'}
{'type': 'checkbox', 'id': 'p-lang-btn-checkbox', 'role': 'button', 'aria-haspopup': 'true', 'data-event-name': 'ui.dropdown-p-lang-btn', 'class': 'vector-dropdown-checkbox mw-interlanguage-selector', 'aria-label': 'Go to an article in another language. Available in 48 languages'}
"""
    prompt = "search box"
    print(get_selector_call(elements=element_dicts, prompt=prompt))
    

if __name__ == "__main__":
    main()
