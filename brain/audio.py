import asyncio, subprocess, uuid, os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import tempfile
import sys
import webrtcvad
import collections
import threading
import torch
import whisper
import time
from piper.voice import PiperVoice
import wave

# === Variável global para integração com GUI ===
gui_callback = None

# === Lock para evitar concorrência no Whisper ===
transcribe_lock = threading.Lock()

# === Corrige o path dos assets do Whisper se for .exe ===
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ["WHISPER_ASSETS"] = os.path.join(base_path, "whisper", "assets")

# === Modelo de transcrição ===
model = whisper.load_model("medium").to("cuda" if torch.cuda.is_available() else "cpu")
current_audio_process = None

# === Carrega o modelo do Piper ===
PIPER_MODEL = "/home/pedro/Projetos/JarvisIA/piper/pt_BR-faber-medium.onnx"  # Ajuste o path conforme seu projeto
piper_voice = PiperVoice.load(PIPER_MODEL)

# === Função principal de fala com suporte à GUI ===
async def speak_with_gui(text):
    global current_audio_process

    if gui_callback:
        gui_callback(f"🤖 Jarvis: {text}")
    else:
        print(f"\n🧠 Jarvis: {text}")

    filename = f"jarvis_{uuid.uuid4().hex}.wav"

    try:
        start_time = time.time()  # <-- INÍCIO cronômetro

        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(piper_voice.config.sample_rate)
            piper_voice.synthesize(text, wav_file)

        end_time = time.time()  # <-- FIM cronômetro

        duration = end_time - start_time
        print(f"⏱️ Tempo para gerar áudio: {duration:.2f} segundos.")

        current_audio_process = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filename],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        current_audio_process.wait()
    except Exception as e:
        print(f"Erro na síntese ou reprodução de áudio: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
        current_audio_process = None

# === Função pública de fala ===
def say(text):
    global current_audio_process

    if current_audio_process and current_audio_process.poll() is None:
        print("🔇 Interrompendo áudio anterior...")
        current_audio_process.terminate()
        current_audio_process = None

    asyncio.run(speak_with_gui(text))

# === Função de escuta com VAD + Whisper ===
def listen():
    global current_audio_process
    stream = None

    if current_audio_process and current_audio_process.poll() is None:
        print("🔇 Interrompendo resposta ativa...")
        current_audio_process.terminate()
        current_audio_process = None

    fs = 16000
    vad = webrtcvad.Vad(2)
    duration_ms = 30
    frame_size = int(fs * duration_ms / 1000)
    block_duration = frame_size / fs if fs > 0 else 0.01

    print("\n🎙️ Ouvindo com VAD...")

    audio = []
    ring_buffer = collections.deque(maxlen=10)
    triggered = False
    silence_duration = 1.5
    silence_blocks = int(silence_duration / block_duration)
    silence_counter = 0

    try:
        stream = sd.InputStream(device=1, samplerate=fs, channels=1, dtype='int16', blocksize=frame_size)
        stream.start()

        while True:
            block, _ = stream.read(frame_size)
            is_speech = vad.is_speech(block.tobytes(), fs)

            if not triggered:
                ring_buffer.append((block, is_speech))
                if sum(1 for _, speech in ring_buffer if speech) > 0.6 * ring_buffer.maxlen:
                    triggered = True
                    audio.extend(b for b, _ in ring_buffer)
                    ring_buffer.clear()
            else:
                audio.append(block)
                if not is_speech:
                    silence_counter += 1
                    if silence_counter > silence_blocks:
                        break
                else:
                    silence_counter = 0
    except Exception as e:
        print(f"Erro durante captura de áudio: {e}")
        return ""
    finally:
        if stream:
            stream.stop()

    audio_np = np.concatenate(audio, axis=0)
    volume_medio = np.abs(audio_np).mean()
    print(f"🔊 Volume médio detectado: {volume_medio:.2f}")

    if volume_medio < 100:
        print("🧘 Volume baixo, ignorando...")
        return ""

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        scipy.io.wavfile.write(f.name, fs, audio_np)
        print("🔎 Transcrevendo com Whisper...")

        try:
            start_time = time.time()

            with transcribe_lock:
                result = model.transcribe(f.name, language="pt")

            end_time = time.time()

            duration = end_time - start_time
            print(f"⏱️ Tempo para transcrever áudio: {duration:.2f} segundos.")
            
            texto = result["text"].strip()
        except Exception as e:
            print(f"Erro na transcrição: {e}")
            return ""

        if texto:
            print("🖙️ Você disse:", texto)
            return texto
        else:
            print("Nenhum texto detectado.")
            return ""
