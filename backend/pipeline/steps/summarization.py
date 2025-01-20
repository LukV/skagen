import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Any, Dict, List
from db.models import AcademicWork
from openai import OpenAI, OpenAIError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

client = OpenAI()
logger = logging.getLogger(__name__)

async def _perform_llm_summarization(abstract: str) -> dict:
    """
    Uses one LLM prompt to extract a summary for a research paper's abstract.

    Args:
        abstract (str): The abstract text of the research paper.

    Returns:
        dict: A JSON object containing the summary and key topics.
        Format: {
            "summary": str,
            "topics": list[str]
        }
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI research assistant tasked with three tasks: "
                        "1/ with summarizing an academic paper's abstract to 1 to 3 "
                        "paragraphs (1200 to 1500 characters in total). Use Markdown "
                        "to format the summary and seperate into paragraphs." 
                        "2/ From that derive a 200 character introductory paragraph summary. "
                        "3/ Derive up to two key topics that encapsulate the main "
                        "themes or concepts of the abstract. "
                        "Respond in the format: \n"
                        "{\"summary\": \"<summary in Markdown format>\", \
                            \"phrase\": \"<phrase>\", \
                            \"topics\": [\"<topic1>\", \"<topic2>\"]}"
                        "All three elements summary, phrase, topics are required." 
                        "Please use valid JSON, and Markdown for the summary."
                    ),
                },
                {"role": "user", "content": abstract},
            ],
        )
        content = response.choices[0].message.content

        if content.startswith("```") and content.endswith("```"):
            content = content.split("\n", 1)[-1].rsplit("\n", 1)[0]

        parsed = json.loads(content)

    except (OpenAIError, json.JSONDecodeError) as e:
        logger.error("Error during LLM summarization: %s", e)
        # Fallback
        parsed = {
            "summary": e,
            "phase": "",
            "topics": []
        }
    
    return parsed

def _get_existing_completion(session: Session, academic_work_id: str) -> tuple:
    """
    Check if an LLM summary exists for a given AcademicWork ID in the database.

    Args:
        session (Session): The database session.
        academic_work_id (str): The ID of the AcademicWork to check.

    Returns:
        str: The existing summary or None if not found.
    """
    try:
        academic_work = session.query(AcademicWork).filter_by(id=academic_work_id).first()
        return (
            academic_work.llm_summary,
            academic_work.llm_phrase,
            academic_work.llm_keywords
        ) if academic_work else None
    except SQLAlchemyError as e:
        logger.error("Error checking llm_summary for ID %s: %s", academic_work_id, e)
        raise

def _update_llm_summary(session: Session, academic_work_id: str, completion: dict) -> None:
    """
    Update the llm_summary column for a given AcademicWork object.

    Args:
        session (Session): The database session.
        academic_work_id (str): The ID of the AcademicWork to update.
        summary (str): The summary to save in the llm_summary column.

    Returns:
        None
    """
    try:
        academic_work = session.query(AcademicWork).filter_by(id=academic_work_id).first()
        if academic_work:
            academic_work.llm_summary = completion["summary"]
            academic_work.llm_phrase = completion["phrase"]
            academic_work.llm_keywords = completion["topics"]
            session.commit()
            logger.info("Updated llm_summary for AcademicWork ID: %s", academic_work_id)
        else:
            logger.warning("AcademicWork ID %s not found.", academic_work_id)
    except SQLAlchemyError as e:
        logger.error("Error updating llm_summary for ID %s: %s", academic_work_id, e)
        session.rollback()
        raise

async def summarize_abstracts(
        search_results: List[Dict[str, Any]],
        session: Session
) -> Dict[str, Any]:
    """
    Summarize the abstracts of academic search results and update the database.

    Args:
        search_results (List[Dict[str, Any]]): A list of search results 
        containing titles and abstracts.
        session (Session): The database session for updates.

    Returns:
        Dict[str, Any]: A dictionary summarizing the results.
    """
    summaries_map = {}

    for result in search_results:
        title = result.get("title", "No title available")
        abstract = result.get("abstract") or result.get("fullText", "")
        academic_work_id = result.get("id")

        if not abstract or not academic_work_id:
            logger.warning("Skipping result with missing abstract or ID: %s", title)
            continue

        combined_text = f"{title}\n{abstract}"
        logger.info("Processing abstract for paper: %s", title)

        # Check for existing summary in the database
        existing_completion = _get_existing_completion(session, academic_work_id)
        if existing_completion and all(existing_completion):
            logger.info("Using existing summary for AcademicWork ID: %s", academic_work_id)
            summaries_map[academic_work_id] = {
                "summary": existing_completion[0],  # llm_summary
                "phrase": existing_completion[1],   # llm_phrase
                "topics": existing_completion[2]    # llm_keywords
            }
        else:
            try:
                # Perform LLM summarization
                completion = await _perform_llm_summarization(combined_text)
                summaries_map[academic_work_id] = completion

                # Update the summary in the database using ThreadPoolExecutor
                with ThreadPoolExecutor() as executor:
                    await asyncio.get_running_loop().run_in_executor(
                        executor, _update_llm_summary, session, academic_work_id, completion
                    )
            except (RuntimeError, SQLAlchemyError, OpenAIError) as e:
                logger.error("Failed to summarize or update \
                             AcademicWork ID %s: %s", academic_work_id, e)

    # Enrich search_results with summaries
    for result in search_results:
        academic_work_id = result.get("id")
        if academic_work_id in summaries_map:
            result["summary"] = summaries_map[academic_work_id]["summary"]
            result["phrase"] = summaries_map[academic_work_id]["phrase"]
            result["keywords"] = summaries_map[academic_work_id]["topics"]

    return search_results

