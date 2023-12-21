import openai


def get_gpt_response(data: str, job_description: str, key: str):
    openai.api_key = key
    function_descriptions = [
        {
            "name": "extract_resume_ratings",
            "description": "Extract information ratings from resume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Extract prospect name",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Write a 80 word summary of the resume",
                    },
                    "years_of_experience": {
                        "type": "number",
                        "description": "Extract prospect total years of experience",
                    },
                    "relevant_skills": {
                        "type": "string",
                        "description": "Extract list of relevant skills to the job",
                    },
                    "company_fit": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect is a fit for the position: [1, 2, ..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "education": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's education matches with the position: [1, 2, ..., 9, 10] 1 being completely unrelated education and 10 being a perfect matched education for the job",
                    },
                    "technical_skills": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's technical skills area a fit for the position: [1, 2, ..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "soft_skills": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's soft skills are a fit for the position: [1, 2,..., 9, 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                    "projects": {
                        "type": "number",
                        "description": "Evaluate in a scale from 1 to 10 how much the prospect's projects are a fit for the position: [1, 2,..., 10] 1 being not fit at all and 10 being a perfect fit",
                    },
                },
                "required": ["name", "years_of_experience"]
            }
        }
    ]

    prompt = f"""You are a professional HR recruiter and your job is to give ratings to a prospect based on the
             job description. Do not output anything else.
             The job description is as follows: {job_description}

             The prospect's resume is as follows: {data}
             """

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=function_descriptions,
        function_call="auto"
    )

    return response
