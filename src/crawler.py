"""Wiki 爬虫 v2 - 按 EU4 Wiki 官方分类结构爬取，保存到对应文件夹

策略:
  1. 从 Game_concepts 分类入口
  2. 遍历子分类（Diplomacy、Military...）爬全部页面
  3. Realm 分类下的子分类（Economy、Estates、Province mechanics）分别归入对应文件夹
  4. 国家只爬精选列表（约 55 个热门/可成立大国）
  5. DLC 和杂项独立处理
  6. 跳过 User 页、编辑页、沙盒页等垃圾
"""

import re
import time
import json
from pathlib import Path
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup


BASE_URL = "https://eu4.paradoxwikis.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"

# ──── 全局会话（复用连接 + 绕过 Cloudflare） ────
_scraper = None
def get_scraper():
    global _scraper
    if _scraper is None:
        _scraper = cloudscraper.create_scraper()
    return _scraper


# ──── 热门国家精选列表（约 55 个） ────
POPULAR_COUNTRIES = [
    # 欧洲 major
    "Ottomans", "France", "Castile", "Spain", "England", "Great_Britain",
    "Austria", "Brandenburg", "Prussia", "Germany",
    "Muscovy", "Russia", "Poland", "Commonwealth",
    "Portugal", "Sweden", "Denmark", "Norway", "Netherlands",
    "Burgundy", "Bavaria", "Bohemia", "Hungary",
    "Byzantium", "Venice", "Genoa", "Papal_States",
    "Milan", "Florence", "Savoy", "Aragon", "Naples",
    "Scotland", "Switzerland",
    "Teutonic_Order", "Livonian_Order", "Riga",
    "Serbia", "Bosnia", "Wallachia", "Moldavia",
    "Novgorod", "Crimea", "Great_Horde", "Golden_Horde",
    # 亚洲 major
    "Ming", "Japan", "Korea", "Oirat", "Timurids", "Mughals", "Manchu",
    "Ayutthaya", "Dai_Viet", "Vijayanagar", "Bahmanis", "Bengal", "Delhi",
    "Kazan", "Qing",
    # 非洲 major
    "Morocco", "Tunis", "Ethiopia", "Mali", "Songhai", "Kongo",
    # 美洲 major
    "Aztec", "Inca", "Huron",
    # 其他
    "Angevin_Kingdom", "Ireland", "Greece", "Italy", "Roman_Empire",
    "Scandinavia", "USA", "Mongol_Empire", "Yuan",
]

# ──── 爬取计划 ────
# folder: 保存的子目录名
# type: "category" → 遍历 Wiki 分类爬全部页面
#       "pages"   → 直接爬指定页面列表
CRAWL_PLAN = [
    # 外交
    {"folder": "diplomacy",  "type": "category", "wiki_cat": "Diplomacy"},

    # 军事
    {"folder": "military",   "type": "category", "wiki_cat": "Military"},

    # 经济（Realm 的子分类）
    {"folder": "economy",    "type": "category", "wiki_cat": "Economy"},

    # 政府管理（Realm 的子分类）
    {"folder": "government", "type": "category", "wiki_cat": "Estates"},
    {"folder": "government", "type": "category", "wiki_cat": "Province_mechanics"},
    # Realm 独立页面中与政府相关的
    {"folder": "government", "type": "pages", "pages": [
        "Absolutism", "Ages", "Government",
        "Great_power", "Great_project",
        "Modifiers", "Prestige", "Stability", "Corruption",
        "Overextension", "War_exhaustion",
        "Monarch_power", "Ruler", "List_of_rulers",
        "Personalities",
        "Monarchy", "Republic", "Theocracy", "Steppe_hordes",
        "Pirate_republic", "Factions",
        "Common_government_reforms", "Parliament",
        "Advisor", "Army",
        "Idea_groups", "National_ideas", "Group_national_ideas",
    ]},

    # 宗教
    {"folder": "religion", "type": "pages", "pages": [
        "Religions", "Catholic", "Confucian",
    ]},

    # 科技/理念
    {"folder": "tech_ideas", "type": "pages", "pages": [
        "Technology", "Ideas", "Institutions", "Westernization",
    ]},

    # 国家
    {"folder": "countries", "type": "pages", "pages": POPULAR_COUNTRIES},

    # DLC
    {"folder": "dlc", "type": "pages", "pages": [
        "Domination", "Emperor", "Res_Publica", "Rule_Britannia",
    ]},

    # 杂项（Game concepts 独立页 + Decisions + Regions）
    {"folder": "misc", "type": "category", "wiki_cat": "Decisions"},
    {"folder": "misc", "type": "category", "wiki_cat": "Regions"},
    {"folder": "misc", "type": "pages", "pages": [
        "Achievements", "Innovativeness", "Ironman", "Jargon",
        "Map", "Multiplayer", "Nation_designer",
        "Native_tribe", "Primitive", "Province_interface",
        "Random_nations", "Random_New_World",
        "Scenarios", "Score_system", "Emperor_of_China",
    ]},
]

