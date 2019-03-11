#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import click

import tasks
from utils import setup_logging


@click.group()
@click.option('--log-level', default='info')
@click.option('--async/--no-async', default=True)
def shera(log_level, async):
    MODE = {True: 'ASYNC', False: 'SYNC'}
    log_level = log_level.upper()
    log_level = getattr(logging, log_level, 'INFO')
    logging.basicConfig(level=log_level)
    setup_logging()
    logger = logging.getLogger('shera')
    logger.info('Running shera in %s mode' % MODE[async])
    os.environ['RQ_ASYNC'] = str(async)


@shera.command()
@click.option('--contracts', type=click.Path(exists=True))
@click.option('--reports', type=click.Path(exists=True))
@click.option('--template', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
@click.option('--source', default='CSVSource', type=click.STRING)
@click.option('--data', default='data/test_from_csv/contracts.csv', type=click.STRING)
def deliver_reports(contracts, reports, template, output, source, data):
    logger = logging.getLogger('shera')
    logger.info('Enqueuing reports to be delivered')
    tasks.deliver_reports(
        contracts,
        reports,
        template,
        output,
        source,
        data,
        bucket=25
    )


if __name__ == '__main__':
    shera(obj={})
