"""EU4 Wiki BFS 爬取入口。

Layer 1 获取国家页和游戏概念分类页，Layer 2 根据国家页中的
``Main:`` 引用继续获取任务树和事件页。输出写入 ``data/raw_data``。
"""

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from eu4_crawler import get_category_pages, get_page_text, scraper
from batch_crawl import batch_crawl, print_report

OUTPUT = ROOT / "data" / "raw_data"
RATE = 0.5  # 礼貌延迟

def info(msg):
    print(f"[INFO] {msg}", flush=True)

def main():
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # ──── Layer 1: 发现候选 ────
    info("=== Phase 1: 发现所有分类的候选页面 ===")

    # 国家页：用 discover_countries 的逻辑（阈值 5000）
    info("获取 Countries 分类...")
    all_country_titles = get_category_pages("Countries")
    # 过滤：非重定向、非噪声、长度 >= 5000
    info(f"  Countries 分类共 {len(all_country_titles)} 个候选，过滤中...")

    # 批量获取元信息来过滤
    country_titles = []
    batch_size = 50
    for i in range(0, len(all_country_titles), batch_size):
        batch = all_country_titles[i:i+batch_size]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "info",
            "format": "json",
        }
        resp = scraper.get("https://eu4.paradoxwikis.com/api.php", params=params, timeout=15)
        data = resp.json()
        for pid, pg in data["query"]["pages"].items():
            if "missing" in pg or "redirect" in pg:
                continue
            t = pg["title"]
            # 过滤噪声
            if t.startswith(("User:", "Template:", "Category:", "File:", "Talk:")):
                continue
            if "/" in t:
                continue
            if re.search(r"(region|super.?region|subcontinent|continent|area|zone|mechanic|countries|formable)", t, re.I):
                continue
            length = pg.get("length", 0)
            if length < 5000:
                continue
            country_titles.append(t)
        time.sleep(RATE)

    info(f"  有效国家页: {len(country_titles)} 个")

    # 其他游戏概念分类（批量获取页面名）
    categories = {
        "diplomacy": "Diplomacy",
        "economy": "Economy",
        "military": "Military",
        "government": "Estates",
    }
    # 额外分类：用 API 直接拿
    extra_categories = {
        "disasters": "Disasters",
        "decisions": "Decisions",
    }

    cat_pages = {}
    for folder, cat_name in {**categories, **extra_categories}.items():
        titles = get_category_pages(cat_name)
        # 过滤噪声
        clean = [t for t in titles if not t.startswith(("User:", "Template:", "Category:", "File:", "Talk:", "Category talk:"))]
        cat_pages[folder] = clean
        info(f"  {folder} ({cat_name}): {len(clean)} 页")

    # 指定页面（旧 CRAWL_PLAN 中非分类覆盖的）
    specific_pages = {
        "government": [
            "Absolutism", "Ages", "Government", "Great_power", "Great_project",
            "Modifiers", "Prestige", "Stability", "Corruption",
            "Overextension", "War_exhaustion",
            "Monarch_power", "Ruler",
            "Personalities", "Monarchy", "Republic", "Theocracy", "Steppe_hordes",
            "Pirate_republic", "Factions",
            "Common_government_reforms", "Parliament",
            "Advisor", "Army", "Idea_groups", "National_ideas", "Group_national_ideas",
            "Government_reforms",
        ],
        "religion": [
            "Religions", "Catholic", "Confucian", "Protestant", "Reformed",
            "Orthodox", "Sunni", "Shia", "Hindu", "Muslim", "Buddhist",
            "Animist", "Shinto", "Sikh", "Nahuatl", "Inti", "Totemist",
        ],
        "tech_ideas": [
            "Technology", "Ideas", "Institutions", "Westernization",
        ],
        "dlc": [
            "Domination", "Emperor", "Res_Publica", "Rule_Britannia",
            "Art_of_War", "Common_Sense", "Mandate_of_Heaven",
            "Cradle_of_Civilization", "Dharma", "Golden_Century",
            "Leviathan", "Lions_of_the_North", "King_of_Kings",
            "Origins", "Winds_of_Change",
        ],
        "misc": [
            "Achievements", "Innovativeness", "Ironman", "Jargon",
            "Map", "Multiplayer", "Nation_designer",
            "Native_tribe", "Primitive", "Province_interface",
            "Random_nations", "Random_New_World",
            "Scenarios", "Score_system", "Emperor_of_China",
            "Trade", "Trade_goods", "Center_of_trade",
            "Development", "Buildings", "Terrain",
        ],
    }

    # province_mechanics 也归入 government
    province_pages = get_category_pages("Province_mechanics")
    province_pages = [t for t in province_pages if not t.startswith(("User:", "Template:", "Category:", "File:", "Talk:"))]
    specific_pages["government"].extend(province_pages)
    info(f"  government (Province_mechanics): {len(province_pages)} 页补充")

    # Regions 分类归入 misc
    region_pages = get_category_pages("Regions")
    region_pages = [t for t in region_pages if not t.startswith(("User:", "Template:", "Category:", "File:", "Talk:"))]
    specific_pages["misc"].extend(region_pages)
    info(f"  misc (Regions): {len(region_pages)} 页补充")

    # ──── Phase 2: 分层爬取 ────
    info("\n=== Phase 2: 开始爬取 ===")

    # 2a. 国家页（Layer 1）
    info("\n--- Layer 1: 爬取国家页 ---")
    result = batch_crawl(country_titles, os.path.join(OUTPUT, "countries"), label="countries", delay=RATE)
    print_report(result)

    # 2b. 从国家页提取 Main: 引用（Layer 2）
    info("\n--- 提取 Main: 引用（BFS 发现） ---")
    countries_dir = os.path.join(OUTPUT, "countries")
    missions_to_crawl = set()
    events_to_crawl = set()

    for fname in os.listdir(countries_dir):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(countries_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue
        for m in re.finditer(r"^Main:\s*(.+)$", content, re.MULTILINE):
            ref = m.group(1).strip()
            ref = ref.split("#")[0]  # 去掉锚点（如 "Ashikaga#Strategy" → "Ashikaga"）
            ref = ref.strip()
            if not ref:
                continue
            if "mission" in ref.lower():
                missions_to_crawl.add(ref)
            elif "event" in ref.lower():
                events_to_crawl.add(ref)

    info(f"  发现任务树引用: {len(missions_to_crawl)} 个")
    info(f"  发现事件引用: {len(events_to_crawl)} 个")
    if missions_to_crawl:
        for m in sorted(missions_to_crawl):
            info(f"    - {m}")
    if events_to_crawl:
        for e in sorted(events_to_crawl):
            info(f"    - {e}")

    # 2c. 爬取任务树（Layer 2）
    if missions_to_crawl:
        info("\n--- Layer 2: 爬取任务树 ---")
        result = batch_crawl(sorted(missions_to_crawl), os.path.join(OUTPUT, "missions"), label="missions", delay=RATE)
        print_report(result)

    if events_to_crawl:
        info("\n--- Layer 2: 爬取事件 ---")
        result = batch_crawl(sorted(events_to_crawl), os.path.join(OUTPUT, "events"), label="events", delay=RATE)
        print_report(result)

    # 2d. 其他分类
    for folder, titles in cat_pages.items():
        if not titles:
            continue
        info(f"\n--- 爬取 {folder} ---")
        result = batch_crawl(titles, os.path.join(OUTPUT, folder), label=folder, delay=RATE)
        print_report(result)

    # 2e. 指定页面
    for folder, titles in specific_pages.items():
        if not titles:
            continue
        info(f"\n--- 爬取 {folder} (指定页面) ---")
        result = batch_crawl(titles, os.path.join(OUTPUT, folder), label=f"{folder}_specific", delay=RATE)
        print_report(result)

    # ──── 最终报告 ────
    info("\n" + "="*60)
    info("全量爬取完成！各目录状态：")
    for folder in sorted(os.listdir(OUTPUT)):
        fpath = os.path.join(OUTPUT, folder)
        if os.path.isdir(fpath):
            idx_path = os.path.join(fpath, "_index.json")
            if os.path.exists(idx_path):
                with open(idx_path, "r") as f:
                    idx = json.load(f)
                info(f"  {folder}: {idx}")
            else:
                count = len([x for x in os.listdir(fpath) if x.endswith(".md")])
                info(f"  {folder}: {count} 页 (无 _index)")

if __name__ == "__main__":
    main()
