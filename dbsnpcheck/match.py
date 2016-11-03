import logging

import vcf


def match_variants(variants, dbsnp):
    """
    Get number of overlapping variants between two files (ex somatic variants and dbSNP)
    """
    vcf_reader_input = vcf.Reader(variants)
    vcf_reader_dbsnp = vcf.Reader(dbsnp)

    n_input_variants = 0
    n_input_variants_in_dbsnp = 0

    for v in vcf_reader_input:
        dbsnp_variants = vcf_reader_dbsnp.fetch(v.CHROM, v.POS - 1, v.POS + 1)

        # can be multiple ALT alleles in the input file, each will count
        for alt in v.ALT:
            n_input_variants += 1

        n_input_variants_in_dbsnp += count_matches(variant=v, dbsnp_variants=dbsnp_variants)

    logging.info("Detected {} somatic variants in the input, of which {} exists in the database VCF. ".format(
        n_input_variants, n_input_variants_in_dbsnp))

    return {'n_somatic_variants': n_input_variants,
            'n_in_dbsnp': n_input_variants_in_dbsnp,
            'frac_in_dbsnp': float(n_input_variants_in_dbsnp) / float(n_input_variants)}


def count_matches(variant, dbsnp_variants):
    """
    Return number of matches between a variant (which can have multiple ALT alleles)
    and a list of dbSNP variants.
    """

    matching_count = 0

    for dbsnp_variant in dbsnp_variants:

        for variant_alt in variant.ALT:
            for dbsnp_alt in dbsnp_variant.ALT:

                if variant.CHROM == dbsnp_variant.CHROM and \
                                variant.POS == dbsnp_variant.POS and \
                                variant_alt == dbsnp_alt:
                    matching_count += 1
                    logging.debug("{}/{} {}/{} matches {}/{} {}/{}".format(
                        variant.CHROM, variant.POS, variant.REF, variant_alt,
                        dbsnp_variant.CHROM, dbsnp_variant.POS, dbsnp_variant.REF, dbsnp_alt
                    ))

    if matching_count == 0:
        logging.debug("{}/{} {}/{} had no matches in the database VCF".format(
            variant.CHROM, variant.POS, variant.REF, variant.ALT))

    return matching_count
