from __future__ import annotations

import streamlit as st
from PyPDF2 import PdfReader
from apps.hr.gpt import get_gpt_response
import yaml
from pathlib import Path
import os


def extract_resume_data(data: str, job_descr: str, key: str) -> dict | None:
    gpt_response = get_gpt_response(data, job_descr, key)
    response_message = gpt_response["choices"][0]["message"]
    reviews = response_message.get("function_call")
    result = reviews.get("arguments")
    if reviews and isinstance(result, dict):
        return result

    if reviews and isinstance(result, str):
        import json
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError as e:
            print("Error: Cannot be convert to a JSON object.")
            print(e)
    return None


def app():
    # ---------------------------------
    # st.set_page_config(page_title='📝 Resume Ratings', page_icon="📝")

    root = Path(__file__).parent.parent.parent
    info_data_path = os.path.join(root, 'apps', 'hr', 'info.yml')
    # data = json.dumps(info_data_path)

    st.title("📝 Resume Ratings")
    st.markdown("Use this application to help you decide if the prospect is a good fit for the job.")

    with st.form(key='resume_form'):
        option = st.selectbox(
            "Pick a JD!",
            ("Software Engineer", "Program Manager", "Data Scientist"),
            index=None,
            placeholder="Select JD",
        )
        if option:

            if option == "Data Scientist":
                job_description = """Excellent understanding of machine learning techniques and algorithms, such as k-NN, Naive Bayes, SVM, Decision Forests, etc.
                    Experience with common data science toolkits, such as R, Weka, NumPy, MatLab, etc. Excellence in at least one of these is highly desirable
                    Great communication skills
                    Experience with data visualisation tools, such as D3.js, GGplot, etc.
                    Proficiency in using query languages such as SQL, Hive, Pig 
                    Experience with NoSQL databases, such as MongoDB, Cassandra, HBase
                    Good applied statistics skills, such as distributions, statistical testing, regression, etc. """

            if option == "Software Engineer":
                job_description = """Proven work experience as a Software Engineer or Software Developer
                    Experience designing interactive applications
                    Ability to develop software in Java, Ruby on Rails, C++ or other programming languages
                    Excellent knowledge of relational databases, SQL and ORM technologies (JPA2, Hibernate)
                    Experience developing web applications using at least one popular web framework (JSF, Wicket, GWT, Spring MVC)
                    Experience with test-driven development
                    Proficiency in software engineering tools
                    Ability to document requirements and specifications
                    BSc degree in Computer Science, Engineering or relevant field
                    """
            if option == "Program Manager":
                job_description = """roven experience as a Program Manager or other managerial position
                    Thorough understanding of project/program management techniques and methods
                    Excellent Knowledge of performance evaluation and change management principles
                    Excellent knowledge of MS Office; working knowledge of program/project management software Basecamp, MS Project is a strong advantage
                    Outstanding leadership and organizational skills
                    Excellent communication skills
                    Excellent problem-solving ability
                    BSc/BA diploma in management or a relevant field; MSc/MA is a plus """

        else:

            job_description = st.text_area(label="""Write the Job Description here.
                                                    Insert key aspects you want to value in the prospect's resume.""",
                                           placeholder="Job description. This field should have at least 100 characters.")
        file = st.file_uploader("Add the prospect's resume in PDF format:", type=["pdf"])
        openai_api_key = "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"
        submitted = st.form_submit_button('Submit')

    if file is not None and len(job_description) > 100:
        pdf_file = PdfReader(file)
        pdf_text = ""
        for page in pdf_file.pages:
            pdf_text += page.extract_text() + "\n"

        resume_data = extract_resume_data(pdf_text, job_description, openai_api_key)
        if resume_data:
            yoe = int(resume_data.get('years_of_experience'))
            education = int(resume_data.get("education", 0))
            company_fit = int(resume_data.get("company_fit", 0))
            technical_skills = int(resume_data.get("technical_skills", 0))
            soft_skills = int(resume_data.get("soft_skills", 0))
            projects = int(resume_data.get("projects", 0))
            average = (education + company_fit + technical_skills + soft_skills + projects) // 5

            st.title("Prospect Review Based On Job Description")
            st.markdown(f"### Name: {resume_data.get('name')}")
            st.markdown(f"#### Relevant skills:\n{resume_data.get('relevant_skills')}")
            st.markdown(f"#### Summary:\n{resume_data.get('summary')}")
            st.slider(
                label="Years of experience",
                min_value=1,
                max_value=15,
                value=int(resume_data.get('years_of_experience')),
                disabled=True)
            st.slider(
                label="Education",
                min_value=1,
                max_value=10,
                value=education,
                disabled=True
            )
            st.slider(
                label="Company fit",
                min_value=1,
                max_value=10,
                value=company_fit,
                disabled=True
            )
            st.slider(
                label="Technical Skills",
                min_value=1,
                max_value=10,
                value=technical_skills,
                disabled=True
            )
            st.slider(
                label="Soft Skills",
                min_value=1,
                max_value=10,
                value=soft_skills,
                disabled=True
            )
            st.slider(
                label="Projects",
                min_value=1,
                max_value=10,
                value=projects,
                disabled=True
            )
            st.markdown("### Average Score")
            st.slider(
                label="",
                min_value=1,
                max_value=10,
                value=average,
                disabled=True
            )

            person_atts = {
                "person_3": {
                    "name": resume_data.get('name'),
                    "yoe": yoe,
                    "education": education,
                    "company_fit": company_fit,
                    "technical_skills": technical_skills,
                    "soft_skills": soft_skills,
                    "projects": projects,
                    "average": average
                }}

            with open(info_data_path, 'r') as f:
                dic = yaml.safe_load(f)
                dic['persons'].update(person_atts)

            with open(info_data_path, 'w') as f:
                yaml.safe_dump(dic, f)

        with open(info_data_path, 'r') as f:
            chart_data = yaml.safe_load(f)

        option = st.selectbox('Select a person attribute:', list(chart_data["persons"]["person_1"].keys()))
        st.write('You selected:', option)
        execute_browse = st.button("Compare!")

        if execute_browse:
            print(option)

            # if option == "average":
            with open(info_data_path, 'r') as f:
                chart_data = yaml.safe_load(f)
                # print(chart_data)

            attribute_values = [person_data[str(option)] for person_data in chart_data["persons"].values()]

            # Plotting the bar chart using Streamlit
            st.bar_chart({f"{option.capitalize()}": attribute_values}, use_container_width=True)






