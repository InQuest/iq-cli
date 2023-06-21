import click
from functools import wraps
from pathlib import Path
import simplejson as json
import textwrap

from iqcli.config import config

help_md = \
"""
Usage:
    ./iq-cli.py [options] session export <id>
    ./iq-cli.py [options] file search [--limit=<limit>] [--eventid=<eventid>] [--signature-name=<signature-name>] [--signature-category=<signature-category>]
    ./iq-cli.py [options] file download id <id> [--output=<output>] [--dfi-output=<dfi-output>]
    ./iq-cli.py [options] file download hash <(md5|sha1|sha256|sha512)> [--output=<output>] [--dfi-output=<dfi-output>]
    ./iq-cli.py [options] file scan <input>
    ./iq-cli.py [options] saved-search <id> [--limit=<limit>]

Options:
    --api=<apikey>              Specify an API key.
    --host=<hostname>           API server hostname.
    --secure=<true|false>       Use HTTPS if true, HTTP if false [default: true].
    --verify-tls=<true|false>   Verify validity of TLS certificate when using HTTPS [default: true].

    --limit                     Maximum number of entries [default: 25].
    --eventid                   Event ID of the Signature hit.
    --signature-name            Name of the Signature hit.
    --signature-category        Category of the Signature hit.
    --output=<output>           Target file. If not set, the file will be streamed to stdout.
    --dfi-output=<dfi-output>   Target location for DFI content. If not set, DFI content will not be downloaded.
"""

class TopLevelGroup(click.Group):
    def format_help(self, ctx, formatter):
        click.echo('InQuest Command Line Driver\n')
        click.echo(help_md)

@click.group(cls=TopLevelGroup)
@click.option('--api')
@click.option('--host')
@click.option('--secure', type=bool)
@click.option('--verify-tls', type=bool)
def cli(api, host, secure, verify_tls):
    if api is not None:
        config['apikey'] = api
    elif 'apikey' not in config:
        raise click.ClickException('API key is required')

    if 'server' not in config:
        config['server'] = {}

    if host is not None:
        config['server']['host'] = host
    elif 'host' not in config['server']:
        raise click.ClickException('Host is required')

    if secure is not None:
        config['server']['secure'] = secure
    elif 'secure' not in config['server']:
        config['server']['secure'] = True

    if verify_tls is not None:
        config['server']['verify'] = verify_tls
    elif 'verify' not in config['server']:
        config['server']['verify'] = True


def format_search_results_as_json_array(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        search_result = f(*args, **kwargs)
        print('[')
        
        for index, entity in enumerate(search_result):
            if index:
                print(',')
            
            print(textwrap.indent(json.dumps(entity, indent=4), ' ' * 4), end='')
        
        print('\n]')
    
    return wrapper


from iqcli.cli import file
from iqcli.cli import saved_search
from iqcli.cli import session
