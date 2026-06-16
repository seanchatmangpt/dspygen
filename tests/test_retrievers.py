"""
Lean RM retriever tests — 12 focused, behavior-driven tests.
All external deps (chromadb, gspread, duckduckgo, sqlite) are mocked.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# ChromaRetriever: init with mocked client, retrieve returns passages
# ===========================================================================

class TestChromaRetriever:
    @pytest.fixture(autouse=True)
    def _load_module(self):
        import dspygen.rm.chroma_retriever  # noqa: F401
        self._mod = sys.modules["dspygen.rm.chroma_retriever"]

    def test_init_with_mocked_client(self, tmp_path):
        from dspygen.rm.chroma_retriever import ChromaRetriever
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = MagicMock()
        with patch.object(self._mod, "chromadb") as mock_chroma:
            mock_chroma.PersistentClient.return_value = mock_client
            r = ChromaRetriever(collection_name="test_col", persist_directory=str(tmp_path))
            assert r.collection_name == "test_col"

    def test_retrieve_returns_passages(self, tmp_path):
        from dspygen.rm.chroma_retriever import ChromaRetriever
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"documents": [["doc_a", "doc_b"]]}
        mock_embed = MagicMock(return_value=[[0.1, 0.2]])

        with patch.object(self._mod, "get_collection", return_value=mock_collection), \
             patch.object(self._mod, "generate_embeddings", return_value=[[0.1, 0.2]]):
            r = ChromaRetriever(collection_name="col", persist_directory=str(tmp_path), embed_fn=mock_embed)
            result = r.forward("test query", k=2)
            assert result == [["doc_a", "doc_b"]]


# ===========================================================================
# WebRetriever: init, retrieve with mocked DuckDuckGo
# ===========================================================================

class TestWebRetriever:
    def test_init(self):
        from dspygen.rm.web_retriever import WebRetriever
        wr = WebRetriever(k=5)
        assert wr.k == 5

    def test_retrieve_with_mocked_ddg(self):
        """forward() with DDG returning empty list gives empty passages, no crash."""
        import dspygen.rm.web_retriever as _mod
        with patch.object(_mod, "_ddg_search", return_value=[]):
            from dspygen.rm.web_retriever import WebRetriever
            wr = WebRetriever(k=3)
            result = wr.forward(query="python testing")
            assert hasattr(result, "passages")
            assert result.passages == []


# ===========================================================================
# PythonCodeRetriever: init, retrieve with mocked file search
# ===========================================================================

class TestPythonCodeRetriever:
    def test_init(self):
        from dspygen.rm.python_code_retriever import PythonCodeRetriever
        r = PythonCodeRetriever(include_signatures=True, include_docstrings=False)
        assert r.include_signatures is True
        assert r.include_docstrings is False

    def test_retrieve_with_mocked_file_search(self, tmp_path):
        """forward() on an empty directory returns empty list without crashing."""
        from dspygen.rm.python_code_retriever import PythonCodeRetriever
        r = PythonCodeRetriever()
        # Empty dir: rglob finds no .py files — must return [] cleanly
        result = r.forward(str(tmp_path))
        assert isinstance(result, list)
        assert result == []


# ===========================================================================
# DataRetriever: init, query with mocked sqlite
# ===========================================================================

class TestDataRetriever:
    def test_init(self, tmp_path):
        from dspygen.rm.data_retriever import DataRetriever
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n3,4\n")
        dr = DataRetriever(str(csv_file))
        assert dr is not None
        assert dr.file_path == csv_file

    def test_query_with_sql(self, tmp_path):
        from dspygen.rm.data_retriever import DataRetriever
        csv_file = tmp_path / "items.csv"
        csv_file.write_text("name,score\nalice,90\nbob,70\n")
        dr = DataRetriever(str(csv_file))
        result = dr.forward(query="SELECT * FROM df WHERE score > 75")
        assert len(result) == 1
        assert result[0]["name"] == "alice"


# ===========================================================================
# GoogleSheetsRetriever: init with mocked client, retrieve returns df
# ===========================================================================

class TestGoogleSheetsRetriever:
    def _make(self, records):
        import pandas as pd
        from dspygen.rm.google_sheets_retriever import GoogleSheetRetriever
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = records
        retriever = object.__new__(GoogleSheetRetriever)
        retriever.pipeline = None
        retriever.step = None
        retriever.spreadsheet_id = "fake_id"
        retriever.sheet_name = "Sheet1"
        retriever.return_columns = []
        retriever.sheet = mock_sheet
        retriever.df = pd.DataFrame(records)
        return retriever

    def test_init_with_mocked_client(self):
        """Bypassing gspread.oauth() by injecting state directly."""
        retriever = self._make([{"col": "val"}])
        assert retriever.spreadsheet_id == "fake_id"
        assert retriever.sheet_name == "Sheet1"

    def test_retrieve_returns_df(self):
        records = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        retriever = self._make(records)
        result = retriever.forward()
        assert len(result) == 2
        assert result[0]["name"] == "Alice"


# ===========================================================================
# Connection error → raises with clear message
# ===========================================================================

class TestConnectionError:
    def test_chroma_connection_error_raises(self, tmp_path):
        """ChromaRetriever.forward() propagates ChromaDB connection errors."""
        import dspygen.rm.chroma_retriever as _mod
        from dspygen.rm.chroma_retriever import ChromaRetriever

        def _fail(*args, **kwargs):
            raise ConnectionError("ChromaDB unreachable")

        with patch.object(_mod, "get_collection", side_effect=_fail):
            r = ChromaRetriever(collection_name="col", persist_directory=str(tmp_path))
            with pytest.raises(Exception, match="ChromaDB unreachable"):
                r.forward("query")


# ===========================================================================
# Empty results → returns empty list, not crash
# ===========================================================================

class TestEmptyResults:
    def test_empty_results_returns_empty_list(self, tmp_path):
        """ChromaRetriever returns empty list when collection query yields nothing."""
        import dspygen.rm.chroma_retriever as _mod
        from dspygen.rm.chroma_retriever import ChromaRetriever

        mock_collection = MagicMock()
        mock_collection.query.return_value = {"documents": [[]]}

        with patch.object(_mod, "get_collection", return_value=mock_collection), \
             patch.object(_mod, "generate_embeddings", return_value=[[0.0]]):
            r = ChromaRetriever(collection_name="col", persist_directory=str(tmp_path))
            result = r.forward("empty query")
            assert isinstance(result, list)
            assert result == [[]]  # outer list with one empty inner list
