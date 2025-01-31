from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import json
import csv


class BCDMIterator:
    """Iterator for BCDM (Barcode Data Matrix) formatted files."""

    def __init__(self, handle):
        self.handle = handle

    def _create_seqrecord(self, record):
        seq = Seq(record.get("nucraw", ""))
        id = record.get("processid", "")
        name = record.get("sampleid", "")
        description = record.get("identification", "")

        seqrecord = SeqRecord(seq, id=id, name=name, description=description)

        seqrecord.annotations["molecule_type"] = "DNA"
        seqrecord.annotations["taxonomy"] = [
            record.get("kingdom", ""),
            record.get("phylum", ""),
            record.get("class", ""),
            record.get("order", ""),
            record.get("family", ""),
            record.get("subfamily", ""),
            record.get("genus", ""),
            record.get("species", ""),
            record.get("subspecies", ""),
        ]

        seqrecord.annotations["bcdm_fields"] = {}
        for key, value in record.items():
            if key not in ["nucraw", "processid", "sampleid", "identification"]:
                seqrecord.annotations["bcdm_fields"][key] = value

        return seqrecord


class BCDMIteratorJsonl(BCDMIterator):
    """Iterator for BCDM (Barcode Data Matrix) formatted JSON lines files."""

    def __iter__(self):
        return self._parse_json()

    def _parse_json(self):
        for line in self.handle:
            record = json.loads(line)
            yield self._create_seqrecord(record)


class BCDMIteratorTsv(BCDMIterator):
    """Iterator for BCDM (Barcode Data Matrix) formatted TSV files."""

    def __iter__(self):
        return self._parse_tsv()

    def _parse_tsv(self):
        tsv_reader = csv.DictReader(self.handle, delimiter="\t")
        for record in tsv_reader:
            yield self._create_seqrecord(record)


# Add the BCDM parser to Biopython's SeqIO
SeqIO._FormatToIterator["bcdm-jsonl"] = BCDMIteratorJsonl
SeqIO._FormatToIterator["bcdm-tsv"] = BCDMIteratorTsv
