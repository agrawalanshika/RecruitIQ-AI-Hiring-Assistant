import os
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd


# ==========================================
# TOP SKILLS CHART GENERATOR
# ==========================================

def generate_top_skills_chart(

    ranked_candidates
):

    all_skills = []

    for candidate in ranked_candidates:

        resume_data = candidate["resume_data"]

        skills = resume_data.get(
            "skills",
            []
        )

        skills = [

            skill.strip().lower()

            for skill in skills
        ]

        all_skills.extend(skills)

    # --------------------------------------
    # Count skill frequency
    # --------------------------------------

    skill_counts = Counter(all_skills)

    # --------------------------------------
    # Top 10 skills
    # --------------------------------------

    top_skills = skill_counts.most_common(10)

    skills = [

        item[0]

        for item in top_skills
    ]

    counts = [

        item[1]

        for item in top_skills
    ]

    # --------------------------------------
    # Create chart
    # --------------------------------------

    plt.figure(

        figsize=(10, 5)
    )

    plt.bar(

        skills,
        counts
    )

    plt.xticks(

        rotation=25
    )

    plt.title(

        "Top Skills Frequency"
    )

    plt.xlabel(

        "Skills"
    )

    plt.ylabel(

        "Frequency"
    )

    plt.tight_layout()

    # --------------------------------------
    # Save chart image
    # --------------------------------------

    chart_path = "data/reports/top_skills_chart.png"

    plt.savefig(

        chart_path
    )

    plt.close()

    return chart_path


# ==========================================
# SKILL MATCH HEATMAP
# ==========================================

def generate_skill_heatmap(

    ranked_candidates
):

    # --------------------------------------
    # Collect all skills
    # --------------------------------------

    all_skills = []

    for candidate in ranked_candidates:

        resume_data = candidate["resume_data"]

        skills = resume_data.get(
            "skills",
            []
        )

        skills = [

            skill.strip()

            for skill in skills
        ]

        all_skills.extend(skills)

    # --------------------------------------
    # Top 10 skills
    # --------------------------------------

    skill_counts = Counter(all_skills)

    top_skills = [

        skill[0]

        for skill in skill_counts.most_common(10)
    ]

    # --------------------------------------
    # Create matrix
    # --------------------------------------

    matrix_data = []

    candidate_names = []

    for candidate in ranked_candidates:

        resume_data = candidate["resume_data"]

        candidate_names.append(

            resume_data["name"]
        )

        candidate_skills = [

            skill.strip()

            for skill in resume_data.get(
                "skills",
                []
            )
        ]

        row = []

        for skill in top_skills:

            if skill in candidate_skills:

                row.append(1)

            else:

                row.append(0)

        matrix_data.append(row)

    # --------------------------------------
    # DataFrame
    # --------------------------------------

    df = pd.DataFrame(

        matrix_data,

        index=candidate_names,

        columns=top_skills
    )

    # --------------------------------------
    # Plot Heatmap
    # --------------------------------------

    plt.figure(

        figsize=(12, 6)
    )

    sns.heatmap(

        df,

        annot=True,

        cmap="Blues",

        cbar=False,

        linewidths=0.5
    )

    plt.title(

        "Skill Match Heatmap"
    )

    plt.tight_layout()

    # --------------------------------------
    # Save chart
    # --------------------------------------

    heatmap_path = (

        "data/reports/skill_heatmap.png"
    )

    plt.savefig(

        heatmap_path
    )

    plt.close()

    return heatmap_path


# ==========================================
# HTML REPORT GENERATOR
# ==========================================

def generate_html_report(

    ranked_candidates
):

    # ======================================
    # GENERATE CHARTS
    # ======================================

    chart_path = generate_top_skills_chart(

        ranked_candidates
    )

    heatmap_path = generate_skill_heatmap(

        ranked_candidates
    )

    # ======================================
    # HTML CONTENT
    # ======================================

    html_content = f"""

    <html>

    <head>

        <title>RecruitIQ Hiring Report</title>

        <style>

            body {{

                font-family: Arial;
                margin: 40px;
                background-color: #0f172a;
                color: white;
            }}

            table {{

                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }}

            th, td {{

                border: 1px solid #334155;
                padding: 12px;
                text-align: left;
            }}

            th {{

                background-color: #1e293b;
                color: white;
            }}

            tr:nth-child(even) {{

                background-color: #111827;
            }}

            h1 {{

                text-align: center;
                color: #38bdf8;
                margin-bottom: 40px;
            }}

            h2 {{

                color: #38bdf8;
                margin-top: 50px;
            }}

            .summary-box {{

                background-color: #1e293b;
                padding: 25px;
                border-radius: 12px;
                margin-bottom: 40px;
                line-height: 1.8;
            }}

            .chart-container {{

                text-align: center;
                margin-top: 40px;
            }}

            img {{

                width: 85%;
                border-radius: 10px;
                margin-top: 20px;
            }}

        </style>

    </head>

    <body>

        <h1>RecruitIQ – AI Hiring Report</h1>

        <div class="summary-box">

            <h2>Recruiter Summary</h2>

            <p>

                This AI-generated report analyzes uploaded candidate resumes
                against the provided job description and ranks applicants
                using skill matching, semantic similarity, CGPA analysis,
                and overall profile alignment.

            </p>

        </div>

        <h2>Candidate Ranking Table</h2>

        <table>

            <tr>

                <th>Rank</th>
                <th>Candidate</th>
                <th>CGPA</th>
                <th>Skills</th>
                <th>Final Score</th>
                <th>Recommendation</th>

            </tr>

    """

    # ======================================
    # ADD TABLE ROWS
    # ======================================

    for index, candidate in enumerate(

        ranked_candidates
    ):

        resume_data = candidate["resume_data"]

        match_result = candidate["match_result"]

        html_content += f"""

        <tr>

            <td>{index + 1}</td>

            <td>{resume_data['name']}</td>

            <td>{resume_data['cgpa']}</td>

            <td>{", ".join(resume_data['skills'])}</td>

            <td>{match_result['final_score']}</td>

            <td>{match_result['recommendation']}</td>

        </tr>

        """

    # ======================================
    # ADD ANALYTICS CHARTS
    # ======================================

    html_content += f"""

        </table>

        <div class="chart-container">

            <h2>Top Skills Frequency Analysis</h2>

            <img src="top_skills_chart.png">

        </div>

        <div class="chart-container">

            <h2>Skill Match Heatmap</h2>

            <img src="skill_heatmap.png">

        </div>

    </body>

    </html>

    """

    # ======================================
    # SAVE REPORT
    # ======================================

    os.makedirs(

        "data/reports",

        exist_ok=True
    )

    output_path = (

        "data/reports/final_report.html"
    )

    with open(

        output_path,

        "w",

        encoding="utf-8"
    ) as file:

        file.write(

            html_content
        )

    return output_path