"""mutations module.

This module contains the functions used to get the mutates from sequences using the
maximum entropy principle.

Contents:
    * get_mutations: Perform mutation analysis on sequence data.
    * get_variants_intersection: Get the intersection of variants.

Todo:
    * Implement tests.
"""
from collections import defaultdict
from sys import exit

from gramep.analysis import mutations_analysis, variants_analysis
from gramep.data_io import (
    annotation_dataframe,
    load_sequences,
    save_diffs_positions,
    save_exclusive_kmers,
    save_intersection_kmers,
    write_frequencies,
    write_report,
)
from gramep.graphics import plot_graphic
from gramep.kmers_utils import kmers_difference, kmers_intersections
from gramep.messages import Messages
from gramep.utilrs import get_freq_kmers

message = Messages()
"""
Set the Message class for logging.
"""


def get_mutations(
    reference_path: str,
    sequence_path: str,
    save_path: str,
    word: int,
    step: int,
    annotation_path: str | None = None,
    mode: str = 'snps',
    snps_max: int = 1,
    dictonary: str = 'DNA',
    create_report: bool = False,
    chunk_size: int = 100,
):
    """
    Perform mutation analysis on sequence data.

    This function performs mutation analysis on the provided sequence data.\
    It calculates variations, k-mer frequencies, and other relevant\
    information based on the input parameters.

    Args:
        reference_path (str): The path to the reference sequence data file.
        sequence_path (str): The path to the sequence data file.
        save_path (str): The path to save the generated results.
        word (int): The length of each k-mer.
        step (int): The step size for moving the sliding window.
        annotation_path (str): The path to the annotation data file.
        snps_max (int, optional): The maximum number of allowed SNPs within \
        an exclusive k-mer. Default is 1.
        dictonary (str, optional): The DNA dictionary for k-mer analysis. \
        Default is 'DNA'.
        create_report (bool, optional): Whether to create a report. Default is False.
        chunk_size (int, optional): The chunk size for loading sequences. \
        Default is 100.

    Returns:
        Message class: A message confirming the analysis was completed.
    """

    message.info_start_objetive('get-mutations method')

    # Check if report will be generated
    annotation_df, sequence_interval = None, None
    if create_report:
        if annotation_path is not None:
            annotation_df, sequence_interval = annotation_dataframe(
                annotation_path=annotation_path
            )
        else:
            message.warning_annotation_file()
            annotation_df, sequence_interval = None, None

    seq_kmers = load_sequences(
        file_path=sequence_path,
        word=word,
        step=step,
        dictonary=dictonary,
        reference=False,
        chunk_size=chunk_size,
    )
    ref_kmers = load_sequences(
        file_path=reference_path,
        word=word,
        step=step,
        dictonary=dictonary,
        reference=True,
        chunk_size=chunk_size,
    )

    seq_kmers_exclusive = kmers_difference(seq_kmers, ref_kmers)
    seq_kmers_intersections = kmers_intersections(seq_kmers, ref_kmers)

    save_exclusive_kmers(
        sequence_path=sequence_path,
        seq_kmers_exclusive=seq_kmers_exclusive,
        save_path=save_path,
    )
    save_intersection_kmers(
        sequence_path=sequence_path,
        seq_kmers_intersections=seq_kmers_intersections,
        save_path=save_path,
    )

    del ref_kmers
    # Analize kmers
    message.info_founded_exclusive_kmers(len(seq_kmers_exclusive))
    message.info_get_kmers()
    message.info_wait()

    diffs_positions, report = mutations_analysis(
        seq_path=sequence_path,
        ref_path=reference_path,
        seq_kmers_exclusive=seq_kmers_exclusive,
        kmers_positions=seq_kmers,
        word=word,
        step=step,
        snps_max=snps_max,
        annotation_dataframe=annotation_df,
        sequence_interval=sequence_interval,
        mode=mode,
        create_report=create_report,
        chunk_size=chunk_size,
    )

    if diffs_positions is None:
        variations = []
        save_diffs_positions(
            sequence_path=sequence_path,
            ref_path=reference_path,
            variations=variations,
            save_path=save_path,
        )
        write_report(
            report=[], sequence_path=sequence_path, save_path=save_path
        )
        message.error_no_exclusive_kmers()
        exit(1)

    freq_kmers, variations = get_freq_kmers(diffs_positions)

    save_diffs_positions(
        sequence_path=sequence_path,
        ref_path=reference_path,
        variations=variations,
        save_path=save_path,
    )

    if create_report:
        write_report(
            report=report, sequence_path=sequence_path, save_path=save_path
        )

    write_frequencies(
        freq_kmers=freq_kmers, sequence_path=sequence_path, save_path=save_path
    )

    if len(variations) > 100:
        message.warning_no_plot()
        return message.info_done()

    plot_graphic(
        variations=variations,
        reference_path=reference_path,
        freq_kmers=freq_kmers,
        sequence_name=sequence_path,
        save_path=save_path,
    )
    return message.info_done()


def get_only_kmers(
    reference_path: str,
    sequence_path: str,
    word: int,
    step: int,
    save_path: str,
    dictonary: str = 'DNA',
    chunk_size: int = 100,
) -> list[str]:
    """
    Extract only exclusive k-mers from sequences.
    
    This function extracts only exclusive k-mers from the provided sequence data.\
    It calculates exclusive k-mers based on the input parameters.
    
    Args:
        reference_path (str): The path to the reference sequence data file.
        sequence_path (str): The path to the sequence data file.
        word (int): The length of each k-mer.
        step (int): The step size for moving the sliding window.
        dictonary (str, optional): The DNA dictionary for k-mer analysis. \
        Default is 'DNA'.
        save_path (str|None, optional): The path to save the generated results. Default is None.
        chunk_size (int, optional): The chunk size for loading sequences. \
        Default is 100.
        
    Returns:
        list[str]: A list of exclusive k-mers.
    """
    message.info_start_objetive('get-only-kmers method')
    seq_kmers = load_sequences(
        file_path=sequence_path,
        word=word,
        step=step,
        dictonary=dictonary,
        reference=False,
        chunk_size=chunk_size,
    )
    ref_kmers = load_sequences(
        file_path=reference_path,
        word=word,
        step=step,
        dictonary=dictonary,
        reference=True,
        chunk_size=chunk_size,
    )

    seq_kmers_exclusive = kmers_difference(seq_kmers, ref_kmers)
    message.info_founded_exclusive_kmers(len(seq_kmers_exclusive))

    save_exclusive_kmers(
        sequence_path=sequence_path,
        seq_kmers_exclusive=seq_kmers_exclusive,
        save_path=save_path,
    )
    message.info_done()

    return seq_kmers_exclusive


def get_variants_intersection(
    save_path: str, intersection_seletion: str = 'ALL'
) -> defaultdict[str, list[str]]:
    """
    Get variants intersection based on selection criteria.

    This function retrieves variants intersection data based on the specified \
    selection criteria.
    The function reads data from the provided save path and performs intersection \
    calculations
    according to the chosen selection option.

    Args:
        save_path (str): The path to the directory containing data to process.
        intersection_seletion (str, optional): The selection criteria for variants \
        intersection. Options: 'ALL' (default).

    Returns:
        defaultdict[str, list[str]]: A dictionary mapping sequence IDs to lists of \
        variants based on the specified selection criteria.
    
    Todo:
        * Rewrite in Rust.
    """

    message.info_start_objetive('get_variants_intersection method')
    variants_intersections = variants_analysis(
        save_path, intersection_seletion
    )
    message.info_done()
    return variants_intersections
