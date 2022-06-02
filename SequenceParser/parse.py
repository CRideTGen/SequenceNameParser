import pathlib
from dataclasses import dataclass
from typing import Protocol
# from abc import ABC, abstractmethod
@dataclass
class FileParts:
    pass

class FileType(Protocol):
    file_dir: pathlib.Path
    file_names: list[str]
    filename_parts: dict

    def gather_file_names(self, keyword: str) -> None:
        ...


class PairedEndIllumina(FileType):
    def __init__(self, file_path: str) -> None:
        self.file_dir = pathlib.Path(file_path)

        if not self.file_dir.is_dir():
            raise ValueError(f"{self.file_dir} is not a valid directory.")

        self.file_names = []
        self.filename_parts = dict()

    def gather_file_names(self, keyword: str = None) -> None:
        if keyword:
            file_names = self.file_dir.glob(f"*{keyword}*fastq*")
        else:
            file_names = self.file_dir.glob(f"*.fastq*")

        self.file_names = [file.name for file in file_names]

        if not self.file_names:
            raise ValueError(f"{self.file_dir} is empty.")


def parser_illumina_sdsi(parser: FileType) -> dict:
    parser.gather_file_names("SDSI")



if __name__ == "__main__":
    t_filetype = PairedEndIllumina("weird")
    parser_illumina_sdsi(parser=t_filetype)
