# Whisper – Fischio per gli amici

Trascrive i video in ordine alfabetico in **SRT** e **TXT**, saltando quelli già completati. Lingua predefinita: **inglese**. Modello predefinito: **turbo**.

1. Scarica **Code → Download ZIP** ed estrai la cartella **dove vuoi**.
2. **Metti i video dentro questa cartella, accanto a `subtitles.py`**, non nelle sottocartelle.
3. Con **Python 3.10+** installato, apri il launcher del tuo sistema:

| Windows | macOS | Linux |
|---|---|---|
| `Avvia_Windows.bat` | `Avvia_macOS.command` | `Avvia_Linux.sh` |

**Il launcher prepara tutto:** crea il venv obbligatorio `.venv`, chiede il modello (**Invio = turbo**), salva `config.json`, installa il backend e, se manca, una copia locale di FFmpeg. Poi scarica il modello e trascrive. Serve Internet per la prima preparazione; gli avvii successivi riutilizzano quanto installato.

Su Mac Apple Silicon usa MLX; sugli altri sistemi installa Whisper/PyTorch, usando la GPU se disponibile oppure la CPU. Driver GPU e build specifiche CUDA/ROCm possono richiedere una configurazione dedicata. Per Intel puoi scegliere `openvino` nel config o con `--backend openvino`: il launcher ne installa le dipendenze.

Modifica `config.json` per cambiare modello (`tiny`, `base`, `small`, `medium`, `large`, `turbo`), lingua o backend. Opzioni temporanee dei launcher: `--model small`, `--backend cpu`, `--force` per rigenerare i risultati. Al primo avvio `--model` salva direttamente la scelta; senza terminale interattivo viene usato `turbo`.

Su macOS/Linux, se necessario: `chmod +x Avvia_macOS.command Avvia_Linux.sh`. Su Linux deve essere disponibile il modulo `venv` di Python (su Debian/Ubuntu: pacchetto `python3-venv`). Se un download fallisce, riapri il launcher per riprovare.
