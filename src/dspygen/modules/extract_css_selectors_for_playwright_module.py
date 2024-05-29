import dspy

import dspy


class ExtractCSSSelectorsForPlaywright(dspy.Signature):
    """
    Extract CSS selector from an HTML script for Playwright to spider the site.
    """
    html_script = dspy.InputField(desc="HTML script of the web page.")
    why = dspy.InputField(desc="Reason or purpose for extracting the CSS selector.")
    what = dspy.InputField(desc="Element or attribute to target for CSS selector extraction.")
    how = dspy.InputField(desc="Specific conditions or rules to apply during extraction.")
    css_selector = dspy.OutputField(desc="CSS selector to be used by Playwright for web scraping.",
                                    prefix="```python\nselector = '",)


class ExtractCSSSelectorsForPlaywrightModule(dspy.Module):
    """ExtractCSSSelectorsForPlaywrightModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, html_script, why, what, how):
        pred = dspy.Predict(ExtractCSSSelectorsForPlaywright)
        self.output = pred(html_script=html_script, why=why, what=what, how=how).css_selector
        return self.output


def extract_css_selectors_for_playwright_call(html_script, why, what, how):
    extract_css_selectors_for_playwright = ExtractCSSSelectorsForPlaywrightModule()
    return extract_css_selectors_for_playwright.forward(html_script=html_script, why=why, what=what, how=how)


def main():
    from dspygen.utils.dspy_tools import init_dspy, init_ol

    init_dspy()
    # init_ol()
    html_script = """
       <html>
         <head>
           <style>
             .main { color: red; }
             #unique { background-color: blue; }
             div > p { margin: 10px; }
           </style>
         </head>
         <body>
           <div class="main">
             <p id="unique">Hello World!</p>
           </div>
         </body>
       </html>
       """
    why = "To find the main content section for scraping."
    what = "div with class 'main'"
    how = "Select the first matching element."
    result = extract_css_selectors_for_playwright_call(html_script=html_script, why=why, what=what, how=how).split("'")[0]
    print(result)


if __name__ == "__main__":
    main()
