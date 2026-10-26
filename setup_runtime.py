#!/usr/bin/env python3
"""Prepare dependencies inside the launcher's virtual environment."""
import importlib
from importlib import metadata
import os
from pathlib import Path
import shutil
import subprocess
import sys


def install_missing(packages):
    missing = []
    for distribution, requirement in packages:
        try:
            metadata.version(distribution)
        except metadata.PackageNotFoundError:
            missing.append(requirement)
    if missing:
        print('Installazione dipendenze: ' + ', '.join(missing), flush=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', *missing], check=True)
        importlib.invalidate_caches()


def prepare(args):
    if sys.prefix == sys.base_prefix:
        raise RuntimeError('La preparazione richiede un venv.')
    backend = args.backend
    if backend == 'auto':
        from subtitles import select_backend
        backend = select_backend('auto')
    if backend == 'mlx':
        packages = [('mlx-whisper', 'mlx-whisper')]
    elif backend == 'openvino':
        packages = [('optimum-intel', 'optimum[openvino]'),
                    ('openvino', 'openvino'), ('transformers', 'transformers'),
                    ('numpy', 'numpy')]
    else:
        packages = [('openai-whisper', 'openai-whisper')]
    install_missing(packages)

    # Whisper invokes the command "ffmpeg". Expose a private copy in the venv
    # when the user has no system installation; no administrator access needed.
    bin_dir = Path(sys.prefix) / ('Scripts' if os.name == 'nt' else 'bin')
    os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ.get('PATH', '')
    if not shutil.which('ffmpeg'):
        install_missing([('imageio-ffmpeg', 'imageio-ffmpeg')])
        import imageio_ffmpeg
        source = Path(imageio_ffmpeg.get_ffmpeg_exe())
        target = bin_dir / ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg')
        shutil.copy2(source, target)
        target.chmod(target.stat().st_mode | 0o111)
    subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def main():
    if sys.version_info < (3, 10):
        print('È necessario Python 3.10 o successivo.', file=sys.stderr)
        return 1
    from subtitles import main as transcribe
    try:
        return transcribe(prepare=prepare)
    except KeyboardInterrupt:
        print('\nPreparazione interrotta. Riapri il launcher per riprovare.')
        return 130
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'Preparazione non riuscita: {exc}\n'
              'Verifica la connessione e riapri il launcher per riprovare.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
