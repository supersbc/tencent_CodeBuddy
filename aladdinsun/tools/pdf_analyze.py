#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import subprocess
from typing import List, Tuple

# Try to ensure useful libs

def ensure(pkg: str):
    try:
        __import__(pkg)
    except Exception:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', pkg], check=False)
        __import__(pkg)

# Prefer pdfplumber if available (better layout text), fallback to PyPDF2
try:
    import pdfplumber  # type: ignore
    PDFPLUMBER = True
except Exception:
    PDFPLUMBER = False
    ensure('PyPDF2')
    from PyPDF2 import PdfReader  # type: ignore

TITLE_RE = re.compile(r"^\s*(?:title\s*[:：]\s*)?(.{6,150})$", re.I)
ABSTRACT_RE = re.compile(r"\bAbstract\b|摘要", re.I)
KEYWORDS_RE = re.compile(r"\bKeywords?\b|关键词", re.I)
INTRO_RE = re.compile(r"\bIntroduction\b|引言", re.I)
METHOD_RE = re.compile(r"\bMethod|Approach|Framework\b|方法|框架", re.I)
RESULT_RE = re.compile(r"\bResult|Evaluation|Experiment\b|结果|实验|评估", re.I)
CONCL_RE = re.compile(r"\bConclusion|Conclusions\b|结论", re.I)

VENUE_PATTERNS = [
    (re.compile(r"IEEE\s+TRANSACTIONS\s+ON\s+([A-Z\-\s]+)", re.I), lambda m: f"IEEE Transactions on {m.group(1).title().strip()}"),
    (re.compile(r"Proceedings\s+of\s+the\s+VLDB\s+Endowment|PVLDB", re.I), lambda m: "PVLDB"),
    (re.compile(r"The\s+VLDB\s+Journal", re.I), lambda m: "The VLDB Journal"),
    (re.compile(r"SIGMOD\b", re.I), lambda m: "SIGMOD"),
    (re.compile(r"ICDE\b", re.I), lambda m: "ICDE"),
]

YEAR_RE = re.compile(r"(19|20)\d{2}")


def extract_text_pages(pdf_path: str, max_pages: int = 5) -> List[str]:
    texts: List[str] = []
    if PDFPLUMBER:
        with pdfplumber.open(pdf_path) as pdf:
            n = min(len(pdf.pages), max_pages)
            for i in range(n):
                try:
                    t = pdf.pages[i].extract_text() or ""
                except Exception:
                    t = ""
                texts.append(t)
    else:
        reader = PdfReader(pdf_path)  # type: ignore
        n = min(len(reader.pages), max_pages)
        for i in range(n):
            try:
                t = reader.pages[i].extract_text() or ""
            except Exception:
                t = ""
            texts.append(t)
    return texts


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def find_block(text: str, start_pat: re.Pattern, stop_pats: List[re.Pattern], max_len: int = 2000) -> str:
    if not text:
        return ""
    m = start_pat.search(text)
    if not m:
        return ""
    start = m.start()
    end = len(text)
    for p in stop_pats:
        m2 = p.search(text, start + 1)
        if m2:
            end = min(end, m2.start())
    return clean(text[start:end])[:max_len]


def extract_sections(pages: List[str]) -> dict:
    blob = "\n\n".join(pages)
    abstract = find_block(blob, ABSTRACT_RE, [KEYWORDS_RE, INTRO_RE, METHOD_RE, RESULT_RE, CONCL_RE])
    keywords = ""
    # Try to capture keywords line
    kw_match = re.search(r"(?:Keywords?\s*[:：]\s*|关键词\s*[:：]\s*)(.+)", blob, re.I)
    if kw_match:
        keywords = clean(kw_match.group(1))[:300]
    intro = find_block(blob, INTRO_RE, [METHOD_RE, RESULT_RE, CONCL_RE])
    method = find_block(blob, METHOD_RE, [RESULT_RE, CONCL_RE])
    results = find_block(blob, RESULT_RE, [CONCL_RE])
    concl = find_block(blob, CONCL_RE, [])
    return {
        'abstract': abstract,
        'keywords': keywords,
        'introduction': intro[:1200],
        'method': method[:1200],
        'results': results[:1200],
        'conclusion': concl[:1200],
        'fulltext_used_chars': len(blob),
    }


def extract_meta(pdf_path: str, first_page: str) -> Tuple[str, str, str]:
    # title, author, venue
    title = ""
    author = ""
    venue = ""
    # Title: first meaningful line
    for line in first_page.splitlines():
        t = line.strip()
        if 6 <= len(t) <= 150 and re.search(r"[A-Za-z\u4e00-\u9fa5]", t) and not re.search(r"^(abstract|摘要)$", t, re.I):
            title = t
            break
    # Authors: simple heuristics on first 30 lines
    for line in first_page.splitlines()[:30]:
        l = line.strip()
        if re.search(r"^by\s+", l, re.I):
            author = clean(re.sub(r"^by\s+", "", l, flags=re.I))
            break
        if ("," in l or "、" in l) and 5 < len(l) <= 120 and not l.lower().startswith("abstract"):
            author = clean(l)
            break
    # Venue: from first pages blob
    blob = first_page
    for pat, fmt in VENUE_PATTERNS:
        m = pat.search(blob)
        if m:
            venue = fmt(m) if callable(fmt) else (fmt or m.group(0).strip())
            break
    return title, author, venue


def analyze_pdf(pdf_path: str) -> dict:
    pages = extract_text_pages(pdf_path, max_pages=5)
    first = pages[0] if pages else ""
    title, author, venue = extract_meta(pdf_path, first)
    secs = extract_sections(pages)
    # Year guess from text
    m = YEAR_RE.search("\n".join(pages[:2]))
    year = m.group(0) if m else ""
    return {
        'file': os.path.basename(pdf_path),
        'path': pdf_path,
        'title': title or '(未识别标题)',
        'author': author or '(未识别作者)',
        'venue': venue or '(未识别期刊/会议)',
        'year': year or '—',
        **secs,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_analyze.py <directory> <output.md>")
        sys.exit(2)
    root = sys.argv[1]
    out_md = sys.argv[2]
    results: List[dict] = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                full = os.path.join(dirpath, fn)
                results.append(analyze_pdf(full))
    results.sort(key=lambda x: x.get('title',''))
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(f"# PDF 分析报告\n\n目录: {root}\n\n共计 {len(results)} 篇\n\n")
        for r in results:
            f.write(f"## {r['title']}\n")
            f.write(f"- 文件: {r['file']}\n")
            f.write(f"- 路径: {r['path']}\n")
            f.write(f"- 作者: {r['author']}\n")
            f.write(f"- 期刊/会议: {r['venue']}\n")
            f.write(f"- 年份: {r['year']}\n")
            f.write("\n")
            if r['abstract']:
                f.write(f"### 摘要\n{r['abstract']}\n\n")
            if r['keywords']:
                f.write(f"### 关键词\n{r['keywords']}\n\n")
            if r['introduction']:
                f.write(f"### 引言（节选）\n{r['introduction']}\n\n")
            if r['method']:
                f.write(f"### 方法/框架（节选）\n{r['method']}\n\n")
            if r['results']:
                f.write(f"### 实验/结果（节选）\n{r['results']}\n\n")
            if r['conclusion']:
                f.write(f"### 结论（节选）\n{r['conclusion']}\n\n")
            f.write("---\n\n")
    print(out_md)

if __name__ == '__main__':
    main()
