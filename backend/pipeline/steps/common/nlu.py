import json
from openai import OpenAI

client = OpenAI()

async def extract_topic_terms(text: str) -> dict:
    """
    Enhanced LLM-based NLU to categorize claims.
    """
    prompt = f"""
    Classify the text below into one of the following `query_type` categories:
      - factual: Objective, verifiable facts (e.g., "The Berlin Wall fell in 1989.").
      - definitional: Claims requiring general evidence from the web (e.g., "5G technology causes cancer.").
      - research-based: Requires academic evidence (e.g., "Social media impacts mental health.").
      - abstract: Interpretative or philosophical ideas (e.g., "Nietzsche’s philosophy emphasizes ambition.").
      - subjective: Personal opinions or preferences (e.g., "Roses are prettier than tulips.").
      - unknown: If the category is unclear or ambiguous.

    Also extract:
      - named_entities: Entities like persons, organizations, locations.
      - keywords: Key phrases from the claim.
      - topics: Up to 3 broad topics.

    Text:
    \"{text}\"

    Return valid JSON:
    {{
      "named_entities": [],
      "keywords": [],
      "topics": [],
      "query_type": "factual/definitional/research-based/abstract/subjective/unknown"
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a concise, factual assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    content = response.choices[0].message.content

    if content.startswith("```") and content.endswith("```"):
        content = content.split("\n", 1)[-1].rsplit("\n", 1)[0]
    
    try:
        parsed = json.loads(content) # type: ignore
    except json.JSONDecodeError:
        # Fallback if the LLM output isn't valid JSON
        parsed = {
            "named_entities": [],
            "keywords": [],
            "topics": [],
            "query_type": "unknown"
        }

    return parsed
