from groq import Groq
import os
import datetime
from gtts import gTTS
from playsound import playsound
from openai import OpenAI
import speech_recognition as sr

os.environ.add
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

## Default Config 
language_select = "Turkish"
i = 0
mic = 1

while True:
    # if mic == 1 :

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source , timeout=2)
    try:
        message = r.recognize_google(audio ,language = "tr" )
        print("Google Speech Recognition thinks you said : " + message)
    except sr.UnknownValueError:
        respond = "Özür dilerim, sizi anlayamadım, belki biraz daha yüksek sesle konuşabilirsiniz."
        print("Google Speech Recognition could not understand audio")
        completion = 0
    except sr.RequestError as e:
        respond = "Üzgünüm, konuşma servisim kapandı."
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        completion = 0

    else : 
        if i == 0:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
            
                messages=[
                    {
                        "role" : "system",
                        "content": f"Tur Rehberi olarak cevap verin, {language_select} dilinde cevap vererek Hoş Geldiniz deyin ve yalnızca {language_select} içinde yanıtlayın , {language_select} içinde yazım denetimi yapın"

                    },
                    { 
                        "role": "user",
                        "content": message
                    },

                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
        )
        else : 
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
            
                message=[
                    {
                        "role" : "system",
                        "content": f"Tur Rehberi olarak cevap verin, zaten hoş geldiniz diyorsanız tekrar etmeyin, {language_select} dilinde cevap vererek"

                    },
                    { 
                        "role": "user",
                        "content": message
                    },

                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
        )


        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        i+=1
        # print(len(completion.choices))
        
    # Step 4: Clean up - remove the audio file after playing

    finally:
        tts = gTTS(completion.choices[0].message.content if completion else respond, lang="tr")
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        print(completion.choices[0].message.content if completion else respond)
        os.remove(audio_file)


