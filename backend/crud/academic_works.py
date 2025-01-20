import asyncio
import random
import re
import logging

import time
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy_pagination import paginate
from schemas import academic_works as work_schemas
from db import models
from core import utils
from openai import OpenAI, OpenAIError

client = OpenAI()
logger = logging.getLogger(__name__)

async def create_academic_work(
        db: Session,
        work: work_schemas.AcademicWorkCreate
) -> models.AcademicWork:
    """
    Adds a single academic work to the database.
    Skips if the record already exists.
    """
    work_id = utils.generate_id('W')
    core_id = work.core_id
    title = _remove_null_bytes(work.title)
    abstract = _remove_null_bytes(work.abstract)
    authors = [{"name": getattr(author, "name", author)} for author in work.authors]
    authors_formatted = _format_authors(authors)
    links = [
        {
            "type": getattr(link, "type", None),
            "url": getattr(link, "url", None),
        }
        for link in work.links
    ]
    year_published = work.year_published or _format_year(work.published_date)
    publisher = _remove_null_bytes(work.publisher)
    pub_str = f"{publisher}." if publisher else ""
    apa_citation = f"{authors_formatted} ({year_published}). {title}. {pub_str}".strip()
    full_text = _remove_null_bytes(work.full_text)

    db_work = models.AcademicWork(
        id = work_id,
        abstract = abstract,
        apa_citation = apa_citation,
        authors = authors,
        authors_formatted = authors_formatted,
        links = links,
        core_id = core_id,
        full_text = full_text,
        published_date = work.published_date,
        publisher = publisher,
        title = title,
        year_published = year_published
    )
    try:
        db.add(db_work)
        db.commit()
        db.refresh(db_work)
    except IntegrityError:
        db.rollback()  # Skip duplicates
        db_work = db.query(models.AcademicWork).filter(
            models.AcademicWork.core_id == core_id
        ).first()
    return db_work

def get_all_academic_works(db: Session, page: int, per_page: int) -> dict:
    """
    Retrieves academic works from the database with pagination.

    Args:
        db (Session): Database session.
        page (int): The page number to retrieve.
        per_page (int): The number of records per page.

    Returns:
        dict: A dictionary containing the current page, total pages, and the academic works.
    """
    query = db.query(models.AcademicWork)
    paginated_result = paginate(query, page, per_page)

    return {
        "total_pages": paginated_result.pages,
        "total_items": paginated_result.total,
        "current_page": page,
        "items": paginated_result.items,
    }

def get_academic_work_by_id(db: Session, academic_work_id: str) -> Optional[models.AcademicWork]:
    """
    Fetches an academic work by their id.
    """
    return db.query(models.AcademicWork).filter(
        models.AcademicWork.id == academic_work_id
    ).first()

def update_academic_work(
        db: Session,
        academic_work_id: str,
        update_data: work_schemas.AcademicWorkUpdate
) -> models.AcademicWork:
    """
    Updates an academic work in the database with the given update data.

    Args:
        db (Session): Database session.
        academic_work_id (str): The ID of the academic work to update.
        update_data (AcademicWorkUpdate): The data to update.

    Returns:
        AcademicWork: The updated academic work.
    """
    academic_work = get_academic_work_by_id(db, academic_work_id)
    if not academic_work:
        raise ValueError("Academic work not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(academic_work, field, value)

    db.commit()
    db.refresh(academic_work)
    return academic_work

async def update_null_llm_extended_summaries(db: Session):
    """
    Updates all academic works with null llm_extended_summary fields.

    Args:
        db (Session): Database session.
    """
    academic_works = db.query(models.AcademicWork).filter(
        models.AcademicWork.llm_extended_summary == None # pylint: disable=C0121
    ).all()

    for academic_work in academic_works:
        title = academic_work.title or ""
        abstract = academic_work.abstract or ""
        full_text = academic_work.full_text or ""
        text = f"# {title}\n ## Abstract \n {abstract} ## Article \n {full_text}"
        academic_work.llm_extended_summary = await _perform_llm_summerization(text)
        logger.info("Extended summary added for %s", title)

    db.commit()

async def _perform_llm_summerization(text: str) -> dict:
    """
    Uses one LLM prompt to extract a summary for a research paper's abstract.

    Args:
        text (str): The full input text.

    Returns:
        dict: A JSON object containing the summary and key topics.
    """
    text = _truncate_text(text, 5000)

    try:
        response = await _retry_request(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI research assistant tasked with rewriting "
                        "a research article in an \"academic breakdown\", "
                        "keeping all nuances and depth, yet using "
                        "clear language. Use Markdown to format your rewrite and separate "
                        "into paragraphs. Keep your article under 5000 words."
                    ),
                },
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error("Error during LLM summarization: %s", e)
        return "Summarization failed."

async def _retry_request(func, *args, max_retries=5, backoff_factor=1.5, **kwargs):
    for i in range(max_retries):
        try:
            return await asyncio.to_thread(func, *args, **kwargs)
        except OpenAIError:
            if i == max_retries - 1:
                raise
            wait_time = backoff_factor * (2 ** i) + random.uniform(0, 1)
            logger.warning("Retrying in %.2f seconds...", wait_time)
            await asyncio.sleep(wait_time)

def _truncate_text(text: str, max_length: int) -> str:
    """
    Truncates the text to the specified maximum length.

    Args:
        text (str): The input text to truncate.
        max_length (int): Maximum length of the text.

    Returns:
        str: Truncated text with an indicator if truncated.
    """
    return text[:max_length] + ("..." if len(text) > max_length else "")

def _remove_null_bytes(value: Optional[str]) -> Optional[str]:
    """
    Removes null bytes (\0) from a given string. If the input is None, it returns None.
    """
    if value is None:
        return None

    if '\0' in value:
        value = value.replace('\0', '')
    return value

def _format_authors(authors: List[Dict[str, str]]) -> str:
    authors_formatted = []
    for author in authors:
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

    formatted_authors = ", ".join(authors_formatted) if authors_formatted else "No listed authors"

    # Truncate to max length of 150 characters
    if len(formatted_authors) > 150:
        return formatted_authors[:147] + "..."

    return formatted_authors

def _format_year(published_date: str) -> str:
    year = "n.d."
    year_match = re.search(r"(\d{4})", published_date)  # simple 4-digit year
    if year_match:
        year = year_match.group(1)
    return year
