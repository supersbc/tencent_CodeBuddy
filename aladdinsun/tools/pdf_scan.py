#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
from datetime import datetime

try:
    from PyPDF2 import PdfReader
except Exception as e:
    print(json.dumps({"error": f"PyPDF2 not available: {e}"}, ensure_ascii=False))
    sys.exit(3)

SOURCE_HINTS = [
    (re.compile(r"arxiv", re.I), "arXiv"),
    (re.compile(r"ieee", re.I), "IEEE"),
    (re.compile(r"acm", re.I), "ACM"),
    (re.compile(r"springer", re.I), "Springer"),
    (re.compile(r"elsevier|sciencedirect", re.I), "Elsevier"),
    (re.compile(r"wiley", re.I), "Wiley"),
    (re.compile(r"nature", re.I), "Nature"),
    (re.compile(r"science\b", re.I), "Science"),
    (re.compile(r"cnki|知网", re.I), "CNKI"),
    (re.compile(r"wanfang|万方", re.I), "万方"),
    (re.compile(r"vip|维普", re.I), "维普"),
]

TEXT_TITLE_PATTERNS = [
    re.compile(r"^\s*(?:title\s*[:：]\s*)?(.{6,150})$", re.I),
]

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s

def guess_source(meta_text: str, page_text: str) -> str:
    blob = f"{meta_text}\n{page_text}" if page_text else meta_text
    for pat, label in SOURCE_HINTS:
        if pat.search(blob or ""):
            return label
    return "未知/未标注"

def extract_year(meta) -> str:
    # Try CreationDate or ModDate like D:20241026123000Z
    for k in ("/CreationDate", "/ModDate", "CreationDate", "ModDate"):
        v = meta.get(k) if hasattr(meta, 'get') else getattr(meta, k, None)
        if not v and isinstance(meta, dict):
            v = meta.get(k)
        if not v:
            continue
        m = re.search(r"(19|20)\d{2}", str(v))
        if m:
            return m.group(0)
    return "—"

def first_meaningful_line(text: str) -> str:
    if not text:
        return ""
    for line in text.splitlines():
        t = line.strip()
        if len(t) >= 6 and len(t) <= 150 and re.search(r"[A-Za-z\u4e00-\u9fa5]", t):
            # Ignore lines that look like authors list with many commas if possible
            return t
    return ""

def extract_title_from_text(text: str) -> str:
    t = first_meaningful_line(text)
    return t

def extract_authors_from_text(text: str) -> str:
    if not text:
        return ""
    # Heuristics: find line starting with 'By ' or near '作者' or contains multiple commas
    for line in text.splitlines()[:30]:
        l = line.strip()
        if re.search(r"^by\s+", l, re.I):
            return clean_text(re.sub(r"^by\s+", "", l, flags=re.I))
        if "作者" in l and len(l) <= 60:
            return clean_text(l.split("作者")[-1].strip(" :：-"))
        if ("," in l or "、" in l) and 5 < len(l) <= 120 and not l.lower().startswith("abstract"):
            return clean_text(l)
    return ""

def scan_pdf(path: str) -> dict:
    try:
        reader = PdfReader(path)
        meta = reader.metadata or {}
        title = clean_text(getattr(meta, 'title', '') or meta.get('/Title') or meta.get('Title') or '')
        author = clean_text(getattr(meta, 'author', '') or meta.get('/Author') or meta.get('Author') or '')
        year = extract_year(meta)
        first_text = ""
        try:
            if reader.pages:
                first_text = reader.pages[0].extract_text() or ""
        except Exception:
            first_text = ""
        if not title:
            title = clean_text(extract_title_from_text(first_text))
        if not author:
            author = clean_text(extract_authors_from_text(first_text))
        meta_text = " ".join([str(meta.get(k, '')) for k in meta.keys()]) if hasattr(meta, 'keys') else str(meta)
        source = guess_source(meta_text, first_text)
        return {
            'file': os.path.basename(path),
            'path': path,
            'title': title or '(未识别标题)',
            'author': author or '(未识别作者)',
            'source': source,
            'year': year,
        }
    except Exception as e:
        return {
            'file': os.path.basename(path),
            'path': path,
            'error': str(e)
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: pdf_scan.py <directory>")
        sys.exit(2)
    root = sys.argv[1]
    results = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                full = os.path.join(dirpath, fn)
                info = scan_pdf(full)
                results.append(info)
    # Output markdown
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"# PDF 文件清单\n\n目录: {root}\n\n生成时间: {now}\n\n共计: {len(results)} 个PDF\n")
    print("| 文件名 | 标题 | 作者 | 来源 | 年份 | 路径 |")
    print("|---|---|---|---|---|---|")
    for r in sorted(results, key=lambda x: x.get('title','')):
        if 'error' in r:
            print(f"| {r['file']} | (解析失败) | - | - | - | {r['path']} |")
        else:
            print("| {} | {} | {} | {} | {} | {} |".format(
                r['file'].replace('|',' '),
                r['title'].replace('|',' '),
                r['author'].replace('|',' '),
                r['source'].replace('|',' '),
                r['year'],
                r['path'].replace('|',' ')
            ))

if __name__ == '__main__':
    main()
