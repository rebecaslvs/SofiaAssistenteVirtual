import speech_recognition as sr
import json
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from unidecode import unidecode
# from bs4 import BeautifulSoup
import wikipedia
import pyttsx3
from difflib import SequenceMatcher
import pyfiglet

figlet = pyfiglet.Figlet()

with open('config.json', mode='r', encoding='utf-8') as arquivoConfiguracoes:
    config = json.load(arquivoConfiguracoes)

prefixoAssistente = config['nome']
perguntas = []
for pergunta in config['perguntas']:
    perguntas.append(pergunta["nome"])


# def formatarPerguntasConfig(perguntas):
#     perguntasFormatadas = []
#     stop_words = set(stopwords.words('portuguese'))
#     for pergunta in perguntas:
#         perguntaFormatada = pergunta.lower()
#         perguntaFormatada = word_tokenize(unidecode(perguntaFormatada))
#         for stop_word in stop_words:
#             if stop_word in perguntaFormatada:
#                 perguntaFormatada.remove(stop_word)
#         pergunta = " ".join(perguntaFormatada)
#         perguntasFormatadas.append(pergunta)
#     return perguntasFormatadas


# def verificarPergunta(texto):
#     textoSemPrefixoAssistente = texto.replace(prefixoAssistente, "")
#     stop_words = set(stopwords.words('portuguese'))
#     textoFormatado = textoSemPrefixoAssistente.lower()
#     textoFormatado = word_tokenize(unidecode(textoFormatado))
#     for stop_word in stop_words:
#         if stop_word in textoFormatado:
#             textoFormatado.remove(stop_word)
#     textoFormatado = " ".join(textoFormatado)
#     for pergunta in formatarPerguntasConfig(perguntas):
#         if pergunta == textoFormatado:
#             print("Aguarde...")
#             buscarConteudo(textoSemPrefixoAssistente)
#             break

def verificarPergunta(texto):
    texto = texto.replace(prefixoAssistente.lower(), '')
    for pergunta in perguntas:
        if compararTextos(pergunta, texto) > 0.7:
            print("Pergunta encontrada: " + pergunta)
            buscarConteudo(pergunta)
            return pergunta


def compararTextos(texto1, texto2):
    return SequenceMatcher(None, texto1, texto2).ratio()


# def buscarConteudo(texto):
#     wikipedia.set_lang("pt")
#     conteudo = wikipedia.page(texto)
#     soup = BeautifulSoup(conteudo.html(), 'html.parser')
#     respostaEsperada = soup.find('p').text
#     print(respostaEsperada)
#     engine = pyttsx3.init()
#     engine.say(respostaEsperada)
#     engine.runAndWait()

def buscarConteudo(texto):
    try:
        wikipedia.set_lang("pt")
        conteudo = wikipedia.summary(texto, sentences=2)
        print(conteudo)
        return conteudo
    except Exception as e:
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
