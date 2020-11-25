

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import *

class SimilarityIn(BaseModel):
    text_1 : str
    text_2 : str
class SimilarityOut(BaseModel):
    score : float
class TokenizeIn(BaseModel):
    text : str
class SynonymIn(BaseModel):
    text : str
class AntonymsIn(BaseModel):
    text : str
class TextToSpeech(BaseModel):
    text : str
    language : Optional[str] = 'en'
app = FastAPI()

@app.get('/')
def home():
    return "Welcome here"

@app.post('/similarity' , response_model=SimilarityOut)
def similarity(text : SimilarityIn):
    score = similarity_(text.text_1, text.text_2)
    return {'score':score}

@app.post('/tokenize', response_model=dict)
def tokenize(text : TokenizeIn):
    tokens = tokenize_(text.text)
    return tokens

@app.post('/synonyms', response_model=dict)
def synonyms(text : SynonymIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = synonyms_(i.strip())
        response[i]=syns
        
    return response

@app.post('/antonyms', response_model=dict)
def antonyms(text : AntonymsIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = antonyms_(i.strip())
        response[i]=syns       
    return response

@app.post('/tospeech')
async def  text_to_speech(text : TextToSpeech ):
    language = text.language
    if len(language)>2:
        language=language[:2].lower()
    elif len(language)<2:
        language='en'
    audio_object = text_to_speech_(text.text,language=language)
    audio_object.save('aud.mp3')
    return FileResponse('aud.mp3')