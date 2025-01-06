import asyncio
import logging
from typing import List, Dict
from openai import OpenAI
import numpy as np

client = OpenAI()
logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "text-embedding-3-large"  # or "text-embedding-3-small"

async def rank_search_results(
    hypothesis_text: str,
    search_results: List[Dict],
    top_n: int = 10
) -> List[Dict]:
    """
    Ranks the given search results based on their similarity 
    to the hypothesis text using OpenAI embeddings (cosine similarity).

    Args:
        hypothesis_text (str): The text of the hypothesis to compare against.
        search_results (List[Dict]): A list of search-result dictionaries
            (e.g., from academic_search) each containing fields like 'title', 
            'description', 'abstract', etc.
        top_n (int, optional): How many top results to return. Defaults to 10.

    Returns:
        List[Dict]: A list of the top N search results (sorted by descending similarity).
                    Each dict is enriched with a "similarity" field 
                    for debugging or further processing.
    """
    # Obtain an embedding for the hypothesis text
    hypothesis_embedding = await _get_embedding_async(hypothesis_text)

    # Embed each search result's text (title + description/abstract)
    # In CORE, "description" is often the abstract or summary.
    for result in search_results:
        # Fallback to empty strings if not present
        title = result.get("title") or ""
        abstract = result.get("description") or result.get("abstract") or ""
        combined_text = f"{title}\n{abstract}"

        embedding_vec = await _get_embedding_async(combined_text)
        result["embedding"] = embedding_vec

    # Compute similarity for each result
    for result in search_results:
        emb = result.get("embedding")
        if emb is None:
            result["similarity"] = -999.0
        else:
            sim = _cosine_similarity(emb, hypothesis_embedding)
            result["similarity"] = sim

    # Sort by descending similarity
    ranked_results = sorted(search_results, key=lambda x: x["similarity"], reverse=True)

    # Return top N - exclude the embedding field
    top_results = [
        {k: v for k, v in result.items() if k != "embedding"}
        for result in ranked_results[:top_n]
    ]

    return top_results

async def _get_embedding_async(text: str) -> List[float]:
    """
    Helper function to get an embedding from the OpenAI API asynchronously.

    Args:
        text (str): The text input to be embedded.

    Returns:
        List[float]: The resulting embedding vector.
    """
    response = await asyncio.to_thread(
        client.embeddings.create,
        model=EMBEDDING_MODEL,
        input=text
    )
    
    embedding_vec = response.data[0].embedding
    return embedding_vec


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Computes cosine similarity between two embedding vectors.

    Args:
        a (List[float]): First embedding vector
        b (List[float]): Second embedding vector

    Returns:
        float: Cosine similarity between the two vectors
    """
    a_np = np.array(a, dtype=np.float32)
    b_np = np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(a_np) * np.linalg.norm(b_np))
    if denom == 0.0:
        return 0.0
    return float(np.dot(a_np, b_np) / denom)
