import unittest
import main
import json
import speech_recognition as sr

with open('config.json', mode='r', encoding='utf-8') as arquivoConfiguracoes:
    config = json.load(arquivoConfiguracoes)

prefixoAssistente = config['nome']
perguntas = []
for pergunta in config['perguntas']:
    perguntas.append(pergunta["nome"])

class TestAssistente(unittest.TestCase):

    def test_compararTextos(self):
        self.assertGreaterEqual(main.compararTextos(
            'Quais as características do renascimento', 'Quais são as caracteristicas do renascimento'), 0.8)
        self.assertLessEqual(main.compararTextos(
            'Quais as características do renascimento', 'Rebeca Silva'), 0.2)

    def test_verificarPergunta(self):
        pergunta = perguntas[0]
        self.assertEqual(main.verificarPergunta(pergunta), pergunta)

    def test_buscarConteudo(self):
        pergunta = perguntas[0]
        respostaEsperada = "Renascimento, Renascença ou Renascentismo são os termos usados para identificar o período da história da Europa aproximadamente entre meados do século XIV e o fim do século XVI. Os estudiosos, contudo, não chegaram a um consenso sobre essa cronologia, havendo variações consideráveis nas datas conforme o autor. Apesar das transformações serem bem evidentes na cultura, sociedade, economia, política e religião, caracterizando a transição do feudalismo para o capitalismo e significando uma evolução em relação às estruturas medievais, o termo é mais comumente empregado para descrever seus efeitos nas artes, na filosofia e nas ciências."
        self.assertEqual(main.buscarConteudo(
            pergunta), respostaEsperada)

    def test_assistente(self):
        self.r = sr.Recognizer()
        with sr.AudioFile('arquivo_de_audio.wav') as source:
            audio = self.r.record(source)
            texto = self.r.recognize_google(audio, language='pt-BR')
            self.assertIsInstance(texto, str)

    def test_formatarTexto(self):
        texto = "o que foi o renascimento"
        resultadoExperado = "o renascimento"
        self.assertEqual(main.formatarTexto(texto), resultadoExperado)


if __name__ == '__main__':
    unittest.main()
