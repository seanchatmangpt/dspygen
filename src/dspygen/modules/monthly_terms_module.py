import dspy
from pydantic import BaseModel, Field
from typing import List


class MonthlyDescription(BaseModel):
    month: int = Field(..., description="The month number, ranging from 1 to 12")
    description: str = Field(..., description="A natural language description of the pricing for the month")


class InvoiceDescriptions(BaseModel):
    deal_terms: str = Field(..., description="The terms of the deal, including free and discounted periods")
    regular_price: float = Field(..., description="The regular monthly price")
    monthly_descriptions: List[MonthlyDescription] = Field(...,
                                                           description="A list of natural language descriptions for each month over a 12-month period")


class GenerateInvoiceDescriptions(dspy.Signature):
    """
    Generate natural language descriptions for each month based on given deal terms.
    The descriptions will be used for invoicing software.
    """

    deal_terms = dspy.InputField(desc="The terms of the deal, including free and discounted periods")
    regular_price = dspy.InputField(desc="The regular monthly price")
    json_schema = dspy.InputField(desc="The JSON schema for the output model")
    monthly_descriptions = dspy.OutputField(
        desc="A list of natural language descriptions for each month over a 12-month period.")


class DealEndMonth(dspy.Signature):
    """
    Calculate the month number when the deal ends based on given deal terms.
    """

    deal_terms = dspy.InputField(desc="The terms of the deal, including free and discounted periods")
    end_month = dspy.OutputField(desc="The month number when the deal ends. Just a int.",
                                 prefix="```python\nend_month: int = ")


def main2():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()
    deal_terms = "2 months free, after that 10% discount for 3 months"

    calculate_end_month = dspy.Predict(DealEndMonth)
    response = calculate_end_month(deal_terms=deal_terms)

    print(response.end_month)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy(model="gpt-4o")
    # deal_terms = "2 months free, after that 10% discount for 3 months"
    #
    # calculate_end_month = dspy.Predict(DealEndMonth)
    # response = calculate_end_month(deal_terms=deal_terms)

    # Example JSON schema based on the Pydantic model

    deal_terms = "2 months free, after that 10% discount for 3 months."
    regular_price = "100.0"

    from dspygen.modules.prompt_to_json_module import instance
    inst = instance(InvoiceDescriptions, deal_terms)
    print(inst)


if __name__ == '__main__':
    main()
