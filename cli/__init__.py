import click
from functools import wraps
from pathlib import Path
import simplejson as json
import textwrap

from config import config


class TopLevelGroup(click.Group):
    def format_help(self, ctx, formatter):
        click.echo('InQuest Command Line Driver\n')
        usage_found = False
        with open(str(Path(__file__).parent) + '/../README.md', 'r') as f:
            for line in f.readlines():
                if -1 != line.find('Usage'):
                    usage_found = True
                if usage_found and -1 != line.find('```'):
                    return
                if usage_found:
                    click.echo(line.rstrip())


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


from cli import file
from cli import saved_search
from cli import session
