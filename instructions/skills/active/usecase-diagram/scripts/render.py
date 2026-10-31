#!/usr/bin/env python3
"""
render.py — Cross-platform PlantUML .puml to .svg compiler and renderer.

Features:
- Pure Python 3 standard library (no pip dependencies required).
- Native cross-platform execution on Windows (PowerShell/CMD), macOS, and Linux.
- PlantUML standard deflate compression + 6-bit encoding algorithm.
- Multi-tier rendering support:
  1. Local offline JAR (if PLANTUML_JAR_PATH environment variable is set).
  2. Private enterprise server (if PLANTUML_SERVER_URL is set).
  3. Public fallback server (https://www.plantuml.com/plantuml/svg/).
- Built-in syntax error detection and SVG validation.

Usage:
    python render.py <path/to/diagram.puml> [--out <path/to/diagram.svg>]
"""

import os
import sys
import zlib
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

# PlantUML custom 64-character alphabet (RFC 4648 base64 is NOT compatible)
_PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def _encode_6bit(b: int) -> str:
    return _PLANTUML_ALPHABET[b & 0x3F]


def _append_3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return _encode_6bit(c1) + _encode_6bit(c2) + _encode_6bit(c3) + _encode_6bit(c4)


def encode_plantuml(data: bytes) -> str:
    """Encode raw bytes using PlantUML 6-bit translation."""
    out = []
    length = len(data)
    for i in range(0, length, 3):
        chunk = data[i:i + 3]
        b1 = chunk[0]
        b2 = chunk[1] if len(chunk) > 1 else 0
        b3 = chunk[2] if len(chunk) > 2 else 0
        out.append(_append_3bytes(b1, b2, b3))
    return "".join(out)


def deflate_and_encode(source_text: str) -> str:
    """Apply raw Deflate compression (without zlib header/checksum) and encode."""
    raw_bytes = source_text.encode("utf-8")
    # Compress with level 9 and strip 2-byte header + 4-byte Adler32 checksum
    compressed = zlib.compress(raw_bytes, 9)[2:-4]
    return encode_plantuml(compressed)


def render_local_jar(src_path: Path, out_path: Path, jar_path: str) -> bool:
    """Render .puml using local plantuml.jar via Java runtime."""
    print(f"[*] Rendering via local PlantUML JAR: {jar_path}")
    try:
        cmd = ["java", "-jar", jar_path, "-tsvg", str(src_path), "-o", str(out_path.parent)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            print(f"[!] PlantUML JAR failed with exit code {res.returncode}:\n{res.stderr}", file=sys.stderr)
            return False
        return True
    except FileNotFoundError:
        print("[!] Java runtime not found on PATH. Cannot execute local JAR.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[!] Error running local JAR: {e}", file=sys.stderr)
        return False


def render_http(source_text: str, out_path: Path) -> bool:
    """Render .puml by querying PlantUML HTTP server."""
    server_base = os.environ.get("PLANTUML_SERVER_URL", "https://www.plantuml.com/plantuml/svg/").strip()
    if not server_base.endswith("/"):
        server_base += "/"

    encoded = deflate_and_encode(source_text)
    target_url = server_base + encoded

    is_public = "plantuml.com" in server_base
    if is_public:
        print(f"[*] Dispatching render request to public server (plantuml.com)...")
    else:
        print(f"[*] Dispatching render request to custom server: {server_base}")

    req = urllib.request.Request(
        target_url,
        headers={
            "User-Agent": "Directive-PlantUML-Renderer/1.0",
            "Accept": "image/svg+xml, */*"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            status = response.status
            if status != 200:
                print(f"[!] Server returned non-200 HTTP status: {status}", file=sys.stderr)
                return False

            svg_content = response.read()

            # Verify response size
            if len(svg_content) < 200:
                print(f"[!] Returned SVG is suspiciously small ({len(svg_content)} bytes). Syntax error likely.", file=sys.stderr)
                return False

            svg_text = svg_content.decode("utf-8", errors="ignore")
            # PlantUML server returns HTTP 200 even for syntax errors, with text inside SVG
            if "Syntax Error?" in svg_text or "An error has occured" in svg_text or "[PlantUML error]" in svg_text:
                print("[!] PlantUML server generated an error SVG. Review .puml syntax for mistakes:", file=sys.stderr)
                for line in svg_text.splitlines():
                    if "<text" in line:
                        print(f"    {line.strip()}", file=sys.stderr)
                return False

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f_out:
                f_out.write(svg_content)

            return True

    except urllib.error.HTTPError as e:
        print(f"[!] HTTP error {e.code}: {e.reason}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"[!] Network connection failed: {e.reason}", file=sys.stderr)
        print("    Check internet connectivity or configure a local server / JAR.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[!] Unexpected error during HTTP render: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python render.py <source.puml> [--out <output.svg>]")
        sys.exit(0)

    src_file = Path(sys.argv[1]).resolve()
    if not src_file.exists():
        print(f"[!] Source file does not exist: {src_file}", file=sys.stderr)
        sys.exit(1)

    out_file = None
    if "--out" in sys.argv:
        try:
            out_idx = sys.argv.index("--out")
            out_file = Path(sys.argv[out_idx + 1]).resolve()
        except (ValueError, IndexError):
            print("[!] Missing path argument after --out", file=sys.stderr)
            sys.exit(1)
    else:
        out_file = src_file.with_suffix(".svg")

    with open(src_file, "r", encoding="utf-8") as f:
        puml_source = f.read()

    # Priority 1: Local JAR if configured
    local_jar = os.environ.get("PLANTUML_JAR_PATH")
    success = False
    if local_jar and os.path.exists(local_jar):
        success = render_local_jar(src_file, out_file, local_jar)
    else:
        success = render_http(puml_source, out_file)

    if success:
        print(f"[+] Successfully rendered: {out_file} ({out_file.stat().st_size} bytes)")
        sys.exit(0)
    else:
        print(f"[!] Render failed for: {src_file}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
