from openai import OpenAI
import pyttsx3
import json
from time import sleep
from pprint import pprint

client = OpenAI()

# GPT vars
cached_responses = [
    {
        "role": "system", 
        "content": "You are a helpful assistant. return json as 'response': \
        'whatever the response is'. please keep responses only a sentence or\
        two in length, meaning they must be quite concise"
    },
    {
        "role": "assistant",
        "content": "Let's begin!"
    }
]

# Speech init
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)

check = 0
def checkpoint():
    global check
    check += 1
    print("Checkpoint", check)

def speak_text(command):
    engine.say(command) 
    engine.runAndWait()

def format_json(role, content):
    return {"role": role, "content": content}

def fetch_response(query):
    cached_responses.append(format_json("user", query))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type":  "json_object"},
        messages=cached_responses
    )
    response = json.loads(response.choices[0].message.content)["response"]

    # Save new message data
    cached_responses.append(format_json("assistant", response))

    return response

def print_content(json_data):
    for item in json_data:
        print(item["content"])


if __name__ == "__main__":
    print(fetch_response("What is 2 + 7?"))
    print(fetch_response("Who invented rock n roll?"))
