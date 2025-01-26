import os
import json
from db.models import Hypothesis
import wikipediaapi as wikidetail
import wikipedia as wikisearch

WIKI_LANG = "en"  # Use English Wikipedia
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1")

def _build_query(entities_or_terms, operator="AND"):
    """
    Build a structured query string for Wikipedia search.
    Args:
        entities_or_terms (list): List of entities or terms to use in the query.
        operator (str): Logical operator to join entities or terms ('AND' or 'OR').
    Returns:
        str: A formatted query string.
    """
    return f" {operator} ".join([f'"{item}"' if " "\
         in item else item for item in entities_or_terms])

async def factual_search_step(hypothesis: Hypothesis, max_results: int = 3):
    """
    Perform a factual search using Wikipedia.
    
    Args:
        hypothesis (Hypothesis): The hypothesis object containing the claim.
        db (Session): The database session.
        max_results (int): The maximum number of results to return.

    Returns:
        List[dict]: A list of dictionaries containing article data.
    """
    try:
        wiki = wikidetail.Wikipedia(
            user_agent="wikipedia-search",
            extract_format=wikidetail.ExtractFormat.WIKI,
            language=WIKI_LANG
        )
        wikisearch.set_lang(WIKI_LANG)

        # Priority 1: Use extracted entities
        if hypothesis.extracted_entities:
            query = _build_query(hypothesis.extracted_entities, operator="AND")
            search_results = wikisearch.search(query, results=max_results)

            if not search_results:
                query = _build_query(hypothesis.extracted_entities, operator="OR")
                search_results = wikisearch.search(query, results=max_results)

        # Priority 2: Use extracted terms if entities fail
        if not search_results and hypothesis.extracted_terms:
            query = _build_query(hypothesis.extracted_terms, operator="AND")
            search_results = wikisearch.search(query, results=max_results)

            if not search_results:
                query = _build_query(hypothesis.extracted_terms, operator="OR")
                search_results = wikisearch.search(query, results=max_results)

        if not search_results:
            return []

        article_data = []
        for title in search_results:
            page = wiki.page(title)

            if not page.exists():
                continue

            # Extract relevant details
            article_data.append({
                "title": page.title,
                "summary": page.summary,
                "url": page.fullurl,
                "text": page.text
            })

            if len(article_data) >= max_results:
                break

        if DEBUG_MODE:
            output_file = "../debug/wikipedia_results.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(article_data, f, ensure_ascii=False, indent=4)

        return article_data

    except Exception as e:
        raise e
