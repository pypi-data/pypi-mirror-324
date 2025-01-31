import os
import pytest
from Bio import SeqIO
from nbitk.SeqIO.BCDM import BCDMIterator

# Paths to test files
BCDM_JSONL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'BCDM.jsonl')
BCDM_TSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'BCDM.tsv')


def test_bcdm_jsonl_parser():
    with open(BCDM_JSONL_PATH, 'r') as handle:
        records = list(SeqIO.parse(handle, 'bcdm-jsonl'))

    assert len(records) == 9  # Assuming 9 records in the file

    # Test the first record
    first_record = records[0]
    assert first_record.id == "AAASF001-17"
    assert first_record.name == "CBGSFMX-0101"
    assert first_record.description == "Lutzomyia cruciata"
    assert str(first_record.seq).startswith(
        "AACATTATATTTTATTTTTGGAGCCTGAGCAGGAATAGTGGGAACATCTTTAAGAATTTTAATTCGAGCAGAATTAGGTCACCCCGGTGCTTTAATTGGTGATGATCAAATTTATAATGTTATTGTTACAGCTCATGCATTTGTAATAATTTTTTTTATAGTTATACCTATTATAATTGGAGGATTTGGTAACTGATTAGTTCCTTTAATATTAGGAGCCCCTGATATAGCATTCCCTCGAATAAATAATATAAGATTTTGACTTTTACCCCCCTCTCTTACTCTCCTTCTTACAAGAAGTATAGTTGAAACTGGGGCAGGAACAGGATGAACTGTTTATCCACCTCTTTCAAGAAATATTGCCCATAGAGGAGCTTCTGTTGATTTAGCAATTTTTTCCCTACATTTAGCCGGGATTTCATCTATTCTTGGAGCAGTAAATTTTATTACTACAGTTATTAATATACGATCTGCTGGAATTACATTAGATCGAATACCTTTATTTGTTTGATCTGTAATAATTACTGCGGTACTTCTATTATTATCATTACCTGTTTTAGCAGGTGCAATTACAATACTTCTAACTGATCGTAATCTAAATACTTCTTTTTTTGACCCTGCGGGAGGTGGGGATCCAATTTTATATCAACATTTATTT")
    assert first_record.annotations['taxonomy'] == ['Animalia', 'Arthropoda', 'Insecta', 'Diptera', 'Psychodidae',
                                                    'Phlebotominae', 'Lutzomyia', 'Lutzomyia cruciata', 'None']
    assert first_record.annotations['bcdm_fields']['bin_uri'] == "BOLD:ADP3520"
    assert first_record.annotations['bcdm_fields']['country'] == "Mexico"
    assert first_record.annotations['bcdm_fields']['coord'] == "(19.3786,-88.1892)"


def test_bcdm_tsv_parser():
    with open(BCDM_TSV_PATH, 'r') as handle:
        records = list(SeqIO.parse(handle, 'bcdm-tsv'))

    assert len(records) == 9  # Assuming 9 records in the file

    # Test the last record
    last_record = records[-1]
    assert last_record.id == "AAASF011-17"
    assert last_record.name == "CBGSFMX-0308"
    assert last_record.description == "Lutzomyia longipalpis"
    assert str(last_record.seq).startswith(
        "AACTTTATATTTTATTTTCGGGGCTTGATCTGGAATAGTGGGGACATCCTTAAGAATTTTAATTCGAGCTGAACTCGGGCATCCTGGAGCATTAATTGGTGATGATCAAATTTATAATGTAATTGTTACAGCCCATGCTTTTGTAATAATTTTTTTTATAGTAATACCTATCATAATTGGGGGATTCGGAAATTGATTAGTTCCTTTAATATTAGGGGCCCCTGATATAGCTTTTCCTCGAATAAATAATATAAGATTCTGACTTTTACCTCCATCTTTAACTTTATTATTAACTAGAAGTATAGTAGAAACTGGAGCAGGAACAGGTTGAACTGTCTACCCACCCTTATCTAGAAATATTGCCCATAGAGGAGCTTCAGTTGATTTAGCAATTTTTTCCCTTCATTTAGCTGGAATTTCATCTATTTTAGGAGCAGTAAATTTTATTACTACAGTAATTAATATGCGATCAACAGGAATTACTTTAGACCGAATACCATTATTTGTCTGATCTGTCGTAATTACTGCAGTTCTTTTATTATTATCTCTCCCTGTTCTAGCAGGAGCTATTACTATACTTTTAACTGATCGAAATCTAAATACTTCTTTTTTTGATCCTGCTGGAGGTGGTGACCCCATTTTATACCAACACTTATTT")
    assert last_record.annotations['taxonomy'] == ['Animalia', 'Arthropoda', 'Insecta', 'Diptera', 'Psychodidae',
                                                   'Phlebotominae', 'Lutzomyia', 'Lutzomyia longipalpis', 'None']
    assert last_record.annotations['bcdm_fields']['bin_uri'] == "BOLD:AAY5017"
    assert last_record.annotations['bcdm_fields']['country'] == "Mexico"
    assert last_record.annotations['bcdm_fields']['coord'] == "(19.5855,-88.5843)"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        with open('non_existent_file.json', 'r') as handle:
            list(SeqIO.parse(handle, 'bcdm-jsonl'))


def test_empty_file():
    empty_file_path = os.path.join(os.path.dirname(__file__), 'data', 'empty.json')
    with open(empty_file_path, 'w') as f:
        pass  # Create an empty file

    with open(empty_file_path, 'r') as handle:
        records = list(SeqIO.parse(handle, 'bcdm-jsonl'))

    assert len(records) == 0

    os.remove(empty_file_path)  # Clean up


def test_record_fields():
    with open(BCDM_JSONL_PATH, 'r') as handle:
        records = list(SeqIO.parse(handle, 'bcdm-jsonl'))

    for record in records:
        assert hasattr(record, 'id')
        assert hasattr(record, 'name')
        assert hasattr(record, 'description')
        assert hasattr(record, 'seq')
        assert 'taxonomy' in record.annotations
        assert 'bcdm_fields' in record.annotations
        assert 'bin_uri' in record.annotations['bcdm_fields']
        assert 'country' in record.annotations['bcdm_fields']
        assert 'coord' in record.annotations['bcdm_fields']


if __name__ == "__main__":
    pytest.main()
