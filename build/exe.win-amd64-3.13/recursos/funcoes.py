import os, time
import json
from datetime import datetime

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    


def escreverDados(nome, pontos):
    data_hora = datetime.now()
    data_str = data_hora.strftime("%d/%m/%Y")
    hora_str = data_hora.strftime("%H:%M:%S")

    # Atualiza base.atitus (por jogador)
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
            dadosDict = json.loads(dados) if dados else {}
    except FileNotFoundError:
        dadosDict = {}

    dadosDict[nome] = (pontos, data_str)
    with open("base.atitus", "w") as banco:
        banco.write(json.dumps(dadosDict))

    # Adiciona ao histórico log.dat
    try:
        with open("log.dat", "r") as f:
            historico = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historico = []

    historico.append({
        "nome": nome,
        "pontos": pontos,
        "data": data_str,
        "hora": hora_str
    })

    with open("log.dat", "w") as f:
        json.dump(historico[-100:], f, indent=2)
