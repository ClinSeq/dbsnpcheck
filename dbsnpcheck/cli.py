import json
import logging
import click

from dbsnpcheck.match import match_variants


@click.command()
@click.option('-V', '--variants', required=True, help="Input VCF file (somatic variants)", type=click.File())
@click.option('-d', '--dbsnp', required=True, help="Database VCF file (known germline variants)", type=click.File())
@click.option('-o', '--output', required=True, help="Output json file", type=click.File(mode='w'))
@click.option('--loglevel', required=False, help="Loglevel", default="INFO")
def base(variants, dbsnp, output, loglevel):
    setup_logging(loglevel)

    logging.info("Using {} and {}".format(variants, dbsnp))

    results = match_variants(variants, dbsnp)

    json.dump(results, output,
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
