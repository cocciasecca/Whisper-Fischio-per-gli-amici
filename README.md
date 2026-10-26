# Whisper – Fischio per gli amici

Trascrive i video in ordine alfabetico e crea file **SRT** e **TXT**, saltando quelli già completati. Lingua predefinita: **inglese**. Modello predefinito: **turbo**.

Scarica la repository da **Code → Download ZIP** ed estraila **dove vuoi**. **I video vanno dentro la cartella del programma, accanto a `subtitles.py`**, non nelle sottocartelle.

1. Installa **Python 3.10+** e **FFmpeg**, disponibili nel `PATH`.
2. Apri il launcher del tuo sistema: `Avvia_Windows.bat`, `Avvia_macOS.command` o `Avvia_Linux.sh`. Crea automaticamente il **venv obbligatorio** `.venv`, poi al primo avvio chiede il modello (**Invio = turbo**) e crea `config.json` con lingua `en`. Senza terminale interattivo usa `turbo`.
3. Installa il backend nella `.venv` (vedi sotto), poi riapri il launcher.

Su macOS/Linux, se necessario: `chmod +x Avvia_macOS.command Avvia_Linux.sh`.

Installa **solo il backend adatto**, dal terminale nella cartella del programma. Usa `.venv/bin/python -m pip install …` su macOS/Linux oppure `.venv\Scripts\python.exe -m pip install …` su Windows:

| Hardware | Pacchetto da installare |
|---|---|
| Mac Apple Silicon | `mlx-whisper` |
| CPU | `openai-whisper` |
| NVIDIA / AMD | Prima PyTorch compatibile con CUDA / ROCm, poi `openai-whisper` |
| Intel GPU | `"optimum[openvino]" transformers numpy` |

Il backend viene scelto automaticamente; l'accelerazione richiede driver e dipendenze compatibili. Il modello viene scaricato al primo utilizzo.

Modifica `config.json` per cambiare modello (`tiny`, `base`, `small`, `medium`, `large`, `turbo`), lingua o backend. I launcher accettano anche opzioni temporanee, per esempio `--model small`, `--backend cpu` e `--force` per rigenerare i risultati. `--model` al primo avvio salva la scelta senza mostrarne la richiesta. Per MLX/OpenVINO puoi indicare un repository Hugging Face compatibile.
