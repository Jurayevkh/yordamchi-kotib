from googletrans import Translator

translator = Translator()

def translateToSomeLang(text: str, dest:str):
    return translator.translate(text,dest=dest)