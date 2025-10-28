#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import hashlib
from collections import defaultdict

# Optional: use PyPDF2 for title extraction
try:
    from PyPDF2 import PdfReader
    HAVE_PYPDF2 = True
except Exception:
    HAVE_PYPDF2 = False


def md5_file(path: str, chunk_size: int = 2 * 1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def extract_title(path: str) -> str:
    if not HAVE_PYPDF2:
        return ""
    try:
        reader = PdfReader(path)
        meta = reader.metadata or {}
        title = getattr(meta, 'title', '') or meta.get('/Title') or meta.get('Title') or ''
        if title:
            return title
        # fallback: first meaningful line of page 1
        try:
            if reader.pages:
                txt = reader.pages[0].extract_text() or ''
                for line in (txt.splitlines() if txt else [])[:20]:
                    t = line.strip()
                    if 6 <= len(t) <= 150 and re.search(r"[A-Za-z\u4e00-\u9fa5]", t) and not re.match(r"^(abstract|摘要)$", t, re.I):
                        return t
        except Exception:
            pass
    except Exception:
        return ""
    return ""


def norm_title(t: str) -> str:
    t = (t or '').strip()
    t = re.sub(r"\s+", " ", t)
    t = t.lower()
    # remove punctuation that often varies
    t = re.sub(r"[\-_,.:;!?'\"]+", "", t)
    return t


def walk_pdfs(root: str):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                yield os.path.join(dirpath, fn)


def main():
    if len(sys.argv) < 2:
        print("Usage: pdf_find_duplicates.py <directory>")
        sys.exit(2)
    root = sys.argv[1]

    by_hash = defaultdict(list)
    by_title = defaultdict(list)

    paths = list(walk_pdfs(root))
    for p in paths:
        try:
            h = md5_file(p)
        except Exception as e:
            h = f"ERROR:{e}"
        by_hash[h].append(p)
        # title bucket
        title = extract_title(p)
        nt = norm_title(title)
        if nt:
            by_title[nt].append((p, title))

    # Print report to stdout (Markdown)
    print(f"# PDF 重复检测报告\n\n目录: {root}\n共扫描: {len(paths)} 个PDF\n")

    # Content duplicates (exact hash)
    dup_hash_groups = [v for v in by_hash.values() if len(v) > 1]
    print(f"## 基于内容哈希的完全重复: {len(dup_hash_groups)} 组\n")
    for i, group in enumerate(dup_hash_groups, 1):
        print(f"### 组 {i} (文件数: {len(group)})")
        for p in group:
            print(f"- {p}")
        print()

    # Title duplicates (same normalized title but possibly different files)
    dup_title_groups = [v for v in by_title.values() if len(v) > 1]
    print(f"## 基于标题的疑似重复: {len(dup_title_groups)} 组\n")
    for i, group in enumerate(dup_title_groups, 1):
        # show original titles once
        titles = list({t for _, t in group if t})
        if titles:
            print(f"### 组 {i} (归一化同名，变体{len(titles)}个)")
            for t in titles:
                print(f"- 标题: {t}")
        else:
            print(f"### 组 {i} (无标题元数据，可能为相同论文不同扫描版)")
        for p, _ in group:
            print(f"  - {p}")
        print()

if __name__ == '__main__':
    main()
