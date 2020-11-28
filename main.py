

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import *

tags_metadata=[
    {
        'name':'similarity',
        'description':'Finds the similarity between 2 sentences using their word vectors.'
    },
    {
        'name':'tokenize',
        'description':'Takes in word, sentences e.t.c and return lexical infromation about each of words. e.g Nouns, Abstract Nouns, Co-ordinating conjunction.'
    },
    {
        'name':'synonyms',
        'description':'Takes in a word or a group of words separated by commas and return a list of english language synonyms for the words.'
    },
    {
        'name':'antonyms',
        'description':'Takes in a word or a group of words separated by commas and return a list of english language antonyms for the words.'
    },
    {
        'name':'tospeech',
        'description':'Takes in a string and returns an audio file of the word.'
    }
]

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
app = FastAPI(title='Tageit',
              description='This is a hobby project for people interesed in using NLP. Email tomibami2020@gmail.com for new functionality you want to be added.',
              openapi_tags=tags_metadata)

@app.get('/')
def home():
    return 'Welcome here'

@app.post('/similarity' , response_model=SimilarityOut,tags=['similarity'])
def similarity(text : SimilarityIn):
    score = similarity_(text.text_1, text.text_2)
    return {'score':score}

@app.post('/tokenize', response_model=dict,tags=['tokenize'])
def tokenize(text : TokenizeIn):
    tokens = tokenize_(text.text)
    return tokens

@app.post('/synonyms', response_model=dict, tags=['synonyms'])
def synonyms(text : SynonymIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = synonyms_(i.strip())
        response[i]=syns
        
    return response

@app.post('/antonyms', response_model=dict, tags=['antonyms'])
def antonyms(text : AntonymsIn ):
    words = text.text.replace(' ','').split(',')
    response = {}
    for i in words:
        syns = antonyms_(i.strip())
        response[i]=syns       
    return response

@app.post('/tospeech' ,tags=['tospeech'])
async def  text_to_speech(text : TextToSpeech ):
    language = text.language
    if len(language)>2:
        language=language[:2].lower()
    elif len(language)<2:
        language='en'
    audio_object = text_to_speech_(text.text,language=language)
    audio_object.save('aud.mp3')
    return FileResponse('aud.mp3')