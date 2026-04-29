"""PlaceholderClient — Python client for the Placeholder Image API."""

import io
from typing import Optional, Dict, Any

import requests
from PIL import Image

DEFAULT_BASE_URL = "https://placeholder-api.surge.sh"


class PlaceholderClient:
    """Client for the Placeholder Image API.

    Args:
        api_key: Optional API key for authenticated requests.
        base_url: Custom base URL. Defaults to the public API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def url(
        self,
        width: int,
        height: int,
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        text: Optional[str] = None,
        format: str = "png",
    ) -> str:
        """Build the URL for a placeholder image.

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            bg_color: Background color as hex string (no #, e.g. "336699").
            text_color: Text color as hex string (no #, e.g. "ffffff").
            text: Custom text overlay.
            format: Image format — "png" (default), "jpg", or "webp".

        Returns:
            The full URL of the placeholder image.
        """
        path = f"/{width}x{height}.{format}"
        params: Dict[str, Any] = {}
        if bg_color:
            params["bg"] = bg_color
        if text_color:
            params["fg"] = text_color
        if text:
            params["text"] = text
        if self.api_key:
            params["key"] = self.api_key

        qs = ""
        if params:
            qs = "?" + "&".join(
                f"{k}={v}" for k, v in params.items()
            )

        return f"{self.base_url}{path}{qs}"

    def generate(
        self,
        width: int,
        height: int,
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        text: Optional[str] = None,
        format: str = "png",
    ) -> Image.Image:
        """Generate a placeholder image and return it as a PIL Image.

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            bg_color: Background color as hex string.
            text_color: Text color as hex string.
            text: Custom text overlay.
            format: Image format — "png", "jpg", or "webp".

        Returns:
            A PIL Image object.
        """
        image_url = self.url(
            width, height,
            bg_color=bg_color,
            text_color=text_color,
            text=text,
            format=format,
        )
        resp = requests.get(image_url, timeout=30)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content))

    def download(
        self,
        width: int,
        height: int,
        filepath: str,
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        text: Optional[str] = None,
        format: str = "png",
    ) -> str:
        """Download a placeholder image and save it to a file.

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            filepath: Destination file path.
            bg_color: Background color as hex string.
            text_color: Text color as hex string.
            text: Custom text overlay.
            format: Image format — "png", "jpg", or "webp".

        Returns:
            The file path the image was saved to.
        """
        img = self.generate(
            width, height,
            bg_color=bg_color,
            text_color=text_color,
            text=text,
            format=format,
        )
        # Determine PIL save format from requested format
        pil_format_map = {"jpg": "JPEG", "png": "PNG", "webp": "WebP"}
        pil_format = pil_format_map.get(format.lower(), "PNG")
        img.save(filepath, format=pil_format)
        return filepath