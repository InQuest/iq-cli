import click
from pathlib import Path
import simplejson as json
import sys

import api
from cli import cli, min_polling_period


@cli.group()
def file():
    pass


@file.command()
@click.option('-l', '--limit', type=int)
@click.option('--eventid')
@click.option('--signature-name')
@click.option('--signature-category')
def search(limit, eventid, signature_name, signature_category):
    search_result = api.search.files(
        limit=limit,
        eventid=eventid,
        signature_name=signature_name,
        signature_category=signature_category,
    )
    for entity in search_result:
        print(json.dumps(entity, indent=4))


@file.group()
def download():
    pass


@download.command('id')
@click.argument('file_id', metavar='ID')
@click.option('-o', '--output')
@click.option('--dfi-output')
def file_id(file_id, output, dfi_output):
    _validate_download_output_paths(output, dfi_output)
    return api.file.download_by_id(file_id, output, dfi_output)


@download.command('hash')
@click.argument('file_hash', metavar='HASH')
@click.option('-o', '--output')
@click.option('--dfi-output')
def file_hash(file_hash, output, dfi_output):
    _validate_download_output_paths(output, dfi_output)
    return api.file.download_by_hash(file_hash, output, dfi_output)


@file.command()
@click.argument('local_file_path', metavar='PATH')
@click.option('-pp', '--polling-period', type=int, default=60)
@click.option('-tt', '--timeout-threshold', type=int, default=600)
def scan(local_file_path, polling_period, timeout_threshold):
    if not Path(local_file_path).exists():
        print(f'File not found: {local_file_path}')
        sys.exit(1)
    if polling_period < min_polling_period:
        print(f'Error: please specify polling period of at least {min_polling_period} seconds')
        sys.exit(1)

    file_record = api.file.scan(local_file_path, polling_period, timeout_threshold)
    if not file_record:
        print('Error: could not fetch file record. Check your local system clock settings and try again later')
        sys.exit(2)
    print(json.dumps(file_record, indent=4))


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
