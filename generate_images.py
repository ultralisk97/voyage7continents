#!/usr/bin/env python3
"""Generate article images via Google Imagen 4.

Reads the API key from the env var GOOGLE_API_KEY (never committed).
Prompts structure follows PLAYBOOK_SEO_TECHNIQUE.md §11.7.

Usage:
    export GOOGLE_API_KEY=...
    python3 generate_images.py <slug> <category>
    # Then edit the PROMPTS block in this file before each run.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "img", "articles")
os.makedirs(OUT_DIR, exist_ok=True)

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("ERROR: set GOOGLE_API_KEY env var before running")

# Imagen 4 Standard (cheaper). Switch to imagen-4.0-ultra-generate-001 for Ultra.
MODEL = os.environ.get("IMAGEN_MODEL", "imagen-4.0-generate-001")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict"

SLUG = sys.argv[1] if len(sys.argv) > 1 else "lima-machu-picchu-pas-cher"

# Edit these 4 prompts per article (cover 16:9 + 3 inline 4:3).
# Anti-AI rules: real camera, candid/amateur style, natural imperfections.
# See PLAYBOOK_SEO_TECHNIQUE.md §11.7 for full guidance.
PROMPTS = [
    (
        "1",
        "16:9",
        "iPhone 15 Pro handheld travel snapshot of Machu Picchu ancient Inca citadel, "
        "morning overcast light with drifting clouds, Huayna Picchu peak partially hidden "
        "in mist, stone walls slightly wet, green terraces, a few tourists at the edge of "
        "frame for scale, unposed composition, subtle motion blur, slight lens flare, "
        "natural uneven light, Flickr travel blog look, NO TEXT",
    ),
    (
        "2",
        "4:3",
        "Fuji X100V travel photo from a bus window: winding Andean highway between Lima "
        "and Cusco, long-distance coach on the road, dusty mountains, scattered clouds, "
        "mid-afternoon soft haze, subtle reflection on the window glass, candid handheld "
        "shot, slight film grain, imperfect framing, backpacker perspective, NO TEXT",
    ),
    (
        "3",
        "4:3",
        "Google Pixel smartphone snapshot along the railway tracks between Hidroeléctrica "
        "and Aguas Calientes Peru, two backpackers walking away from camera, wet wooden "
        "sleepers, lush tropical vegetation pressing in on both sides, overcast humid "
        "afternoon light, distant small waterfall, slight motion blur, candid travel "
        "photojournalism feel, ISO 800 grain, NO TEXT",
    ),
    (
        "4",
        "4:3",
        "Handheld travel snapshot of a white Peruvian minivan collectivo parked on a busy "
        "Cusco street near Antonio Lorena terminal, locals loading bags, a woman in "
        "traditional dress walking past, midday overcast light, colorful peeling shop "
        "signs in background, Andes silhouette above rooftops, documentary style, slight "
        "shadow imbalance, unposed moment, NO TEXT",
    ),
]


def generate(prompt: str, aspect: str) -> bytes:
    body = json.dumps(
        {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": aspect,
                "personGeneration": "allow_adult",
            },
        }
    ).encode()
    req = urllib.request.Request(
        URL,
        data=body,
        headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    preds = data.get("predictions") or []
    if not preds:
        raise RuntimeError(f"No predictions in response: {data}")
    b64 = preds[0].get("bytesBase64Encoded")
    if not b64:
        raise RuntimeError(f"No image bytes in prediction: {preds[0]}")
    return base64.b64decode(b64)


def main() -> None:
    for idx, aspect, prompt in PROMPTS:
        out = os.path.join(OUT_DIR, f"{SLUG}-{idx}.jpg")
        print(f"[{idx}] {aspect}  ->  {out}")
        try:
            img = generate(prompt, aspect)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.read().decode()[:600]}")
            continue
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        with open(out, "wb") as f:
            f.write(img)
        print(f"  ok ({len(img) // 1024} kB)")


if __name__ == "__main__":
    main()
