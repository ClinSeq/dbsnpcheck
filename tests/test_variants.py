import unittest

import vcf

from dbsnpcheck.match import match_variants


class TestVariants(unittest.TestCase):
    vcf = "tests/variants.vcf.gz"
    vcf_with_genotypes = "tests/variants-with-genotypes.vcf.gz"

    def test_snp_is_found(self):
        alt = vcf.model._Substitution('T')
        variant = vcf.model._Record(1, 123, '.', 'A', [alt], None,
                                    None, {}, None, {}, None)

        dbsnp_variants = [vcf.model._Record(1, 123, '.', 'A', [alt], None,
                                            None, {}, None, {}, None)]

        matching_count = match_variants(variant, dbsnp_variants)

        self.assertEqual(matching_count, 1)

    def test_does_not_count_other_alt(self):
        somatic_alt = vcf.model._Substitution('T')
        germline_alt = vcf.model._Substitution('C')

        variant = vcf.model._Record(1, 123, '.', 'A', [somatic_alt], None,
                                    None, {}, None, {}, None)

        dbsnp_variants = [vcf.model._Record(1, 123, '.', 'A', [germline_alt], None,
                                            None, {}, None, {}, None)]

        matching_count = match_variants(variant, dbsnp_variants)

        self.assertEqual(matching_count, 0)

    def test_indels_found(self):
        alt_int = vcf.model._Substitution('ATTT')
        variant_ins = vcf.model._Record(1, 123, '.', 'A', [alt_int], None,
                                        None, {}, None, {}, None)
        dbsnp_variants_ins = [vcf.model._Record(1, 123, '.', 'A', [alt_int], None,
                                                None, {}, None, {}, None)]

        matching_count = match_variants(variant_ins, dbsnp_variants_ins)
        self.assertEqual(matching_count, 1)

        alt_del = vcf.model._Substitution('G')
        variant_del = vcf.model._Record(1, 123, '.', 'GAAA', [alt_del], None,
                                        None, {}, None, {}, None)
        dbsnp_variants_del = [vcf.model._Record(1, 123, '.', 'GAAA', [alt_del], None,
                                                None, {}, None, {}, None)]

        matching_count = match_variants(variant_del, dbsnp_variants_del)
        self.assertEqual(matching_count, 1)

    def test_does_not_count_adjacent_variant(self):
        alt = vcf.model._Substitution('T')
        pos = 123

        variant = vcf.model._Record(1, pos, '.', 'A', [alt], None,
                                    None, {}, None, {}, None)
        dbsnp_variants = [vcf.model._Record(1, pos-1, '.', 'A', [alt], None,
                                            None, {}, None, {}, None)]

        matching_count = match_variants(variant, dbsnp_variants)

        self.assertEqual(matching_count, 0)
