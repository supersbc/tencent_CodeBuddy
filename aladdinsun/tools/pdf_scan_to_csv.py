#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import csv
import subprocess

def ensure_package(pkg: str):
    try:
        __import__(pkg)
    except Exception:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', pkg], check=False)
        __import__(pkg)

ensure_package('PyPDF2')
from PyPDF2 import PdfReader

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

def clean_text(s: str) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()

def extract_year(meta) -> str:
    for k in ("/CreationDate", "/ModDate", "CreationDate", "ModDate"):
        v = None
        try:
            v = meta.get(k)
        except Exception:
            pass
        if not v:
            try:
                v = getattr(meta, k)
            except Exception:
                v = None
        if not v:
            continue
        m = re.search(r"(19|20)\d{2}", str(v))
        if m:
            return m.group(0)
    return ""

def first_meaningful_line(text: str) -> str:
    if not text:
        return ""
    for line in text.splitlines():
        t = line.strip()
        if 6 <= len(t) <= 150 and re.search(r"[A-Za-z\u4e00-\u9fa5]", t):
            return t
    return ""

def extract_authors_from_text(text: str) -> str:
    if not text:
        return ""
    for line in text.splitlines()[:30]:
        l = line.strip()
        if re.search(r"^by\s+", l, re.I):
            return clean_text(re.sub(r"^by\s+", "", l, flags=re.I))
        if "作者" in l and len(l) <= 60:
            return clean_text(l.split("作者")[-1].strip(" :：-"))
        if ("," in l or "、" in l) and 5 < len(l) <= 120 and not l.lower().startswith("abstract"):
            return clean_text(l)
    return ""

def guess_source(meta_text: str, page_text: str) -> str:
    blob = f"{meta_text}\n{page_text}" if page_text else meta_text
    for pat, label in SOURCE_HINTS:
        if pat.search(blob or ""):
            return label
    return ""

def scan_pdf(path: str):
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
            pass
        if not title:
            title = clean_text(first_meaningful_line(first_text))
        if not author:
            author = clean_text(extract_authors_from_text(first_text))
        meta_text = " ".join([str(meta.get(k, '')) for k in getattr(meta, 'keys', lambda: [])()]) if hasattr(meta, 'keys') else str(meta)
        source = guess_source(meta_text, first_text) or ""
        return [os.path.basename(path), title, author, source, year, path]
    except Exception as e:
        return [os.path.basename(path), '(解析失败)', '-', '-', '', path]


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_scan_to_csv.py <directory> <output.csv>")
        sys.exit(2)
    root = sys.argv[1]
    out_csv = sys.argv[2]

    rows = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                full = os.path.join(dirpath, fn)
                rows.append(scan_pdf(full))

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['文件名','标题','作者','来源','年份','路径'])
        writer.writerows(rows)
    print(out_csv)

if __name__ == '__main__':
    main()
