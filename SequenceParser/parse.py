import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class FileParts:
    prefix: str
    sample_name: str
    s_part: str
    read_direction: str
    suffix: str

    def __init__(self, filename):
        self.prefix = self.get_prefix(filename)
        self.sample_name = self.get_sample_name(filename)
        self.s_part = self.get_s_part(filename)
        self.read_direction = self.get_read_direction(filename)
        self.suffix = self.get_suffix(filename)

    def get_prefix(self, filename: str) -> str:
        match = re.search(r"(.*-)[0-9A-Za-z]_", filename)
        return match.group(1)

    def get_sample_name(self, filename: str) -> str:
        match = re.search(r"[0-9A-Za-z]_.*M[2,3]", filename)
        return match.group(0)

    def get_s_part(self, filename: str) -> str:
        match = re.search(r"_S[0-9]{1,3}_", filename)
        return match.group(0)

    def get_read_direction(self, filename: str) -> str:
        match = re.search(r"_(R[1,2])_", filename)
        return match.group(1)

    def get_suffix(self, filename: str) -> str:
        match = re.search(r"_001[.].*", filename)
        return match.group(0)


class FileType(Protocol):
    file_dir: Path
    file_names: dict[str, list[str]]
    filename_parts: list[FileParts]

    def gather_file_names(self, keyword: str) -> None:
        ...

    def parse_file_names(self):
        ...


class PairedEndIllumina:
    def __init__(self, file_path: str) -> None:
        self.file_dir = Path(file_path)

        if not self.file_dir.is_dir():
            raise ValueError(f"{self.file_dir} is not a valid directory.")

        self.file_names = dict()
        self.file_parts = list()

    def gather_file_names(self, keyword: str = None) -> None:
        if keyword:
            forward_reads = self.file_dir.glob(f"*{keyword}*R1*fastq*")
            reverse_reads = self.file_dir.glob(f"*{keyword}*R2*fastq*")
        else:
            forward_reads = self.file_dir.glob(f"*R1*fastq*")
            reverse_reads = self.file_dir.glob(f"*R2*fastq*")

        self.file_names["forward_reads"] = [file.name for file in forward_reads]
        self.file_names["reverse_reads"] = [file.name for file in reverse_reads]

        if not self.file_names["forward_reads"] and not self.file_names["reverse_reads"]:
            raise ValueError(f"{self.file_dir} is empty.")

    def parse_file_names(self):

        pass
