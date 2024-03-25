# import pytest
#
# from dspygen.rm.doc_retriever import DocRetriever
#
# # Define the path to your test files
# TEST_FILES_PATH = "test_files/"
#
# # List of test cases, each case is a tuple: (filename, expected unique phrase)
# test_cases = [
#     ("sample.txt", "uniquephrase"),
#     ("sample.md", "uniquephrase"),
#     ("sample.pdf", "uniquephrase"),
#     ("sample.docx", "uniquephrase"),
#     ("sample.html", "uniquephrase")
# ]
#
#
#
# @pytest.mark.parametrize("file_name, expected_phrase", test_cases)
# def test_text_file_retriever(file_name, expected_phrase):
#     """
#     Test TextFileRetriever for various text file types.
#     """
#     file_path = TEST_FILES_PATH + file_name
#     retriever = DocRetriever([file_path], search_query=expected_phrase)
#     results = retriever.forward()
#
#     assert len(results) > 0, "No results returned."
#     for result in results:
#         assert expected_phrase in result["text"], f"{expected_phrase} not found in {file_name}."
#
# if __name__ == "__main__":
#     pytest.main()
