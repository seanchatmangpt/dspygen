import dspy

from dspygen.rm.doc_retriever import DocRetriever
from dspygen.utils.dspy_tools import init_dspy


def main():
    drt = DocRetriever(path="/Users/sac/Downloads/BusPatterns.pdf")
    business_text = drt.forward()
    print(business_text)

    init_dspy()

    business_text += "\nCreate a table of contents for the business patterns document, no software patterns."

    pred = dspy.Predict("business_text -> yaml_table_of_contents")
    result = pred.forward(business_text=business_text).yaml_table_of_contents
    # print(result)


if __name__ == '__main__':
    main()
