import pytest
from SequenceParser.parse import PairedEndIllumina, FileParts


@pytest.fixture(scope="session")
def sequence_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data")
    (fn / "test_R1_001.fastq").touch()
    (fn / "weird_key_R1_001.fastq").touch()
    (fn / "weird_R1_001.fastq").touch()
    (fn / "test_R2_001.fastq").touch()
    (fn / "weird_key_R2_001.fastq").touch()
    (fn / "weird_R2_001.fastq").touch()

    return str(fn)


@pytest.fixture(scope="session")
def empty_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("empty")
    return str(fn)


def test_gather_file_names_no_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names()
    assert tmp_class.file_names["forward_reads"] == ["test_R1_001.fastq", "weird_key_R1_001.fastq",
                                                     "weird_R1_001.fastq"]
    assert tmp_class.file_names["reverse_reads"] == ["test_R2_001.fastq", "weird_key_R2_001.fastq",
                                                     "weird_R2_001.fastq"]


def test_gather_file_names_with_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names(keyword="key")
    assert tmp_class.file_names["forward_reads"] == ["weird_key_R1_001.fastq"]
    assert tmp_class.file_names["reverse_reads"] == ["weird_key_R2_001.fastq"]


def test_gather_file_names_empty_dir(empty_dir):
    tmp_class = PairedEndIllumina(empty_dir)
    with pytest.raises(ValueError) as excinfo:
        tmp_class.gather_file_names()


def test_paired_end_illumina():
    with pytest.raises(ValueError) as excinfo:
        PairedEndIllumina("/path/to/not_a_dir")


test_filename = "TGen-CoV-AZ-Tiled-C_SDSI_M2_S265_R2_001.fastq"
test_prefix = "TGen-CoV-AZ-Tiled-"
test_sample_name = "C_SDSI_M2"
test_s_part = "_S265_"
test_read_direction = "R2"
test_suffix = "_001.fastq"

test_fileparts = FileParts(test_filename)

def test_get_prefix():
    assert test_fileparts.prefix == test_prefix


def test_get_sample_name():
    assert test_fileparts.sample_name == test_sample_name


def test_get_s_part():
    assert test_fileparts.s_part == test_s_part


def test_get_read_direction():
    assert test_fileparts.read_direction == test_read_direction


def test_get_suffix():
    assert test_fileparts.suffix == test_suffix
