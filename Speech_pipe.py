import os
from openai import OpenAI

def speech_2_txt():
    client = OpenAI(api_key='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')
    origin = '/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/uploads/'
    target = '/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/old_files/'
    files = os.listdir(origin)
    #print(files)

    for q in files:
        os.rename(origin + q, target + q)
        #print(origin+q)
        audio_file = target + q
        audio_file= open(audio_file, "rb")
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        return transcription.text

def chatgpt(text):
    file1 = open('prompt.txt','r')
    prompt = file1.read()
    client = OpenAI(api_key='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')
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]
    )
    file = open('ans.py','w')
    file.write(response.choices[0].message.content)
    file.close()

trans = speech_2_txt()
print(trans)
print("entering chatGPT")
chatgpt(trans)
print("ChatGPT done")
