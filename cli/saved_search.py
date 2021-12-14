import click

import api
from cli import cli, format_search_results_as_json_array


@cli.command()
@click.argument('search_id', metavar='ID')
@click.option('-l', '--limit', type=int, default=25, show_default=True)
@format_search_results_as_json_array
def saved_search(search_id, limit):
    return api.search.saved(id=search_id, limit=limit)
