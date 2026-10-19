# Whisper Subtitles

Trascrive i video di una cartella in **ordine alfabetico**, creando per ciascuno un file **`.srt`** (sottotitoli) e **`.txt`** (testo). Usa **Whisper Small**, lingua **inglese** e salta i video già elaborati.

## Avvio

Metti i video nella cartella del programma, poi apri:

| Sistema | File |
|---|---|
| macOS | `Avvia_macOS.command` |
| Windows | `Avvia_Windows.bat` |
| Linux | `Avvia_Linux.sh` |

Richiede **Python 3** e **FFmpeg** nel `PATH`, più il backend installato (vedi sotto). Su macOS/Linux, se necessario: `chmod +x Avvia_macOS.command Avvia_Linux.sh`.

## Installazione backend

Consigliato un ambiente virtuale `.venv` nella cartella del programma. Installa **solo** il backend adatto alla tua macchina:

| Hardware | Backend | Installazione |
|---|---|---|
| Mac Apple Silicon | MLX / Metal | `pip install mlx-whisper` |
| NVIDIA (Windows/Linux) | PyTorch CUDA | PyTorch CUDA da [pytorch.org](https://pytorch.org/get-started/locally/) + `pip install openai-whisper` |
| AMD compatibile (Linux; Windows limitato) | PyTorch ROCm | PyTorch ROCm compatibile + `pip install openai-whisper` |
| Intel GPU (Windows/Linux) | OpenVINO | `pip install "optimum[openvino]" transformers numpy` |
| CPU | Whisper | `pip install openai-whisper` |

**GPU non garantita:** servono driver e versioni compatibili. `--backend auto` seleziona MLX, CUDA/ROCm o OpenVINO quando disponibili; altrimenti usa CPU.

## Opzioni

Da terminale, nella cartella del programma:

```bash
python subtitles.py                        # avvio automatico
python subtitles.py --language it          # lingua italiana
python subtitles.py --force                # rigenera i file esistenti
python subtitles.py --backend openvino     # Intel GPU
python subtitles.py --backend torch        # NVIDIA/AMD ROCm
python subtitles.py --backend cpu          # forza CPU
python subtitles.py "/percorso/ai/video"   # cartella diversa
```

I launcher accettano le stesse opzioni (es. `./Avvia_Linux.sh --force`). Per OpenVINO: `--ov-device GPU` (predefinito), `CPU` o `AUTO`.

> Al primo avvio il modello viene scaricato da Internet. Le trascrizioni successive possono essere eseguite offline con modello e dipendenze già disponibili.
