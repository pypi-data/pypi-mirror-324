from ...utils.gpu import get_device

def default_rag_embedder():
    """Get the default embedder for Retrieval-Augmented Generation (RAG)."""
    from ...runnables.embedders.commons import HuggingFaceEmbeddings
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': get_device()}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )