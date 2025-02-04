from gramep import __version__
from gramep.classify_utils import classify as _classify
from gramep.classify_utils import predict as _predict
from gramep.config import execute_configparser
from gramep.grid_search import grid_search as _grid_search
from gramep.mutations import get_mutations as _get_mutations
from gramep.mutations import get_only_kmers as _get_only_kmers
from gramep.mutations import (
    get_variants_intersection as _get_variants_intersection,
)
from rich.console import Console
from typer import Context, Exit, Option, Typer
from typing_extensions import Annotated

app = Typer(rich_markup_mode='rich')
console = Console()


def show_version(flag):
    if flag:
        print(f'GRAMEP version: {__version__}')
        raise Exit(code=0)


def complete_dicts():
    return ['DNA', 'RNA', 'ALL']


def complete_objective():
    return ['get-mutations', 'get-intersection', 'classify', 'predict']


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(
        False,
        '--version',
        '-v',
        callback=show_version,
        is_eager=True,
        help='Show version and exit.',
    ),
):
    message = (
        'Welcome to GRAMEP! Type gramep --help to see the available commands.'
    )
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def get_mutations(
    reference_path: Annotated[
        str,
        Option(
            '--rpath', help=':open_file_folder: Path to reference sequence.'
        ),
    ],
    sequence_path: Annotated[
        str, Option('--spath', help=':open_file_folder: Path to sequence.')
    ],
    save_path: Annotated[
        str,
        Option('--save-path', help=':open_file_folder: Path to save results.'),
    ],
    word: Annotated[
        int, Option('--word', '-w', help=':straight_ruler: Word size.')
    ],
    step: Annotated[
        int, Option('--step', '-s', help=':next_track_button: Step size.')
    ],
    annotation_path: Annotated[
        str,
        Option('--apath', help=':open_file_folder: Path to annotation file.'),
    ] = None,
    mode: Annotated[
        str,
        Option(
            '--mode',
            help=':heavy_check_mark: Mode. Options: snps (only SNPs) or indels (indels and SNPs).',
        ),
    ] = 'snps',
    snps_max: Annotated[
        int,
        Option(
            '--snps-max', help=':heavy_check_mark: Max number of SNPs allowed.'
        ),
    ] = 1,
    dictonary: Annotated[
        str,
        Option(
            '--dictonary',
            '-d',
            help=':dna::book: DNA dictionary.',
            shell_complete=complete_dicts,
        ),
    ] = 'DNA',
    create_report: Annotated[
        bool, Option('--create-report', help=':clipboard: Create report.')
    ] = False,
    chunk_size: Annotated[
        int,
        Option(
            '--chunk-size',
            help=':package: Chunk size for loading sequences.',
        ),
    ] = 100,
):
    """
    Perform k-mers analysis and optionally generate a report.
    """
    _get_mutations(
        reference_path=reference_path,
        sequence_path=sequence_path,
        annotation_path=annotation_path,
        mode=mode,
        save_path=save_path,
        word=word,
        step=step,
        snps_max=snps_max,
        dictonary=dictonary,
        create_report=create_report,
        chunk_size=chunk_size,
    )


@app.command()
def get_only_kmers(
    reference_path: Annotated[
        str,
        Option(
            '--rpath', help=':open_file_folder: Path to reference sequence.'
        ),
    ],
    sequence_path: Annotated[
        str, Option('--spath', help=':open_file_folder: Path to sequences.')
    ],
    word: Annotated[
        int, Option('--word', '-w', help=':straight_ruler: Word size.')
    ],
    step: Annotated[
        int, Option('--step', '-s', help=':next_track_button: Step size.')
    ],
    save_path: Annotated[
        str,
        Option('--save-path', help=':open_file_folder: Path to save results.'),
    ],
    dictonary: Annotated[
        str,
        Option(
            '--dictonary',
            '-d',
            help=':dna::book: DNA dictionary.',
            shell_complete=complete_dicts,
        ),
    ] = 'DNA',
    chunk_size: Annotated[
        int,
        Option(
            '--chunk-size',
            help=':package: Chunk size for loading sequences.',
        ),
    ] = 100,
):
    """
    Get only  exclusive k-mers.
    """
    _get_only_kmers(
        reference_path=reference_path,
        sequence_path=sequence_path,
        word=word,
        step=step,
        save_path=save_path,
        dictonary=dictonary,
        chunk_size=chunk_size,
    )


@app.command()
def get_intersection(
    save_path: Annotated[
        str,
        Option(
            '--save-path',
            help=':open_file_folder: Folder where the results obtained through the get-mutations subcommand were saved.',
        ),
    ],
    intersection_seletion: Annotated[
        str,
        Option(
            '--intersection-seletion',
            '-selection',
            help=":heavy_check_mark: Select intersection type. To specify the variants for intersection, provide them separated by '-'. For example: 'variant1-variant2-variant3'.",
        ),
    ] = 'ALL',
):
    """
    Get intersection between variants.
    """
    _get_variants_intersection(
        save_path=save_path, intersection_seletion=intersection_seletion
    )


