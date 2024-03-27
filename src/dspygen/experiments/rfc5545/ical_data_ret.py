from dspygen.rm.data_retriever import DataRetriever
from dspygen.utils.file_tools import data_dir


def main():
    """Main function"""

    ret = DataRetriever(data_dir('dev.csv'), "SELECT * FROM event").forward()
    print(ret)


if __name__ == '__main__':
    main()
