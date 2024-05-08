# import os
#
# import pytest
# #
# from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
# from dspygen.rm.data_retriever import DataRetriever
#
#
# def test_data_retriever_sql_query():
#     """
#     Test DataRetriever with a direct SQL query on the Chinook.db using a SQLite connection.
#     This assumes DataRetriever has been adjusted to accept and use a connection object.
#     """
#     # Assuming DataRetriever is adapted to accept a SQL query and connection directly
#     db_path = f"../../data/chinook.db"
#
#     data_retriever = DataRetriever(
#         file_path=db_path,
#         query="SELECT ArtistId, Name FROM Artist WHERE Name LIKE ?",
#         return_columns=["ArtistId", "Name"],
#         read_options={'params': ('%AC/DC%',)}  # This is correct; just make sure it's used in read_any.
#     )
#
#     # Assuming forward method is adapted to execute the SQL query with provided connection
#     result = data_retriever.forward()
#
#     assert len(result) > 0, "No results found"
#     assert any(artist['Name'] == 'AC/DC' for artist in result), "AC/DC not found in the results"
# #
# #
# # CSV_CONTENT = """id,name,age,city
# # 1,Alice,30,New York
# # 2,Bob,25,Los Angeles
# # 3,Charlie,35,Chicago
# # 4,Diana,28,New York
# # 5,Evan,40,Los Angeles
# # """
# #
# #
# # @pytest.fixture
# # def sample_csv_file(tmp_path):
# #     # Create a temporary CSV file
# #     file_path = tmp_path / "sample_data.csv"
# #     file_path.write_text(CSV_CONTENT)
# #     return str(file_path)
# #
# #
# # @pytest.skip("Chinook.db is not available in the CI environment")
# # def test_data_retriever(sample_csv_file):
# #     # SQL query to filter data
# #     query = "SELECT * FROM df WHERE age > 30"
# #     return_columns = ['name', 'age', 'city']
# #
# #     # Initialize DataRetriever with the path to the temporary CSV file
# #     data_retriever = DataRetriever(file_path=sample_csv_file, return_columns=return_columns)
# #
# #     # Execute the query using the forward method
# #     filtered_results = data_retriever.forward(query=query)
# #
# #     # Assertions to verify the results are as expected
# #     expected_results = [
# #         {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
# #         {'name': 'Evan', 'age': 40, 'city': 'Los Angeles'}
# #     ]
# #
# #     assert filtered_results == expected_results, "The filtered results did not match the expected output."
# #
# #
# # @pytest.skip("Chinook.db is not available in the CI environment")
# # def test_csv_pipeline():
# #     context = execute_pipeline(f'/Users/sac/dev/dspygen/tests/pipeline/data_hello_world_pipeline.yaml',
# #                                init_ctx={"csv_file": "/Users/sac/dev/dspygen/tests/data/greek.csv"})
# #     assert len(context.data) == 5
