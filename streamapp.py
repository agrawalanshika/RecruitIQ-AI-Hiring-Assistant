import os
import streamlit as st
import pandas as pd

from app.agents.workflow_agent import (
    run_workflow_agent
)

from app.tools.resume_parser import extract_text_from_pdf
from app.utils.text_cleaner import clean_resume_text
from app.tools.llm_extractor import extract_resume_data
from app.tools.jd_parser import parse_job_description
from app.tools.matching_engine import calculate_match_score
from app.tools.explanation_engine import generate_explanation
from app.tools.pdf_report_generator import generate_pdf_report
from app.tools.semantic_matcher import calculate_semantic_similarity

from app.databases.database_manager import (

    create_table,
    save_candidate
)

import urllib.parse
import base64

import json
from datetime import datetime


HR_USERNAME = "admin"

HR_PASSWORD = "hr123"


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


create_table()


def set_bg_image(image_file):

    with open(image_file, "rb") as img_file:

        encoded_string = base64.b64encode(
            img_file.read()
        ).decode()

    page_bg_img = f"""
    <style>

    .stApp {{

        background:
            linear-gradient(
                rgba(0, 0, 0, 0.65),
                rgba(0, 0, 0, 0.65)
            ),
            url("data:image/png;base64,{encoded_string}");

        background-size: cover;

        background-position: center;

        background-attachment: fixed;
    }}

    </style>
    """

    st.markdown(
        page_bg_img,
        unsafe_allow_html=True
    )


st.set_page_config(

    page_title="RecruitIQ – AI Hiring Assistant",

    layout="wide"

    
)
set_bg_image(
    "bg.png"
)

