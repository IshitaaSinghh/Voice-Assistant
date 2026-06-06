import pyttsx3 as tts
import speech_recognition as sr
import datetime as dt
import google.genai as genai

#Defining the class for Voice Assistant
class VoiceAssistant:
    def __init__(self, name="chatbot"):
        self.name = name
        self.client = genai.Client(api_key= "")
        
        current_hour = dt.datetime.now().hour
        greet_message = "Hello, Good "
        if (current_hour<12):
            greet_message += "Morning"
        elif (current_hour<18):
            greet_message += "Afternoon"
        else:
            greet_message += "Evening"

        greet_message += ", Mam"

        self.text_to_voice(greet_message)

    def text_to_voice(self, text):
        print(f"{self.name} said: {text}")

        voice_engine= tts.init()
 
        # for voice in voice_engine.getProperty("voices"):
        #     print(voice)

        # voices = voice_engine.getProperty("voices")

        # voice_engine.setProperty("voice", voices[1].id)
        # voice_engine.setProperty("rate", 250)

        voice_engine.say(text)
        voice_engine.runAndWait()

    def voice_to_text(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as microphone:
            print(f"{self.name} said: Please say something, I'm listening")
            voice = recognizer.listen(microphone)

        try:
            text = recognizer.recognize_google(voice)
        except Exception:
            return None
        else:
            return text
        
    def get_answer(self, question):
        if question in ("what is your name", "what's your name", "whats your name",
                        "what is yor name", "what's yor name", "whats yor name"):
            answer = (f"My name is {self.name}")
        elif question in ("who are you", 'hu are you', 'hu r u'):
            answer = (f"I am your voice assistant, Mam")
        elif question in ("who created you", "who developed you", 
                          "hu created you", "hu developed you"):
            answer = (f"I am developed by you")
        elif any(word in question for word in ("what", "who", "when", "how", "tell", "describe", "where")):
            answer = self.client.models.generate_content(model="gemini-2.5-flash", contents = question +"and keep it short")
            is_ai_generated = True
            is_long_answer = False
            return answer, is_ai_generated, is_long_answer
        elif 'write' in question or 'create' in question or 'generate' in question:
            answer = self.client.models.generate_content_stream(model = 'gemini-2.5-flash', contents=question)
            is_ai_generated = True
            is_long_answer = True
            return answer, is_ai_generated, is_long_answer
        else:
            answer = "I don't know about it ,mam"
        is_ai_generated = False
        is_long_answer = False
        return answer, is_ai_generated, is_long_answer

voice_assistant = VoiceAssistant()

while True:
    question = voice_assistant.voice_to_text()

    if question is not None:
        question = question.lower()
        if question in ('stop', 'exit', 'quit'):
            print(f"You said: {question}")
            break
        print(f"You asked: {question}")
        answer, is_ai_generated, is_long_answer = voice_assistant.get_answer(question)
        if is_ai_generated and is_long_answer :
            voice_assistant.text_to_voice("Please wait, im getting ur answer, mam")
            for line in answer:
                line = line.text
                if '*' in line:
                    line =line .replace("*", " ")
                if '#' in line:
                    line=line.replace("#", " ")
                print(line)
            voice_assistant.text_to_voice("This is the end of your answer, mam")
        elif is_ai_generated and not is_long_answer:

            answer = answer.text
            if '*' in answer:
                answer=answer.replace("*", " ")
            if '#' in answer:
                answer=answer.replace("#", " ")
            voice_assistant.text_to_voice(answer)
            print(answer)
        else:
            voice_assistant.text_to_voice(answer)
    else:
        voice_assistant.text_to_voice("I did not understand what you said, Mam")

voice_assistant.text_to_voice("Bye, I am leaving now mam")
