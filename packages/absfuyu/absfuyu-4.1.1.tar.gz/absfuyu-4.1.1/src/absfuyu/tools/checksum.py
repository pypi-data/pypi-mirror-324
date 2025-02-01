"""
Absufyu: Checksum
-----------------
Check MD5, SHA256, ...

Version: 1.1.0
Date updated: 01/02/2025 (dd/mm/yyyy)
"""

# Module level
###########################################################################
__all__ = ["Checksum", "checksum_operation"]


# Library
###########################################################################
import hashlib
from pathlib import Path
from typing import Literal

from absfuyu.core import tqdm

# Function
###########################################################################


# Deprecated
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
        while True:
            data = f.read(4096)
            if len(data) == 0:
                break
            else:
                hash_engine.update(data)
    return hash_engine.hexdigest()


class Checksum:
    def __init__(
        self,
        path: str | Path,
        hash_mode: str | Literal["md5", "sha1", "sha256", "sha512"] = "sha256",
        save_result_to_file: bool = False,
    ) -> None:
        self.path = Path(path)
        self.hash_mode = hash_mode
        self.save_result_to_file = save_result_to_file
        self.checksum_result_file_name = "checksum_results.txt"

    def _get_hash_engine(self):
        hash_mode = self.hash_mode
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
        return hash_engine

    def _checksum_operation(
        self,
        file: Path | str,
    ) -> str:
        """This performs checksum"""

        hash_engine = self._get_hash_engine().copy()
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
        return hash_engine.hexdigest()  # type: ignore

    def checksum(self, recursive: bool = True) -> str:
        """Perform checksum

        Parameters
        ----------
        recursive : bool, optional
            Do checksum for every file in the folder (including child folder), by default True

        Returns
        -------
        str
            Checksum hash
        """
        if self.path.absolute().is_dir():
            new_path = self.path.joinpath(self.checksum_result_file_name)
            # List of files
            if recursive:
                file_list: list[Path] = [
                    x for x in self.path.glob("**/*") if x.is_file()
                ]
            else:
                file_list = [x for x in self.path.glob("*") if x.is_file()]

            # Checksum
            res = []
            for x in tqdm(file_list, desc="Calculating hash", unit_scale=True):
                name = x.relative_to(self.path)
                res.append(f"{self._checksum_operation(x)} | {name}")
            output = "\n".join(res)
        else:
            new_path = self.path.with_name(self.checksum_result_file_name)
            output = self._checksum_operation(self.path)

        # Save result
        if self.save_result_to_file:
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(output)

        return output


# Run
###########################################################################
if __name__ == "__main__":
    pass
