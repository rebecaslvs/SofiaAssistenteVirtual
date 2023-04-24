import speech_recognition as sr
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# from unidecode import unidecode
# from bs4 import BeautifulSoup
import wikipedia
from difflib import SequenceMatcher
import pyfiglet

# SE for a primeira vez, precisa fazer download dos pacaotes adicionais
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

figlet = pyfiglet.Figlet()

with open('config.json', mode='r', encoding='utf-8') as arquivoConfiguracoes:
    config = json.load(arquivoConfiguracoes)

prefixoAssistente = config['nome']
perguntas = []
for pergunta in config['perguntas']:
    perguntas.append(pergunta["nome"])


def verificarPergunta(texto):
    texto = texto.replace(prefixoAssistente.lower(), '')
    for pergunta in perguntas:
        if compararTextos(pergunta, texto) > 0.7:
            print("Pergunta encontrada: " + pergunta)
            buscarConteudo(pergunta)
            return pergunta


def compararTextos(texto1, texto2):
    return SequenceMatcher(None, texto1, texto2).ratio()


def formatarTexto(texto):
    stop_words = set(stopwords.words('portuguese'))
    tokens = word_tokenize(texto)
    for stop_word in stop_words:
        if stop_word in tokens:
            tokens.remove(stop_word)
    return " ".join(tokens)


def buscarConteudo(texto):
    textoFormatado = formatarTexto(texto)
    try:
        wikipedia.set_lang("pt")
        conteudo = wikipedia.summary(textoFormatado, sentences=2)
        print(conteudo)
        return conteudo
    except Exception as e:
        conteudo = wikipedia.search(textoFormatado)
        if len(conteudo) > 0:
            print("Buscando por: " + conteudo[0])
            buscarConteudo(conteudo[0])
        else:
            print("Erro ao buscar conteúdo: " + str(e))


def iniciarAssistente():
    looping = True
    r = sr.Recognizer()
    while looping:
        with sr.Microphone() as source:
            print("Diga alguma coisa: ")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
            try:
                texto = r.recognize_google(audio, language='pt-BR')
                if "desligar" in texto.lower():
                    looping = False
                    break
                print(texto)
                if texto.lower().startswith(prefixoAssistente.lower()):
                    verificarPergunta(texto)
            except:
                print("Não entendi")
                looping = False


if __name__ == '__main__':
    print(figlet.renderText(prefixoAssistente))
    # adicionar legendas - mensagens de boas-vindas
    iniciarAssistente()
