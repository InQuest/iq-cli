import click

import iqcli.api
from iqcli.cli import cli, format_search_results_as_json_array


@cli.command()
@click.argument('search_id', metavar='ID')
@click.option('-l', '--limit', type=int, default=None, show_default=True)
@format_search_results_as_json_array
def saved_search(search_id, limit):
    return iqcli.api.search.saved(id=search_id, limit=limit)