# ──── 需要跳过的不干净页面模式 ────
SKIP_PATTERNS = [
    "index_php",       # 爬虫误爬的编辑页面
    "User:", "user:",  # 用户页面
    "Sandbox",         # 沙盒页面
    "Special:",        # 特殊页面
    "Template:",       # 模板
    "Help:",           # 帮助页
    "File:",           # 文件页
    "Wikipedia:",      # 跨维基
    "Category:",       # 分类页本身
]


# ═══════════ 网络功能 ═══════════

def fetch_page(url: str) -> str:
    """获取页面 HTML"""
    scraper = get_scraper()
    resp = scraper.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    if "Please enable JavaScript" in resp.text[:500]:
        raise RuntimeError(f"Cloudflare 拦截: {url}")
    return resp.text


def is_clean_page(page_name: str) -> bool:
    """判断是否为干净的 Wiki 内容页面（跳过垃圾）"""
    for pat in SKIP_PATTERNS:
        if pat in page_name:
            return False
    return True


def url_to_page_name(url: str) -> str:
    """从 URL 提取页面名"""
    name = url.replace(BASE_URL, "").strip("/")
    return name


# ═══════════ 分类页面遍历 ═══════════

def get_pages_in_category(category_name: str) -> list[str]:
    """获取某个 Wiki 分类下的所有页面链接"""
    cat_url = f"{BASE_URL}/Category:{category_name}"
    print(f"  遍历分类: {category_name}")
    html = fetch_page(cat_url)
    soup = BeautifulSoup(html, "html.parser")

    pages = []
    # 分类页面的链接在 #mw-pages 或 .mw-content-text 下
    for a in soup.select("#mw-pages a[href], .mw-content-text a[href]"):
        href = a.get("href", "")
        # 只保留页面链接（排除分类内链接和特殊链接）
        if not href.startswith("/"):
            continue
        page_name = href.strip("/")
        # 排除分类自身的递归链接
        if page_name.startswith("Category:"):
            continue
        # 检查是否为干净的页面
        if is_clean_page(page_name):
            pages.append(page_name)

    # 去重
    pages = list(set(pages))
    print(f"    发现 {len(pages)} 个有效页面")

    # 检查是否有分页
    # MediaWiki 分类页可能有多页，检查 "next page" 链接
    next_link = soup.select_one("a:contains('next page'), a:contains('next 200')")
    if next_link:
        next_url = urljoin(cat_url, next_link["href"])
        print(f"    有下一页，递归获取...")
        more_pages = get_pages_in_category(category_name)  # 简单递归
        # 实际上这个递归不对，因为 URL 变了但 category name 没变
        # 等我处理下...

    return pages


def get_all_pages_in_category(category_name: str) -> list[str]:
    """获取分类下所有页面（处理分页）"""
    all_pages = []
    seen = set()
    next_url = f"{BASE_URL}/Category:{category_name}"

    while next_url:
        print(f"  分类: {category_name} (页面: {next_url.split('?')[-1] if '?' in next_url else '第1页'})")
        try:
            html = fetch_page(next_url)
        except Exception as e:
            print(f"    ❌ 获取失败: {e}")
            break

        soup = BeautifulSoup(html, "html.parser")

        # 提取当前页的链接
        for a in soup.select("#mw-pages a[href], .mw-content-text a[href]"):
            href = a.get("href", "")
            if not href.startswith("/"):
                continue
            page_name = href.strip("/")
            if page_name.startswith("Category:"):
                continue
            if page_name in seen:
                continue
            if is_clean_page(page_name):
                seen.add(page_name)
                all_pages.append(page_name)

        # 找下一页
        next_link = soup.select_one("a:contains('next page'), a:contains('next 200')")
        if next_link and next_link.get("href"):
            next_url = urljoin(BASE_URL, next_link["href"])
        else:
            next_url = None

    print(f"    共 {len(all_pages)} 个页面")
    return all_pages


# ═══════════ 页面抓取与保存 ═══════════

def fetch_wiki_page(page_name: str) -> tuple[str, str]:
    """获取 Wiki 页面内容，返回 (markdown_text, title)"""
    # 对特殊字符进行编码
    from urllib.parse import quote
    encoded_name = quote(page_name, safe="/")
    url = f"{BASE_URL}/{encoded_name}"
    html = fetch_page(url)
    title = _extract_title(html)
    text = _html_to_markdown(html, url)
    return text, title


def _extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.select_one("h1#firstHeading, .firstHeading h1")
    return h1.get_text(strip=True) if h1 else page_name


