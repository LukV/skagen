import logging
import re
import json
from typing import Any, Dict, List
from db.models import Hypothesis
from openai import OpenAI, OpenAIError

client = OpenAI()

logger = logging.getLogger(__name__)

async def _parse_core_record(record: Dict) -> Dict:
    """Parse a CORE API record to retrieve relevant fields"""

    title = record.get("title", "Untitled")
    paper_abstract = record.get("abstract") or record.get("description", "")
    full_text = record.get("fullText", "")
    raw_authors = record.get("authors", [])
    authors_formatted = []
    for author in raw_authors:
        full_name = author.get("name", "").strip()
        if not full_name:
            continue

        if "," in full_name:
            # Already in "LastName, FirstName" format
            last_first = full_name.split(",")
            last_name = last_first[0].strip()
            first_name = last_first[1].strip() if len(last_first) > 1 else ""
        else:
            # Possibly "FirstName LastName"
            name_parts = full_name.split()
            last_name = name_parts[-1]
            first_name = " ".join(name_parts[:-1])

        # Build "LastName, F." (initials only for first name)
        initials = [f"{x[0]}." for x in first_name.split() if x]  # e.g. "Melissa" -> "M."
        initials_str = " ".join(initials)
        if initials_str:
            formatted_name = f"{last_name}, {initials_str}"
        else:
            # fallback if first name is absent
            formatted_name = last_name

        authors_formatted.append(formatted_name)

    # Join multiple authors with commas for a simple APA-like style
    authors_str = ", ".join(authors_formatted) if authors_formatted else "No listed authors"

    year = record.get("yearPublished", None)
    if not year:
        published_date = record.get("publishedDate", "")
        year_match = re.search(r"(\d{4})", published_date)  # simple 4-digit year
        if year_match:
            year = year_match.group(1)
        else:
            year = "n.d."  # no date

    publisher = record.get("publisher", "")

    display_url = ""
    links = record.get("links", [])
    for link in links:
        if link.get("type") == "display":
            display_url = link.get("url", "")
            break

    if not display_url:
        # If we have a "downloadUrl" or something else, we could use it
        display_url = record.get("downloadUrl", "")

    # Build APA-like Citation
    pub_str = f"{publisher}." if publisher else ""
    apa_citation = f"{authors_str} ({year}). {title}. {pub_str} {display_url}".strip()

    # Return a structured dict
    return {
        "title": title,
        "abstract": paper_abstract,
        "authors": authors_formatted,        # list of parsed authors
        "full_text": full_text,
        "year": year,
        "publisher": publisher,
        "url": display_url,
        "citation_apa": apa_citation
    }

