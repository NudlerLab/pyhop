#!/usr/bin/env python

import os
import gzip
import json
import argparse

from .parse import parse_fastq

def read_config(filename):
    '''
    Reads .json config file and returns dictionary corresponding to 
    ``samples`` key

    Samples section of config file must containt mappings:
        ``sample_name``: ``barcode``
    '''
    with open(filename) as fi:
        config = json.load(fi)
    return config['samples']


def hamming(s1, s2):
    '''
    Computes Hamming distance between s1 and s2.
    '''
    if len(s1) != len(s2):
        raise ValueError('s1 and s2 must be the same length to compute Hamming distance!')
    return sum(ch1 != ch2 for ch1,ch2 in zip(s1, s2))


def dmux_and_trim(fastq, samples, result_dir=None, transposon='ACAGGTTGGATGATAAG', progress=1000000):
    # This will hold output files in the form
    # `barcode`: `file handle`
    # So we keep track of them to close on exit
    output_files = {}
    stat_dict = {}
    # Then we build a list (well, set) of all barcode lengths
    bcls = {len(x) for _, x in samples.items()}
    cnt = 0
    for seqid,seq,qual in parse_fastq(fastq):
        cnt += 1
        # get barcode
        all_bc = [seq[:x] for x in bcls if seq[:x] in samples.values()]
        if len(all_bc) != 1:
            # Barcode corresponds to more than one sample or unknown barcode, drop it
            # Potentially we might want to implement error correction here
            continue
        bc = all_bc[0]
        
        # trim transposon allowing for 1 mismatch
        # check for both 14 and 15-mers
        tpos = 16 + len(bc)
        tlen = len(transposon)
        # Read is too short, skip it
        if len(seq) < tpos+tlen+1:
            continue
            
        if hamming(seq[tpos:tpos+tlen], transposon) < 2:
            seq = seq[len(bc):tpos]
            qual = qual[len(bc):tpos]
        elif hamming(seq[tpos+1:tpos+tlen+1], transposon) < 2:
            seq = seq[len(bc):tpos+1]
            qual = qual[len(bc):tpos+1]
        else:
            # No transposon sequence in the read, skip
            continue
        
        # output to corresponding file and update stat
        if not bc in output_files:
            basename = '{}_trimmed.fastq.gz'.format(bc)
            if result_dir is not None:
                out_filename = os.path.join(result_dir, basename)
            else:
                out_filename = basename
            fh = gzip.open(out_filename, 'wt')
            output_files[bc] = fh
            print('\tcreated output file:\t{}'.format(out_filename))
            
        output_files[bc].write('@{seqid}\n{seq}\n+\n{qual}\n'.format(
                seqid=seqid,
                seq=seq,
                qual=qual
            ))
        
        if not bc in stat_dict:
            stat_dict[bc] = 1
        else:
            stat_dict[bc] += 1
            
        if cnt % progress == 0:
            print('processed: {} reads...'.format(cnt))
        
    # Cleanup: close output files
    for _,fh in output_files.items():
        fh.close()
    
    return stat_dict


def main():
    parser = argparse.ArgumentParser(description='''
    pyhop demultiplexing script
    Part of the pipeline for TN-Seq data analysis
    '''
    )

    parser.add_argument('fastq_file', type=str, help='.fastq file with reads')
    parser.add_argument('-c', '--config', type=str,
            help='config file. Mutually exclusive with -s.')
    parser.add_argument('-t', '--transposon', type=str, default='ACAGGTTGGATGATAAG',
            help='transposon sequence')
    parser.add_argument('-s', '--samples', type=str, nargs='+',
            help='sample:barcode mappings. Mutually exclusive with -c.')
    parser.add_argument('-p', '--progress', type=int, default=1000000,
            help='print progress message every this many reads.')
    parser.add_argument('-d', '--dir', type=str, help='output directory')

    args = parser.parse_args()
    kwargs = vars(args)
    if 'config' in kwargs and 'samples' in kwargs:
        raise ValueError('--config and --samples options are mutually exclusive.')
    if not('config' in kwargs or 'samples' in kwargs):
        raise ValueError('Must provide either config file (--config) or samples mapping (--samples).')
    if 'config' in kwargs:
        samples = read_config(kwargs['config'])
    else:
       samples = {}
       for s in kwargs['samples']:
           try:
               sample, barcode = s.split(':')
           except ValueError:
               print("Wrong samples mapping. Must be in ``sample``:``barcode`` format.")
           samples.update({sample:barcode})
           
    stat_dict = dmux_and_trim(kwargs['fastq'], samples, result_dir,
        progress=kwargs['progress'], transposon=kwargs['transposon'])

    for sample,reads in stat_dict.items():
        print('Sample:\t{}\t-\t{} reads.'.format(sample, reads))
    print('Done.')

if __name__ == "__main__":
    main()
