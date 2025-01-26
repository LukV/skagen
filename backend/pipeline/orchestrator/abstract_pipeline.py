from pipeline.utils.helpers import publish_update, handle_pipeline_error
from sqlalchemy.orm import Session
from db.models import Hypothesis
from openai import OpenAI

client = OpenAI()

async def start_abstract_pipeline(hypothesis: Hypothesis, db: Session):
    """
    Orchestrates the abstract hypothesis validation pipeline.
    """
    try:
        step = "InterpretAbstractClaim"
        title = "Interpreting Abstract Claim"

        await publish_update(hypothesis, step, title)

        # Generate discourse using LLM
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a critical thinker trying \
                 to challenge the input hypotheses, based on facts for which you cite sources."},
                {"role": "user", "content": f"Interpret and discuss the claim: {hypothesis.content}"}
            ],
        )
        hypothesis.result = response.choices[0].message.content
        hypothesis.status = "Completed"
        db.commit()

        await publish_update(hypothesis, step, title, comment="Abstract claim processed.")

    except Exception as e:
        await handle_pipeline_error(e, step, title, hypothesis, db)