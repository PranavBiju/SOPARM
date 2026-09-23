import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def speech_2_txt():
    client = OpenAI(api_key=API_KEY)
    origin = '/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/uploads/'
    target = '/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/old_files/'
    files = os.listdir(origin)

    for q in files:
        os.rename(origin + q, target + q)
        audio_file = open(target + q, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text

def get_intent(text):
    client = OpenAI(api_key=API_KEY)

    prompt = """You are a voice command classifier for a robotic arm in a pharmacy.
Given the user's spoken command, classify it into one of these intents:

- "run_pipeline": If the user wants to do ANYTHING related to medicine — pick up, identify, weigh, measure, check, get, grab, place, drop, move, scan, read, or handle a medicine bottle in any way.
- "unknown": If the command is completely unrelated to medicine or the robot arm.

Reply with ONLY the intent string, nothing else. No quotes, no explanation."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip().lower()

def write_action(intent):
    with open('ans.py', 'w') as f:
        if "run_pipeline" in intent:
            f.write("import identify_unkown\n\nidentify_unkown.identify_new()\n")
            print("Action: Running full medicine pipeline")
        else:
            f.write("print('Command not recognized. Please try again.')\n")
            print("Action: Command not recognized, skipping.")

trans = speech_2_txt()
print("You said:", trans)
intent = get_intent(trans)
print("Intent:", intent)
write_action(intent)
