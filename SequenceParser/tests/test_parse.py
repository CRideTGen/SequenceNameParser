import pytest
from SequenceParser.parse import PairedEndIllumina, FileParts


@pytest.fixture(scope="session")
def sequence_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data")
    (fn / "TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R1_001.fastq").touch()
    (fn / "TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R2_001.fastq").touch()
    (fn / "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R1_001.fastq").touch()
    (fn / "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R2_001.fastq").touch()
    (fn / "TGen-CoV-AZ-Tiled-1_M2_S257_R1_001.fastq").touch()
    (fn / "TGen-CoV-AZ-Tiled-1_M2_S257_R2_001.fastq").touch()

    return str(fn)


@pytest.fixture(scope="session")
def empty_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("empty")
    return str(fn)


def test_gather_file_names_no_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names()
    assert tmp_class.file_names["forward_reads"] == ["TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R1_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R1_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_M2_S257_R1_001.fastq"]
    assert tmp_class.file_names["reverse_reads"] == ["TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R2_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R2_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_M2_S257_R2_001.fastq"]


def test_gather_file_names_with_key(sequence_dir):
    tmp_class = PairedEndIllumina(sequence_dir)
    tmp_class.gather_file_names(keyword="SDSI")
    assert tmp_class.file_names["forward_reads"] == ["TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R1_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R1_001.fastq"]

    assert tmp_class.file_names["reverse_reads"] == ["TGen-CoV-AZ-Tiled-1_SDSI_M2_S256_R2_001.fastq",
                                                     "TGen-CoV-AZ-Tiled-1_SDSI_M3_S256_R2_001.fastq"]


def test_gather_file_names_empty_dir(empty_dir):
    tmp_class = PairedEndIllumina(empty_dir)
    with pytest.raises(ValueError) as excinfo:
        tmp_class.gather_file_names()


def test_paired_end_illumina():
    with pytest.raises(ValueError) as excinfo:
        PairedEndIllumina("/path/to/not_a_dir")


@pytest.fixture(scope="session")
def fileparts_test_variables():
    test_filename1 = "TGen-CoV-AZ-Tiled-C_SDSI_M2_S265_R1_001.fastq"
    test_filename2 = "TGen-CoV-AZ-Tiled-C_SDSI_M2_S265_R2_001.fastq"
    test_filename3 = "TGen-CoV-AZ-Tiled-C_SDSI_M3_S265_R2_001.fastq"

    test_fileparts = FileParts()
    test_fileparts.parse_file(filename=test_filename1)
    test_fileparts.parse_file(filename=test_filename2)
    test_fileparts.parse_file(filename=test_filename3)
    return test_fileparts


def test_get_prefix(fileparts_test_variables):
    assert fileparts_test_variables.prefix == ["TGen-CoV-AZ-Tiled-", "TGen-CoV-AZ-Tiled-", "TGen-CoV-AZ-Tiled-"]


def test_get_sample_name(fileparts_test_variables):
    assert fileparts_test_variables.sample_name == ["C_SDSI_M2", "C_SDSI_M2", "C_SDSI_M3"]


def test_get_s_part(fileparts_test_variables):
    assert fileparts_test_variables.s_part == ["_S265_", "_S265_", "_S265_"]


def test_get_read_direction(fileparts_test_variables):
    assert fileparts_test_variables.read_direction == ["R1", "R2", "R2"]


def test_get_suffix(fileparts_test_variables):
    assert fileparts_test_variables.suffix == ["_001.fastq", "_001.fastq", "_001.fastq"]
