SOTTOTITOLI MULTIPIATTAFORMA
==========================

Metti questi file nella cartella contenente i video e avvia:
- macOS: Avvia_macOS.command
- Windows: Avvia_Windows.bat
- Linux: Avvia_Linux.sh

I video vengono elaborati in ordine alfabetico e producono .srt e .txt.
Il modello predefinito e' Whisper Small e la lingua e' inglese.
I file gia' elaborati vengono saltati.

PRIMA INSTALLAZIONE
-------------------
Installa Python 3 e FFmpeg (quest'ultimo deve essere disponibile nel PATH).
Installa poi il backend opportuno dentro un ambiente virtuale .venv
nella stessa cartella, se possibile (vedi requirements.txt).

Esempi:
Apple Silicon: python3 -m venv .venv && .venv/bin/pip install mlx-whisper
Windows CPU: py -3 -m venv .venv && .venv\Scripts\pip install openai-whisper
Linux CPU: python3 -m venv .venv && .venv/bin/pip install openai-whisper

Per GPU NVIDIA/AMD ROCm e Intel leggi requirements.txt: occorrono
versioni adeguate di PyTorch o OpenVINO e driver compatibili.

Su macOS e Linux puo' essere necessario rendere eseguibile il launcher:
chmod +x Avvia_macOS.command Avvia_Linux.sh
Su Linux, se il doppio clic apre l'editor, seleziona 'Esegui come programma'
o avvialo dal terminale: ./Avvia_Linux.sh

Da terminale puoi passare opzioni al launcher, per esempio:
./Avvia_Linux.sh --force
./Avvia_macOS.command --language it
Avvia_Windows.bat --backend cpu

I launcher cercano prima Python nell'ambiente locale .venv e poi
l'installazione di Python del sistema.
