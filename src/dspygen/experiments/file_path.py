import os

from dspygen.utils.file_tools import pages_dir


def main():
    print(pages_dir())
    # print(pages_dir("hello.py"))

    print(os.path.exists(pages_dir()))
    # print(os.path.exists(pages_dir("hello.py"))


if __name__ == '__main__':
    main()
