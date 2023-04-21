import speech_recognition as sr
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
import wikipedia

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
            print("Achei a pergunta")
            buscarConteudo(textoSemPrefixoAssistente)
            break


def buscarConteudo(texto):
    wikipedia.set_lang("pt")
    conteudo = wikipedia.page(texto)
    print(conteudo.content)


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Diga alguma coisa: ")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        if texto.lower().startswith(prefixoAssistente.lower()):
            print(texto)
            verificarPergunta(texto)

    except:
        print("Não entendi")
