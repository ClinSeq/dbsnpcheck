# dbsnpcheck

[![Build Status](https://travis-ci.org/clinseq/dbsnpcheck.svg?branch=master)](https://travis-ci.org/clinseq/dbsnpcheck)
[![Coverage Status](https://coveralls.io/repos/github/clinseq/dbsnpcheck/badge.svg?branch=master)](https://coveralls.io/github/clinseq/dbsnpcheck?branch=master)

`dbsnpcheck` is a python package which counts the number of somatic SNVs in an input file are present in a dbSNP (or other) VCF file. It's useful for identifying cases with potential contamination of the tumor in a tumor/normal pair, which can cause an excess of somatic calls to be generated, overlaping known germline sites.

Make sure to use dbSNP with somatic variants removed, such as `common_all`, or filter `All` on the `SAO` INFO field. See `https://www.ncbi.nlm.nih.gov/variation/docs/human_variation_vcf/` and `https://www.ncbi.nlm.nih.gov/variation/docs/glossary/` for further information 

# Installation

`pip install git+https://github.com/clinseq/dbsnpcheck`

# Examples

~~~bash
dbsnpcheck --input somatic.vcf.gz --dbsnp dbsnp.vcf.gz 
~~~

# File requirements

`dbsnpcheck` requires the vcf files to be compressed with `bgzip` and indexed with `tabix` in order to work. This is required for the random access to variants provided by the index, which gives a significant performance increase over using non-indexed vcf files.
