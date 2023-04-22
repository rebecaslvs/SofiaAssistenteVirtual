import speech_recognition as sr
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from bs4 import BeautifulSoup
import wikipedia
import pyttsx3

with open('config.json', mode='r', encoding='utf-8') as arquivoConfiguracoes:
    config = json.load(arquivoConfiguracoes)

prefixoAssistente = config['nome']
perguntas = []
for pergunta in config['perguntas']:
    perguntas.append(pergunta["nome"])


def formatarPerguntasConfig(perguntas):
    perguntasFormatadas = []
    stop_words = set(stopwords.words('portuguese'))
    for pergunta in perguntas:
        perguntaFormatada = pergunta.lower()
        perguntaFormatada = word_tokenize(unidecode(perguntaFormatada))
        for stop_word in stop_words:
            if stop_word in perguntaFormatada:
                perguntaFormatada.remove(stop_word)
        pergunta = " ".join(perguntaFormatada)
        perguntasFormatadas.append(pergunta)
    return perguntasFormatadas


def verificarPergunta(texto):
    textoSemPrefixoAssistente = texto.replace(prefixoAssistente, "")
    stop_words = set(stopwords.words('portuguese'))
    textoFormatado = textoSemPrefixoAssistente.lower()
    textoFormatado = word_tokenize(unidecode(textoFormatado))
    for stop_word in stop_words:
        if stop_word in textoFormatado:
            textoFormatado.remove(stop_word)
    textoFormatado = " ".join(textoFormatado)
    for pergunta in formatarPerguntasConfig(perguntas):
        if pergunta == textoFormatado:
            print("Aguarde...")
            buscarConteudo(textoSemPrefixoAssistente)
            break


def buscarConteudo(texto):
    wikipedia.set_lang("pt")
    conteudo = wikipedia.page(texto)
    soup = BeautifulSoup(conteudo.html(), 'html.parser')
    respostaEsperada = soup.find('p').text
    print(respostaEsperada)
    engine = pyttsx3.init()
    engine.say(respostaEsperada)
    engine.runAndWait()


print("Olá, eu sou a " + prefixoAssistente +
      " e estou aqui para te ajudar.")
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Qual a sua dúvida sobre o renascimento? ")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        if texto.lower().startswith(prefixoAssistente.lower()):
            print("Sua pergunta: " + texto)
            verificarPergunta(texto)
    except:
        print("Desculpa, não encontrei uma resposta!")
