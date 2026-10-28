from bs4 import BeautifulSoup
import re


def html_to_markdown(html: str, limit: int = 32000) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    for tag in soup(["script", "style", "noscript", "svg", "template"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    lines = []
    for element in main.find_all(["h1", "h2", "h3", "p", "li", "tr", "blockquote"], recursive=True):
        if element.find_parent(["p", "li", "tr", "blockquote"]):
            continue
        line = re.sub(r"\s+", " ", element.get_text(" ", strip=True))
        if line:
            prefix = "# " if element.name == "h1" else "## " if element.name in {"h2", "h3"} else "- " if element.name == "li" else ""
            lines.append(prefix + line)
    if not lines:
        lines = [re.sub(r"\s+", " ", main.get_text(" ", strip=True))]
    markdown = "\n".join(lines)[:limit]
    return {"title": title, "markdown": markdown, "characters": len(markdown)}
