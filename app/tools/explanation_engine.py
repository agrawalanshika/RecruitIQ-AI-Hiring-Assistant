def generate_explanation(

    match_result,

    resume_data,

    jd_data
):

    matched_skills = match_result["matched_skills"]

    missing_skills = match_result["missing_skills"]

    recommendation = match_result["recommendation"]

    explanation = []

    # -----------------------------------
    # Skill Match Analysis
    # -----------------------------------

    if len(matched_skills) >= 5:

        explanation.append(

            f"Candidate strongly matches key JD skills including {', '.join(matched_skills[:5])}."
        )

    elif len(matched_skills) >= 3:

        explanation.append(

            f"Candidate partially matches required skills including {', '.join(matched_skills[:3])}."
        )

    elif len(matched_skills) > 0:

        explanation.append(

            f"Candidate has limited alignment with skills such as {', '.join(matched_skills)}."
        )

    else:

        explanation.append(

            "Very few required technical skills were detected."
        )

    # -----------------------------------
    # CGPA Evaluation
    # -----------------------------------

    try:

        candidate_cgpa = float(

            resume_data["cgpa"]
        )

        required_cgpa = float(

            jd_data["minimum_cgpa"]
        )

        if candidate_cgpa >= required_cgpa:

            explanation.append(

                "Candidate satisfies the CGPA requirement."
            )

        else:

            # Add CGPA issue to missing skills
            missing_skills.append(

                f"CGPA below preferred criteria ({required_cgpa})"
            )

            explanation.append(

                "Candidate CGPA is below the preferred criteria."
            )

    except:

        explanation.append(

            "CGPA information could not be fully evaluated."
        )

    # -----------------------------------
    # Missing Skills Analysis
    # -----------------------------------

    if len(missing_skills) >= 5:

        explanation.append(

            f"Several important skills are missing including {', '.join(missing_skills[:5])}."
        )

    elif len(missing_skills) > 0:

        explanation.append(

            f"Some required skills are missing such as {', '.join(missing_skills)}."
        )

    else:

        explanation.append(

            "Most required technical skills are present."
        )

    # -----------------------------------
    # Project Evaluation
    # -----------------------------------

    if resume_data["projects"]:

        explanation.append(

            "Relevant project experience was identified in the resume."
        )

    else:

        explanation.append(

            "Relevant project experience was not strongly identified."
        )

    # -----------------------------------
    # Final Recommendation
    # -----------------------------------

    if recommendation == "Hire":

        explanation.append(

            "Overall profile demonstrates strong alignment with the job description."
        )

    else:

        explanation.append(

            "Overall profile alignment is insufficient for hiring based on the current JD requirements."
        )

    # -----------------------------------
    # Final Combined Explanation
    # -----------------------------------

    final_explanation = " ".join(

        explanation
    )

    return final_explanation