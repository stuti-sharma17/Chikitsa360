# Ayurveda AI Chatbot

https://github.com/TenzinNsut/AyurvedaChatbot/assets/105097758/f7945a94-117f-4305-a97d-e490af9c310b

![diagram-export-17-5-2024-9_14_42-am](https://github.com/TenzinNsut/AyurvedaChatbot/assets/105097758/a9c692ae-df0e-49e6-9033-e7b665fe6ccc)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
This project aims to develop an interactive chatbot system that can provide information on Ayurvedic treatments for various skin diseases. By leveraging natural language processing (NLP), semantic search, and large language models (LLMs), the chatbot enables users to ask questions about skin conditions and retrieve relevant answers extracted from an authoritative Ayurvedic reference book.
The core components of the chatbot include:

- A knowledge base containing chunks of text from the reference book
- Embedding and semantic indexing of the text chunks
- Pinecone, a cloud database for storing and similarity searching of the vectorized data
- A query embedding and search module to find the most relevant chunks
- An LLM for answer refinement and generalized responses

## System Overview and Methodology

## 2.1 Knowledge Base Creation
The first step involves extracting the text content from an Ayurvedic book focused on skin diseases. Since the book's content is extensive and exceeds the token limit of most LLMs, the text is divided into smaller chunks. This chunking process allows the subsequent components to process the data more efficiently.

## 2.2 Embedding and Semantic Indexing
To enable semantic similarity matching, the text chunks are converted into vector representations using an embedding model. Each chunk is transformed into a high-dimensional vector that captures its semantic meaning. These vector embeddings are then stored in Pinecone, a cloud database designed for efficient similarity search and retrieval.

## 2.3 User Query Processing
When a user submits a question to the chatbot, the query undergoes the same embedding process as the knowledge base chunks. The vectorized query is then used to perform a similarity search against the indexed chunks in Pinecone. Pinecone calculates the similarity scores between the query vector and the stored chunk vectors, identifying the most semantically relevant chunks.

## 2.4 Answer Retrieval and Refinement
The chunks with the highest similarity scores are retrieved from Pinecone and ranked based on their relevance to the user's query. The top-ranked chunk is considered the most appropriate answer. However, to enhance the coherence and naturalness of the response, the selected chunk is passed through an LLM, specifically the Llama model from Meta. The LLM refines the answer, ensuring a more human-like and contextually appropriate response.
In cases where the user's query does not have an exact match in the knowledge base, the LLM generates a generalized response based on the available information. This fallback mechanism ensures that the chatbot provides a satisfactory response even when faced with queries that are not directly addressed in the reference book.

## Conclusion
The Ayurveda chatbot developed in this project demonstrates the effective integration of NLP techniques, semantic search, and LLMs to create an interactive information retrieval system. By leveraging a comprehensive Ayurvedic book on skin diseases as the knowledge base, the chatbot enables users to access relevant information quickly and easily.
The combination of text chunking, embedding, semantic indexing, and LLM-based answer refinement allows the chatbot to provide accurate and naturalistic responses to user queries. The use of Pinecone as the cloud database for storing and searching vectorized data ensures efficient retrieval of the most relevant chunks.

## Features
- Natural language understanding and processing
- Semantic search for relevant information retrieval
- Integration with a comprehensive Ayurvedic knowledge base 
- Generative responses using Llama2 a large language model
- User-friendly interface for seamless interaction

## Installation
To run the Ayurveda AI Chatbot locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ayurveda-ai-chatbot.git
   ```

2. Install the required dependencies:
   ```
   cd ayurveda-ai-chatbot
   pip install -r requirements.txt
   ```

3. Set up the necessary environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key for accessing the language model
   - `PINECONE_API_KEY`: Your Pinecone API key for semantic search
   - `PINECONE_ENV`: The Pinecone environment for your indexes

4. Run the chatbot:
   ```
   python app.py
   ```

5. Access the chatbot through the provided URL or interface.

## Usage
To interact with the Ayurveda AI Chatbot, simply enter your query or question related to Ayurvedic treatments for skin diseases. The chatbot will process your input, retrieve relevant information from its knowledge base, and provide a personalized response.

You can ask questions like:
- "What are some Ayurvedic remedies for eczema?"
- "How can I use neem to treat acne?"
- "What dietary recommendations does Ayurveda suggest for healthy skin?"

The chatbot will analyze your query and provide accurate and informative responses based on Ayurvedic principles and knowledge.
