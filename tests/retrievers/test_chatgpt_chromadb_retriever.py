import pytest
from unittest.mock import patch, MagicMock

from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever


# Fixture for setting up a mocked version of ChatGPTChromaDBRetriever
@pytest.fixture
def setup_retriever():
    with patch('chromadb.PersistentClient') as mock_client, \
            patch('chromadb.utils.embedding_functions.DefaultEmbeddingFunction') as mock_embedding_function, \
            patch('dspygen.rm.chatgpt_chromadb_retriever.data_dir', return_value='/mocked/data/dir'), \
            patch('dspygen.rm.chatgpt_chromadb_retriever.calculate_file_checksum', return_value='mocked_checksum'):
        # Set up mock responses
        mock_embedding_function.return_value = MagicMock(return_value='mocked_embeddings')
        mock_client.return_value.get_or_create_collection.return_value.query.return_value = {
            "documents": ["Mocked Document 1", "Mocked Document 2"]
        }

        # Instantiate the retriever with mocks
        retriever = ChatGPTChromaDBRetriever(json_file_path="/mocked/data/dir/conversations.json",
                                             collection_name="chatgpt")

        yield retriever


def test_forward_happy_path(setup_retriever):
    # Call the forward function with a sample query
    query = "Sample query"
    results = setup_retriever.forward(query_or_queries=query, k=2, contains="Sample", role="assistant")

    # Assertions to ensure the forward function behaves as expected
    assert len(results) == 2  # Assuming the mocked query returns 2 documents
    assert "Mocked Document 1" in results
    assert "Mocked Document 2" in results
