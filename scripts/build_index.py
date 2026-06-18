#!/usr/bin/env python3
import html
import os
import shutil
import sys
from pathlib import Path

# Pages in this folder are PUBLIC and shown in the lists (homepage + README).
LISTED_DIR = "html_files"
# Pages in this folder are reachable by URL but NOT shown in any list.
UNLISTED_DIR = "unlisted"


def main():
    listed_src = Path(sys.argv[1] if len(sys.argv) > 1 else LISTED_DIR)
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "_site")
    unlisted_src = Path(sys.argv[3] if len(sys.argv) > 3 else UNLISTED_DIR)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    listed = publish(listed_src, out)      # shown in the lists
    unlisted = publish(unlisted_src, out)  # reachable, but hidden from the lists

    (out / ".nojekyll").write_text("", encoding="utf-8")

    # Homepage: keep your own html_files/index.html if present, else generate.
    if (listed_src / "index.html").exists():
        print("Found your own index.html in the listed folder -- keeping it.")
    else:
        (out / "index.html").write_text(render_index(listed), encoding="utf-8")
        print(f"Generated _site/index.html listing {len(listed)} page(s).")

    base = site_base_url()
    Path("README.md").write_text(render_readme(listed, base), encoding="utf-8")
    print(f"README.md lists {len(listed)} page(s); {len(unlisted)} unlisted page(s) "
          f"deployed but hidden. Base URL: {base or '(relative)'}")


def publish(src, out):
    """Copy everything in src into out, add a clean /name URL for each .html,
    and return the list of clean stem names found."""
    if not src.is_dir():
        return []
    shutil.copytree(src, out, dirs_exist_ok=True)
    pages = sorted(
        p.relative_to(src).as_posix()
        for p in src.rglob("*.html")
        if p.name.lower() != "index.html"
    )
    stems = []
    for rel in pages:
        stem = rel[:-5]  # drop ".html"
        clean = out / stem / "index.html"
        clean.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(out / rel, clean)
        stems.append(stem)
    return stems


def site_base_url():
    """Absolute base URL of the live site, ending with '/'. May be '' locally."""
    explicit = os.environ.get("SITE_BASE_URL")
    if explicit:
        return explicit.rstrip("/") + "/"

    repo = os.environ.get("GITHUB_REPOSITORY", "")  # "owner/name"
    if "/" in repo:
        owner, name = repo.split("/", 1)
        owner_l = owner.lower()
        if name.lower() == f"{owner_l}.github.io":
            return f"https://{owner_l}.github.io/"
        return f"https://{owner_l}.github.io/{name}/"
    return ""  # local run with no env -> relative links


def render_readme(links, base):
    if links:
        rows = []
        for stem in links:
            url = (base + stem + "/") if base else (stem + "/")
            rows.append(f"- [{stem}]({url})")
        body = "\n".join(rows)
    else:
        body = "_No pages yet — drop an `.html` file into the `html_files/` folder and push._"

    home = base or "./"
    count = len(links)
    return f"""<!-- AUTO-GENERATED on every push. Do not edit by hand --
     add or remove .html files in the html_files/ folder instead. -->
# My pages

🌐 **Live site:** {home}

**{count}** page{'' if count == 1 else 's'}:

{body}
"""


def render_index(links):
    if links:
        items = "\n".join(
            f'        <li><a href="{html.escape(stem)}/">{html.escape(stem)}</a></li>'
            for stem in links
        )
    else:
        items = '        <li class="empty">No pages yet &mdash; drop an HTML file into the folder and push.</li>'

    n = len(links)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BienePie's S3cr4t3 P4g3s</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Space Grotesk', sans-serif;
    background: #0d0f14;
    color: #e8eaf0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 48px 20px;
  }}
  main {{ width: 100%; max-width: 640px; }}
  h1 {{ font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 4px; }}
  p.sub {{ font-family: 'Space Mono', monospace; color: #8b93a7; margin-bottom: 28px; font-size: 0.9rem; }}
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
    font-weight: 500;
    transition: border-color .15s, transform .15s;
  }}
  li a:hover {{ border-color: #5b8cff; transform: translateX(3px); }}
  li.empty {{ font-family: 'Space Mono', monospace; color: #8b93a7; padding: 14px 0; }}
</style>
</head>
<body>
  <main>
    <h1>BienePie's S3cr4t3 P4g3s</h1>
    <p class="sub">{n} page{'' if n == 1 else 's'} &middot; click to open</p>
    <ul>
{items}
    </ul>
  </main>
</body>
</html>