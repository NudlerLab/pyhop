# pyhop
TN-Seq analysis pipeline

# Setup

Create and activate virtual environment (wither ``pyvenv`` or ``conda``)

Clone the repo:

``git clone https://github.com/eco32i/pyhop.git``

Install development version:

``pip install -e pyhop``

# Basic usage

``pyhop`` can be used in both interactive (``jupyter`` notebook) and command line mode. See ``notebooks`` directory for example notebooks with different steps of the analysis

To run from the command line:

``dmux.py reads.fastq.gz [options]``

```
usage: dmux.py [-h] [-c CONFIG] [-t TRANSPOSON] [-s SAMPLES [SAMPLES ...]]
               [-p PROGRESS] [-d DIR]
               fastq_file

pyhop demultiplexing script Part of the pipeline for TN-Seq data analysis

positional arguments:
  fastq_file            .fastq file with reads

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file. Mutually exclusive with -s.
  -t TRANSPOSON, --transposon TRANSPOSON
                        transposon sequence
  -s SAMPLES [SAMPLES ...], --samples SAMPLES [SAMPLES ...]
                        sample:barcode mappings. Mutually exclusive with -c.
  -p PROGRESS, --progress PROGRESS
                        print progress message every this many reads.
  -d DIR, --dir DIR     output directory
  ```
