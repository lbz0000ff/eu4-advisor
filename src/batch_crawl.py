"""
EU4 Wiki 批量爬取工具集

设计原则：
  Agent 做决策，规则做执行。本模块只提供工具函数，BFS 策略由 Agent 自行编排。

用法 (Agent 调用):
  from batch_crawl import discover_countries, discover_event_pages, batch_crawl, print_report
  candidates = discover_countries(threshold=5000)
  result = batch_crawl([c["title"] for c in candidates], "../data/raw/countries")
  print_report(result)
"""

import json
import os
import re
import sys
import time

from eu4_crawler import get_page_text, get_category_pages, scraper

RATE_LIMIT = 0.5  # API 请求间隔（秒）

# 非国家页面过滤
COUNTRY_SKIP_PATTERNS = re.compile(
    r"(region|super.?region|subcontinent|continent|area|zone|mechanic|countries|formable)", re.I
)
COUNTRY_SKIP_PREFIXES = ("User:", "Template:", "Category:", "File:", "Talk:")

# ---------------------------------------------------------------------------
# 发现阶段
# ---------------------------------------------------------------------------

def get_pages_info(titles, batch_size=50):
    """批量获取页面元信息 (length, redirect, touched)"""
    results = {}
    for i in range(0, len(titles), batch_size):
        batch = titles[i:i + batch_size]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "info",
            "format": "json",
        }
        resp = scraper.get(
            "https://eu4.paradoxwikis.com/api.php", params=params, timeout=15
        )
        data = resp.json()
        for pid, pg in data["query"]["pages"].items():
            if "missing" not in pg:
                results[pg["title"]] = pg
        time.sleep(RATE_LIMIT)
    return results