def _html_to_markdown(html: str, page_url: str = "") -> str:
    """将 Wiki 页面 HTML 转为纯文本 Markdown"""
    soup = BeautifulSoup(html, "html.parser")

    content = soup.select_one("#mw-content-text")
    if content is None:
        content = soup.select_one("#bodyContent, main")
    if content is None:
        content = soup.body
    if content is None:
        return ""

    lines = []
    for el in content.find_all(["h2", "h3", "h4", "p", "li", "pre"]):
        tag = el.name
        text = el.get_text(strip=True)
        if not text:
            continue

        if tag.startswith("h"):
            level = int(tag[1]) + 1
            lines.append(f"{'#' * level} {text}")
            lines.append("")
        elif tag == "p":
            lines.append(text)
            lines.append("")
        elif tag == "li":
            parent = el.find_parent(["ol", "ul"])
            prefix = "1. " if parent and parent.name == "ol" else "- "
            lines.append(f"{prefix}{text}")
        elif tag == "pre":
            lines.append(f"```\n{text}\n```")
            lines.append("")

    return "\n".join(lines)


def save_page(page_name: str, text: str, title: str, folder: str):
    """保存页面到 data/raw/{folder}/{page_name}.md"""
    safe_name = re.sub(r"[^\w\-]", "_", page_name)
    dest_dir = RAW_DIR / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{safe_name}.md"
    path.write_text(text, encoding="utf-8")
    return path


# ═══════════ 主爬取逻辑 ═══════════

def crawl_all(delay: float = 1.0):
    """按爬取计划爬取所有页面"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    succeeded = 0
    failed = 0
    skipped = 0
    stats = {}

    for entry in CRAWL_PLAN:
        folder = entry["folder"]
        folder_pages = 0
        folder_ok = 0

        if entry["type"] == "category":
            print(f"\n{'='*50}")
            print(f"分类爬取: {entry['wiki_cat']} → {folder}/")
            print(f"{'='*50}")

            page_names = get_all_pages_in_category(entry["wiki_cat"])
            if not page_names:
                print(f"  ⚠ 未找到页面，跳过")
                continue

            for page_name in page_names:
                total += 1
                folder_pages += 1

                # 检查是否已经在本地（避免重复爬）
                safe_name = re.sub(r"[^\w\-]", "_", page_name)
                local_path = RAW_DIR / folder / f"{safe_name}.md"
                if local_path.exists():
                    print(f"  ⏭ 已存在: {page_name}")
                    skipped += 1
                    folder_ok += 1
                    continue

                try:
                    print(f"  [{total}] 爬取: {page_name}")
                    text, title = fetch_wiki_page(page_name)
                    save_page(page_name, text, title, folder)
                    succeeded += 1
                    folder_ok += 1
                    print(f"    ✅ {title}")
                except Exception as e:
                    failed += 1
                    print(f"    ❌ {e}")

                time.sleep(delay)

        elif entry["type"] == "pages":
            pages = entry["pages"]
            print(f"\n{'='*50}")
            print(f"指定页面爬取: {len(pages)} 页 → {folder}/")
            print(f"{'='*50}")

            for page_name in pages:
                total += 1
                folder_pages += 1

                safe_name = re.sub(r"[^\w\-]", "_", page_name)
                local_path = RAW_DIR / folder / f"{safe_name}.md"
                if local_path.exists():
                    print(f"  ⏭ 已存在: {page_name}")
                    skipped += 1
                    folder_ok += 1
                    continue

                try:
                    print(f"  [{total}] 爬取: {page_name}")
                    text, title = fetch_wiki_page(page_name)
                    save_page(page_name, text, title, folder)
                    succeeded += 1
                    folder_ok += 1
                    print(f"    ✅ {title}")
                except Exception as e:
                    failed += 1
                    print(f"    ❌ {e}")

                time.sleep(delay)

        stats[folder] = {"total": folder_pages, "ok": folder_ok}

    # 输出统计
    print(f"\n{'='*50}")
    print(f"爬取完成！")
    print(f"  成功: {succeeded}, 已存在(跳过): {skipped}, 失败: {failed}")
    if failed > 0:
        print(f"  ⚠ 有 {failed} 个页面失败，可重新运行尝试")
    print(f"\n各文件夹统计:")
    for folder, s in sorted(stats.items()):
        print(f"  {folder}: {s['ok']}/{s['total']} 页")

    return succeeded, failed


def clean_old_flat_raw():
    """清理旧的扁平原始文件（可选）"""
    old_files = list(RAW_DIR.glob("*.md"))
    if old_files:
        print(f"\n发现 {len(old_files)} 个旧扁平文件（不在子目录中）")
        resp = input("是否删除它们？(y/n): ").strip().lower()
        if resp == "y":
            for f in old_files:
                f.unlink()
                print(f"  已删除: {f.name}")
            print("旧文件清理完成")


if __name__ == "__main__":
    import sys

    print("Eu4RAG Wiki 爬虫 v2")
    print(f"原始文件将保存在: {RAW_DIR}")
    print()

    crawl_all(delay=1.0)

    if "--clean" in sys.argv:
        clean_old_flat_raw()
