import click
import simplejson as json

import iqcli.api
from iqcli.cli import cli


@cli.group()
def session():
    pass


@session.command()
@click.argument('session_id', metavar='ID')
def export(session_id):
    entity = iqcli.api.session.export(session_id=session_id)
    
    if entity:
        print(json.dumps(entity, indent=4))
