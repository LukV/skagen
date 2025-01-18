import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Any, Dict, List
from db.models import AcademicWork
from openai import OpenAI, OpenAIError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

client = OpenAI()

logger = logging.getLogger(__name__)

async def _perform_llm_summarization(abstract: str) -> str:
    """
    Uses one LLM prompt to extract a summary for a research paper's abstract.

    Args:
        abstract (str): The abstract text of the research paper.

    Returns:
        str: The summarized content of the abstract.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI research assistant tasked with "
                        "summarizing an academic paper's abstract to 1 to 3 "
                        "paragraphs, with a total length of 1200 to 1500 characters."
                    ),
                },
                {"role": "user", "content": abstract},
            ],
        )
        return response.choices[0].message.content.strip()
    
    except OpenAIError as e:
        logger.error("Error during LLM summarization: %s", e)
        raise RuntimeError("Failed to summarize the abstract due to an LLM error.") from e
    
def _get_existing_summary(session: Session, academic_work_id: str) -> str:
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
        return academic_work.llm_summary if academic_work else None
    except SQLAlchemyError as e:
        logger.error("Error checking llm_summary for ID %s: %s", academic_work_id, e)
        raise

def _update_llm_summary(session: Session, academic_work_id: str, summary: str) -> None:
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
            academic_work.llm_summary = summary
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
        abstract = result.get("abstract", "")
        academic_work_id = result.get("id")

        if not abstract or not academic_work_id:
            logger.warning("Skipping result with missing abstract or ID: %s", result)
            continue

        combined_text = f"{title}\n{abstract}"
        logger.info("Processing abstract for paper: %s", title)

        # Check for existing summary in the database
        existing_summary = _get_existing_summary(session, academic_work_id)
        if existing_summary:
            logger.info("Using existing summary for AcademicWork ID: %s", academic_work_id)
            summaries_map[academic_work_id] = existing_summary
        else:
            try:
                # Perform LLM summarization
                summary = await _perform_llm_summarization(combined_text)
                summaries_map[academic_work_id] = summary

                # Update the summary in the database using ThreadPoolExecutor
                with ThreadPoolExecutor() as executor:
                    await asyncio.get_running_loop().run_in_executor(
                        executor, _update_llm_summary, session, academic_work_id, summary
                    )
            except (RuntimeError, SQLAlchemyError, OpenAIError) as e:
                logger.error("Failed to summarize or update AcademicWork ID %s: %s", academic_work_id, e)

    # Enrich search_results with summaries
    for result in search_results:
        academic_work_id = result.get("id")
        if academic_work_id in summaries_map:
            result["summary"] = summaries_map[academic_work_id]

    return search_results