def discover_countries(threshold=5000):
    """获取所有国家页，过滤并评分"""
    print("[discover] 获取 Countries 分类成员...")
    titles = get_category_pages("Countries")
    print(f"[discover] 共 {len(titles)} 个候选页，获取元信息...")

    info = get_pages_info(titles)

    candidates = []
    for title, pg in info.items():
        if "redirect" in pg:
            continue
        # 过滤非国家页面
        if COUNTRY_SKIP_PREFIXES and title.startswith(COUNTRY_SKIP_PREFIXES):
            continue
        if "/" in title:  # 子页面 / Mod 页（如 "Code Geass/Holy Britannian Empire"）
            continue
        if COUNTRY_SKIP_PATTERNS.search(title):
            continue

        length = pg.get("length", 0)
        if length < threshold:
            continue

        # 评分信号：页面长度
        score = min(length / 500, 20)  # 最长 10KB → 20 分, 之后不再增加
        candidates.append({
            "title": title,
            "length": length,
            "score": round(score, 1),
            "pageid": pg.get("pageid"),
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    print(f"[discover] 达标 (>{threshold}KB): {len(candidates)} 个国家")
    return candidates


def discover_event_pages():
    """从 List of event lists 获取所有事件页名"""
    print("[discover] 解析 List of event lists...")
    text = get_page_text("List of event lists")
    if not text:
        print("[discover]  WARNING: 无法获取 List of event lists")
        return []

    # 提取所有 [[Page Name]] 形式的链接（事件页）
    import re
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', text)
    # 过滤出看起来像事件页的（包含 "events" 或 "Events"）
    event_pages = sorted(set(
        l for l in links if "event" in l.lower() and ":" not in l
    ))
    print(f"[discover] 找到 {len(event_pages)} 个事件页引用")
    return event_pages


# ---------------------------------------------------------------------------
# 爬取阶段
# ---------------------------------------------------------------------------

def _safe(text):
    """替换不可打印字符，避免 GBK 编码崩溃"""
    if isinstance(text, str):
        return text.encode("utf-8", errors="replace").decode("utf-8")
    return text


def batch_crawl(titles, output_dir, label="pages", delay=RATE_LIMIT):
    """批量爬取页面并保存为 .md 文件"""
    os.makedirs(output_dir, exist_ok=True)

    results = {"succeeded": [], "failed": [], "skipped": []}
    total = len(titles)

    for idx, title in enumerate(titles, 1):
        safe_name = title.replace("/", "_").replace(" ", "_")
        safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in safe_name)
        filepath = os.path.join(output_dir, f"{safe_name}.md")

        if os.path.exists(filepath):
            results["skipped"].append(title)
            if idx <= 1 or idx % 20 == 0:
                print(f"  [{idx}/{total}] SKIP ({len(results['succeeded'])} so far)")
            continue

        content = get_page_text(title)
        if content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            results["succeeded"].append(title)
        else:
            results["failed"].append(title)

        if (idx) % 10 == 0 or idx == total:
            ok = len(results["succeeded"])
            fail = len(results["failed"])
            print(f"  [{idx}/{total}] ... {ok} OK, {fail} FAIL")

        time.sleep(delay + (1 if len(results["failed"]) > 0 else 0))  # 失败后加长延迟

    # 更新爬取清单
    _update_index(output_dir, results)
    return results


def _update_index(output_dir, results):
    """更新 output_dir 下的 _index.json 爬取清单（紧凑格式）"""
    index_path = os.path.join(output_dir, "_index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {"pages": 0, "crawled": 0, "failed": 0, "last_crawl": None}

    index["crawled"] += len(results["succeeded"])
    index["failed"] += len(results["failed"])
    index["pages"] = index["crawled"] + index["failed"]
    index["last_crawl"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------

def print_report(results):
    """打印爬取报告"""
    total = len(results["succeeded"]) + len(results["failed"]) + len(results["skipped"])
    ok = len(results["succeeded"])
    fail = len(results["failed"])
    skip = len(results["skipped"])

    print(f"\n{'='*50}")
    print(f"爬取完成: {total} 个页面")
    print(f"  ✅ 成功: {ok}")
    print(f"  ⏭️  跳过: {skip}（已存在）")
    print(f"  ❌ 失败: {fail}")
    if fail:
        print(f"  失败列表: {', '.join(results['failed'])}")
    print(f"{'='*50}")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# CLI 入口 — Agent 通过 cmd_execute 调用
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="EU4 Wiki 爬取工具集")
    sub = parser.add_subparsers(dest="command")

    # discover-countries
    dc = sub.add_parser("discover-countries", help="发现国家页候选")
    dc.add_argument("--threshold", type=int, default=5000, help="页面长度阈值（字节）")
    dc.add_argument("--json", action="store_true", help="输出 JSON 供 Agent 解析")

    # discover-events
    sub.add_parser("discover-events", help="发现事件页候选")

    # crawl
    cr = sub.add_parser("crawl", help="批量爬取页面")
    cr.add_argument("titles", nargs="+", help="要爬取的页面标题")
    cr.add_argument("--output", "-o", default=".", help="输出目录")
    cr.add_argument("--label", default="pages", help="日志标签")

    # crawl-file (从文件读标题列表)
    cf = sub.add_parser("crawl-file", help="从文件读取标题列表并爬取")
    cf.add_argument("file", help="标题列表文件（每行一个标题）")
    cf.add_argument("--output", "-o", default=".", help="输出目录")
    cf.add_argument("--label", default="pages", help="日志标签")

    # status
    st = sub.add_parser("status", help="查看爬取状态")
    st.add_argument("dirs", nargs="+", help="要查看的 output_dir")

    args = parser.parse_args()

    if args.command == "discover-countries":
        candidates = discover_countries(threshold=args.threshold)
        if args.json:
            print(json.dumps(candidates, ensure_ascii=False))
        else:
            print(f"\n共 {len(candidates)} 个候选国家:")
            for c in candidates[:20]:
                print(f"  {c['title']:30s} {c['length']:>6}B  score={c['score']}")
            if len(candidates) > 20:
                print(f"  ... 还有 {len(candidates)-20} 个")

    elif args.command == "discover-events":
        pages = discover_event_pages()
        print(f"\n共 {len(pages)} 个事件页面:")
        for p in pages:
            print(f"  {p}")

    elif args.command == "crawl":
        results = batch_crawl(args.titles, args.output, label=args.label)
        print_report(results)

    elif args.command == "crawl-file":
        with open(args.file, "r", encoding="utf-8") as f:
            titles = [line.strip() for line in f if line.strip()]
        print(f"从 {args.file} 读取了 {len(titles)} 个标题")
        results = batch_crawl(titles, args.output, label=args.label)
        print_report(results)

    elif args.command == "status":
        for d in args.dirs:
            ipath = os.path.join(d, "_index.json")
            if os.path.exists(ipath):
                with open(ipath, "r", encoding="utf-8") as f:
                    idx = json.load(f)
                print(f"{d}: {idx}")
            else:
                print(f"{d}: (无 _index.json)")


if __name__ == "__main__":
    main()
