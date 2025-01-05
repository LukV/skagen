import httpx
import asyncio
from typing import List, Dict
from pipeline.steps.academic_sources.core import search_core
from db.models import Hypothesis

async def search_pubmed(hypothesis: Hypothesis) -> List[Dict]:
    """Query the PubMed API for biomedical papers."""
    tokens = list(set(hypothesis.extracted_topics + 
            hypothesis.extracted_terms + 
            hypothesis.extracted_entities)) # type: ignore
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": " OR ".join(tokens),
        "retmode": "json",
        "retmax": 5 
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            ids = data.get("esearchresult", {}).get("idlist", [])
            return [{"pubmed_id": pid, "source": "PubMed"} for pid in ids]
        except Exception as e:
            print(f"Error querying PubMed: {e}")
            return []


async def search_europe_pmc(hypothesis: Hypothesis) -> List[Dict]:
    """Query the Europe PMC API for academic papers."""
    tokens = list(set(hypothesis.extracted_topics + 
            hypothesis.extracted_terms + 
            hypothesis.extracted_entities)) # type: ignore
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    results = []
    limit = 5 

    for token in tokens:
        params = {
            "query": token,
            "resultType": "core",
            "pageSize": limit,
            "format": "json"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                for item in data.get("resultList", {}).get("result", []):
                    results.append({
                        "title": item.get("title"),
                        "authors": item.get("authorString"),
                        "abstract": item.get("abstractText"),
                        "full_text_link": item.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url"),
                        "source": "Europe PMC"
                    })
            except Exception as e:
                print(f"Error querying Europe PMC for term '{token}': {e}")
    return results


async def search_doaj(hypothesis: Hypothesis) -> List[Dict]:
    """Query the DOAJ API for open-access journals."""
    tokens = list(set(hypothesis.extracted_topics + 
            hypothesis.extracted_terms + 
            hypothesis.extracted_entities)) # type: ignore
    
    base_url = "https://doaj.org/api/v1/search/articles"
    results = []
    limit = 5 

    for token in tokens:
        params = {"q": token, "pageSize": limit}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                for item in data.get("results", []):
                    results.append({
                        "title": item.get("bibjson", {}).get("title"),
                        "authors": [author.get("name") for author in item.get("bibjson", {}).get("author", [])],
                        "abstract": item.get("bibjson", {}).get("abstract"),
                        "full_text_link": item.get("bibjson", {}).get("link", [{}])[0].get("url"),
                        "source": "DOAJ"
                    })
            except Exception as e:
                print(f"Error querying DOAJ for term '{token}': {e}")
    return results

async def perform_academic_search(hypothesis: Hypothesis) -> List[Dict]:
    """
    Perform academic search across multiple open-access sources.

    Args:
        terms (List[str]): Extracted terms from the hypothesis.
        query_type (str): Type of query ('factual', 'research-based', 'abstract').

    Returns:
        List[Dict]: Combined search results.
    """
    # Modular search tasks based on sources
    search_tasks = [
        search_core(hypothesis),
        search_pubmed(hypothesis),
        search_europe_pmc(hypothesis),
        search_doaj(hypothesis)
    ]

    # # Add pre-trained model inference for summarization/insights
    # if domain == "biomedical":
    #     # Example: PubMed GPT for biomedical domain
    #     async def pubmed_gpt_inference(terms):
    #         # Simulate model inference (replace with actual model call)
    #         return [{"summary": f"Inferred biomedical insights for {term}"} for term in terms]

    #     search_tasks.append(pubmed_gpt_inference(terms))
    # elif domain == "social-sciences":
    #     # Example: SPECTER or BLOOM for social sciences
    #     async def specter_inference(terms):
    #         return [{"summary": f"Inferred social science insights for {term}"} for term in terms]

    #     search_tasks.append(specter_inference(terms))

    # Run all searches concurrently
    results = await asyncio.gather(*search_tasks)

    # Flatten and deduplicate results
    combined_results = [item for sublist in results for item in sublist]
    unique_results = {item["title"]: item for item in combined_results}.values()

    return list(unique_results)