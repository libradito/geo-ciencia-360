import hashlib, re, pathlib

css  = pathlib.Path("_site/styles.css")
html = pathlib.Path("_site/dashboard.html")

digest  = hashlib.md5(css.read_bytes()).hexdigest()[:8]
content = html.read_text(encoding="utf-8")
updated = re.sub(
    r'href="styles\.css"',
    f'href="styles.css?v={digest}"',
    content,
)
html.write_text(updated, encoding="utf-8")
print(f"[cache-bust] styles.css?v={digest}")
