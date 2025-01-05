import os
import urllib.parse
import time
from datetime import datetime, timezone
import httpx
import dateutil.parser
from dotenv import load_dotenv
from backend.db.models import Hypothesis

load_dotenv()

CORE_API_KEY = os.getenv("CORE_API_KEY")

async def build_search_query(
    hypothesis: Hypothesis,
    max_length: int = 80
) -> str:
    """
    Generates a search-engine-style query string from extracted NLU data.
    Optionally, you can integrate an LLM here to refine or expand with synonyms.
    """

    # Combine all extracted items (filter out duplicates)
    tokens = list(set(hypothesis.extracted_topics +
            hypothesis.extracted_terms +
            hypothesis.extracted_entities)) # type: ignore

    # Example approach: join tokens with " AND " for a more precise query
    # You can tweak logic or use an LLM to add synonyms / synonyms list
    query = " AND ".join(tokens)

    # Optionally limit length
    if len(query) > max_length:
        query = query[:max_length]

    # CORE queries often benefit from ensuring a field with an abstract/description
    # We might add 'and _exists_:description' or 'AND _exists_:description'
    # to focus on papers with abstracts
    query += " AND _exists_:description"

    # URL-encode the query to be safe for GET params
    encoded_query = urllib.parse.quote(query)
    return encoded_query

async def fetch_core_results(
    base_url: str,
    query: str,
    limit: int = 5,
    scroll: bool = False,
    scroll_id: str = ""
) -> dict:
    """
    Makes a single GET request to the CORE API, handling rate-limit (429) and server errors (5xx).

    Args:
        base_url (str): The CORE API endpoint for searching works.
        query (str): The encoded query string.
        limit (int): Number of results to fetch per request.
        scroll (bool): Whether to use scrolling to retrieve more results.
        scroll_id (str): An optional scroll ID if continuing a scroll.

    Returns:
        dict: Parsed JSON response from the CORE API.
    """
    headers = {"Authorization": f"Bearer {CORE_API_KEY}"}
    url = f"{base_url}?q={query}&limit={limit}"

    if scroll:
        url += "&scroll=true"
    if scroll_id:
        url += f"&scrollId={scroll_id}"

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url, headers=headers)

            # Handle rate limit (429) with X-RateLimit-Retry-After
            if response.status_code == 429:
                retry_after_str = response.headers.get('X-RateLimit-Retry-After')
                if retry_after_str:
                    retry_after = dateutil.parser.parse(retry_after_str)
                    now = datetime.now(timezone.utc)
                    if retry_after > now:
                        sleep_time = (retry_after - now).seconds + 1
                        time.sleep(sleep_time)
                        continue
                else:
                    # If no retry header, do a fallback sleep
                    time.sleep(5)
                    continue
            elif response.status_code >= 500:
                response.raise_for_status()

            data = response.json()
            return data

async def search_core(
        hypothesis: Hypothesis,
        overall_limit: int = 5) -> list[dict]:
    """
    High-level function to query the CORE API for academic papers.

    Steps:
      1. Build a query from topics, terms, entities.
      2. Fetch results (can do single or scroll approach).
      3. Parse and return up to 'overall_limit' results.

    Returns:
        list[dict]: A list of result dictionaries.
    """
    base_url = "https://api.core.ac.uk/v3/search/works"

    # 1. Generate search query
    encoded_query = await build_search_query(hypothesis)

    # 2. Fetch initial batch
    response_data = await fetch_core_results(
        base_url,
        encoded_query,
        limit=overall_limit,
        scroll=False)

    if "results" not in response_data:
        return []

    results_list = response_data["results"]

    # If you want scrolling to get more pages, set scroll=True and handle the logic:
    # scroll_id = response_data.get("scrollId")
    # while scroll_id and len(results_list) < overall_limit:
    #     next_data = await fetch_core_results(
    #           base_url, encoded_query,
    #           limit=overall_limit, scroll=True, scroll_id=scroll_id)
    #     scroll_id = next_data.get("scrollId")
    #     more_results = next_data.get("results", [])
    #     results_list.extend(more_results)
    #     # break if there's no scrollId or we've reached overall_limit

    # 3. Parse final results, up to overall_limit
    parsed_results = []
    used_titles = set()
    for item in results_list:
        title = item.get("title")
        if not title or title in used_titles:
            continue

        parsed_results.append({
            "id": item.get("id"),
            "title": title,
            "authors": item.get("authors", []),
            "abstract": item.get("description"),
            "full_text_link": item.get("fullTextUrl"),
            "source": "CORE"
        })
        used_titles.add(title)

        if len(parsed_results) >= overall_limit:
            break

    print(f"Found {len(parsed_results)} results from CORE.")
    return parsed_results
