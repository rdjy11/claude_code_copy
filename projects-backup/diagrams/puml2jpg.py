"""
Export PlantUML diagrams to JPEG images.
Uses Kroki API (simpler, no encoding needed) with PlantUML server as fallback.
"""
import re
import sys
import zlib
from pathlib import Path
from io import BytesIO
from PIL import Image
import requests

USER_AGENT = "Mozilla/5.0 (compatible; ClaudeCode)"
PLANTUML_SERVER = "https://www.plantuml.com/plantuml"
KROKI_SERVER = "https://kroki.io"
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def encode_plantuml(text: str) -> str:
    data = zlib.compress(text.encode("utf-8"))[2:-4]
    result = []
    i = 0
    while i < len(data):
        if i + 3 <= len(data):
            b1, b2, b3 = data[i], data[i + 1], data[i + 2]
            n = (b1 << 16) | (b2 << 8) | b3
            result.append(ALPHABET[(n >> 18) & 0x3F])
            result.append(ALPHABET[(n >> 12) & 0x3F])
            result.append(ALPHABET[(n >> 6) & 0x3F])
            result.append(ALPHABET[n & 0x3F])
            i += 3
        elif i + 2 == len(data):
            b1, b2 = data[i], data[i + 1]
            n = ((b1 << 8) | b2) << 2
            result.append(ALPHABET[(n >> 12) & 0x3F])
            result.append(ALPHABET[(n >> 6) & 0x3F])
            result.append(ALPHABET[n & 0x3F])
            break
        else:
            n = data[i] << 4
            result.append(ALPHABET[(n >> 6) & 0x3F])
            result.append(ALPHABET[n & 0x3F])
            break
    return "".join(result)


def download_png_kroki(text: str) -> bytes:
    """Render via Kroki (primary — POST raw text, no encoding)."""
    resp = requests.post(
        f"{KROKI_SERVER}/plantuml/png",
        data=text.encode("utf-8"),
        headers={"Content-Type": "text/plain; charset=utf-8", "User-Agent": USER_AGENT},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.content


def download_png_plantuml(text: str) -> bytes:
    """Render via public PlantUML server (fallback — encoded URL)."""
    encoded = encode_plantuml(text)
    url = f"{PLANTUML_SERVER}/png/{encoded}"
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    return resp.content


def download_png(text: str) -> bytes:
    """Try Kroki first, then PlantUML server."""
    for name, fn in [("Kroki", download_png_kroki), ("PlantUML", download_png_plantuml)]:
        try:
            data = fn(text)
            print(f"    [{name}]", end=" ")
            return data
        except Exception as e:
            print(f"    [{name} failed: {e}]", end="")
    raise RuntimeError("All renderers failed")


def png_to_jpeg(png_data: bytes, quality: int = 92) -> bytes:
    img = Image.open(BytesIO(png_data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def main(puml_path: str, output_dir: str):
    path = Path(puml_path)
    content = path.read_text(encoding="utf-8")

    pattern = re.compile(r"@startuml\s+(\w+)\s*\n(.*?)@enduml", re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print("No @startuml blocks found.")
        sys.exit(1)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for name, diagram_text in matches:
        full_text = f"@startuml\n{diagram_text}@enduml"
        print(f"  {name}...", end="")

        png_data = download_png(full_text)
        jpeg_data = png_to_jpeg(png_data)

        jpeg_path = out / f"{name}.jpg"
        jpeg_path.write_bytes(jpeg_data)
        print(f"OK → {len(jpeg_data):,} bytes")

    print(f"\nDone. {len(matches)} JPEGs → {out.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <input.puml> [output_dir]")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "output")
