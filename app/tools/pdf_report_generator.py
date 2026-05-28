import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from collections import Counter

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter


# ==========================================
# TOP SKILLS CHART
# ==========================================

def generate_top_skills_chart(

    ranked_candidates
):

    all_skills = []

    for candidate in ranked_candidates:

        skills = candidate[
            "Matched Skills"
        ]

        if isinstance(skills, str):

            skills = skills.split(",")

        skills = [

            skill.strip().lower()

            for skill in skills
        ]

        all_skills.extend(skills)

    skill_counts = Counter(all_skills)

    top_skills = skill_counts.most_common(10)

    skills = [

        item[0]

        for item in top_skills
    ]

    counts = [

        item[1]

        for item in top_skills
    ]

    plt.figure(

        figsize=(8, 4)
    )

    plt.bar(

        skills,
        counts
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

    plt.xticks(

        rotation=25
    )

    plt.tight_layout()

    chart_path = (

        "top_skills_chart.png"
    )

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

    all_skills = []

    for candidate in ranked_candidates:

        skills = candidate[
            "Matched Skills"
        ]

        if isinstance(skills, str):

            skills = skills.split(",")

        skills = [

            skill.strip()

            for skill in skills
        ]

        all_skills.extend(skills)

    skill_counts = Counter(all_skills)

    top_skills = [

        skill[0]

        for skill in skill_counts.most_common(10)
    ]

    matrix_data = []

    candidate_names = []

    for candidate in ranked_candidates:

        candidate_names.append(

            candidate["Candidate Name"]
        )

        candidate_skills = [

            skill.strip()

            for skill in candidate[
                "Matched Skills"
            ].split(",")
        ]

        row = []

        for skill in top_skills:

            if skill in candidate_skills:

                row.append(1)

            else:

                row.append(0)

        matrix_data.append(row)

    df = pd.DataFrame(

        matrix_data,

        index=candidate_names,

        columns=top_skills
    )

    plt.figure(

        figsize=(10, 5)
    )

    sns.heatmap(

        df,

        annot=True,

        cmap="Blues",

        linewidths=0.5,

        cbar=False
    )

    plt.title(

        "Skill Match Heatmap"
    )

    plt.tight_layout()

    heatmap_path = (

        "skill_heatmap.png"
    )

    plt.savefig(

        heatmap_path
    )

    plt.close()

    return heatmap_path


# ==========================================
# PDF REPORT GENERATOR
# ==========================================

def generate_pdf_report(

    ranked_candidates,

    output_path="candidate_report.pdf"
):

    doc = SimpleDocTemplate(

        output_path,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    # ===================================
    # TITLE
    # ===================================

    title = Paragraph(

        "RecruitIQ – AI Hiring Report",

        styles['Title']
    )

    story.append(title)

    story.append(

        Spacer(1, 20)
    )

    # ===================================
    # SUMMARY
    # ===================================

    summary = """

    This AI-generated report evaluates
    candidate resumes against the given
    job description.

    """

    summary_para = Paragraph(

        summary,

        styles['BodyText']
    )

    story.append(summary_para)

    story.append(

        Spacer(1, 25)
    )

    # ===================================
    # DATAFRAME
    # ===================================

    df = pd.DataFrame(

        ranked_candidates
    )

    # ===================================
    # CANDIDATE SCORE CHART
    # ===================================

    plt.figure(

        figsize=(6, 3)
    )

    plt.bar(

        df["Candidate Name"],

        df["Final Score"]
    )

    plt.title(
        "Candidate Scores"
    )

    plt.ylabel(
        "Final Score"
    )

    plt.xticks(

        rotation=15,

        fontsize=8
    )

    plt.tight_layout()

    score_chart_path = (

        "candidate_scores_chart.png"
    )

    plt.savefig(

        score_chart_path
    )

    plt.close()

    # ===================================
    # PIE CHART
    # ===================================

    hire_counts = df[
        "Recommendation"
    ].value_counts()

    plt.figure(

        figsize=(3, 3)
    )

    plt.pie(

        hire_counts,

        labels=hire_counts.index,

        autopct='%1.1f%%'
    )

    plt.title(
        "Hire vs No Hire"
    )

    pie_chart_path = (

        "hire_pie_chart.png"
    )

    plt.savefig(

        pie_chart_path
    )

    plt.close()

    # ===================================
    # ANALYTICS DASHBOARD
    # ===================================

    story.append(

        Paragraph(

            "Recruitment Analytics Dashboard",

            styles['Heading2']
        )
    )

    story.append(

        Spacer(1, 15)
    )

    score_chart_img = Image(

        score_chart_path,

        width=280,

        height=180
    )

    pie_chart_img = Image(

        pie_chart_path,

        width=220,

        height=220
    )

    charts_table = Table(

        [[

            score_chart_img,

            pie_chart_img

        ]],

        colWidths=[300, 240]
    )

    story.append(

        charts_table
    )

    story.append(

        Spacer(1, 30)
    )

    # ===================================
    # TOP SKILLS CHART
    # ===================================

    top_skills_chart = (

        generate_top_skills_chart(
            ranked_candidates
        )
    )

    story.append(

        Paragraph(

            "Top Skills Frequency Analysis",

            styles['Heading2']
        )
    )

    story.append(

        Spacer(1, 10)
    )

    story.append(

        Image(

            top_skills_chart,

            width=450,

            height=250
        )
    )

    story.append(

        Spacer(1, 25)
    )

    # ===================================
    # SKILL HEATMAP
    # ===================================

    heatmap_chart = (

        generate_skill_heatmap(
            ranked_candidates
        )
    )

    story.append(

        Paragraph(

            "Skill Match Heatmap",

            styles['Heading2']
        )
    )

    story.append(

        Spacer(1, 10)
    )

    story.append(

        Image(

            heatmap_chart,

            width=450,

            height=250
        )
    )

    story.append(

        PageBreak()
    )

    # ===================================
    # CANDIDATE DETAILS
    # ===================================

    for idx, candidate in enumerate(

        ranked_candidates,

        start=1
    ):

        heading = Paragraph(
            

            f"\n<b>Candidate #{idx}: "
            f"{candidate['Candidate Name']}</b>",

            styles['Heading2']
        )

        story.append(heading)

        story.append(

            Spacer(1, 10)
        )

        details = f"""

        <b>Email:</b>
        {candidate['Email']}<br/><br/>

        <b>Phone:</b>
        {candidate['Phone']}<br/><br/>

        <b>CGPA:</b>
        {candidate['CGPA']}<br/><br/>

        <b>Semantic Score:</b>
        {candidate['Semantic Score']}<br/><br/>

        <b>Final Score:</b>
        {candidate['Final Score']}<br/><br/>

        <b>Recommendation:</b>
        {candidate['Recommendation']}<br/><br/>

        <b>Matched Skills:</b>
        {candidate['Matched Skills']}<br/><br/>

        <b>Missing Skills:</b>
        {candidate['Missing Skills']}<br/><br/>

        <b>Explanation:</b>
        {candidate['Explanation']}<br/><br/>

        """

        paragraph = Paragraph(

            details,

            styles['BodyText']
        )

        story.append(paragraph)

        story.append(

            Spacer(1, 25)
        )

    # ===================================
    # BUILD PDF
    # ===================================

    doc.build(story)

    return output_path