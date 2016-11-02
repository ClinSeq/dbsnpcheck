import logging


def match_variants(variant, dbsnp_variants):

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
