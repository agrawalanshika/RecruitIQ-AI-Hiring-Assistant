def calculate_match_score(resume_data, jd_data):

   

    resume_skills = set(

        skill.lower()

        for skill in resume_data["skills"]

    )

    jd_skills = set(

        skill.lower()

        for skill in jd_data["required_skills"]

    )

    matched_skills = resume_skills.intersection(jd_skills)

    missing_skills = jd_skills - resume_skills

    if len(jd_skills) > 0:

        skills_score = (

            len(matched_skills) / len(jd_skills)

        ) * 10

    else:

        skills_score = 0

   

    cgpa_score = 0

    try:

        candidate_cgpa = float(

            resume_data["cgpa"]

        )

        required_cgpa = float(

            jd_data["minimum_cgpa"]

        )

        if candidate_cgpa >= required_cgpa:

            cgpa_score = 10

        else:

            cgpa_score = (

                candidate_cgpa / required_cgpa

            ) * 10

    except:

        cgpa_score = 5

        candidate_cgpa = 0

        required_cgpa = 0

    

    education_score = 0

    resume_education = [

        edu.lower()

        for edu in resume_data["education"]

    ]

    jd_education = [

        edu.lower()

        for edu in jd_data["education_required"]

    ]

    matched_education = 0

    for edu in jd_education:

        if edu in resume_education:

            matched_education += 1

    if len(jd_education) > 0:

        education_score = (

            matched_education / len(jd_education)

        ) * 10

    else:

        education_score = 5

   

    project_score = 0

    total_project_matches = 0

    for project in resume_data["projects"]:

        tech_stack = [

            tech.lower()

            for tech in project["tech_stack"]

        ]

        for skill in jd_skills:

            if skill in tech_stack:

                total_project_matches += 1

    if len(jd_skills) > 0:

        project_score = (

            total_project_matches / len(jd_skills)

        ) * 10

        if project_score > 10:

            project_score = 10

    else:

        project_score = 5

   
    communication_score = 8

    

    final_score = (

        (skills_score * 0.30) +

        (education_score * 0.15) +

        (project_score * 0.20) +

        (communication_score * 0.10) +

        (cgpa_score * 0.25)

    )

    

    recommendation = "No Hire"

    missing_count = len(missing_skills)

    cgpa_ok = candidate_cgpa >= required_cgpa

   

    if (

        final_score >= 7 and
        cgpa_ok and
        (missing_count == 0 or missing_count==1)

    ):

        recommendation = "Hire"



    elif (

        missing_count==0 or missing_count == 1

    ):

        recommendation = "Review"

   

    else:

        recommendation = "No Hire"



    result = {

        "skills_score": round(

            skills_score, 2

        ),

        "education_score": round(

            education_score, 2

        ),

        "project_score": round(

            project_score, 2

        ),

        "communication_score": round(

            communication_score, 2

        ),

        "cgpa_score": round(

            cgpa_score, 2

        ),

        "final_score": round(

            final_score, 2

        ),

        "matched_skills": list(

            matched_skills

        ),

        "missing_skills": list(

            missing_skills

        ),

        "recommendation": recommendation

    }

    return result
