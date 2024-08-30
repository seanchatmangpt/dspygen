# Advanced Document and Data Retrieval System

This package provides a suite of high-performance retriever classes designed for efficient handling of various document and data file formats. Built with scalability and flexibility in mind, these retrievers integrate seamlessly with DSPy for advanced data processing pipelines.

## Key Features

- Multi-format support for documents and structured data
- Efficient text extraction and data querying
- Seamless integration with DSPy pipelines
- Optimized for large-scale data processing

## Retriever Classes

### ChatGPTChromaDBRetriever

`ChatGPTChromaDBRetriever` is a sophisticated retriever class designed for efficient storage, indexing, and retrieval of ChatGPT conversation data. It leverages ChromaDB for vector storage and similarity search capabilities, making it ideal for large-scale conversation analysis and information retrieval tasks.

#### Key Features

- Efficient storage and indexing of ChatGPT conversations
- Vector-based similarity search using ChromaDB
- Automatic processing and updating of conversation data
- Customizable embedding functions (default: Ollama embedding)
- Seamless integration with DSPy pipelines

#### Usage Example

```python
from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever

# Initialize the retriever
retriever = ChatGPTChromaDBRetriever(
    json_file_path="path/to/conversations.json",
    collection_name="chatgpt_conversations",
    persist_directory="path/to/persist",
    check_for_updates=True
)

# Perform a simple query
query = "What are the key features of transformer models?"
results = retriever.forward(query, k=3)

print("Top 3 relevant passages:")
for i, result in enumerate(results, 1):
    print(f"{i}. {result[:200]}...")  # Print first 200 characters of each result

# Use in a DSPy pipeline
class ConversationAnalysisPipeline(dspy.Module):
    def __init__(self):
        self.retriever = ChatGPTChromaDBRetriever()
    
    def forward(self, query):
        relevant_passages = self.retriever.forward(query, k=5)
        return dspy.Prediction(relevant_info=relevant_passages)

pipeline = ConversationAnalysisPipeline()
result = pipeline("Explain the concept of attention in neural networks")
print("Relevant information:", result.relevant_info)

# Advanced usage with filters
assistant_responses = retriever.forward(
    query="Explain the benefits of transfer learning",
    k=3,
    role="assistant"  # Only retrieve responses from the assistant
)

print("Top 3 assistant explanations on transfer learning:")
for i, response in enumerate(assistant_responses, 1):
    print(f"{i}. {response[:200]}...")  # Print first 200 characters of each response
```



### DataRetriever

`DataRetriever` is a versatile and powerful class designed for efficient retrieval and querying of structured data from various file formats. It seamlessly integrates with DSPy pipelines and supports SQL-like querying capabilities.

#### Key Features

- Supports multiple file formats including CSV, Excel, SQL databases, JSON, Parquet, and more
- SQL-like querying capabilities using pandasql
- Efficient data loading and processing
- Seamless integration with DSPy pipelines

#### Usage Example

```python
from dspygen.rm.data_retriever import DataRetriever

# Initialize DataRetriever with a CSV file
data_retriever = DataRetriever(file_path='sales_data.csv')

# Perform a SQL-like query on the data
query = "SELECT product_name, SUM(sales_amount) as total_sales FROM df GROUP BY product_name ORDER BY total_sales DESC LIMIT 5"
top_products = data_retriever.forward(query=query)

print("Top 5 Products by Sales:")
for product in top_products:
    print(f"{product['product_name']}: ${product['total_sales']:.2f}")

# Use in a DSPy pipeline
class SalesAnalysisPipeline(dspy.Module):
    def __init__(self):
        self.retriever = DataRetriever(file_path='sales_data.csv')
    
    def forward(self, query):
        results = self.retriever.forward(query=query)
        return dspy.Prediction(analysis_results=results)

pipeline = SalesAnalysisPipeline()
result = pipeline("SELECT region, AVG(sales_amount) as avg_sales FROM df GROUP BY region")
print("Average Sales by Region:", result.analysis_results)
```

### DocRetriever

`DocRetriever` is an advanced text extraction tool designed for multiple document formats. It supports reading and cleaning text from various document types, making it ideal for preprocessing text data for NLP tasks.

#### Usage Example


```python
from dspygen.rm.doc_retriever import DocRetriever

# Initialize DocRetriever with a PDF file
doc_retriever = DocRetriever(path='example_document.pdf')

# Extract full text from the document
full_text = doc_retriever.forward()
print("Full text length:", len(full_text))

# Extract text in chunks of 1000 characters
text_chunks = doc_retriever.forward(chunk_chars=1000)
print("Number of chunks:", len(text_chunks))
print("First chunk preview:", text_chunks[0][:100])

# Use in a DSPy pipeline
class DocumentAnalysisPipeline(dspy.Module):
    def __init__(self, document_path):
        self.retriever = DocRetriever(path=document_path)
    
    def forward(self, chunk_size=None):
        if chunk_size:
            return dspy.Prediction(document_chunks=self.retriever.forward(chunk_chars=chunk_size))
        return dspy.Prediction(full_text=self.retriever.forward())

pipeline = DocumentAnalysisPipeline('example_document.pdf')
result = pipeline(chunk_size=500)
print("Number of document chunks:", len(result.document_chunks))
```

#### Supported File Types

- EPUB (.epub)
- PDF (.pdf)
- Text (.txt)
- Markdown (.md)
- Word Document (.docx)

