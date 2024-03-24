import dspy


class WebRetriever(dspy.Retrieve):
    def __init__(self, source, **kwargs):
        super().__init__()

        self.source = source

    def forward(self, query, **kwargs):
        return None


def main():
    rm = WebRetriever(source="<html><form><button type='submit'/></form></html>")
    print(rm.forward(query="What is the css selector for the submit button?"))


if __name__ == '__main__':
    main()
