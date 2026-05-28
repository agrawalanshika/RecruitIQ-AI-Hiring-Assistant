from app.agents.recruitement_agent import (
    recruitment_agent
)


# -----------------------------------
# Run ATS Agent
# -----------------------------------

def evaluate_candidate_with_agent(

    resume_path,
    jd_text
):

    # -----------------------------------
    # Build Agent Query
    # -----------------------------------

    query = f"""

    Evaluate this candidate.

    Use autonomous_resume_evaluator_tool.

    Input format MUST be:

    RESUME_PATH:
    {resume_path}

    JOB_DESCRIPTION:

    {jd_text}

    """

    # -----------------------------------
    # Invoke Agent
    # -----------------------------------

    response = recruitment_agent.invoke({

        "input": query
    })

    return response["output"]