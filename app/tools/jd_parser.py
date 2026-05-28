import re

from app.utils.skills_database import SKILLS


def parse_job_description(jd_text):

    # -----------------------------------
    # Extract Required Skills
    # -----------------------------------

    required_skills = []

    for skill in SKILLS:

        if skill.lower() in jd_text.lower():

            required_skills.append(skill)

    required_skills = list(set(required_skills))

    # -----------------------------------
    # Extract Minimum CGPA
    # -----------------------------------

    cgpa_patterns = [

        r'CGPA[:\s]*([0-9]+\.?[0-9]*)',

        r'GPA[:\s]*([0-9]+\.?[0-9]*)',

        r'Minimum CGPA[:\s]*([0-9]+\.?[0-9]*)'
    ]

    minimum_cgpa = None

    for pattern in cgpa_patterns:

        match = re.search(

            pattern,

            jd_text,

            re.IGNORECASE
        )

        if match:

            minimum_cgpa = match.group(1)

            break

    # -----------------------------------
    # Extract Role / Job Title
    # -----------------------------------

    role = None

    role_patterns = [

        r'Role[:\s]*(.+)',

        r'Position[:\s]*(.+)',

        r'Job Title[:\s]*(.+)',

        r'We are hiring\s+(?:an?|the)?\s*(.+)',

        r'Hiring for\s+(?:an?|the)?\s*(.+)'
    ]

    for pattern in role_patterns:

        match = re.search(

            pattern,

            jd_text,

            re.IGNORECASE
        )

        if match:

            role = match.group(1).strip()

            # Remove unwanted trailing text
            role = role.split("\n")[0]

            break

    # -----------------------------------
    # Extract Experience
    # -----------------------------------

    experience_required = None

    exp_match = re.search(

        r'(\d+)\+?\s*years',

        jd_text,

        re.IGNORECASE
    )

    if exp_match:

        experience_required = exp_match.group(1)

    # -----------------------------------
    # Extract Education
    # -----------------------------------

    education_keywords = [

        "B.Tech",
        "M.Tech",
        "Bachelor",
        "Master",
        "Computer Science",
        "Engineering",
        "B.E",
        "M.E",
        "BCA",
        "MCA"
    ]

    education_required = []

    for edu in education_keywords:

        if edu.lower() in jd_text.lower():

            education_required.append(edu)

    education_required = list(set(education_required))

    # -----------------------------------
    # Final Structured JD Data
    # -----------------------------------

    jd_data = {

        "role": role,

        "required_skills": required_skills,

        "minimum_cgpa": minimum_cgpa,

        "experience_required": experience_required,

        "education_required": education_required,

        "keywords": []
    }

    return jd_data