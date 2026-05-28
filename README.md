# 📑 RecruitIQ-AI-Hiring-Assistant
**Intelligent AI hiring assistant developed with Python, Streamlit, and LangChain that automates resume screening, skill matching, candidate ranking, and recruitment workflow management through an interactive HR dashboard.**



## 🚀 Features
- Resume Parsing
- Job Description Analysis
- Skill Matching Engine
- Weighted Candidate Scoring
- Semantic Resume Matching
- Candidate Ranking System
- AI-based Hiring Recommendation
- Report Generation
- Recruitment History Tracking
- Secure HR Login System
- Interactive Streamlit Dashboard


## :memo: Tech Stack
- **Frontend using Streamlit**
- **Backend with Python**
- **Langchain and Groq LLM as core AI tools**
- **SQLite for Database**
- **Visualization using Matplotlib and Seaborn**
- **Report Generation using Report Lab**


## :arrow_down: Project Workflow
1. HR logs into the platform securely
2. HR uploads Job Description file
3. Multiple resumes are uploaded
4. AI tools extracts structured information from resumes
5. Resume skills are matched with JD requirements
6. Candidates are scored using weighted scoring
7. Candidates are ranked automatically
8. Reports and analytics are generated
9. HR can view candidates resume individually and email them
10. Recruitment history is stored for future access

## :label: Screenshots

<table>
  <tr>
    <td>
      <img src="assets/screenshots/dashboard.png" width="100%"/>
    </td>

<td>
  <img src="assets/screenshots/history.png" width="100%"/>
</td>


  </tr>

  <tr>
    <td>
      <img src="assets/screenshots/charts1.png" width="100%"/>
    </td>

<td>
  <img src="assets/screenshots/charts2.png" width="100%"/>
</td>


  </tr>
</table>



## :pushpin: Scoring Criteria
| Parameter           | Weightage |
| ------------------- | --------- |
| Skills Matching     | 30%       |
| CGPA Matching       | 25%       |
| Project Relevance   | 20%       |
| Education Matching  | 15%       |
| Communication Score | 10%       |



## :bulb: Recommendation Logic
- Hire → Strong skill and score match
- Review → Almost complete skill match with minor missing criteria
- No Hire → Low overall relevance


## :heavy_plus_sign: Installation
#### Clone Repository
```
git clone https://github.com/agrawalanshika/RecruitIQ-AI-Hiring-Assistant.git
```

#### Navigate to Project
``` cd RecruitIQ-AI-Hiring-Assistant ```

#### Install Dependencies
``` pip install -r requirements.txt ```

#### Add Environment Variables
Create a .env file:
```
GROQ_API_KEY=your_api_key
```

#### Run Application
``` streamlit run streamapp.py ```


## 📁 Folder Structure
```text
RecruitIQ-AI-Hiring-Assistant/
│
├── app/
├── data/
├── streamapp.py
├── main.py
├── requirements.txt
├── README.md
```


## :triangular_flag_on_post: Future Improvements
1. LinkedIn Profile Analysis
2. Interview Scheduling
3. Multi-HR Authentication
4. Cloud Deployment


## :technologist: Author
### Anshika Agrawal


