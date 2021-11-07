import click
from pathlib import Path

from config import config

min_polling_period = 10


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


from cli import file
from cli import session
