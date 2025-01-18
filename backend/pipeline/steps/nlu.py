from openai import OpenAI
import json

client = OpenAI()

async def extract_topic_terms(text: str) -> dict:
    """
    Uses one LLM prompt to extract:
      1) named_entities
      2) keywords
      3) topics
    Returns a dict with keys: 'named_entities', 'keywords', 'topics'.
    """
    prompt = f"""
    Please (1) extract data from the text below and (2) define the `query_type`. 
    The `query_type` should be one of the following: 'research-based', 'factual', or 'abstract'.

    1.	Query Types
	•	Factual: Simple, objective statements.
	•	Research-Based: Statements requiring evidence from academic literature.
	•	Abstract: Philosophical or interpretive ideas that lack a strict evidence base.
	2.	Query Type Definitions
	•	Factual:
	•	Example: “The UN headquarters are in New York.”
	•	Requires structured, factual sources (e.g., Wikidata, encyclopedias).
	•	Research-Based:
	•	Example: “Social media have a negative impact on children’s concentration.”
	•	Requires scholarly evidence (e.g., PubMed, CORE).
	•	Abstract:
	•	Example: “Nietzsche’s emphasis on the ‘will to power’ suggests that ambition stimulates innovation.”
	•	Requires interpretation and discourse, best handled by LLMs.
    
    Output valid JSON with double quotes, e.g. `"United Nations"` and no extra keys.

    Text:
    \"{text}\"

    Return a JSON object with exactly these keys:
    1. named_entities: an array of strings representing persons, organizations, or locations (multi-word allowed).
    2. keywords: an array of strings representing key phrases from the text (multi-word allowed).
    3. topics: an array of up to 3 broad conceptual topics relevant to the text.

    Output must be valid JSON with double quotes and no extra keys. For example:
    {{
      "named_entities": [],
      "keywords": [],
      "topics": [],
      "query_type": "research-based"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o-mini", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "system", "content": "You are a concise, factual assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # lower temperature => less creativity, more accuracy
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
            "topics": []
        }

    return parsed
