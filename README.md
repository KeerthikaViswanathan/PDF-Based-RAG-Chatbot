# PDF Expert Bot – RAG-Based Question Answering System

## Overview

PDF Expert Bot is a **Retrieval-Augmented Generation (RAG)** application that allows users to upload a PDF and ask questions about its content.

The system extracts text from the PDF, divides it into smaller overlapping chunks, finds the most relevant chunks using **semantic similarity**, and uses a **Groq-hosted LLM** to generate answers based only on the retrieved document content.

This helps reduce unsupported answers and provides **page-level source references** for better transparency.

---

## Features

* Upload and process PDF documents
* Split document text into overlapping chunks
* Perform semantic search using Sentence Transformers
* Retrieve the top 4 relevant chunks for each question
* Generate answers using Groq API
* Provide page-level citations
* Display the retrieved source sections
* Prevent unsupported answers using a similarity threshold
* Conversational question-answering interface using Streamlit

---

## Project Workflow

```text
              PDF Upload
                   ↓
            Text Extraction
                   ↓
               Chunking
          200 words / chunk
                   ↓
            Text Embeddings
       Sentence Transformers
                   ↓
          Semantic Similarity
                   ↓
       Retrieve Top 4 Chunks
                   ↓
             Context
                   ↓
             Groq LLM
                   ↓
          Generated Answer
                   ↓
       Page Citation + Sources
```

---

## Technologies Used

### AI / GenAI

* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* Prompt Engineering
* Semantic Search
* Text Embeddings

### Python

* Python
* Streamlit
* PyPDF
* NumPy
* python-dotenv

### Models & APIs

* Sentence Transformers
* `all-MiniLM-L6-v2`
* Groq API

### Concepts

* Document Chunking
* Overlapping Chunks
* Vector Similarity
* Context Retrieval
* Hallucination Reduction
* Page-Level Citations

---

## How It Works

### 1. PDF Upload

The user uploads a PDF through the Streamlit interface.

### 2. Text Extraction

PyPDF extracts the text from each page while keeping track of the page number.

### 3. Chunking

The extracted text is divided into smaller chunks.

The project uses:

```text
Chunk size: 200 words
Overlap: 40 words
```

The overlap helps preserve context between neighboring chunks.

### 4. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The user's question is also converted into an embedding.

### 5. Semantic Search

The system calculates similarity between the question embedding and document chunk embeddings.

The **top 4 most relevant chunks** are selected.

### 6. Context Retrieval

The selected chunks are provided to the LLM as context.

### 7. Answer Generation

Groq API generates the answer using only the retrieved document context.

The prompt instructs the model not to use outside information.

### 8. Source Display

The application displays:

* Page number
* Similarity score
* Retrieved document text

This allows the user to verify where the answer came from.

---

## Hallucination Reduction

The system uses two mechanisms to reduce unsupported answers.

### Similarity Threshold

A minimum similarity score is defined:

```python
MIN_SCORE = 0.25
```

If the retrieved content is not sufficiently relevant, the system responds:

```text
I couldn't find that in the document.
```

### Context-Restricted Generation

The LLM is instructed to answer only from the retrieved document context and not use outside knowledge.

---

## Project Structure

```text
PDF-Expert-Bot/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── data/
│
└── tests/
```

### Important

The `.env` file contains the Groq API key and should **not be uploaded to GitHub**.

Example:

```text
GROQ_API_KEY=your_api_key
```

---

## Installation

Clone the project or download the source code.

Install the required packages:

```bash
pip install -r requirements.txt
```

### Example `requirements.txt`

```text
numpy
streamlit
pypdf
sentence-transformers
groq
python-dotenv
```

---

## API Configuration

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

The application reads the API key using `python-dotenv`, so the key does not need to be written directly inside the Python source code.

---

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL in your browser.

Upload a PDF and start asking questions.

---

## Example

### User:

```text
What is the main purpose of this document?
```

### System:

```text
The main purpose of the document is ...
(p. 2)
```

The application also provides the relevant retrieved source sections under **Sources Used**.

---

## RAG Configuration

| Parameter                |            Value |
| ------------------------ | ---------------: |
| Chunk Size               |        200 words |
| Chunk Overlap            |         40 words |
| Retrieved Chunks         |            Top 4 |
| Minimum Similarity Score |             0.25 |
| Embedding Model          | all-MiniLM-L6-v2 |
| Interface                |        Streamlit |
| LLM API                  |             Groq |

---

## Skills Demonstrated

* Python
* Streamlit
* RAG
* LLM Integration
* Semantic Search
* Sentence Embeddings
* Document Processing
* Prompt Engineering
* Vector Similarity
* Context Retrieval
* API Integration
* Environment Variable Management
* Hallucination Reduction



---

## Project Summary

**PDF Expert Bot** demonstrates how RAG can combine **document retrieval, semantic embeddings, and LLM generation** to build a question-answering system that provides answers grounded in uploaded documents.
