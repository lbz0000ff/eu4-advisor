"""Tests for the public repository setup entry point."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class SetupScriptTest(unittest.TestCase):
    def test_setup_uses_repository_root_without_running_pipeline(self) -> None:
        setup_path = ROOT / "scripts" / "setup.py"
        spec = importlib.util.spec_from_file_location("oiratrag_setup", setup_path)
        self.assertIsNotNone(spec)
        assert spec is not None
        self.assertIsNotNone(spec.loader)
        assert spec.loader is not None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertEqual(module.ROOT, ROOT)
        self.assertTrue(callable(module.main))

    @patch("subprocess.run")
    def test_setup_runs_complete_data_pipeline(self, run_mock) -> None:
        run_mock.return_value.stdout = "Oirat"
        setup_path = ROOT / "scripts" / "setup.py"
        spec = importlib.util.spec_from_file_location("oiratrag_setup_pipeline", setup_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module.main()

        commands = [call.args[0][1] for call in run_mock.call_args_list]
        self.assertEqual(
            commands,
            [
                "scripts/crawl_wiki.py",
                "src/markdown_normalizer.py",
                "src/chunk.py",
                "src/embed.py",
                "src/rag.py",
            ],
        )
