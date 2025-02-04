"""
kmers_utils
===========

This module provides utility functions for working with k-mers.

Contents:
    * kmers_difference: Calculate the difference in k-mers between two defaultdicts.
    * kmers_intersections: Calculate the intersection in k-mers between two defaultdicts.

Note:
This module assumes that the input sequence contains characters from the \
DNA alphabet ('ACTG') by default. Custom alphabets can be specified using \
the 'dictionary' parameter.

Todo:
    * Implement tests.
"""
from collections import defaultdict


def kmers_difference(
    seq_kmers: defaultdict, ref_kmers: defaultdict
) -> list[str]:
    """
    Calculate the difference in k-mers between two defaultdicts.

    This function takes two defaultdicts containing k-mers and their frequency positions counts,
    calculates the k-mer differences between them, and returns a list of k-mers that
    are present in the 'seq_kmers' defaultdict but not in the 'ref_kmers' defaultdict.

    Args:
        seq_kmers (defaultdict): A defaultdict mapping k-mers to their frequency counts
                                 in the sequence data.
        ref_kmers (defaultdict): A defaultdict mapping k-mers to their frequency counts
                                 in the reference data.

    Returns:
        list[str]: A list of k-mers present in 'seq_kmers' but not in 'ref_kmers'.
    """
    seq = set(seq_kmers)
    ref = set(ref_kmers)
    return list(seq - ref)


def kmers_intersections(
    seq_kmers: defaultdict, ref_kmers: defaultdict
) -> list[str]:
    """
    Calculate the intersection in k-mers between two defaultdicts.

    This function takes two defaultdicts containing k-mers and their frequency positions counts,
    calculates the k-mer intersection between them, and returns a list of k-mers that
    are present in both defaultdicts.

    Args:
        seq_kmers (defaultdict): A defaultdict mapping k-mers to their frequency counts
                                 in the sequence data.
        ref_kmers (defaultdict): A defaultdict mapping k-mers to their frequency counts
                                 in the reference data.

    Returns:
        list[str]: A list of k-mers present in both defaultdicts.
    """
    seq = set(seq_kmers)
    ref = set(ref_kmers)

    return list(seq.intersection(ref))
