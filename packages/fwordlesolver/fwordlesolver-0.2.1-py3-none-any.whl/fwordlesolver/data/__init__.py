import gzip
from importlib import resources


all_words = []

with resources.open_binary("fwordlesolver.data", "sowpods.txt.gz") as fo:
    all_words = gzip.decompress(fo.read()).decode("utf-8").splitlines()


__all__ = ["all_words"]
