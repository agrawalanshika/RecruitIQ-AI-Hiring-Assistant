from app.agents.recruitement_agent import (
    recruitment_agent
)


def evaluate_candidate_with_agent(

    resume_path,
    jd_text
):

  

    query = f"""

    Evaluate this candidate.

    Use autonomous_resume_evaluator_tool.

    Input format MUST be:

    RESUME_PATH:
    {resume_path}

    JOB_DESCRIPTION:

    {jd_text}

    """

   

    response = recruitment_agent.invoke({

        "input": query
    })

    return response["output"]
