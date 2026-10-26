# Whisper – Fischio per gli amici

Trascrive i video in ordine alfabetico in **SRT** e **TXT**, saltando quelli già completati. Lingua predefinita: **inglese**. Modello predefinito: **turbo**.

## Come lo uso?

1. Clicca **Code → Download ZIP** ed estrai la cartella dove vuoi.
2. Metti i video dentro questa cartella.
3. Con **Python 3.10+** installato, apri il launcher del tuo sistema:

| Windows | macOS | Linux |
|---|---|---|
| `Avvia_Windows.bat` | `Avvia_macOS.command` | `Avvia_Linux.sh` |

Modifica `config.json` per cambiare modello (`tiny`, `base`, `small`, `medium`, `large`, `turbo`), lingua o backend. Opzioni temporanee dei launcher: `--model small`, `--backend cpu`, `--force` per rigenerare i risultati. Al primo avvio `--model` salva direttamente la scelta; senza terminale interattivo viene usato `turbo`.

Su macOS/Linux, se necessario: `chmod +x Avvia_macOS.command Avvia_Linux.sh`. Su Linux deve essere disponibile il modulo `venv` di Python (su Debian/Ubuntu: pacchetto `python3-venv`). Se un download fallisce, riapri il launcher per riprovare.
