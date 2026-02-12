import os
from pathlib import Path

from django.conf import settings

from .helper import download_hugging_face_embeddings
from .prompt import prompt_template


class ChatbotConfigError(RuntimeError):
    pass


_qa_chain = None
_init_error = None
_initialized = False


def _resolve_model_path():
    model_path = os.environ.get("LLM_MODEL_PATH", "").strip()
    if model_path:
        path = Path(model_path)
        if not path.is_absolute():
            path = settings.BASE_DIR / path
        return path

    return (
        settings.BASE_DIR
        / "AI chat"
        / "AyurvedaChatbot"
        / "model"
        / "llama-2-7b-chat.ggmlv3.q4_0.bin"
    )


def get_qa_chain():
    global _qa_chain, _init_error, _initialized

    if _initialized:
        if _init_error:
            raise ChatbotConfigError(_init_error)
        return _qa_chain

    _initialized = True

    pinecone_api_key = os.environ.get("PINECONE_API_KEY", "").strip()
    pinecone_api_env = (
        os.environ.get("PINECONE_API_ENV", "").strip()
        or os.environ.get("PINECONE_ENV", "").strip()
    )
    index_name = os.environ.get("PINECONE_INDEX", "pinecone-index").strip()

    if not pinecone_api_key or not pinecone_api_env:
        _init_error = (
            "Chatbot not configured: set PINECONE_API_KEY and "
            "PINECONE_API_ENV (or PINECONE_ENV)."
        )
        raise ChatbotConfigError(_init_error)

    model_path = _resolve_model_path()
    if not model_path.exists():
        _init_error = (
            f"Chatbot model not found at {model_path}. "
            "Set LLM_MODEL_PATH to the correct file path."
        )
        raise ChatbotConfigError(_init_error)

    try:
        import pinecone
        from langchain.chains import RetrievalQA
        from langchain.llms import CTransformers
        from langchain.prompts import PromptTemplate
        from langchain.vectorstores import Pinecone
    except ImportError as exc:
        _init_error = (
            "Chatbot dependencies are missing. Install requirements with "
            "`pip install -r requirements.txt`."
        )
        raise ChatbotConfigError(_init_error) from exc

    embeddings = download_hugging_face_embeddings()

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_env)
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    llm = CTransformers(
        model=str(model_path),
        model_type="llama",
        config={"max_new_tokens": 512, "temperature": 0.6},
    )

    _qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return _qa_chain