async def _prepare_prompt(hypothesis_content: str, search_results: List[Dict[str, Any]]) -> str:
    """
    Prepare a prompt to feed into an LLM or summarization engine.
    You can customize the prompt style, level of detail, chain-of-thought requests, etc.
    """
    # Intro / system role
    system_instruction = (
        "You must only rely on the given search results when forming your summary and conclusions. "
        "Do not fabricate or hallucinate sources or additional claims."
    )

    # User's hypothesis
    user_statement = (
        f"The user’s hypothesis is:\n\"{hypothesis_content}\"\n\n"
        "The user wants to see if current research supports, refutes, \
            or remains inconclusive about this hypothesis."
    )

    # Papers context
    papers_intro = "Below are the relevant search results:\n"
    papers_list = []
    for idx, paper in enumerate(search_results, start=1):
        parsed_paper = await _parse_core_record(paper)
        title = parsed_paper.get("title", "No Title")
        citation_apa = parsed_paper.get("citation_apa", "No Citation")
        snippet = paper.get("abstract", "No abstract provided")

        papers_list.append(
            f"{idx}. Citation (APA-like): {citation_apa}\n"
            f"   Title: {title}\n"
            f"   Abstract/Snippet:\n"
            f"   {snippet}\n"
        )

    papers_str = "\n".join(papers_list)

    # Instructions for final output
    instructions = (
        "Based on these search results:\n"
        "### Task\n"
        "Given the hypothesis and the list of search results:\n"
        "1. **Classify** the hypothesis:\n"
        "   - `[A] Supported`: Evidence agrees with the hypothesis.\n"
        "   - `[B] Partially Supported`: Some evidence agrees; others are neutral \
            or contradictory.\n"
        "   - `[C] Inconclusive`: Evidence is neutral or conflicting.\n"
        "   - `[D] Refuted`: Evidence disagrees with the hypothesis.\n\n"
        "2. **Motivation**: Provide an explanation for the classification, with an \
                overall summary and then references to each source, use markdown, and \
                    formatted as:\n"
        "   - Brief summary of the overall findings.\n"
        "   - Per source a list item:\n"
        "     - Source **1**: Supports the hypothesis by showing evidence of...\n"
        "     - Source **2**: Refutes the hypothesis due to...\n\n"
        "3. **Sources**: List *all* sources by index, including the citation and URL.\n\n"
        "### Output Format\n"
        "{{\n"
        "    \"classification\": \"A | B | C | D\",\n"
        "    \"motivation\": \"Explanation with references to source indices.\",\n"
        "    \"sources\": [\n"
        "        {{\"index\": 1, \"citation\": \"APA-like citation\", \"url\": \"source URL\"}},\n"
        "        ...\n"
        "    ]\n"
        "}}"
        "5. Do not invent or cite sources that are not in the provided search results.\n"
        "6. Do not include additional keys in your JSON; adhere to the exact schema.\n"
        "7. Make sure the JSON is valid (no trailing commas, no additional text \
                    outside the JSON, no additional or redundant braces, characters escaped).\n"
    )

    prompt = (
        f"System Instruction:\n{system_instruction}\n\n"
        f"User Statement:\n{user_statement}\n\n"
        f"{papers_intro}{papers_str}\n\n"
        f"{instructions}"
    )

    return prompt


async def _perform_llm_summarization(prompt: str) -> Dict[str, Any]:
    """
    Uses one LLM prompt to extract:
      1) label
      2) summary
      3) motivation
    Returns a dict.
    """
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-4o-mini", "gpt-3.5-turbo", etc.
        messages=[
            {
                "role": "system", 
                "content": "You are an AI research assistant tasked with \
                    summarizing academic search results for a user's \
                        hypothesis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # lower temperature => less creativity, more accuracy
    )

    content = response.choices[0].message.content
    print(content)

    try:
        # Handle extra braces
        sanitized_content = content.strip()
        if sanitized_content.startswith('{{') and sanitized_content.endswith('}}'):
            sanitized_content = sanitized_content[1:-1]  # Remove one level of braces

        # Sanitize invalid Unicode sequences
        sanitized_content = re.sub(
            r'\\u([0-9a-fA-F]{0,3}[^0-9a-fA-F])', 
            r'\\u00\1', 
            sanitized_content
        )
        sanitized_content = sanitized_content.replace('\n', '').replace('\r', '').strip()

        # Parse the JSON
        parsed = json.loads(sanitized_content)
    except (OpenAIError, json.JSONDecodeError) as e:
        # Fallback if the LLM output isn't valid JSON
        parsed = {
            "classification": "error",
            "motivation": f"Internal error: {e}",
            "sources": []
        }

    return parsed

async def summarize_results(
    search_results: List[Dict[str, Any]],
    hypothesis: Hypothesis
    ) -> Dict[str, Any]:
    """
    Summarize the results of academic search, referencing relevant sources.
    Return a JSON-like dict with 'label', 'summary', 'motivation', 'sources', 
    and 'chain_of_thought'.
    
    Args:
        search_results (List[Dict[str, Any]]): A list of search results (papers).
    
    Returns:
        Dict[str, Any]: A structured response containing classification label,
                        summary, motivation, chain_of_thought, and source citations.
    """
    if not search_results:
        logger.warning("No search results provided to summarization step.")
        return {
            "classification": "no_data",
            "motivation": "No papers were provided.",
            "sources": []
        }

    prompt = await _prepare_prompt(hypothesis.content, search_results)

    try:
        llm_response = await _perform_llm_summarization(prompt)
        return llm_response
    except (OpenAIError, json.JSONDecodeError) as e:
        logger.error("Error summarizing results: %s", str(e))
        return {
            "classification": "error",
            "motivation": f"Internal error: {e}",
            "sources": []
        }
