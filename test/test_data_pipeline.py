"""Tests for the reproducible Wiki data pipeline paths."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NormalizerPathTest(unittest.TestCase):
    def test_normalizer_connects_raw_data_to_data_normalized(self) -> None:
        module = load_module(
            "oiratrag_markdown_normalizer",
            ROOT / "src" / "markdown_normalizer.py",
        )

        self.assertEqual(module.DATA_DIR, ROOT / "data" / "raw_data")
        self.assertEqual(module.OUT_DIR, ROOT / "data" / "data_normalized")


class CrawlerPathTest(unittest.TestCase):
    def test_crawler_writes_to_repository_raw_data_directory(self) -> None:
        crawler_path = ROOT / "scripts" / "crawl_wiki.py"
        self.assertTrue(crawler_path.exists(), "scripts/crawl_wiki.py is missing")
        crawler_module = types.ModuleType("eu4_crawler")
        crawler_module.get_category_pages = lambda category: []
        crawler_module.get_page_text = lambda title: None
        crawler_module.scraper = None
        batch_module = types.ModuleType("batch_crawl")
        batch_module.batch_crawl = lambda *args, **kwargs: {}
        batch_module.print_report = lambda result: None
        with patch.dict(
            sys.modules,
            {"eu4_crawler": crawler_module, "batch_crawl": batch_module},
        ):
            module = load_module("oiratrag_crawl_wiki", crawler_path)

        self.assertEqual(module.OUTPUT, ROOT / "data" / "raw_data")
