# dbsnpcheck

[![Build Status](https://travis-ci.org/ClinSeq/dbsnpcheck.svg?branch=master)](https://travis-ci.org/ClinSeq/dbsnpcheck)

`dbsnpcheck` is a python package which counts the number of somatic SNVs in an input file are present in a dbSNP (or other) VCF file. It's useful for identifying cases with potential contamination of the tumor in a tumor/normal pair, which can cause an excess of somatic calls to be generated, overlaping known germline sites.

Make sure to use dbSNP with somatic variants removed, such as `common_all`, or filter `All` on the `SAO` INFO field. See `https://www.ncbi.nlm.nih.gov/variation/docs/human_variation_vcf/` and `https://www.ncbi.nlm.nih.gov/variation/docs/glossary/` for further information 

# Installation

~~~bash
pip install git+https://github.com/clinseq/dbsnpcheck
~~~

`dbsnpcheck` supports Python versions 2.7, 3.4 and 3.5.

# Examples

~~~bash

dbsnpcheck --input somatic.vcf.gz --dbsnp dbsnp.vcf.gz --output results.json

~~~

The output json file will look like so: 

~~~
{
    "frac_in_dbsnp": 0.2
    "n_in_dbsnp": 4,
    "n_somatic_variants": 20,
}
~~~

# Input file requirements

`dbsnpcheck` requires the vcf files to be compressed with `bgzip` and indexed with `tabix` in order to work. This is required for the random access to variants provided by the index, which gives a significant performance increase over using non-indexed vcf files.
