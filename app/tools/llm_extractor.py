import re

from app.utils.skills_database import SKILLS
import gender_guesser.detector as gender


def extract_resume_data(resume_text):

    # -----------------------------
    # Prepare Lines
    # -----------------------------

    lines = resume_text.split("\n")

    # -----------------------------
    # Extract Name
    # -----------------------------

    probable_name = ""

    for line in lines[:10]:

        line = line.strip()

        if not line:
            continue

        # Ignore emails/numbers
        if "@" in line:
            continue

        if any(char.isdigit() for char in line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            probable_name = line
            break

    # -----------------------------
    # Extract Email
    # -----------------------------

    email = re.findall(

         r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

        resume_text
    )

    # -----------------------------
    # Extract Phone Number
    # -----------------------------

    phone = re.findall(

        r'\+?\d[\d -]{8,12}\d',

        resume_text
    )

    # -----------------------------
    # Extract CGPA / GPA
    # -----------------------------

    cgpa_patterns = [

        r'CGPA[:\s]*([0-9]+\.?[0-9]*)',

        r'GPA[:\s]*([0-9]+\.?[0-9]*)',

        r'([0-9]+\.[0-9]+)\s*/\s*10'
    ]

    cgpa = None

    for pattern in cgpa_patterns:

        match = re.search(

            pattern,

            resume_text,

            re.IGNORECASE
        )

        if match:

            cgpa = match.group(1)
            break

    # -----------------------------
    # Extract Skills
    # -----------------------------

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in resume_text.lower():

            found_skills.append(skill)

    found_skills = list(set(found_skills))

    # -----------------------------
    # Extract Education
    # -----------------------------

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

    education_found = []

    for edu in education_keywords:

        if edu.lower() in resume_text.lower():

            education_found.append(edu)

    education_found = list(set(education_found))

    # -----------------------------
    # Extract Projects + Tech Stack
    # -----------------------------

    projects = []

    ignore_keywords = [

        "developed",
        "built",
        "created",
        "designed",
        "implemented",
        "using",
        "responsible",
        "course",
        "certification",
        "workshop",
        "cgpa",
        "university",
        "college",
        "@gmail",
        "@yahoo",
        "@outlook"
    ]

    for line in lines:

        clean_line = line.strip()

        # Ignore short lines
        if len(clean_line) < 5:
            continue

        # Ignore emails
        if "@" in clean_line:
            continue

        # Ignore bullet-description lines
        if any(

            keyword in clean_line.lower()

            for keyword in ignore_keywords
        ):

            continue

        # Detect project titles
        if "|" in clean_line or " - " in clean_line:

            # -----------------------------------
            # Detect Tech Stack
            # -----------------------------------

            tech_stack = []

            for skill in SKILLS:

                if skill.lower() in clean_line.lower():

                    tech_stack.append(skill)

            # -----------------------------------
            # Split Project Title
            # -----------------------------------

            parts = re.split(

                r"\||-",

                clean_line
            )

            project_name = parts[0].strip()

            domain = ""

            if len(parts) > 1:

                domain = parts[1].strip()

            # Ignore noisy long titles
            if len(project_name.split()) > 6:
                continue

            # Ignore tiny names
            if len(project_name) < 3:
                continue

            projects.append({

                "project_name": project_name,

                "domain": domain,

                "tech_stack": list(set(tech_stack))
            })

    # -----------------------------
    # Remove Duplicate Projects
    # -----------------------------

    unique_projects = []

    seen = set()

    for project in projects:

        key = project["project_name"]

        if key not in seen:

            unique_projects.append(project)

            seen.add(key)

    # -----------------------------
    # Final Structured Data
    # -----------------------------

    data = {

        "name": probable_name,

        "email": email,

        "phone": phone,

        "cgpa": cgpa,

        "skills": found_skills,

        "education": education_found,

        "projects": unique_projects
    }

    return data