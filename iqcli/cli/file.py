import click
from pathlib import Path
import sys

import iqcli.api
from iqcli.cli import cli, format_search_results_as_json_array


@cli.group()
def file():
    pass


@file.command()
@click.option('-l', '--limit', type=int, default=iqcli.api.default_limit, show_default=True)
@click.option('--eventid')
@click.option('--signature-name')
@click.option('--signature-category')
@format_search_results_as_json_array
def search(limit, eventid, signature_name, signature_category):
    return iqcli.api.search.files(
        limit=limit,
        eventid=eventid,
        signature_name=signature_name,
        signature_category=signature_category,
    )


@file.group()
def download():
    pass


@download.command('id')
@click.argument('file_id', metavar='ID')
@click.option('-o', '--output')
@click.option('--dfi-output')
def file_id(file_id, output, dfi_output):
    _validate_download_output_paths(output, dfi_output)
    return iqcli.api.file.download_by_id(file_id, output, dfi_output)


@download.command('hash')
@click.argument('file_hash', metavar='HASH')
@click.option('-o', '--output')
@click.option('--dfi-output')
def file_hash(file_hash, output, dfi_output):
    _validate_download_output_paths(output, dfi_output)
    return iqcli.api.file.download_by_hash(file_hash, output, dfi_output)


@file.command()
@click.argument('local_file_path', metavar='PATH')
def scan(local_file_path):
    if not Path(local_file_path).exists():
        print(f'File not found: {local_file_path}')
        sys.exit(1)
    
    print(iqcli.api.file.scan(local_file_path))


def _validate_download_output_paths(output=None, dfi_output=None):
    if output is not None:
        target_dir = Path(output).parent
        
        if not Path(target_dir).exists():
            print(f'Error: directory does not exist: {target_dir}')
            sys.exit(-1)

    if dfi_output is not None:
        if not Path(dfi_output).exists():
            print(f'Error: directory does not exist: {dfi_output}')
            sys.exit(-1)
        
        if not Path(dfi_output).is_dir():
            print(f'Error: {dfi_output} is not a directory')
            sys.exit(-1)
