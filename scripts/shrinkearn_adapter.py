"""ShrinkEarn API adapter. Keep the key in GitHub Actions secrets."""
import json, os, re
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_ENDPOINT = "https://shrinkearn.com/api"

class ShrinkEarnError(RuntimeError):
    pass

def create_short_link(destination_url, alias=None):
    key = os.environ.get("SHRINKEARN_API_KEY", "").strip()
    if not key:
        raise ShrinkEarnError("Missing SHRINKEARN_API_KEY secret")
    parsed = urlparse(destination_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("destination_url must be a valid http(s) URL")
    params = {"api": key, "url": destination_url}
    if alias:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,50}", alias):
            raise ValueError("Invalid alias")
        params["alias"] = alias
    req = Request(API_ENDPOINT + "?" + urlencode(params),
                  headers={"Accept": "application/json", "User-Agent": "KatMoviesWorld/1.0"})
    try:
        with urlopen(req, timeout=20) as response:
            raw = response.read(65536).decode("utf-8", errors="replace")
    except HTTPError as exc:
        raise ShrinkEarnError(f"ShrinkEarn HTTP error: {exc.code}") from None
    except (URLError, TimeoutError) as exc:
        raise ShrinkEarnError(f"Could not reach ShrinkEarn: {type(exc).__name__}") from None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ShrinkEarnError("ShrinkEarn returned non-JSON data") from None
    if not isinstance(data, dict) or str(data.get("status", "")).lower() == "error":
        raise ShrinkEarnError(str(data.get("message", "ShrinkEarn rejected request")) if isinstance(data, dict) else "Unexpected response")
    short_url = data.get("shortenedUrl")
    if not isinstance(short_url, str) or urlparse(short_url).scheme not in ("http", "https"):
        raise ShrinkEarnError("Response missing valid shortenedUrl")
    return short_url
