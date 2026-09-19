from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        chunks = self.store.search(question, top_k=top_k)
        if not chunks:
            return "No relevant information was found in the knowledge base."

        context = "\n\n".join(
            f"[{index}] Source: {chunk.get('metadata', {}).get('source', 'unknown')}\n"
            f"{chunk['content']}"
            for index, chunk in enumerate(chunks, start=1)
        )
        prompt = (
            "Answer the question using only the context below. "
            "Cite supporting context using its bracketed number (for example, [1]). "
            "If the context does not contain the answer, say so.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        return self.llm_fn(prompt)
