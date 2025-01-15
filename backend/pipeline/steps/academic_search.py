import json
import logging
import os
import time
from typing import List, Dict, Optional
import urllib.parse
from datetime import datetime, timezone
import httpx
import dateutil.parser
from db.models import Hypothesis
from sqlalchemy.orm import Session
from openai import OpenAI
from crud.academic_works import create_academic_work
from schemas.academic_works import AcademicWorkCreate, AcademicWorkResponse
from fastapi.encoders import jsonable_encoder

client = OpenAI()

logger = logging.getLogger(__name__)

CORE_API_KEY = os.getenv("CORE_API_KEY")

async def _build_search_query(hypothesis: Hypothesis, max_length: int = 80) -> str:
    """
    Builds a URL-encoded query string from extracted hypothesis data.
    """
    tokens = set(
        (hypothesis.extracted_topics or [])
        + (hypothesis.extracted_terms or [])
        + (hypothesis.extracted_entities or [])
    )

    # Join with AND for more precise searching
    raw_query = " AND ".join(tokens)

    # Truncate if too long
    if len(raw_query) > max_length:
        raw_query = raw_query[:max_length]

    # CORE queries often benefit from restricting to docs with abstracts
    raw_query += " AND _exists_:description"

    return urllib.parse.quote(raw_query)

async def _build_search_query_with_gpt(hypothesis: Hypothesis, max_length: int = 80) -> str:
    """
    Refines a hypothesis into a search query string compatible with CORE API.

    Returns:
        str: A CORE API-compatible search query string.
    """

    # Default to an empty list if entities are None
    extracted_entities = hypothesis.extracted_entities or []

    # Prepare input for GPT-4
    prompt = (
        "Using the following inputs, generate a structured search query compatible with CORE API. "
        "Use logical operators like AND, OR, and parentheses for grouping. Prioritize combining "
        "extracted topics with extracted terms using AND, and include entities if they exist. "
        f"Ensure the query is concise and accurate. The maximum string length is {max_length}\n\n"
        f"Topics: {hypothesis.extracted_topics}\n"
        f"Terms: {hypothesis.extracted_terms}\n"
        f"Entities: {extracted_entities}\n\n"
        "Output only the search query string, no extra text."
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-4o-mini", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "system", "content": "You are a concise, factual assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # lower temperature => less creativity, more accuracy
    )

    query = response.choices[0].message.content
    logger.info("[CORE] search query: %s", query)

    return query


async def _fetch_results(
    query: str,
    exclude_text: Optional[bool] = False,
    limit: int = 5,
    scroll: bool = False,
    scroll_id: Optional[str] = None
) -> Dict:
    """
    Low-level function to fetch data from CORE API with rate-limit handling.
    """
    base_url = "https://api.core.ac.uk/v3/search/works"
    headers = {"Authorization": f"Bearer {CORE_API_KEY}"}

    params = {
        "q": query,
        "limit": str(limit),
    }
    if exclude_text:
        params["exclude"] = "fullText"
    if scroll:
        params["scroll"] = "true"
    if scroll_id:
        params["scrollId"] = scroll_id

    async with httpx.AsyncClient(follow_redirects=True) as async_client:
        while True:
            response = await async_client.get(base_url, headers=headers, params=params)

            # Handle 429 (rate limit)
            if response.status_code == 429:
                retry_after_str = response.headers.get("X-RateLimit-Retry-After")
                if retry_after_str:
                    retry_time = dateutil.parser.parse(retry_after_str)
                    now_utc = datetime.now(timezone.utc)
                    if retry_time > now_utc:
                        sleep_secs = (retry_time - now_utc).seconds + 1
                        time.sleep(sleep_secs)
                        continue
                else:
                    time.sleep(5)
                    continue
            elif response.status_code >= 500:
                # Server-side error
                time.sleep(5)
                continue
            elif response.status_code != 200:
                # Non-recoverable error
                logger.error("[CORE] HTTP %s: %s", response.status_code, response.text)
                response.raise_for_status()

            data = response.json()
            return data

async def perform_academic_search(
        hypothesis: Hypothesis,
        db: Session = None,
        overall_limit: int = 10,
        exclude_fulltext: Optional[bool] = False) -> List[AcademicWorkResponse]:
    """
    High-level function to query the CORE API for open-access papers.
    """
    query_str = await _build_search_query_with_gpt(hypothesis, max_length=80)
    response_data = await _fetch_results(
        query_str,
        exclude_fulltext,
        limit=overall_limit,
        scroll=False
    )

    results = response_data.get("results", [])
    if not results:
        return []

    parsed_results = []
    used_titles = set()

    for item in results:
        title = item.get("title")
        if not title or title in used_titles:
            continue

        # Construct the academic work object
        academic_work = AcademicWorkCreate(
            abstract=item.get("abstract") or item.get("description", ""),
            authors=item.get("authors", []),
            core_id=str(item.get("id")),
            full_text=item.get("fullText", ""),
            published_date=item.get("publishedDate", ""),
            publisher=item.get("publisher", ""),
            title=title,
            year_published=str(item.get("yearPublished")) or None
        )

        # Create the academic work in the database
        created_work = await create_academic_work(db, academic_work)

        # Convert the created work into a dictionary if needed
        if created_work:
            # Assuming `created_work` is an object, convert to dict
            created_work_response = AcademicWorkResponse.model_validate(created_work)
            created_work_dict = json.loads(created_work_response.model_dump_json())
            used_titles.add(title)
            parsed_results.append(created_work_dict)

        # Stop if we've reached the overall limit
        if len(parsed_results) >= overall_limit:
            break

    return parsed_results
