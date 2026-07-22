import re, time
import cloudscraper
import wikitextparser as wtp
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

# 要保留和格式化的模板名
KEEP_TEMPLATES = {
    "Country", "Country2", "Province", "Trade good",
    "Religion", "Government", "Area", "Region",
    "Achievement", "Startup", "Main", "MultiColumn",
}


def clean_wikitext(wikitext: str) -> str:
    parsed = wtp.parse(wikitext)
    parts = []

    # 收集已处理的模板字节区间，之后从源码删除
    spans_to_remove = []

    # ---- 1. 提取已知模板 ----
    for t in parsed.templates:
        name = t.name.strip()
        if name not in KEEP_TEMPLATES:
            continue

        spans_to_remove.append(t.span)

        if name in ("Country", "Country2", "Province", "Trade good", "Religion", "Government", "Area", "Region"):
            lines = []
            for arg in t.arguments:
                k = arg.name.strip()
                v = _inline_clean(arg.value)
                if k and v:
                    lines.append(f"{k}: {v}")
            if lines:
                parts.append("\n".join(lines))

        elif name == "Decision":
            parts.append(_fmt_decision(t))

        elif name == "Achievement":
            args = [a.value.strip() for a in t.arguments]
            if len(args) >= 2:
                parts.append(f"Achievement: {_inline_clean(args[0])} — {_inline_clean(args[1])}")

        elif name == "Startup":
            args = [a.value.strip() for a in t.arguments]
            if len(args) >= 2:
                parts.append(_inline_clean(args[1]))

        elif name == "Main":
            args = [a.value.strip() for a in t.arguments]
            if args:
                parts.append(f"Main: {_inline_clean(args[0])}")

        elif name == "MultiColumn":
            # 容器模板，提取正文内容（第一个参数）而非丢弃
            args = [a.value for a in t.arguments]
            if args:
                content = _inline_clean(args[0])
                if content:
                    parts.append(content)

    # ---- 2. 从源码移除已提取的模板 ----
    # 倒序删除，不破坏未处理部分的偏移
    text = wikitext
    for start, end in sorted(spans_to_remove, reverse=True):
        text = text[:start] + text[end:]

    # ---- 3. 替换 flag/icon 后再去掉剩下的 {{...}} 模板 ----
    text = re.sub(r'\{\{flag\|([^|}]*)(\|[^}]*)?\}\}', r'\1', text)
    text = re.sub(r'\{\{icon\|[^}]*\}\}', '', text)
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'\{\{[^{}]*\}\}', '', text)

    # ---- 4. 提取表格 ----
    parsed2 = wtp.parse(text)
    for table in parsed2.tables:
        rows = []
        cap = _inline_clean(table.caption) if table.caption else ""
        if cap:
            rows.append(f"[{cap}]")
        for row in table.data(span=False):
            cells = [_inline_clean(c) for c in row]
            if any(cells):
                rows.append(" | ".join(cells))
        if rows:
            parts.append("\n".join(rows))

    # ---- 5. 纯文本 ----
    text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]*)\]\]', r'\2', text)
    text = re.sub(r"'''?''?", '', text)
    text = re.sub(r'<[^>]+>', '', text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    lines = [l for l in lines if not l.startswith(("|", "!")) and l not in ("|-", "|}")]

    if lines:
        parts.append("\n".join(lines))

    return "\n\n".join(parts)


def _inline_clean(text: str) -> str:
    """清洗模板参数值中的 wiki 标记，保留可读文本"""
    s = text
    s = re.sub(r'\{\{flag\|([^|}]*)(\|[^}]*)?\}\}', r'\1', s)
    s = re.sub(r'\{\{icon\|[^}]*\}\}', "", s)
    s = re.sub(r'\{\{[^{}]*\}\}', "", s)
    s = re.sub(r"'''?''?", "", s)
    s = re.sub(r'\[\[([^|\]]*\|)?([^\]]*)\]\]', r"\2", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def _fmt_decision(t: wtp.Template) -> str:
    """将 {{Decision|...}} 格式化为可读文本"""
    lines = ["[Decision]"]
    for arg in t.arguments:
        name = arg.name.strip()
        val = _inline_clean(arg.value)
        if name:
            lines.append(f"  {name}: {val}")
    return "\n".join(lines)


def extract_ideas_from_html(html: str) -> str | None:
    """从 HTML 渲染中提取 {{idea}} 模板生成的国家理念"""
    soup = BeautifulSoup(html, "html.parser")
    for box in soup.select(".eu4box"):
        heading = box.select_one(".heading")
        if heading and "ideas" in heading.get_text().lower():
            for tag in box.select(".mw-editsection, hr"):
                tag.decompose()
            lines = ["[Ideas]"]
            for tag in box.find_all(["p", "dd"]):
                text = tag.get_text(strip=True)
                if text:
                    lines.append(text)
            return "\n".join(lines)
    return None


def extract_html_decisions(html: str) -> list[str]:
    """从 HTML 提取决议（包括 {{#lst:...}} 跨页嵌入的）"""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for box in soup.select(".eu4box"):
        heading = box.select_one(".heading")
        if heading and "ideas" in heading.get_text().lower():
            continue
        h3 = box.select_one("h3")
        if h3 is None:
            continue
        headline = h3.find("span", class_="mw-headline")
        if headline is None:
            continue
        name = headline.get_text(strip=True)

        # 去除噪音（编辑链接、过期提示、水平线、标题框）
        for tag in box.select(".mw-editsection, .ambox, hr, .heading"):
            tag.decompose()

        # 将 img 替换为 alt 文本（保留"Empire rank"等关键内容）
        # 但丢弃纯图标文件名（如"Execute decision.png"）
        for img_tag in box.find_all("img"):
            alt = img_tag.get("alt", "")
            if alt and not re.search(r'\.(png|jpg|jpeg|gif|svg)$', alt, re.I):
                img_tag.replace_with(alt)
            else:
                img_tag.decompose()

        parts = []
        # 风味文本（第一段）
        flavor = box.find("p")
        if flavor:
            parts.append(flavor.get_text(strip=True))
        # collapsible 内容：按 <td> 分段，每个表格列内 inline 文本自然流动
        collapsible = box.select_one(".mw-collapsible-content")
        if collapsible:
            for td in collapsible.find_all("td"):
                t = td.get_text(separator=" ", strip=True)
                if t:
                    parts.append(t)
            for child in collapsible.children:
                if child.name == "small":
                    t = child.get_text(strip=True)
                    if t:
                        parts.append(t)
        text = "\n".join(parts)
        results.append(f"[Decision] {name}\n{text}")
    return results


def get_category_pages(category: str) -> list[str]:
    pages = []
    cmcontinue = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": "max",
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        resp = scraper.get(
            "https://eu4.paradoxwikis.com/api.php", params=params, timeout=15
        )
        data = resp.json()
        for m in data["query"]["categorymembers"]:
            pages.append(m["title"])
        if "continue" in data and "cmcontinue" in data["continue"]:
            cmcontinue = data["continue"]["cmcontinue"]
        else:
            break
        time.sleep(0.5)
    return pages


def get_page_wikitext(title: str) -> str | None:
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
    }
    resp = scraper.get(
        "https://eu4.paradoxwikis.com/api.php", params=params, timeout=15
    )
    data = resp.json()
    if "error" in data:
        return None
    return data["parse"]["wikitext"]["*"]


def get_page_text(title: str, retries: int = 2) -> str | None:
    for attempt in range(retries + 1):
        try:
            params = {
                "action": "parse",
                "page": title,
                "prop": "text|wikitext",
                "format": "json",
            }
            resp = scraper.get(
                "https://eu4.paradoxwikis.com/api.php", params=params, timeout=15
            )
            data = resp.json()
        except Exception:
            if attempt < retries:
                time.sleep(2)
                continue
            return None

        if "error" in data:
            return None

        break

    wikitext = data["parse"]["wikitext"]["*"]
    html = data["parse"]["text"]["*"]

    parts = []
    ideas = extract_ideas_from_html(html)
    if ideas:
        parts.append(ideas)

    decisions = extract_html_decisions(html)
    for d in decisions:
        parts.append(d)

    text = clean_wikitext(wikitext)
    if text:
        parts.append(text)

    return "\n\n".join(parts)


# CLI 入口：python eu4_crawler.py "Page Title"  → 打印清洗后文本
if __name__ == "__main__":
    import sys
    title = sys.argv[1] if len(sys.argv) > 1 else "List_of_event_lists"
    print(get_page_text(title))
