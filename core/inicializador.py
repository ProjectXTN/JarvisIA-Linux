import os
import subprocess
import requests
import time
import platform
from brain.audio import listen

LOCK_FILE = "jarvis.lock"
VISION_MODELS = ["llama3.2-vision:90b", "llama3.2", "llama3.3"]

# Detecta o sistema operacional
def detectar_ollama_host():
    host = os.getenv("OLLAMA_HOST")
    if host:
        return host
    sistema = platform.system()
    if sistema == "Windows":
        return "http://localhost:11434"
    else:
        return "http://10.0.2.2:11434"


OLLAMA_HOST = detectar_ollama_host()


def ja_esta_rodando():
    if os.path.exists(LOCK_FILE):
        return True
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        return False
    except Exception as e:
        print(f"Erro ao criar lock: {e}")
        return True

def remover_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def iniciar_llava():
    try:
        requests.get(OLLAMA_HOST)
        print(f"✅ Conectado ao Ollama em {OLLAMA_HOST}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao Ollama em {OLLAMA_HOST}")
        print("Certifique-se que o Ollama está rodando no Windows ou na máquina local!")
        time.sleep(5)

    aquecer_modelo_vision()

def aquecer_modelo_vision():
    print("🔥 Pré-aquecendo o modelo vision...")
    try:
        requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "llama3.2-vision:90b",
                "prompt": "<image>nula</image>\nIgnore isso."
            },
            timeout=10
        )
    except Exception as e:
        print(f"Erro ao pré-aquecer modelo: {e}")

def modo_passivo():
    print("Modo passivo ativado. Aguardando a hotword 'Jarvis'...")
    while True:
        texto = listen()
        if not texto:
            continue

        texto = texto.strip()
        if "jarvis" in texto.lower():
            return texto


def gerar_resposta(prompt, modelo="llama3.2-vision:90b"):
    try:
        resposta = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if resposta.ok:
            return resposta.json()["response"].strip()
        else:
            print(f"Erro na resposta do Ollama: {resposta.status_code} {resposta.text}")
            return "Desculpe, houve um erro ao consultar a inteligência."
    except Exception as e:
        print(f"Erro durante consulta ao Ollama: {e}")
        return "Desculpe, houve um problema de conexão com a inteligência."
