import dspy
from typer import Typer


app = Typer()


class RequestContractModule(dspy.Module):
    """Verbose Documentation for the DSPy Module"""

    def forward(self, request, chars: str = "500"):
        pred = dspy.Predict("contract_request, chars -> contract_fine_print")
        result = pred(contract_request=request, chars=chars).contract_fine_print
        return result


def request_contract_call(request, chars="500"):
    request_contract = RequestContractModule()
    return request_contract.forward(request=request, chars=chars)


@app.command()
def module_test(request, chars="500"):
    """Verbose Documentation for the DSPy Module"""
    print(request_contract_call(request=request, chars=chars))


def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    request = "Employment contract to hire a Senior Principle Software Engineer for a Fortune 100 company"
    print(request_contract_call(request=request))


if __name__ == "__main__":
    main()
