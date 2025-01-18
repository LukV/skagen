import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from db.models import AcademicWork
from typing import Any, Dict, List
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

def update_llm_summary(session: Session, academic_work_id: str, summary: str) -> None:
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
    tasks = []
    summaries_map = {}

    for result in search_results:
        title = result.get("title", "No title available")
        abstract = result.get("abstract", "")

        if not abstract:
            logger.warning("Skipping result with missing abstract: %s", result.get("id", "unknown ID"))
            continue

        combined_text = f"{title}\n{abstract}"
        logger.info("Summarizing abstract for paper: %s", title)

        # Perform LLM summarization
        summary_task = asyncio.create_task(_perform_llm_summarization(combined_text))
        tasks.append((result.get("id"), summary_task))

    for academic_work_id, task in tasks:
        try:
            summary = await task
            summaries_map[academic_work_id] = summary

            # Update the summary in the database using ThreadPoolExecutor
            with ThreadPoolExecutor() as executor:
                await asyncio.get_running_loop().run_in_executor(
                    executor, update_llm_summary, session, academic_work_id, summary
                )
        except (RuntimeError, SQLAlchemyError, OpenAIError) as e:
            logger.error("Failed to summarize or update AcademicWork ID %s: %s", academic_work_id, e)
        
        # Enrich search_results with summaries
    for result in search_results:
        academic_work_id = result.get("id")
        if academic_work_id in summaries_map:
            result["summary"] = summaries_map[academic_work_id]

    return search_results


