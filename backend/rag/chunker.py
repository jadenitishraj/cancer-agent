from llama_index.core import Document
from llama_index.core.node_parser import (
    SentenceSplitter,
    HierarchicalNodeParser,
    SentenceWindowNodeParser,
    SemanticSplitterNodeParser
)
from llama_index.embeddings.openai import OpenAIEmbedding

def get_splitter_for_type(doc_type: str):
    """Returns the appropriate LlamaIndex splitter based on document type."""
    if doc_type == "paragraph":
        return SemanticSplitterNodeParser(
            buffer_size=1, 
            breakpoint_percentile_threshold=95, 
            embed_model=OpenAIEmbedding()
        )
    elif doc_type == "code":
        return HierarchicalNodeParser.from_defaults(chunk_sizes=[600, 150])
    elif doc_type == "transcript":
        return SentenceWindowNodeParser.from_defaults(
            window_size=3,
            window_metadata_key="window",
            original_text_metadata_key="original_text"
        )
    else:
        return SentenceSplitter(chunk_size=600, chunk_overlap=100)

def chunk_document(text: str, filename: str, doc_type: str) -> list:
    """Wraps text in a LlamaIndex Document and splits it into nodes."""
    doc = Document(
        text=text,
        metadata={"filename": filename, "doc_type": doc_type}
    )
    splitter = get_splitter_for_type(doc_type)
    nodes = splitter.get_nodes_from_documents([doc])
    
    return [
        {
            "id": node.node_id,
            "text": node.get_content(),
            "metadata": node.metadata
        }
        for node in nodes
    ]
