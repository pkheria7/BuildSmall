from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException

from app.core.models import Document, SourceType


def _extract_video_id(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.strip("/")
    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
    raise ValueError("Could not find a YouTube video ID in the URL.")


def extract_youtube(url: str) -> Document:
    video_id = _extract_video_id(url)
    api = YouTubeTranscriptApi()
    try:
        if hasattr(api, "fetch"):
            transcript = api.fetch(video_id)
            transcript_items = transcript.to_raw_data()
        else:
            transcript_items = YouTubeTranscriptApi.get_transcript(video_id)
    except YouTubeTranscriptApiException as exc:
        raise ValueError(
            "Could not fetch the YouTube transcript. On hosted environments such as "
            "Hugging Face Spaces, YouTube often blocks transcript requests from datacenter IPs. "
            "Paste the transcript into the YouTube transcript fallback box and retry."
        ) from exc

    if not transcript_items:
        raise ValueError(
            "No transcript was available for this YouTube video. Paste the transcript into "
            "the YouTube transcript fallback box and retry."
        )

    lines = []
    for item in transcript_items:
        timestamp = int(item.get("start", 0))
        minutes, seconds = divmod(timestamp, 60)
        text = item.get("text", "").strip()
        if text:
            lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")

    return Document(
        source_type=SourceType.YOUTUBE,
        title=f"YouTube Transcript {video_id}",
        text="\n".join(lines).strip(),
        source=url,
        metadata={"video_id": video_id, "segments": len(transcript_items)},
    )
