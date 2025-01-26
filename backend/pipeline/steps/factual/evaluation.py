import json
from typing import Any, Dict, List
from openai import OpenAI, OpenAIError
from db.models import Hypothesis

client = OpenAI()


async def _prepare_prompt(hypothesis_content: str, search_results: List[Dict[str, Any]]) -> str:
    """
    Prepare a prompt to feed into an LLM or summarization engine.
    You can customize the prompt style, level of detail, chain-of-thought requests, etc.
    """
    # User's hypothesis
    user_statement = (
        f"The user’s claim is:\n\"{hypothesis_content}\"\n\n"
        "The user wants to see if below seach results support, refute, \
            or remain inconclusive about this claim."
    )

    # Papers context
    papers = f"Below are the relevant articles:\n\n{search_results}"

    # Instructions for final output
    instructions = (
        "Based on these Wikipedia articles:\n"
        "### Task\n"
        "1. **Classify** the claim:\n"
        "   - `[A] Supported`: Evidence agrees with the hypothesis.\n"
        "   - `[B] Partially Supported`: Some evidence agrees; others are neutral \
            or contradictory.\n"
        "   - `[C] Inconclusive`: Evidence is neutral or conflicting.\n"
        "   - `[D] Refuted`: Evidence disagrees with the hypothesis.\n\n"
        "2. **Motivation**: Provide a concise explanation for your classification:\n"
        "   - Brief summary of the overall findings.\n"
        "   - Highlight the most relevant articles.\n"
        "{{\n"
        "    \"classification\": \"A | B | C | D\",\n"
        "    \"motivation\": \"Explanation with references to source indices.\",\n"
        "}}"
        "3. Do not invent or cite sources that are not in the provided search results.\n"
        "4. Make sure the JSON is valid (no trailing commas, no additional text \
                    outside the JSON, no additional or redundant braces, characters escaped).\n"
    )

    prompt = (
        f"User Statement:\n{user_statement}\n\n"
        f"{papers}\n\n"
        f"{instructions}"
    )

    return prompt

async def _perform_llm_summarization(prompt: str) -> Dict[str, Any]:
    """
    Uses one LLM prompt to extract an evaluation based on an 
    input prompt.
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o-mini", "gpt-3.5-turbo", etc.
        messages=[
            {
                "role": "system", 
                "content": "You are concise, factual assistant tasked with \
                    evaluating academic search results to support or refute \
                         a user's hypothesis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # lower temperature => less creativity, more accuracy
    )

    content = response.choices[0].message.content
    if content.startswith("```") and content.endswith("```"):
        content = content.split("\n", 1)[-1].rsplit("\n", 1)[0]

    try:
        parsed = json.loads(content)
    except (OpenAIError, json.JSONDecodeError) as e:
        # Fallback if the LLM output isn't valid JSON
        parsed = {
            "classification": "error",
            "motivation": f"Internal error: {e}"
        }

    return parsed

async def evaluate_factual_claim(hypothesis: Hypothesis, article_data: List[Dict[str, Any]]):
    """
    Example step: Evaluate the factual claim.
    Replace this with actual implementation.
    """
    # Prepare the prompt for evaluation
    prompt = await _prepare_prompt(hypothesis.content, article_data)

    try:
        # Use LLM to analyze the hypothesis based on article data
        llm_response = await _perform_llm_summarization(prompt)

        # Add articles and highlight the most relevant one
        sources = []
        for idx, article in enumerate(article_data, start=1):
            sources.append({
                "index": idx,
                "title": article.get("title", "No Title"),
                "url": article.get("url"),
                "summary": article.get("summary", "No summary provided."),
                "relevant": False  # To be updated based on LLM response
            })

        # Highlight the key article if mentioned in the motivation
        motivation = llm_response.get("motivation", "")
        for source in sources:
            if source["title"] in motivation:
                source["relevant"] = True

        # Add sources with relevance info to the response
        llm_response["sources"] = sources

        return llm_response

    except Exception as e: # pylint: disable=broad-except
        return {
            "classification": "error",
            "motivation": f"An error occurred during evaluation: {e}"
        }
