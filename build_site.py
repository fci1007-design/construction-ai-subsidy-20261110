#!/usr/bin/env python3
"""Build a self-contained HTML reading page from content.md."""

from pathlib import Path
import html
import re

import markdown


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "content.md"
OUTPUT = ROOT / "index.html"
TASK_ITEM = re.compile(
    r"^(?P<prefix>[ \t]*(?:[-+*]|\d+[.)])[ \t]+)"
    r"\[(?P<checked>[ xX])\][ \t]+",
    re.MULTILINE,
)

TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="@@TITLE@@">
  <link rel="icon" href="data:,">
  <title>@@TITLE@@</title>
  <style>
    :root {
      color-scheme: light;
      font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "PingFang TC",
        "Microsoft JhengHei", sans-serif;
      color: #1d2939;
      background: #f2f5f8;
      font-synthesis: none;
      text-rendering: optimizeLegibility;
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      min-width: 320px;
      margin: 0;
      font-size: 18px;
      line-height: 1.75;
    }

    .skip-link {
      position: fixed;
      z-index: 20;
      top: 8px;
      left: 8px;
      padding: 10px 14px;
      transform: translateY(-160%);
      border-radius: 8px;
      color: #fff;
      background: #123b68;
    }

    .skip-link:focus {
      transform: translateY(0);
    }

    .page-layout {
      display: grid;
      grid-template-columns: minmax(220px, 280px) minmax(0, 920px);
      justify-content: center;
      align-items: start;
      gap: clamp(20px, 3vw, 44px);
      width: min(100%, 1500px);
      margin: 0 auto;
      padding: 24px;
    }

    .page-outline {
      position: sticky;
      top: 18px;
      z-index: 5;
      max-height: calc(100vh - 36px);
    }

    .page-outline details {
      display: flex;
      flex-direction: column;
      max-height: inherit;
      overflow: hidden;
      border: 1px solid #cbd5df;
      border-radius: 14px;
      background: #fff;
      box-shadow: 0 8px 24px rgb(22 39 61 / 6%);
    }

    .page-outline summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 58px;
      padding: 12px 17px;
      color: #15375b;
      font-size: 18px;
      font-weight: 750;
      cursor: pointer;
      list-style: none;
    }

    .page-outline summary::-webkit-details-marker {
      display: none;
    }

    .page-outline summary::after {
      width: 9px;
      height: 9px;
      border-right: 2px solid currentColor;
      border-bottom: 2px solid currentColor;
      transform: rotate(45deg);
      transition: transform 140ms ease;
      content: "";
    }

    .page-outline details:not([open]) summary::after {
      transform: rotate(-45deg);
    }

    .page-outline nav {
      overflow-y: auto;
      padding: 2px 10px 12px;
      overscroll-behavior: contain;
    }

    .toc ul {
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .toc ul ul {
      padding-left: 12px;
    }

    .toc li {
      margin: 2px 0;
    }

    .toc a {
      display: block;
      min-height: 40px;
      padding: 7px 9px;
      border-radius: 7px;
      color: #34445a;
      font-size: 16px;
      line-height: 1.55;
      text-decoration: none;
      overflow-wrap: anywhere;
    }

    .toc a:hover,
    .toc a:focus-visible {
      outline: 2px solid #3b6ea8;
      outline-offset: 1px;
      color: #123b68;
      background: #edf4fb;
    }

    .toc a[aria-current="location"] {
      border-left: 3px solid #2463a6;
      color: #123b68;
      background: #e8f1fa;
      font-weight: 700;
    }

    .document {
      min-width: 0;
    }

    .markdown-body {
      min-width: 0;
      padding: clamp(22px, 4vw, 64px);
      border: 1px solid #d9e0e8;
      border-radius: 16px;
      background: #fff;
      box-shadow: 0 12px 36px rgb(22 39 61 / 6%);
      font-size: 18px;
      line-height: 1.85;
      overflow-wrap: anywhere;
    }

    .markdown-body :is(h1, h2, h3, h4, h5, h6, [id]) {
      scroll-margin-top: 5rem;
    }

    .markdown-body h1 {
      margin: 0 0 1.2em;
      color: #142b43;
      font-size: clamp(2rem, 4vw, 2.7rem);
      line-height: 1.32;
    }

    .markdown-body h2 {
      margin-top: 2.5em;
      padding-top: 0.75em;
      border-top: 1px solid #dce3eb;
      color: #15375b;
      font-size: 1.55em;
      line-height: 1.45;
    }

    .markdown-body h3 {
      margin-top: 1.9em;
      color: #1c4268;
      font-size: 1.25em;
      line-height: 1.5;
    }

    .markdown-body h4,
    .markdown-body h5,
    .markdown-body h6 {
      margin-top: 1.6em;
      color: #264b70;
      font-size: 1.08em;
      line-height: 1.5;
    }

    .markdown-body a {
      color: #155da0;
      text-decoration-thickness: 1px;
      text-underline-offset: 0.18em;
    }

    .markdown-body a:hover {
      color: #0c3f72;
    }

    .markdown-body p,
    .markdown-body ul,
    .markdown-body ol,
    .markdown-body blockquote {
      margin-top: 1em;
      margin-bottom: 1em;
    }

    .markdown-body ul,
    .markdown-body ol {
      padding-left: 1.55em;
    }

    .markdown-body li + li {
      margin-top: 0.3em;
    }

    .markdown-body blockquote {
      padding: 0.4em 1em;
      border-left: 4px solid #557ba4;
      color: #42546a;
      background: #f5f8fb;
    }

    .markdown-body hr {
      margin: 2em 0;
      border: 0;
      border-top: 1px solid #dce3eb;
    }

    .markdown-body table {
      display: block;
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      border-collapse: collapse;
      border-spacing: 0;
      font-size: 0.92em;
      overscroll-behavior-x: contain;
    }

    .markdown-body th,
    .markdown-body td {
      min-width: 7rem;
      padding: 0.65em 0.8em;
      border: 1px solid #cbd5df;
      text-align: left;
      vertical-align: top;
    }

    .markdown-body th {
      color: #183b5e;
      background: #edf2f7;
    }

    .markdown-body code {
      padding: 0.1em 0.32em;
      border-radius: 4px;
      background: #f1f4f7;
      overflow-wrap: anywhere;
    }

    .markdown-body pre {
      max-width: 100%;
      padding: 1em;
      overflow: auto;
      border-radius: 10px;
      background: #f1f4f7;
    }

    .markdown-body pre code {
      padding: 0;
      background: transparent;
    }

    .markdown-body img {
      max-width: 100%;
      height: auto;
    }

    .markdown-body input[type="checkbox"] {
      width: 1.15em;
      height: 1.15em;
      margin: 0 0.4em 0 0;
      accent-color: #235d93;
      vertical-align: -0.12em;
    }

    @media (max-width: 900px) {
      .page-layout {
        grid-template-columns: minmax(0, 1fr);
        gap: 14px;
        padding: 12px;
      }

      .page-outline {
        top: 0;
        max-height: 65vh;
        max-height: 65dvh;
      }

      .page-outline details[open] {
        max-height: 65vh;
        max-height: 65dvh;
      }

      .markdown-body {
        padding: clamp(20px, 5vw, 32px);
      }
    }

    @media (max-width: 480px) {
      .page-layout {
        padding: 8px;
      }

      .markdown-body {
        border-radius: 12px;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      html {
        scroll-behavior: auto;
      }

      *,
      *::before,
      *::after {
        transition-duration: 0.01ms !important;
      }
    }

    @media print {
      body {
        background: #fff;
      }

      .page-layout {
        display: block;
        width: 100%;
        padding: 0;
      }

      .page-outline,
      .skip-link {
        display: none;
      }

      .markdown-body {
        padding: 0;
        border: 0;
        border-radius: 0;
        box-shadow: none;
      }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#document">略過大綱並前往正文</a>
  <div class="page-layout">
    <aside class="page-outline" aria-label="文件導覽">
      <details id="outline-details" open>
        <summary>文件大綱</summary>
        <nav id="document-outline" aria-label="文件大綱">
          @@TOC@@
        </nav>
      </details>
    </aside>
    <main id="document" class="document" tabindex="-1">
      <article class="markdown-body">
        @@CONTENT@@
      </article>
    </main>
  </div>
  <script>
    (() => {
      const details = document.getElementById("outline-details");
      const outline = document.getElementById("document-outline");
      const mobile = window.matchMedia("(max-width: 900px)");
      const links = Array.from(outline.querySelectorAll('a[href^="#"]'));
      const linkByHeading = new Map();
      const headings = [];

      const syncOutline = (event) => {
        details.open = !event.matches;
      };

      syncOutline(mobile);
      mobile.addEventListener("change", syncOutline);

      for (const link of links) {
        const heading = document.getElementById(decodeURIComponent(link.hash.slice(1)));
        if (!heading) continue;
        headings.push(heading);
        linkByHeading.set(heading, link);
        link.addEventListener("click", () => {
          if (mobile.matches) details.open = false;
        });
      }

      if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          if (visible.length === 0) return;
          for (const link of links) link.removeAttribute("aria-current");
          linkByHeading.get(visible[0].target)?.setAttribute("aria-current", "location");
        }, { rootMargin: "-8% 0px -78% 0px", threshold: 0 });

        for (const heading of headings) observer.observe(heading);
      }
    })();
  </script>
