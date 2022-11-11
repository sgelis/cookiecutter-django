# Standard library
import unicodedata


def strip_accents(string: str) -> str:
    return unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("utf8")
