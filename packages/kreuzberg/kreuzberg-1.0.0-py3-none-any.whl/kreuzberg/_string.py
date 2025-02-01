from __future__ import annotations

from charset_normalizer import detect


def safe_decode(byte_data: bytes, encoding: str | None = None) -> str:
    """Decode a byte string safely, removing invalid sequences.

    Args:
        byte_data: The byte string to decode.
        encoding: The encoding to use when decoding the byte string.

    Returns:
        The decoded string.
    """
    if not byte_data:
        return ""

    if encoding:
        try:
            return byte_data.decode(encoding, errors="ignore")
        except UnicodeDecodeError:  # pragma: no cover
            pass

    encodings = ["utf-8", "latin-1"]
    if encoding := detect(byte_data).get("encoding"):
        encodings.append(encoding)

    for encoding in encodings:
        try:
            return byte_data.decode(encoding, errors="ignore")
        except UnicodeDecodeError:  # pragma: no cover  # noqa: PERF203
            pass

    return byte_data.decode("latin-1", errors="replace")