</body>
</html>
"""


def build_site() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+?)\s*$", source, re.MULTILINE)
    if title_match is None:
        raise ValueError(f"No level-one Markdown heading found in {SOURCE}")

    def render_task_item(match: re.Match[str]) -> str:
        checked = match.group("checked").lower() == "x"
        state = "已完成" if checked else "待辦事項"
        checked_attribute = " checked" if checked else ""
        return (
            f'{match.group("prefix")}<input class="task-checkbox" type="checkbox" '
            f'disabled aria-label="{state}"{checked_attribute}> '
        )

    markdown_source = TASK_ITEM.sub(render_task_item, source)
    markdown_source = markdown_source.replace(
        "[20261110.txt](../../20261110.txt)",
        "20261110.txt",
    )
    parser = markdown.Markdown(
        extensions=["extra", "toc"],
        extension_configs={"toc": {"toc_depth": "2-6"}},
        output_format="html5",
    )
    article_html = parser.convert(markdown_source)
    toc_html = parser.toc

    source_heading_count = len(re.findall(r"^#{1,6}[ \t]+", source, re.MULTILINE))
    rendered_heading_count = len(re.findall(r"<h[1-6]\b", article_html))
    if source_heading_count != rendered_heading_count:
        raise ValueError(
            "Markdown heading count changed during rendering: "
            f"{source_heading_count} source, {rendered_heading_count} rendered"
        )

    article_ids = set(re.findall(r'\bid="([^"]+)"', article_html))
    toc_targets = set(re.findall(r'href="#([^"]+)"', toc_html))
    fragment_targets = set(re.findall(r'href="#([^"]+)"', article_html))
    missing_targets = (toc_targets | fragment_targets) - article_ids
    if missing_targets:
        raise ValueError(f"Unresolved in-page links: {', '.join(sorted(missing_targets))}")

    page = (
        TEMPLATE.replace("@@TITLE@@", html.escape(title_match.group(1).strip(), quote=True))
        .replace("@@TOC@@", toc_html)
        .replace("@@CONTENT@@", article_html)
    )
    OUTPUT.write_text(page, encoding="utf-8")
    print(
        f"Built {OUTPUT.name}: {rendered_heading_count} headings, "
        f"{len(toc_targets)} outline links"
    )


if __name__ == "__main__":
    build_site()
