from langchain_groq import ChatGroq

from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain

from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# Load LLM
# -----------------------------------

llm = ChatGroq(

    model_name="llama-3.1-8b-instant",

    temperature=0
)

# -----------------------------------
# Prompt Template
# -----------------------------------

prompt = PromptTemplate(

    input_variables=[

        "job_description",

        "candidate_data"
    ],

    template="""

You are an expert HR recruiter.

Analyze all candidates for the given job description.

JOB DESCRIPTION:
{job_description}

CANDIDATES:
{candidate_data}

Tasks:

1. Compare all candidates
2. Identify strongest candidates
3. Identify weakest candidates
4. Recommend top hires
5. Explain WHY candidates were selected
6. Mention missing skills where relevant
7. Provide final recruiter summary

Give professional HR-style analysis.

"""
)

# -----------------------------------
# Workflow Chain
# -----------------------------------

workflow_chain = LLMChain(

    llm=llm,

    prompt=prompt
)

# -----------------------------------
# Run Workflow Agent
# -----------------------------------

def run_workflow_agent(

    jd_text,

    ranked_candidates
):

    # -----------------------------------
    # Build Candidate Summary
    # -----------------------------------

    candidate_summary = ""

    for idx, candidate in enumerate(

        ranked_candidates,

        start=1
    ):

        candidate_summary += f"""

Candidate {idx}

Name:
{candidate['Candidate Name']}

Final Score:
{candidate['Final Score']}

Recommendation:
{candidate['Recommendation']}

Matched Skills:
{candidate['Matched Skills']}

Missing Skills:
{candidate['Missing Skills']}

Explanation:
{candidate['Explanation']}

"""

    # -----------------------------------
    # Invoke LLM
    # -----------------------------------

    response = workflow_chain.run({

        "job_description": jd_text,

        "candidate_data": candidate_summary
    })

    return response