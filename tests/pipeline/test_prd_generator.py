from pprint import pprint

import inflection
import pytest

from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.rm.data_retriever import DataRetriever

FEATURE_CSV_CONTENT = """FeatureID,FeatureDescription
1,Document Upload
2,Generate Unique Signing Link
3,Email Link to Signer
4,Signature Capture
5,Document Preview
6,Save Signature
7,Confirm Signature Placement
8,Email Confirmation to Sender
9,Signature Validation
10,Document Download
11,Mobile Responsive Design
12,API for Document Management
13,Drag-and-Drop Document Upload
14,Custom Signing Instructions
15,Link Expiration
"""


@pytest.fixture
def sample_feature_csv_file(tmp_path):
    # Create a temporary CSV file for features
    file_path = tmp_path / "features.csv"
    file_path.write_text(FEATURE_CSV_CONTENT)
    return str(file_path)


def test_feature_data_retriever(sample_feature_csv_file):
    # This example query is a placeholder. In a real scenario, you'd have specific logic to filter or process CSV data.
    query = "SELECT * FROM df WHERE FeatureID <= 10"
    return_columns = ['FeatureDescription']

    # Initialize DataRetriever with the path to the temporary CSV file
    data_retriever = DataRetriever(file_path=sample_feature_csv_file, return_columns=return_columns)

    # Execute the query using the forward method
    filtered_results = data_retriever.forward(query=query)

    # Assertions to verify the results are as expected
    expected_results = [
        {'FeatureDescription': 'Document Upload'},
        {'FeatureDescription': 'Generate Unique Signing Link'},
    ]

    assert len(filtered_results) == 10, "The filtered results did not match the expected number of features."
    for expected, actual in zip(expected_results, filtered_results):
        assert expected == actual, f"Expected {expected}, but got {actual}."


def test_feature_data_retriever(sample_feature_csv_file):
    # This example query is a placeholder. In a real scenario, you'd have specific logic to filter or process CSV data.
    query = "SELECT * FROM df WHERE FeatureID <= 10"
    return_columns = ['FeatureDescription']

    # Initialize DataRetriever with the path to the temporary CSV file
    data_retriever = DataRetriever(file_path=sample_feature_csv_file, return_columns=return_columns)

    # Execute the query using the forward method
    filtered_results = data_retriever.forward(query=query)


# def test_feature_code_generation(sample_feature_csv_file):
#     # This example query is a placeholder. In a real scenario, you'd have specific logic to filter or process CSV data.
#     query = "SELECT * FROM df"
#     return_columns = ['FeatureDescription']
#
#     # Initialize DataRetriever with the path to the temporary CSV file
#     data_retriever = DataRetriever(file_path=sample_feature_csv_file, return_columns=return_columns)
#
#     # Execute the query using the forward method
#     filtered_results = data_retriever.forward(query=query)
#
#     for result in filtered_results:
#         print(result)
#         context = execute_pipeline('/Users/sac/dev/dspygen/tests/pipeline/gherkin_pipeline.yaml', init_ctx={"processed_data": result})
#
#         file_name = f"{inflection.underscore(result['FeatureDescription'])}.tsx"
#         file_name = inflection.dasherize(file_name)
#
#         with open(file_name, 'w') as f:
#             f.write(context.react_code)
#             print(f"React JSX code written to {file_name}")
