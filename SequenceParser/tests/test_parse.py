import pytest
from SequenceParser.parse import PairedEndIllumina


@pytest.fixture(scope="session")
def sequence_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data")
    (fn / "test.fastq").touch()
    (fn / "weird_key.fastq").touch()
    (fn / "weird.fastq").touch()
    [print(x) for x in fn.glob("*")]
    return str(fn)


@pytest.fixture(scope="session")
def empty_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("empty")
    return str(fn)


def test_gather_file_names_no_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names()
    assert tmp_class.file_names == ["test.fastq", "weird_key.fastq", "weird.fastq"]


def test_gather_file_names_with_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names(keyword="key")
    assert tmp_class.file_names == ["weird_key.fastq"]


def test_gather_file_names_empty_dir(empty_dir):
    tmp_class = PairedEndIllumina(empty_dir)
    with pytest.raises(ValueError) as excinfo:
        tmp_class.gather_file_names()


def test_paired_end_illumina():
    with pytest.raises(ValueError) as excinfo:
        PairedEndIllumina("/path/to/not_a_dir")
