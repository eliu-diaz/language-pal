"""Pre-downloads the speech models so the first mic tap does not stall.

Run once after cloning:

    uv run python fetch_models.py
"""

import sys

from speech_models import MODEL_SIZE, fetch_model, is_model_cached


def main() -> int:
    sizes = sys.argv[1:] or [MODEL_SIZE]

    for size in sizes:
        if is_model_cached(size):
            print(f"{size}: already cached")
            continue

        print(f"{size}: downloading (this is a few hundred MB, one time)...")
        path = fetch_model(size)
        print(f"{size}: ready at {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