if not st.session_state.logged_in:


    left_col, center_col, right_col = st.columns([1, 2, 1])

    with center_col:

        st.markdown(
            """
            <div 
            ">
            <h1 style="
                text-align:center;
                color:white;
                margin-bottom:10px;
            ">
                RecruitIQ HR Login
            </h1>

            <p style="
                text-align:center;
                color:#9ca3af;
                margin-bottom:30px;
                font-size:18px;
            ">
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.button(
            "Login",
            use_container_width=True
        )

        if login_button:
            with st.spinner("Logging in..."):
                import time
                time.sleep(2)


                if (

                    username == HR_USERNAME and
                    password == HR_PASSWORD

                ):

                    st.session_state.logged_in = True

                    st.success(
                        "Login Successful!"
                    )
                    time.sleep(1)
                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password"
                    )

        st.stop()




    st.markdown(
        "AI-powered recruitment intelligence and candidate screening platform"
    )


if st.sidebar.button("Logout"):

    with st.spinner("Logging out..."):

        import time

        time.sleep(2)

        st.session_state.logged_in = False

        st.rerun()



st.sidebar.success(

    f"Logged in as: {HR_USERNAME}"

)



page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Recruitment History"

    ]

)

if page == "Dashboard":

    st.title(

        "RecruitIQ – AI Hiring Assistant"

    )

    st.markdown(

        "AI-powered recruitment intelligence and candidate screening platform"

    )

    st.sidebar.header(

        "Upload Files"

    )
if page == "Dashboard":



    # Upload JD
    jd_file = st.sidebar.file_uploader(

        "Upload Job Description (.txt)",

        type=["txt"]
    )

    # Upload Resumes
    resume_files = st.sidebar.file_uploader(

        "Upload Multiple Resumes (.pdf)",

        type=["pdf"],

        accept_multiple_files=True
    )


    if st.sidebar.button("Analyze Candidates"):

        if jd_file and resume_files:


            jd_text = jd_file.read().decode("utf-8")

            jd_data = parse_job_description(jd_text)


            candidate_results = []

            os.makedirs(

                "temp_resumes",

                exist_ok=True
            )

            for uploaded_file in resume_files:

                temp_path = os.path.join(

                    "temp_resumes",

                    uploaded_file.name
                )


                with open(temp_path, "wb") as f:

                    f.write(

                        uploaded_file.getbuffer()
                    )


                resume_text = extract_text_from_pdf(

                    temp_path
                )


                cleaned_resume = clean_resume_text(

                    resume_text
                )
                
                semantic_score = calculate_semantic_similarity(

                    cleaned_resume,

                    jd_text
                )


                resume_data = extract_resume_data(

                    cleaned_resume
                )

             

                match_result = calculate_match_score(

                    resume_data,

                    jd_data
                )


                explanation = generate_explanation(

                    match_result,

                    resume_data,

                    jd_data
                )


                candidate_data = {

                    "Candidate Name":
                        resume_data["name"],

                    "CGPA":
                        resume_data["cgpa"],

                    "Email":
                        ", ".join(
                            resume_data["email"]
                        ),

                    "Phone":
                        ", ".join(
                            resume_data["phone"]
                        ),

                    "Skills":
                        ", ".join(
                            resume_data["skills"]
                        ),

                    "Semantic Score":
                        semantic_score,

                    "Final Score":
                        match_result["final_score"],

                    "Recommendation":
                        match_result["recommendation"],

                    "Matched Skills":
                        ", ".join(
                            match_result["matched_skills"]
                        ),

                    "Missing Skills":
                        ", ".join(
                            match_result["missing_skills"]
                        ),

                    "Explanation":
                        explanation,

                    "Resume Path":
                        temp_path
                }

        
                candidate_results.append(

                    candidate_data
                )

    

                save_candidate(

                    candidate_data
                )


            ranked_candidates = sorted(

                candidate_results,

                key=lambda x: (
                    x["Final Score"],
                    x["Semantic Score"]
                ),

                reverse=True
            )


            timestamp_str = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            pdf_report_path = f"data/reports/report_{timestamp_str}.pdf"

 

            generate_pdf_report(

                ranked_candidates,

                output_path=pdf_report_path
            )



            with st.spinner(

                "Running AI Recruiter Workflow..."
            ):

                try:

                    workflow_analysis = run_workflow_agent(

                        jd_text,

                        ranked_candidates
                    )

                except Exception as e:

                    workflow_analysis = (

                        f"Workflow Agent Error: {str(e)}"
                    )

            df = pd.DataFrame(

                ranked_candidates
            )


            st.success(
                "Analysis Completed Successfully!"
            )


            history_file = "data/history/history.json"

            # Load existing history
            try:

                with open(history_file, "r") as file:

                    history_data = json.load(file)

            except:

                history_data = []

            # Create session entry
            session_entry = {

                "timestamp": datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                ),

                "job_description": jd_file.name,

                "report_file": pdf_report_path,

                "total_candidates": len(ranked_candidates)

            }

            # Append session
            history_data.append(session_entry)

            # Save back
            with open(history_file, "w") as file:

                json.dump(

                    history_data,
                    file,
                    indent=4
                )


            total_candidates = len(df)

            selected_candidates = len(

                df[df["Recommendation"] == "Hire"]

            )

            review_candidates = len(

        df[df["Recommendation"] == "Review"]

    )

            average_score = round(

                df["Final Score"].mean(),

                2
            )

            top_score = round(

                df["Final Score"].max(),

                2
            )


            col1, col2, col3, col4 = st.columns(4)

            col1.metric(

                "👥Total Candidates",

                total_candidates
            )

            col2.metric(

                "✅Shortlisted",

                selected_candidates
            )

            col3.metric(

                "🟡Under Review",

                review_candidates
            )

            col4.metric(

                "🏆Top Score",

                top_score
            )

           

            st.header(
                "AI Hiring Insights"
            )

            st.info(

                workflow_analysis
            )

           

            st.header(
                "Download Reports"
            )


            csv = df.to_csv(

                index=False
            ).encode("utf-8")

        

            download_col1, download_col2 = st.columns(2)

         

            with download_col1:

                st.download_button(

                    label="📄 Download CSV Report",

                    data=csv,

                    file_name="candidate_ranking.csv",

                    mime="text/csv",

                    use_container_width=True
                )

           

            with open(

                pdf_report_path,

                "rb"
            ) as pdf_file:

                PDFbyte = pdf_file.read()

            with download_col2:

                st.download_button(

                    label="📑 Download PDF Report",

                    data=PDFbyte,

                    file_name="candidate_report.pdf",

                    mime="application/pdf",

                    use_container_width=True
                )

    

            st.header("Candidates")

 

            st.markdown(
                """
                <style>

                .candidate-box {
                    border: 1px solid #2d3748;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 20px;
                    background-color: #111827;
                    min-height: 100px;
                }

                .candidate-name {

                    font-size: 25px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: skyblue;
                }

                .candidate-text {
                    font-size: 16px;
                    line-height: 1;
                    color: beige;
                }

                </style>
                """,
                unsafe_allow_html=True
            )

           

            for i in range(0, len(ranked_candidates), 2):

                cols = st.columns(2)

                for j in range(2):

                    if i + j < len(ranked_candidates):

                        candidate = ranked_candidates[i + j]

                        with cols[j]:

                       

                            email = candidate["Email"]

                            if "," in email:
                                email = email.split(",")[0]

                            

                            with st.container(border=True):

                        

                                st.markdown(
                                    f"""
                                    <div class="candidate-name">
                                        {candidate['Candidate Name']}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


                                st.markdown(
                                    f"""
                                    <div class="candidate-text">

                                    <p>📧 <b>Email:</b> {email}</p>

                                    <p>📞 <b>Phone:</b> {candidate['Phone']}</p>

                                    <p>🎓 <b>CGPA:</b> {candidate['CGPA']}</p>

                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                               

                                recommendation = candidate["Recommendation"]

                            

                                if recommendation == "Hire":

                                    badge_color = "#0f5132"
                                    text_color = "#75ffb1"

                                elif recommendation == "Review":

                                    badge_color = "#664d03"
                                    text_color = "#ffd666"

                                else:

                                    badge_color = "#5c1a1a"
                                    text_color = "#ff8a8a"

                                st.markdown(
                                    f"""
                                    <div style="
                                        display:inline-block;
                                        padding:8px 18px;
                                        border-radius:20px;
                                        background:{badge_color};
                                        color:{text_color};
                                        font-weight:700;
                                        font-size:15px;
                                        margin-top:5px;
                                        margin-bottom:15px;
                                    ">
                                        {recommendation.upper()}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

        

                                # skills = candidate["Matched Skills"].split(",")

                                # st.markdown(
                                #     "### Skills"
                                # )

                                # skills_html = ""

                                # for skill in skills[:8]:

                                #     skill = skill.strip()

                                #     skills_html += f"""
                                #     <span style="
                                #         display:inline-block;
                                #         background:rgba(59,130,246,0.18);
                                #         color:#7dd3fc;
                                #         padding:6px 14px;
                                #         margin:4px;
                                #         border-radius:18px;
                                #         font-size:14px;
                                #         font-weight:600;
                                #         border:1px solid rgba(125,211,252,0.25);
                                #     ">
                                #         {skill}
                                #     </span>
                                #     """

                                # st.markdown(
                                #     skills_html,
                                #     unsafe_allow_html=True
                                # )

                

                                button_col1, button_col2 = st.columns(2)

                            

                                with button_col1:

                                    with open(
                                        candidate["Resume Path"],
                                        "rb"
                                    ) as pdf_file:

                                        PDFbyte = pdf_file.read()

                                    st.download_button(
                                        label="View Resume",
                                        data=PDFbyte,
                                        file_name=os.path.basename(
                                            candidate["Resume Path"]
                                        ),
                                        mime="application/pdf",
                                        key=f"resume_{i+j}",
                                        use_container_width=True
                                    )


                                with button_col2:

                                    candidate_name = candidate[
                                        "Candidate Name"
                                    ]

                                    recommendation = candidate[
                                        "Recommendation"
                                    ]


                                    if recommendation == "Hire":

                                        subject = (
                                            "Congratulations! You are shortlisted"
                                        )

                                        body = f"""
            Dear {candidate_name},

            Congratulations!

            We are pleased to inform you that you have been shortlisted for the next round of the recruitment process.
            Our HR team will contact you soon for informing about the furthur process.

            Regards,
            HR Team
            """

                                    elif recommendation=="No Hire":

                                        subject = (
                                            "Application Update"
                                        )

                                        body = f"""
            Dear {candidate_name},

        We carefully reviewed your background and experience and we regret to inform you that we decided not to proceed with your application.
        Although this role didn't work out, we may contact you if we come across another opening that we think may be a good match for your skills and experience.

        Thankyou for your interest in this opportunity and Best of Luck for your future endeavours.


            Regards,
            HR Team
            """
                                    else:

                                        subject = (
                                            "Application Update"
                                        )

                                        body = f"""
            Dear {candidate_name},

    Thank you for applying for the position at our company.

    After an initial AI-assisted evaluation of your profile, your application has been placed under further review by our recruitment team. Your skills and experience demonstrate promising alignment with the role requirements, and we would like to conduct an additional manual assessment before making a final decision.

    Our team will carefully review your profile and contact you regarding the next steps in the recruitment process.

    We appreciate your interest and patience throughout the evaluation process.

    Best regards,
    HR Recruitment Team
            """


                                    mailto_link = (
                                        f"mailto:{email}"
                                        f"?subject={urllib.parse.quote(subject)}"
                                        f"&body={urllib.parse.quote(body)}"
                                    )

                                    st.link_button(
                                        "Send Email",
                                        mailto_link,
                                        use_container_width=True
                                    )
        


        else:

            st.warning(
                "Please upload both JD and resumes."
            )
  

elif page == "Recruitment History":

    st.title(
        "📜 Recruitment History"
    )

    st.markdown(
        "View previous hiring sessions and reports"
    )

    history_file = "data/history/history.json"

    try:

        with open(history_file, "r") as file:

            history_data = json.load(file)

        if len(history_data) > 0:

            for session in reversed(history_data):

                with st.container():

                    st.markdown(
                        f"""
                        ### 📅 {session['timestamp']}

                        📄 **Job Description:**  
                        {session['job_description']}

                        👥 **Total Candidates:**  
                        {session['total_candidates']}
                        """
                    )

                    report_path = session[
                        "report_file"
                    ]

                    if os.path.exists(report_path):

                        with open(
                            report_path,
                            "rb"
                        ) as pdf_file:

                            st.download_button(

                                label="📥 Download Report",

                                data=pdf_file,

                                file_name="candidate_report.pdf",

                                mime="application/pdf",

                                key=session['timestamp']
                            )

                    st.markdown("---")

        else:

            st.info(
                "No recruitment history available"
            )

    except:

        st.warning(
            "History file not found"
        )
