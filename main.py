import os

from app.tools.resume_parser import extract_text_from_pdf
from app.utils.text_cleaner import clean_resume_text
from app.tools.llm_extractor import extract_resume_data
from app.tools.jd_parser import parse_job_description
from app.tools.matching_engine import calculate_match_score
from app.tools.ranking_engine import rank_candidates
from app.tools.report_generator import generate_html_report



with open("data/sample_jd.txt", "r", encoding="utf-8") as file:

    jd_text = file.read()

jd_data = parse_job_description(jd_text)


resume_folder = "data/resumes"

candidate_results = []

for filename in os.listdir(resume_folder):

    if filename.endswith(".pdf"):

        file_path = os.path.join(

            resume_folder,

            filename
        )

        # Extract Resume Text
        resume_text = extract_text_from_pdf(file_path)

        cleaned_resume = clean_resume_text(resume_text)

        # Structured Resume Data
        resume_data = extract_resume_data(cleaned_resume)

        # Matching Score
        match_result = calculate_match_score(

            resume_data,

            jd_data
        )

        candidate_results.append({

            "resume_file": filename,

            "resume_data": resume_data,

            "match_result": match_result

        })


ranked_candidates = rank_candidates(

    candidate_results
)


print("\n=========== FINAL RANKING ===========\n")

for index, candidate in enumerate(ranked_candidates):

    print(f"Rank #{index + 1}")

    print(

        "Candidate:",

        candidate["resume_data"]["name"]
    )

    print(

        "Final Score:",

        candidate["match_result"]["final_score"]
    )

    print(

        "Recommendation:",

        candidate["match_result"]["recommendation"]
    )

    print(

        "Matched Skills:",

        candidate["match_result"]["matched_skills"]
    )

    print("\n----------------------------------\n")


report_path = generate_html_report(

    ranked_candidates
)

print("\nHTML Report Generated Successfully")

print(report_path)
