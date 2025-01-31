# `nbitk`: Naturalis BioInformatics ToolKit

This project is intended as a foundational toolkit for bioinformatics research at Naturalis Biodiversity Center. The 
toolkit is written in Python and is designed to be easy to use and easy to extend.

## The Big Idea

BioPython has good support for a lot of bioinformatics use cases. For example, for reading and writing standard DNA
sequence file formats, `Bio.SeqIO` is the go-to solution. However, we at Naturalis also operate on formats that are not 
supported by biopython, such as BCDM, or spreadsheets, or JSON files, and we have a need for more attributes on 
certain object than provided by BioPython. Rather than reinventing the wheel for those formats and passing around 
non-standard sequence objects (e.g. a dict or whatever), the sensible thing would be to build up a common toolkit that 
extends biopython for those use cases. 

This toolkit is intended to provide such functionality. It is not intended to replace BioPython, but to extend it.
It is meant to be stable and relatively lightweight, so we mean to be quite hesitant to add features that are not
likely to be needed for a lot of use cases. As some examples for use cases that we _do_ want to support:

- Reading and writing taxonomic trees from formats not yet supported by BioPython. For example: DarwinCore 
  representations such as the Dutch species register; taxonomic trees implied by custom FASTA headers;
  taxonomic lineages and trees produced by various (web) services for taxonomic name resolution.
- Reading and writing sequences from formats not yet supported by BioPython. For example: JSON files produced by
  barcoding and metabarcoding pipelines.
- Interactions with services within the Naturalis architecture, such as S3 buckets, DataBricks, LIMS, Galaxy, etc.

However, anything that is likely to require a lot of maintenance to stay up to date (such as wrappers around tools
that are frequently updated) is probably not a good fit for this toolkit.

## Who is this for?

The principal users and developers of this toolkit are the bioinformaticians at Naturalis Biodiversity Center.
Design changes and feature requests should therefore be discussed with the bioinformatics team.

## Installation

The toolkit is intended to be released on PyPI and can be installed using pip:

```bash
pip install nbitk
```

To minimize dependency hell, the general idea is _not_ to release the toolkit itself on conda with loads of
dependencies. Rather, we will release the toolkit on PyPI and let the user install the dependencies they need
themselves. This way, we can keep the toolkit lightweight and easy to install.

## Usage

The toolkit is meant for programmatic use. It is not intended to be used as a command line tool. Consult the
various modules and classes for documentation on how to use the toolkit. In addition, the scripts in the 
`tests` directory provide examples of how to use the toolkit.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for 
submitting pull requests to us.