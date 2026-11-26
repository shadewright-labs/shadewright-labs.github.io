"""Fails if a published page loads anything from another origin or carries inline code or styles.

Checks every .html file under the given folder (default: _site):
- no <script> element at all, inline or external (the site has no JavaScript);
- no <style> element and no style= attribute (the Content-Security-Policy allows only the stylesheet file);
- no on* event handler attributes;
- no resource from another origin: img src and srcset, source srcset, link href (stylesheets, icons),
  form action, iframe, object, embed, audio, video, track;
- a Content-Security-Policy meta element with default-src 'none'.
Also checks the stylesheets under assets/ for url() and @import of another origin.
Links that a person follows (<a href>) may point anywhere.
Standard library only; run with: python3 -I scripts/check-pages.py _site
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

EXTERNAL = re.compile(r"^\s*(?:[a-z][a-z0-9+.-]*:|//)", re.I)
RESOURCE_ATTRS = {
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "link": ("href",),
    "form": ("action",),
    "iframe": ("src",),
    "object": ("data",),
    "embed": ("src",),
    "audio": ("src",),
    "video": ("src", "poster"),
    "track": ("src",),
    "input": ("src",),
}


def is_external(value):
    # data: and blob: URLs count as another origin too: the policy allows 'self' only.
    return bool(EXTERNAL.match(value))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problems = []
        self.csp = None

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        values = dict(attrs)
        if tag == "script":
            self.problems.append((line, "<script> element"))
        if tag == "style":
            self.problems.append((line, "<style> element"))
        for name, _ in attrs:
            if name == "style":
                self.problems.append((line, f"style= attribute on <{tag}>"))
            if name.startswith("on"):
                self.problems.append((line, f"{name}= event handler on <{tag}>"))
        for name in RESOURCE_ATTRS.get(tag, ()):
            value = values.get(name)
            if not value:
                continue
            urls = [part.strip().split()[0] for part in value.split(",") if part.strip()] if name == "srcset" else [value]
            for url in urls:
                if is_external(url):
                    self.problems.append((line, f"<{tag} {name}> loads another origin: {url}"))
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "content-security-policy":
            self.csp = values.get("content") or ""

    handle_startendtag = handle_starttag


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    failed = False
    pages = sorted(root.rglob("*.html"))
    if not pages:
        print(f"check-pages: no HTML files under {root}")
        return 1
    for path in pages:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        page.close()
        if page.csp is None or "default-src 'none'" not in page.csp:
            page.problems.append((1, "no Content-Security-Policy meta element with default-src 'none'"))
        for line, text in page.problems:
            print(f"{path}:{line}: {text}")
            failed = True
    sheets = sorted(root.rglob("*.css"))
    for path in sheets:
        for number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)|@import\s+['\"]([^'\"]+)", text):
                url = match.group(1) or match.group(2)
                if is_external(url):
                    print(f"{path}:{number}: stylesheet loads another origin: {url}")
                    failed = True
    print(f"check-pages: {len(pages)} pages and {len(sheets)} stylesheets checked, {'problems found' if failed else 'no problems'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
