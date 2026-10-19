#!/usr/bin/env python3
"""Batch SRT/TXT transcription: MLX (Apple), PyTorch (CUDA/ROCm), OpenVINO (Intel), CPU."""
import argparse
import platform
import sys
from pathlib import Path

VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.m4v', '.wmv', '.flv', '.ts'}


def stamp(seconds):
    ms = max(0, round(float(seconds) * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def select_backend(requested):
    if requested != 'auto':
        return requested
    if platform.system() == 'Darwin' and platform.machine() == 'arm64':
        return 'mlx'
    try:
        import torch
        if torch.cuda.is_available():  # CUDA also covers ROCm builds
            return 'torch'
    except ImportError:
        pass
    try:
        import openvino as ov
        if 'GPU' in ov.Core().available_devices:
            return 'openvino'
    except (ImportError, RuntimeError):
        pass
    return 'cpu'


def transcribe_mlx(video, args):
    import mlx_whisper
    model = args.model or 'mlx-community/whisper-small'
    result = mlx_whisper.transcribe(str(video), path_or_hf_repo=model,
                                   language=args.language, task='transcribe',
                                   initial_prompt=args.prompt, verbose=False)
    return result['segments']


def transcribe_torch(video, args, device):
    import whisper
    model = whisper.load_model(args.model or 'small', device=device)
    result = model.transcribe(str(video), language=args.language,
                              initial_prompt=args.prompt, verbose=False,
                              fp16=(device == 'cuda'))
    return result['segments']


def transcribe_openvino(video, args):
    # Optimum Intel exports Whisper to OpenVINO; Transformers handles timestamps.
    from optimum.intel import OVModelForSpeechSeq2Seq
    from transformers import AutoProcessor, pipeline
    model_id = args.model or 'openai/whisper-small'
    model = OVModelForSpeechSeq2Seq.from_pretrained(model_id, export=True, device=args.ov_device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline('automatic-speech-recognition', model=model,
                    tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor)
    # Read audio using ffmpeg: mono, 16 kHz float32, avoiding optional audio dependencies.
    import subprocess
    import numpy as np
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-i', str(video), '-f', 'f32le',
               '-ac', '1', '-ar', '16000', '-']
    proc = subprocess.run(command, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors='replace'))
    audio = np.frombuffer(proc.stdout, dtype=np.float32)
    if not len(audio):
        raise ValueError('Audio vuoto')
    kwargs = {'language': args.language, 'task': 'transcribe'}
    if args.prompt:
        print('  Nota: --prompt non supportato dal backend OpenVINO: ignorato.')
    result = pipe({'array': audio, 'sampling_rate': 16000}, return_timestamps=True,
                  chunk_length_s=30, generate_kwargs=kwargs)
    return [{'start': x['timestamp'][0], 'end': x['timestamp'][1] or len(audio)/16000,
             'text': x['text']} for x in result['chunks']]


def write_outputs(segments, srt, txt, force):
    if force or not srt.exists():
        temp = srt.with_name(srt.name + '.tmp')
        with temp.open('w', encoding='utf-8') as f:
            for i, seg in enumerate((s for s in segments if s['text'].strip()), 1):
                f.write(f"{i}\n{stamp(seg['start'])} --> {stamp(seg['end'])}\n{seg['text'].strip()}\n\n")
        temp.replace(srt)
        print('  Salvato:', srt.name)
    if force or not txt.exists():
        temp = txt.with_name(txt.name + '.tmp')
        temp.write_text('\n'.join(s['text'].strip() for s in segments if s['text'].strip()) + '\n', encoding='utf-8')
        temp.replace(txt)
        print('  Salvato:', txt.name)


def main():
    parser = argparse.ArgumentParser(description='Trascrive video in SRT e TXT su macOS, Windows e Linux.')
    parser.add_argument('folder', nargs='?', default='.')
    parser.add_argument('--backend', choices=['auto', 'mlx', 'torch', 'openvino', 'cpu'], default='auto')
    parser.add_argument('--model', help='Modello: small (torch), repo Hugging Face (MLX/OpenVINO)')
    parser.add_argument('--language', default='en')
    parser.add_argument('--prompt', default=None)
    parser.add_argument('--ov-device', choices=['GPU', 'CPU', 'AUTO'], default='GPU')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        parser.error(f'Cartella inesistente: {folder}')
    videos = sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS),
                    key=lambda p: (p.name.casefold(), p.name))
    backend = select_backend(args.backend)
    print(f'Cartella: {folder}\nBackend: {backend}\nVideo trovati: {len(videos)}', flush=True)
    done = skipped = failed = 0
    for n, video in enumerate(videos, 1):
        srt, txt = video.with_suffix('.srt'), video.with_suffix('.txt')
        print(f'\n[{n}/{len(videos)}] {video.name}', flush=True)
        if not args.force and srt.exists() and txt.exists():
            print('  Già completato: salto.')
            skipped += 1
            continue
        try:
            if backend == 'mlx':
                segments = transcribe_mlx(video, args)
            elif backend == 'openvino':
                segments = transcribe_openvino(video, args)
            elif backend in ('torch', 'cpu'):
                if backend == 'torch':
                    import torch
                    if not torch.cuda.is_available():
                        raise RuntimeError('GPU CUDA/ROCm non rilevata da PyTorch.')
                segments = transcribe_torch(video, args, 'cuda' if backend == 'torch' else 'cpu')
            write_outputs(segments, srt, txt, args.force)
            done += 1
        except KeyboardInterrupt:
            print('\nInterrotto. I risultati precedenti sono conservati.')
            return 130
        except Exception as exc:
            print(f'  ERRORE ({type(exc).__name__}): {exc}', file=sys.stderr)
            failed += 1
    print(f'\nFinito: {done} elaborati, {skipped} saltati, {failed} errori.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
