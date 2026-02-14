from __future__ import annotations

import base64
import hashlib


def derive_password(*, key: str, seed: str, iterations: int, length: int) -> str:
    """Derive a deterministic password from (key, seed) using PBKDF2-HMAC-SHA256."""
    if not key.strip():
        raise ValueError("key cannot be empty")
    if not seed.strip():
        raise ValueError("seed cannot be empty")
    if iterations < 1_000:
        raise ValueError("iterations must be >= 1000")
    if not (8 <= length <= 128):
        raise ValueError("length must be between 8 and 128")

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        key.encode("utf-8"),
        seed.encode("utf-8"),
        iterations,
        dklen=64,
    )
    # urlsafe to avoid + and /; strip padding
    pwd = base64.urlsafe_b64encode(derived).decode("utf-8").rstrip("=")
    return pwd[:length]
