#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import subprocess
from datetime import datetime

# Ensure dependencies

def ensure_package(pkg: str):
    try:
        __import__(pkg)
    except Exception:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', pkg], check=False)
        __import__(pkg)

# Ensure PyPDF2 and openpyxl
ensure_package('PyPDF2')
ensure_package('openpyxl')

from PyPDF2 import PdfReader
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

VENUE_PATTERNS = [
    # IEEE Transactions / Journals (capture full name)
    (re.compile(r"IEEE\s+TRANSACTIONS\s+ON\s+([A-Z\-\s]+)", re.I), lambda m: f"IEEE Transactions on {m.group(1).title().strip()}"),
    (re.compile(r"IEEE\s+ACCESS", re.I), lambda m: "IEEE Access"),
    (re.compile(r"IEEE\s+SOFTWARE", re.I), lambda m: "IEEE Software"),
    # ACM Journals / Proceedings
    (re.compile(r"Proceedings\s+of\s+the\s+ACM\s+on\s+([A-Za-z\s]+)", re.I), lambda m: f"Proceedings of the ACM on {m.group(1).strip()}"),
    (re.compile(r"ACM\s+Transactions\s+on\s+([A-Za-z\s]+)", re.I), lambda m: f"ACM Transactions on {m.group(1).strip()}"),
    (re.compile(r"SIGMOD\b", re.I), lambda m: "SIGMOD"),
    (re.compile(r"SIGKDD|KDD\b", re.I), lambda m: "KDD"),
    # VLDB
    (re.compile(r"Proceedings\s+of\s+the\s+VLDB\s+Endowment|PVLDB", re.I), lambda m: "PVLDB"),
    (re.compile(r"The\s+VLDB\s+Journal", re.I), lambda m: "The VLDB Journal"),
    # Other common venues
    (re.compile(r"ICDE\b", re.I), lambda m: "ICDE"),
    (re.compile(r"WWW\b", re.I), lambda m: "WWW"),
    (re.compile(r"NeurIPS|NIPS\b", re.I), lambda m: "NeurIPS"),
    (re.compile(r"ICML\b", re.I), lambda m: "ICML"),
    (re.compile(r"AAAI\b", re.I), lambda m: "AAAI"),
    (re.compile(r"IJCAI\b", re.I), lambda m: "IJCAI"),
    (re.compile(r"USENIX\b", re.I), lambda m: "USENIX"),
    (re.compile(r"OSDI\b", re.I), lambda m: "OSDI"),
    (re.compile(r"NSDI\b", re.I), lambda m: "NSDI"),
    (re.compile(r"CCS\b", re.I), lambda m: "CCS"),
    (re.compile(r"S\s*&\s*P|Security\s+and\s+Privacy", re.I), lambda m: "IEEE S&P"),
    (re.compile(r"EuroSys\b", re.I), lambda m: "EuroSys"),
    (re.compile(r"Middleware\b", re.I), lambda m: "Middleware"),
    # Publishers / Platforms (as fallback if no venue found)
    (re.compile(r"Springer", re.I), lambda m: "Springer"),
    (re.compile(r"Elsevier|ScienceDirect", re.I), lambda m: "Elsevier"),
    (re.compile(r"Wiley", re.I), lambda m: "Wiley"),
    (re.compile(r"Nature", re.I), lambda m: "Nature"),
    (re.compile(r"Science\b", re.I), lambda m: "Science"),
    (re.compile(r"CNKI|知网", re.I), lambda m: "CNKI"),
    (re.compile(r"万方|Wanfang", re.I), lambda m: "万方"),
    (re.compile(r"维普|VIP", re.I), lambda m: "维普"),
    (re.compile(r"arXiv", re.I), lambda m: "arXiv"),
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
    return "—"


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
    # 1) Try specific venue patterns first (journals/conferences)
    for pat, formatter in VENUE_PATTERNS:
        m = pat.search(blob or "")
        if m:
            return formatter(m) if callable(formatter) else (formatter or m.group(0).strip())
    # 2) Fallback
    return "未知/未标注"


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
            'title': '(解析失败)',
            'author': '-',
            'source': '-',
            'year': '-',
            'error': str(e)
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_scan_to_excel.py <directory> <output.xlsx>")
        sys.exit(2)
    root = sys.argv[1]
    out_xlsx = sys.argv[2]

    rows = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                full = os.path.join(dirpath, fn)
                rows.append(scan_pdf(full))

    wb = Workbook()
    ws = wb.active
    ws.title = 'PDF清单'

    headers = ['文件名', '标题', '作者', '来源', '年份', '路径']
    ws.append(headers)

    for r in rows:
        ws.append([r.get('file',''), r.get('title',''), r.get('author',''), r.get('source',''), r.get('year',''), r.get('path','')])

    # Column widths
    widths = [30, 60, 50, 15, 8, 100]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64+i)].width = w

    # Header style
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Freeze header
    ws.freeze_panes = 'A2'

    # Save
    os.makedirs(os.path.dirname(out_xlsx), exist_ok=True)
    wb.save(out_xlsx)

    print(f"生成完成: {out_xlsx}  共 {len(rows)} 条")

if __name__ == '__main__':
    main()
