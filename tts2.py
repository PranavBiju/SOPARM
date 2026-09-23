from gtts import gTTS
from playsound import playsound


def tts(answer):
    # The text that you want to convert to audio
    mytext = answer

    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine
    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named "welcome.mp3"
    myobj.save("test.mp3")
    playsound("test.mp3")

if __name__ == "__main__":
    tts("Hello")