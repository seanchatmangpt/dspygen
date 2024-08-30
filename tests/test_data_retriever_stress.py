import pytest
import time
from dspygen.rm.data_retriever import DataRetriever

CSV_PATH = "/Users/sac/dev/dspygen/data/21KLinkedInConnections.csv"

@pytest.fixture
def data_retriever():
    return DataRetriever(file_path=CSV_PATH)

def test_large_dataset_loading(data_retriever):
    start_time = time.time()
    result = data_retriever.forward()
    end_time = time.time()
    
    assert len(result) > 20000, "Dataset should contain over 20,000 records"
    assert end_time - start_time < 5, "Loading should take less than 5 seconds"

def test_complex_query_execution(data_retriever):
    query = """
    SELECT 
        Company, 
        COUNT(*) as employee_count,
        AVG(CAST(SUBSTR(Connected, 1, INSTR(Connected, ' ') - 1) AS INTEGER)) as avg_connection_days
    FROM df
    WHERE Position LIKE '%Engineer%'
    GROUP BY Company
    HAVING employee_count > 5
    ORDER BY employee_count DESC, avg_connection_days DESC
    LIMIT 10
    """
    
    start_time = time.time()
    result = data_retriever.forward(query=query)
    end_time = time.time()
    
    assert len(result) == 10, "Query should return top 10 companies"
    assert end_time - start_time < 10, "Complex query should execute in less than 10 seconds"
    assert all('Company' in row and 'employee_count' in row and 'avg_connection_days' in row for row in result)

def test_multiple_queries_performance(data_retriever):
    queries = [
        "SELECT COUNT(*) as total FROM df",
        "SELECT Position, COUNT(*) as count FROM df GROUP BY Position ORDER BY count DESC LIMIT 5",
        "SELECT Company, AVG(CAST(SUBSTR(Connected, 1, INSTR(Connected, ' ') - 1) AS INTEGER)) as avg_days FROM df GROUP BY Company HAVING avg_days > 365 ORDER BY avg_days DESC LIMIT 10",
        "SELECT * FROM df WHERE Position LIKE '%Data Scientist%' AND Company IN (SELECT Company FROM df GROUP BY Company HAVING COUNT(*) > 10)",
    ]
    
    start_time = time.time()
    results = [data_retriever.forward(query=query) for query in queries]
    end_time = time.time()
    
    assert len(results) == 4, "All queries should execute successfully"
    assert end_time - start_time < 20, "Multiple complex queries should execute in less than 20 seconds"

def test_large_result_set(data_retriever):
    query = "SELECT * FROM df WHERE Connected LIKE '%year%'"
    
    start_time = time.time()
    result = data_retriever.forward(query=query)
    end_time = time.time()
    
    assert len(result) > 1000, "Large result set should contain over 1000 records"
    assert end_time - start_time < 15, "Large result set query should execute in less than 15 seconds"

def test_memory_usage(data_retriever):
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # Memory in MB
    
    # Perform a memory-intensive operation
    result = data_retriever.forward()
    del result  # Clear the result to see memory usage after garbage collection
    
    end_memory = process.memory_info().rss / 1024 / 1024  # Memory in MB
    memory_increase = end_memory - start_memory
    
    assert memory_increase < 1000, f"Memory usage increase should be less than 1000 MB, but was {memory_increase:.2f} MB"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])