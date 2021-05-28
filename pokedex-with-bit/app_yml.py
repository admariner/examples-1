__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import click
import sys
from glob import glob

from jina import Flow, DocumentArray
from jina.logging import default_logger as logger

IMAGE_SRC = 'data/**/*.png'
MAX_DOCS = int(os.environ.get('JINA_MAX_DOCS', 50000))


def config():
    num_encoders = 1 if sys.argv[1] == 'index' else 1
    shards = 8

    os.environ['JINA_SHARDS'] = str(num_encoders)
    os.environ['JINA_SHARDS_INDEXERS'] = str(shards)
    os.environ['JINA_WORKSPACE'] = './workspace'
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))


def index(num_docs: int):
    # Runs indexing for all images
    num_docs = min(num_docs, len(glob(os.path.join(os.getcwd(), IMAGE_SRC),
                                      recursive=True)))

    with Flow.load_config('flows/index.yml') as flow:
        flow.index(inputs=DocumentArray.from_files(IMAGE_SRC, size=num_docs),
                request_size=64, read_mode='rb')


def query_restful():
    # Starts the restful query API
    flow = Flow.load_config('flows/query.yml')
    flow.use_rest_gateway()
    with flow:
        flow.block()


@click.command()
@click.option(
    '--task',
    '-t',
    type=click.Choice(
        ['index', 'query_restful'], case_sensitive=False
    ),
)
@click.option('--num_docs', '-n', default=MAX_DOCS)
def main(task: str, num_docs: int):
    config()
    workspace = os.environ['JINA_WORKSPACE']
    if task == 'index':
        if os.path.exists(workspace):
            logger.error(f'\n +----------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                         | \
                    \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                         | \
                    \n +----------------------------------------------------------------------------------+')
            sys.exit(1)
        index(num_docs)
    if task == 'query_restful':
        if not os.path.exists(workspace):
            logger.error(f'The directory {workspace} does not exist. Please index first via `python app.py -t index`')
            sys.exit(1)
        query_restful()


if __name__ == '__main__':
    main()
