import dspy


class NaturalLanguageDataRetriever(dspy.Retrieve):
    def __init__(self, **kwargs):
        super().__init__()
    
    def forward(self, **kwargs):
        return None


def main():
    rm = NaturalLanguageDataRetriever()
    print(rm.forward())
    
    
if __name__ == '__main__':
    main()
      