🧠 Jarvis IA

Jarvis is an intelligent, sarcastic, and futuristic AI assistant inspired by Tony Stark's iconic system.
Built in Python, it features voice interaction, vision models, command automation, emotional memory, music search, autonomous learning, and much more — all running locally on your machine.

💻 Requirements

    Python 3.10

    CUDA-compatible GPU (optional, for faster Whisper)

    Ollama running on Windows Host (for LLaMA 3.3 and LLaMA 3.2 Vision models)

    Ubuntu Virtual Machine (for running Jarvis)

    ffmpeg, git, git-lfs

    Internet connection for web search and autonomous learning

    PulseAudio or ALSA configured for microphone input in VM

🔥 Main Features

    🎙 Wake Word Detection — Activates on hearing “Jarvis”

    🎧 Voice Activity Detection (VAD) — Smart, real-time listening

    🗣 Text-to-Speech — Fast local voice synthesis with Piper (no cloud dependencies)

    🎧 Speech-to-Text — High-performance transcription with Whisper (or Whisper.cpp for CPU)

    🧠 Contextual Memory — LLaMA 3.3 (for deep answers and continuity)

    👁 Vision Model — LLaMA 3.2 Vision 90B (for image understanding)

    🧩 Multi-command parsing — e.g. “Open the folder and play music”

    🔍 Web fallback — If uncertain, Jarvis searches autonomously

    🖼 Vision from local images — Describe images inside imagens/ folder

    💾 Short-term Memory — Session context

    🧠 Long-term Persistent Memory — Stored in SQLite

    ❤️ Emotional Memory — Save happy/sad moments by voice

    📘 Reflective Mode — Voice journaling with emotional tagging

    🧠 Autonomous Web Learning — Scrapes and stores new knowledge

    💻 App and System Control — Open apps, folders, browser tabs

    🎵 Apple Music Integration — Search, play, control music via voice

    🧱 Highly Modular Architecture — Easy to extend new commands

🗂 Project Structure

jarvis/
├── comandos/          # Modular commands (music, system, folders, memory, etc.)
├── brain/             # Audio, memory, utils, dev tools
├── core/              # Model initialization and system integration
├── imagens/           # Local images for vision tasks
├── tests/             # Model testing scripts
├── jarvis.py          # Main executable
├── requirements.txt   # Python dependencies
└── README.md          # This file

🗣️ Example Voice Commands

    "Jarvis, open the downloads folder"

    "Jarvis, describe the image skyline"

    "Jarvis, shut down"

    "Jarvis, play Arctic Monkeys"

    "Jarvis, search on the internet what is quantum computing"

    "Jarvis, remember that coding made me happy"

    "Jarvis, what made me happy this month?"

    "Jarvis, let's write today's diary"

🖼️ Vision Mode (LLaMA 3.2 Vision 90B)

Trigger advanced image understanding with:

    "Describe the image skyline with details"

    "Give me a detailed description of the image"

(Default: falls back to a faster text-only model when not specifically vision-triggered.)
🎵 Apple Music Integration

Jarvis can:

    🎶 Open your library: "Jarvis, open Apple Music"

    🔍 Search and play: "Jarvis, play Arctic Monkeys"

    ⏯ Pause, resume, next track: "pause music", "next song"

❤️ Emotional Memory

    Save emotional events:
    "Jarvis, remember that my birthday made me happy"

    Retrieve memories:
    "Jarvis, what made me happy this month?"

    Reflective voice journaling:
    "Jarvis, I want to record today's diary"

🧠 Autonomous Learning

Jarvis learns dynamically:

    "Jarvis, search what is quantum entanglement and learn it"

It will:

    Scrape trustworthy sources

    Summarize the information

    Save it into the long-term memory database (with timestamp)

🚀 Getting Started

# Clone the repository
git clone https://github.com/ProjectXTN/Jarvis_IA.git

# Navigate to the project
cd Jarvis_IA

# Create the virtual environment
python3.10 -m venv venv-linux

# Activate the environment
source venv-linux/bin/activate

# Install Python dependencies
pip install -r requirements.txt

    Make sure Ollama is running on your Windows host:

ollama serve

    Set the proper OLLAMA_HOST inside your Ubuntu VM if needed:

export OLLAMA_HOST="http://<your_windows_ip>:11500"

(Jarvis detects it automatically if configured.)
🔒 Lock System

Jarvis uses a .lock file to ensure only one instance runs at a time.
🧘 Voice Deactivation

You can stop active interaction by saying:

    "Jarvis, stop responding"

    "Jarvis, silence"

    "Jarvis, mute"

Jarvis will return to passive wake-word listening.
📈 Performance Tips

    Increase VM CPU cores and RAM for better real-time performance.

    Piper TTS is up to 10x faster than cloud TTS systems.

✨ Made with 💥 by Pedro