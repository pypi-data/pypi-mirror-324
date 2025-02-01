"""
Absufyu: Checksum
-----------------
Check MD5, SHA256, ...

Version: 1.0.0
Date updated: 01/02/2025 (dd/mm/yyyy)
"""

# Module level
###########################################################################
__all__ = ["checksum_operation"]


# Library
###########################################################################
import hashlib
from pathlib import Path
from typing import Literal


# Function
###########################################################################
def checksum_operation(
    file: Path | str,
    hash_mode: str | Literal["md5", "sha1", "sha256", "sha512"] = "sha256",
) -> str:
    """This performs checksum"""
    if hash_mode.lower() == "md5":
        hash_engine = hashlib.md5()
    elif hash_mode.lower() == "sha1":
        hash_engine = hashlib.sha1()
    elif hash_mode.lower() == "sha256":
        hash_engine = hashlib.sha256()
    elif hash_mode.lower() == "sha512":
        hash_engine = hashlib.sha512()
    else:
        hash_engine = hashlib.md5()

    with open(Path(file), "rb") as f:
        # Read and hash the file in 4K chunks. Reading the whole
        # file at once might consume a lot of memory if it is
        # large.
        while True:
            data = f.read(4096)
            if len(data) == 0:
                break
            else:
                hash_engine.update(data)
    return hash_engine.hexdigest()


# Run
###########################################################################
if __name__ == "__main__":
    pass
