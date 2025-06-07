import json

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

import os

GEMINI_API_KEY = 'AIzaSyDNPTNh3hw-6Y0S6XH4wRLMTNgVGMoqSlw'
genai.configure(api_key=GEMINI_API_KEY)
app = FastAPI()
origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:50733"  # Your specific port if different
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat(history=[])
class UserResponse(BaseModel):
    user_response: str

@app.post("/gemini_explanation")
async def get_new_explanation(user_response: UserResponse):
    # Assuming `chat.send_message()` is some function you have elsewhere
    response = chat.send_message(f"""
          You are an 10+ years experienced UPSC educator. You have to give explanation for 
          the mcq questions that is sent to you as input {user_response.user_response} which is a stringified json.
          Generate a detailed explanation as string stating why the particular option is correct and why others are wrong.
          In order to give detailed explanation to the UPSC aspirants.
    """)
    raw_text = response.text
    print(raw_text)
    raw_text = raw_text.replace("`", "")
    raw_text = raw_text.replace("json", "")

    return {"Message": "Gemini explanation", "explanation": raw_text}


@app.get("/gemini_generatequestions")
async def get_questions(topic: str):
    # Assuming `chat.send_message()` is some function you have elsewhere
    response = chat.send_message(f"""
          You are an 10+ years experienced technical education expert. Your task is to generate 10 questions
           based on the prompt provided by the user {topic}. Analyse the prompt correctly and generate the 
           questions which are on the level of GATE exams an entrance exam for higher studies in 
           premier institutes that are conducted in INDIA. Strictly make sure that the output is in form of json array 
           which consists on questions, option_a, option_b, option_c, option_d, correct_answer, explanation, 
           categories to which the question belongs to. And also strictly ensure that i will convert ur output string to json so i shouldn't get any json parse error be careful on this""")
    raw_text = response.text
    raw_text = raw_text.replace("`", "")
    raw_text = raw_text.replace("\n", "")
    raw_text = raw_text.replace("\\", "")
    raw_text = raw_text.replace("json", "")
    print(raw_text)
    questions = json.loads(raw_text)

    # Ensure the questions is a list
    if not isinstance(questions, list):
        raise ValueError("The response is not a list")

    return {"Message": "Gemini questions", "questions": questions}




@app.get("/gemini_performanceanalysis")
async def get_performance_analysis(topic: str):
    # Assuming `chat.send_message()` is some function you have elsewhere
    response = chat.send_message(f"""
          You are an 10+ years experienced technical education expert. Your task is to generate a 
          brief summary helping the user to use this as an input for planning their further studies 
          plan to excel in the exam. Focus on informing them their weaker and stronger areas and also 
          help them to make themselves stronger. A string which contains of category and scores where 
          multiple category-score is comma separated {topic}. Give the output in form of a string and also adhere to 
          the points that are given.
    """)
    raw_text = response.text
    print(raw_text)
    raw_text = raw_text.replace("`", "")
    raw_text = raw_text.replace("json", "")
    raw_text = raw_text.replace("*", "")

    return {"Message": "Gemini analysis", "feedback": raw_text}


@app.get("/gemini_prediction")
async def get_performance_analysis(pastdata: str, currentdata: str):
    # Assuming `chat.send_message()` is some function you have elsewhere
    response = chat.send_message(f"""
          You are an intelligent agent good in predicting that whether if a question is skipped by the user 
          what is the probability that they might had attempted correct or wrong. Also give the 
          explanation about ur prediction why do u think so that too  based on the history and the 
          current data. Analyse the past performance data {pastdata} where the userscore on particular category will be shared with you as comma separated values
           and look onto the present response {currentdata} where u will have the question, category and whether user has answered or 
           skipped and on the basis of this generate a short summary around 8 lines as an output by adhering to the rules i mentioned. If past data is not available then motivate the user to take the test for future predictions.
    """)
    raw_text = response.text
    print(raw_text)
    raw_text = raw_text.replace("`", "")
    raw_text = raw_text.replace("json", "")
    raw_text = raw_text.replace("*", "")

    return {"Message": "Gemini prediction", "prediction": raw_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