@app.command()
def classify(
    word: Annotated[
        int, Option('--word', '-w', help=':straight_ruler: Word size.')
    ],
    step: Annotated[
        int, Option('--step', '-s', help=':next_track_button: Step size.')
    ],
    save_path: Annotated[
        str,
        Option('--save-path', help=':open_file_folder: Path to save results.'),
    ],
    dir_path: Annotated[
        str,
        Option(
            '--dir-path',
            '-dpath',
            help=':open_file_folder: Path to directory containing variants.',
        ),
    ],
    get_kmers: Annotated[
        bool,
        Option(
            '--get-kmers',
            help=':straight_ruler: Get only k-mers.',
        ),
    ] = False,
    reference_path: Annotated[
        str,
        Option(
            '--reference-path',
            '-rpath',
            help=':open_file_folder: Path to reference sequence.',
        ),
    ] = None,
    dictonary: Annotated[
        str,
        Option(
            '--dictonary',
            '-d',
            help=':dna::book: DNA dictionary.',
            shell_complete=complete_dicts,
        ),
    ] = 'DNA',
    chunk_size: Annotated[
        int,
        Option(
            '--chunk-size',
            help=':package: Chunk size for loading sequences.',
        ),
    ] = 100,
):
    """
    Classify variants.
    """
    _classify(
        word=word,
        step=step,
        save_path=save_path,
        dir_path=dir_path,
        get_kmers=get_kmers,
        reference_path=reference_path,
        dictonary=dictonary,
        chunk_size=chunk_size,
    )


@app.command()
def predict(
    word: Annotated[
        int, Option('--word', '-w', help=':straight_ruler: Word size.')
    ],
    step: Annotated[
        int, Option('--step', '-s', help=':next_track_button: Step size.')
    ],
    save_path: Annotated[
        str,
        Option('--save-path', help=':open_file_folder: Path to save results.'),
    ],
    predict_seq_path: Annotated[
        str,
        Option(
            '--predict-seq-path',
            '-pseqpath',
            help=':open_file_folder: Path to sequences to be predicted.',
        ),
    ],
    dir_path: Annotated[
        str,
        Option(
            '--dir-path',
            '-dpath',
            help=':open_file_folder: Path to directory containing the files.',
        ),
    ],
    dictonary: Annotated[
        str, Option('--dict', '-d', help=':dna::book: DNA dictionary.')
    ],
    load_ranges_path: Annotated[
        str,
        Option(
            '--load-ranges-path',
            '-lrpath',
            help=':open_file_folder: Path to ranges file.',
        ),
    ],
    load_model_path: Annotated[
        str,
        Option(
            '--load-model-path',
            '-lmpath',
            help=':open_file_folder::robot: Path to model file.',
        ),
    ],
    chunk_size: Annotated[
        int,
        Option(
            '--chunk-size',
            help=':package: Chunk size for loading sequences.',
        ),
    ] = 100,
):
    """
    Predict variants.
    """
    _predict(
        word=word,
        step=step,
        save_path=save_path,
        predict_seq_path=predict_seq_path,
        dir_path=dir_path,
        dictonary=dictonary,
        load_ranges_path=load_ranges_path,
        load_model_path=load_model_path,
        chunk_size=chunk_size,
    )


@app.command()
def from_configfile(
    objetive: Annotated[
        str,
        Option(
            '--objective',
            '-o',
            help=':memo: Objective. Options: get-mutations, get-intersection, classify, predict or phylogenic.',
            shell_complete=complete_objective,
        ),
    ],
    config_file: Annotated[
        str,
        Option(
            '--config-file',
            '-c',
            help=':open_file_folder: Path to config file.',
        ),
    ],
):
    """
    Execute GRAMEP from a config file.
    """
    execute_configparser(objective=objetive, config_file=config_file)


@app.command()
def grid_search(
    reference_path: Annotated[
        str,
        Option(
            '--rpath', help=':open_file_folder: Path to reference sequence.'
        ),
    ],
    sequence_path: Annotated[
        str, Option('--spath', help=':open_file_folder: Path to sequence.')
    ],
    min_word: Annotated[
        int,
        Option(
            '--min-word',
            '-minw',
            help=':straight_ruler::heavy_minus_sign: Min word size.',
        ),
    ],
    max_word: Annotated[
        int,
        Option(
            '--max-word',
            '-maxw',
            help=':straight_ruler::heavy_plus_sign: Max word size.',
        ),
    ],
    min_step: Annotated[
        int,
        Option(
            '--min-step',
            '-mins',
            help=':next_track_button::heavy_minus_sign: Min step size.',
        ),
    ],
    max_step: Annotated[
        int,
        Option(
            '--max-step',
            '-maxs',
            help=':next_track_button::heavy_plus_sign: Max step size.',
        ),
    ],
    dictonary: Annotated[
        str,
        Option(
            '--dictonary',
            '-d',
            help=':dna::book: DNA dictionary.',
            shell_complete=complete_dicts,
        ),
    ] = 'DNA',
):
    """
    Perform grid search to suggest a value for word and step size.
    """
    _grid_search(
        reference_path=reference_path,
        sequence_path=sequence_path,
        min_word=min_word,
        max_word=max_word,
        min_step=min_step,
        max_step=max_step,
        dictonary=dictonary,
    )
