import argparse
from importlib import metadata
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import setup_runtime as setup
import subtitles


class SetupTests(unittest.TestCase):
    def test_installs_only_missing_packages_with_venv_python(self):
        with patch.object(metadata, 'version', side_effect=['1', metadata.PackageNotFoundError]), \
                patch.object(setup.subprocess, 'run') as run:
            setup.install_missing([('installed', 'installed'), ('missing', 'missing[extra]')])
        run.assert_called_once_with(
            [sys.executable, '-m', 'pip', 'install', 'missing[extra]'], check=True)

    def test_existing_dependencies_do_not_trigger_install(self):
        with patch.object(metadata, 'version', return_value='1'), \
                patch.object(setup.subprocess, 'run') as run:
            setup.install_missing([('installed', 'installed')])
        run.assert_not_called()

    def test_backend_packages(self):
        for backend, package in [('mlx', 'mlx-whisper'), ('cpu', 'openai-whisper'),
                                 ('torch', 'openai-whisper'), ('openvino', 'optimum[openvino]')]:
            with self.subTest(backend=backend), patch.object(sys, 'prefix', '/test-venv'), \
                    patch.object(setup, 'install_missing') as install, \
                    patch.object(setup.shutil, 'which', return_value='/usr/bin/ffmpeg'), \
                    patch.object(setup.subprocess, 'run'), patch.dict(setup.os.environ):
                setup.prepare(argparse.Namespace(backend=backend))
                self.assertIn(package, [req for _, req in install.call_args.args[0]])

    def test_missing_ffmpeg_is_copied_into_venv(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'bundled-ffmpeg'
            source.write_bytes(b'test binary')
            bin_dir = Path(tmp) / ('Scripts' if setup.os.name == 'nt' else 'bin')
            bin_dir.mkdir()
            module = Mock(get_ffmpeg_exe=Mock(return_value=str(source)))
            with patch.object(sys, 'prefix', tmp), patch.object(setup, 'install_missing') as install, \
                    patch.object(setup.shutil, 'which', return_value=None), \
                    patch.dict(sys.modules, {'imageio_ffmpeg': module}), \
                    patch.dict(setup.os.environ), patch.object(setup.subprocess, 'run'):
                setup.prepare(argparse.Namespace(backend='cpu'))
                target = bin_dir / ('ffmpeg.exe' if setup.os.name == 'nt' else 'ffmpeg')
                self.assertEqual(target.read_bytes(), b'test binary')
                self.assertEqual(setup.os.environ['PATH'].split(setup.os.pathsep)[0], str(bin_dir))
                self.assertEqual(install.call_count, 2)

    def test_global_python_is_rejected_before_installation(self):
        with patch.object(sys, 'prefix', sys.base_prefix), \
                patch.object(setup, 'install_missing') as install:
            with self.assertRaises(RuntimeError):
                setup.prepare(argparse.Namespace(backend='cpu'))
            install.assert_not_called()

    def test_config_exists_before_preparation(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / 'config.json'
            def prepare(args):
                self.assertTrue(config_path.exists())
                self.assertEqual(args.model, 'turbo')
                self.assertEqual(args.language, 'en')
            with patch.object(sys, 'prefix', tmp), patch.object(subtitles, 'CONFIG_PATH', config_path), \
                    patch.object(sys, 'argv', ['subtitles.py', tmp, '--backend', 'cpu']), \
                    patch.object(sys.stdin, 'isatty', return_value=False):
                self.assertEqual(subtitles.main(prepare=prepare), 0)

    def test_failed_installation_stops_startup(self):
        with patch.object(sys, 'version_info', (3, 10)), \
                patch.object(subtitles, 'main', side_effect=setup.subprocess.CalledProcessError(1, 'pip')):
            self.assertEqual(setup.main(), 1)


if __name__ == '__main__':
    unittest.main()
