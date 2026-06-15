#!/usr/bin/env python3
import html
import shutil
import sys
from pathlib import Path


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "html_files")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "_site")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    if not src.is_dir():
        print(f"Source folder '{src}' does not exist -- publishing an empty site.")
        (out / ".nojekyll").write_text("", encoding="utf-8")
        (out / "index.html").write_text(render_index([]), encoding="utf-8")
        return

    shutil.copytree(src, out, dirs_exist_ok=True)

    (out / ".nojekyll").write_text("", encoding="utf-8")

    pages = sorted(
        p.relative_to(out).as_posix()
        for p in out.rglob("*.html")
        if p.name.lower() != "index.html"
    )

    if (out / "index.html").exists():
        print("Found your own index.html in the folder -- keeping it.")
        return

    (out / "index.html").write_text(render_index(pages), encoding="utf-8")
    print(f"Generated index.html listing {len(pages)} page(s).")


def render_index(pages):
    if pages:
        items = "\n".join(
            f'        <li><a href="{html.escape(p)}">{html.escape(p)}</a></li>'
            for p in pages
        )
    else:
        items = '        <li class="empty">No HTML files yet &mdash; drop some into the folder and push.</li>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My HTML files</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    background: #0d0f14;
    color: #e8eaf0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 48px 20px;
  }}
  main {{ width: 100%; max-width: 640px; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  p.sub {{ color: #8b93a7; margin-bottom: 28px; font-size: 0.95rem; }}
  ul {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
  li a {{
    display: block;
    padding: 14px 18px;
    background: #161a24;
    border: 1px solid #2a3045;
    border-radius: 10px;
    color: #e8eaf0;
    text-decoration: none;
    font-size: 1.05rem;
    transition: border-color .15s, transform .15s;
  }}
  li a:hover {{ border-color: #5b8cff; transform: translateX(3px); }}
  li.empty {{ color: #8b93a7; padding: 14px 0; }}
</style>
</head>
<body>
  <main>
    <h1>My HTML files</h1>
    <p class="sub">{len(pages)} page{'' if len(pages) == 1 else 's'} &middot; click to open</p>
    <ul>
{items}
    </ul>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
