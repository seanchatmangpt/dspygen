import dspy
from dspygen.modules.file_name_module import file_name_call


class CodeWriter():
    def __init__(self, **kwargs):
        super().__init__()
    
    def forward(self, **kwargs):
        return None


def code_writer_call(source):
    rm = CodeWriter()
    return rm.forward(source=source)


def main():
    rm = CodeWriter()
    print(rm.forward())
    
    
if __name__ == '__main__':
    main()
      