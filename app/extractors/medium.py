from urllib.parse import quote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from app.core.models import Document, SourceType


FREEDIUM_BASE = "https://freedium-mirror.cfd"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)


def extract_medium(url: str) -> Document:
    source_url = url.strip()
    html, mirror_url = _fetch_freedium_html(source_url)
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "form", "nav", "header", "footer"]):
        tag.decompose()

    title = _extract_title(soup) or "Medium Article"
    body = soup.find("article") or soup.find("main") or soup.body
    if body is None:
        raise ValueError("Freedium returned a page without readable article content.")

    text_parts = _extract_text_parts(body)
    image_parts = _extract_images(body, mirror_url)
    combined = "\n\n".join([*text_parts, *image_parts]).strip()

    if len(combined) < 300:
        raise ValueError(
            "Could not extract enough readable content from the Medium article through Freedium. "
            "Check that the article URL is public and try again."
        )

    return Document(
        source_type=SourceType.MEDIUM,
        title=title,
        text=combined,
        source=source_url,
        metadata={
            "mirror_url": mirror_url,
            "images": len(image_parts),
            "extractor": "freedium-mirror.cfd",
        },
    )


def _fetch_freedium_html(source_url: str) -> tuple[str, str]:
    candidates = _freedium_candidates(source_url)
    errors: list[str] = []
    for candidate in candidates:
        try:
            response = requests.get(
                candidate,
                headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
                timeout=45,
            )
            response.raise_for_status()
            if response.text.strip():
                return response.text, response.url
        except requests.RequestException as exc:
            errors.append(f"{candidate}: {exc}")
    raise ValueError("Could not fetch the Medium article through Freedium. " + " | ".join(errors[-2:]))


def _freedium_candidates(source_url: str) -> list[str]:
    parsed = urlparse(source_url)
    if "freedium" in parsed.netloc:
        return [source_url]
    return [
        f"{FREEDIUM_BASE}/{source_url}",
        f"{FREEDIUM_BASE}/{quote(source_url, safe='')}",
    ]


def _extract_title(soup: BeautifulSoup) -> str:
    for selector in ['meta[property="og:title"]', 'meta[name="twitter:title"]']:
        tag = soup.select_one(selector)
        if tag and tag.get("content"):
            return tag["content"].strip()
    heading = soup.find("h1")
    if heading:
        return heading.get_text(" ", strip=True)
    if soup.title:
        return soup.title.get_text(" ", strip=True)
    return ""


def _extract_text_parts(body) -> list[str]:
    parts: list[str] = []
    seen: set[str] = set()
    for tag in body.find_all(["h1", "h2", "h3", "p", "li", "blockquote", "pre", "figcaption"]):
        text = tag.get_text(" ", strip=True)
        if not text or text in seen:
            continue
        seen.add(text)
        if tag.name in {"h1", "h2", "h3"}:
            parts.append(f"## {text}")
        elif tag.name == "blockquote":
            parts.append(f"> {text}")
        else:
            parts.append(text)
    return parts


def _extract_images(body, base_url: str) -> list[str]:
    images: list[str] = []
    seen: set[str] = set()
    for image in body.find_all("img"):
        src = image.get("src") or image.get("data-src") or image.get("data-original")
        if not src:
            continue
        absolute_src = urljoin(base_url, src)
        if absolute_src in seen:
            continue
        seen.add(absolute_src)
        alt = image.get("alt", "").strip()
        if alt:
            images.append(f"Image: {alt}\nURL: {absolute_src}")
        else:
            images.append(f"Image URL: {absolute_src}")
    return images
