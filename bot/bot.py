import random
import re
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def rolar_dado(lados=6, quantidade=1, seed=None):
    random.seed(seed)
    resultados = [random.randint(1, lados) for _ in range(quantidade)]
    return resultados

def parse_rolagem(entrada):
    padrao = r"(\d+)d(\d+)(?:\s*([+-])\s*(\d+))?"
    match = re.match(padrao, entrada.strip())
    if not match:
        raise ValueError("Formato inválido. Use 'XdY [+|-] Z', como '1d20 + 3' ou '3d10 - 5'.")
    quantidade = int(match.group(1))
    lados = int(match.group(2))
    modificador = int(match.group(4)) if match.group(4) else 0
    if match.group(3) == "-":
        modificador = -modificador
    return quantidade, lados, modificador

def calcular_rolagem(entrada, seed=None):
    try:
        quantidade, lados, modificador = parse_rolagem(entrada)
        resultados = rolar_dado(lados, quantidade, seed)
        total = sum(resultados) + modificador
        return f"Resultados dos dados: {resultados}, Total: {total}"
    except ValueError as e:
        return str(e)

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.form.get("Body")
    resposta = calcular_rolagem(msg)
    twiml_resp = MessagingResponse()
    twiml_resp.message(resposta)
    return str(twiml_resp)

if __name__ == "__main__":
    app.run(debug=True)
