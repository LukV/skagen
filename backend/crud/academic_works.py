import re
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import academic_works as work_schemas
from db import models
from core import utils

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

    return ", ".join(authors_formatted) if authors_formatted else "No listed authors"

def _format_year(published_date: str) -> str:
    year = "n.d."
    year_match = re.search(r"(\d{4})", published_date)  # simple 4-digit year
    if year_match:
        year = year_match.group(1)
    return year
