from langchain.tools import tool

from app.tools.resume_parser import (
    extract_text_from_pdf
)

from app.utils.text_cleaner import (
    clean_resume_text
)

from app.tools.llm_extractor import (
    extract_resume_data
)

from app.tools.jd_parser import (
    parse_job_description
)

from app.tools.matching_engine import (
    calculate_match_score
)

# -----------------------------------
# Resume Parser Tool
# -----------------------------------

@tool
def resume_parser_tool(

    resume_path: str
):

    """
    Parses a resume PDF and extracts
    structured candidate information.
    """

    resume_text = extract_text_from_pdf(

        resume_path
    )

    cleaned_resume = clean_resume_text(

        resume_text
    )

    resume_data = extract_resume_data(

        cleaned_resume
    )

    return str(resume_data)


# -----------------------------------
# JD Parser Tool
# -----------------------------------

@tool
def jd_parser_tool(

    jd_text: str
):

    """
    Parses a job description and extracts
    required skills and hiring criteria.
    """

    jd_data = parse_job_description(

        jd_text
    )

    return str(jd_data)


# -----------------------------------
# Autonomous Resume Evaluator Tool
# -----------------------------------

# -----------------------------------
# Autonomous Resume Evaluator Tool
# -----------------------------------

@tool
def autonomous_resume_evaluator_tool(

    input_data: str
):

    """
    Evaluates a candidate resume
    against a job description.
    """

    import re

    # -----------------------------------
    # Extract Resume Path
    # -----------------------------------

    resume_match = re.search(

        r"RESUME_PATH:\s*(.*?)\s*JOB_DESCRIPTION:",

        input_data,

        re.IGNORECASE | re.DOTALL
    )

    if not resume_match:

        return "Resume path not found."

    resume_path = resume_match.group(1).strip().replace(",","")

    # -----------------------------------
    # Extract Job Description
    # -----------------------------------

    jd_match = re.search(

        r"JOB_DESCRIPTION:(.*)",

        input_data,

        re.IGNORECASE | re.DOTALL
    )

    if not jd_match:

        return "Job description not found."

    jd_text = jd_match.group(1).strip()

    # -----------------------------------
    # Parse Resume
    # -----------------------------------

    resume_text = extract_text_from_pdf(

        resume_path
    )

    cleaned_resume = clean_resume_text(

        resume_text
    )

    resume_data = extract_resume_data(

        cleaned_resume
    )

    # -----------------------------------
    # Parse JD
    # -----------------------------------

    jd_data = parse_job_description(

        jd_text
    )

    # -----------------------------------
    # Calculate Match
    # -----------------------------------

    result = calculate_match_score(

        resume_data,

        jd_data
    )

    return str(result)