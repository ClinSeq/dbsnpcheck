import json
import logging
import click
import vcf

from dbsnpcheck.match import match_variants


@click.command()
@click.option('-V', '--variants', required=True, help="Input VCF file (somatic variants)", type=click.File())
@click.option('-d', '--dbsnp', required=True, help="Database VCF file (known germline variants)", type=click.File())
@click.option('-o', '--output', required=True, help="Output json file", type=click.File(mode='w'))
@click.option('--loglevel', required=False, help="Loglevel", default="INFO")
def base(variants, dbsnp, output, loglevel):
    setup_logging(loglevel)

    logging.info("Using {} and {}".format(variants, dbsnp))

    vcf_reader_input = vcf.Reader(variants)
    vcf_reader_dbsnp = vcf.Reader(dbsnp)

    n_input_variants = 0
    n_input_variants_in_dbsnp = 0

    for v in vcf_reader_input:
        dbsnp_variants = vcf_reader_dbsnp.fetch(v.CHROM, v.POS-1, v.POS+1)

        # can be multiple ALT alleles in the input file, each will count
        for alt in v.ALT:
            n_input_variants += 1

        n_input_variants_in_dbsnp += match_variants(variant=v, dbsnp_variants=dbsnp_variants)

    logging.info("Detected {} somatic variants in the input, of which {} exists in the database VCF. ".format(
        n_input_variants, n_input_variants_in_dbsnp))

    json.dump({'n_somatic_variants':n_input_variants,
               'n_in_dbsnp': n_input_variants_in_dbsnp,
               'frac_in_dbsnp': float(n_input_variants_in_dbsnp)/float(n_input_variants)}, output,
              sort_keys=True, indent=4)


def setup_logging(loglevel="INFO"):
    """
    Set up logging
    :param loglevel: loglevel to use, one of ERROR, WARNING, DEBUG, INFO (default INFO)
    :return:
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(levelname)s %(asctime)s %(funcName)s - %(message)s')
    logging.info("Started log with loglevel %(loglevel)s" % {"loglevel": loglevel})
