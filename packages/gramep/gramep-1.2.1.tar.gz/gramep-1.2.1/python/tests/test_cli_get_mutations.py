from shutil import rmtree

from gramep.cli import app
from pytest import fixture, mark
from typer.testing import CliRunner

runner = CliRunner()

REF_PATH = 'data/reference/SARS-CoV2_wuhan_refseq.fasta'
SEQ_PATH = 'data/VOCs/'
ANNOT_PATH = (
    'data/reference_annotation/GCF_009858895.2_ASM985889v3_genomic.gff'
)
SAVE_PATH = 'data/output/mutations/'


@fixture(scope='module', autouse=True)
def remove_save_path():
    rmtree('data/output/', ignore_errors=True)


def test_stdout():
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0


def test_stdout_without_version():
    result = runner.invoke(app)
    assert result.exit_code == 0


@mark.parametrize(
    'variant',
    [
        'Alpha.fasta',
        'Beta.fasta',
        'Delta.fasta',
        'Gamma.fasta',
    ],
)
def test_get_mutations_with_report_and_kmers(variant, caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + variant,
            '--apath',
            ANNOT_PATH,
            '--save-path',
            SAVE_PATH,
            '-w',
            '10',
            '-s',
            '1',
            '--create-report',
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


@mark.parametrize(
    'variant',
    [
        'Alpha.fasta',
        'Beta.fasta',
        'Delta.fasta',
        'Gamma.fasta',
    ],
)
def test_get_mutations_without_report(variant, caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + variant,
            '--apath',
            ANNOT_PATH,
            '--save-path',
            SAVE_PATH,
            '-w',
            '10',
            '-s',
            '1',
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


@mark.parametrize(
    'variant',
    [
        'Alpha.fasta',
        'Beta.fasta',
        'Delta.fasta',
        'Gamma.fasta',
    ],
)
def test_get_mutations_complete(variant, caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + variant,
            '--apath',
            ANNOT_PATH,
            '--save-path',
            SAVE_PATH,
            '-w',
            '10',
            '-s',
            '1',
            '--snps-max',
            '1',
            '-d',
            'DNA',
            '--create-report',
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


def test_get_mutations_error_no_kmers(caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + 'Omicron.fasta',
            '--apath',
            ANNOT_PATH,
            '--save-path',
            SAVE_PATH,
            '-w',
            '3',
            '-s',
            '1',
        ],
    )
    assert result.exit_code == 1
    assert 'No exclusive kmers were identified.' in caplog.text


def test_get_mutations_error_no_kmers_no_annotation(caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + 'Omicron.fasta',
            '--save-path',
            SAVE_PATH,
            '-w',
            '3',
            '-s',
            '1',
            '--create-report',
        ],
    )
    assert result.exit_code == 1
    assert 'No exclusive kmers were identified.' in caplog.text


def test_get_intersection_default(caplog):
    result = runner.invoke(
        app,
        ['get-intersection', '--save-path', SAVE_PATH],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


@mark.parametrize(
    'intersection_seletion', ['Beta-Delta', 'Beta-Alpha', 'Beta-Delta-Alpha']
)
def test_get_intersection_with_selection(intersection_seletion, caplog):
    result = runner.invoke(
        app,
        [
            'get-intersection',
            '--save-path',
            SAVE_PATH,
            '--intersection-seletion',
            intersection_seletion,
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


def test_get_mutations_all_dict(caplog):
    result = runner.invoke(
        app,
        [
            'get-mutations',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + 'Alpha.fasta',
            '--save-path',
            SAVE_PATH,
            '-w',
            '10',
            '-s',
            '1',
            '-d',
            'ALL',
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text


def test_get_only_kmers(caplog):
    result = runner.invoke(
        app,
        [
            'get-only-kmers',
            '--rpath',
            REF_PATH,
            '--spath',
            SEQ_PATH + 'Alpha.fasta',
            '-w',
            '10',
            '-s',
            '1',
            '--save-path',
            SAVE_PATH,
        ],
    )
    assert result.exit_code == 0
    assert 'Done!' in caplog.text
