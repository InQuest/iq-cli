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
    config['apikey'] = api or config['apikey']
    config['server']['host'] = host or config['server']['host']
    config['server']['secure'] = secure or config['server']['secure']
    config['server']['verify'] = verify_tls or config['server']['verify']


from cli import file
