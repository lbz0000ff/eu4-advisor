"""Tests for the public repository setup entry point."""

import importlib.util
import unittest
from pathlib import Path


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
