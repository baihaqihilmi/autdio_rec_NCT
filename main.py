r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source , timeout=2)
        message = r.recognize_google(audio ,language = "tr" )
        try:

            print("Google Speech Recognition thinks you said : " + message)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
