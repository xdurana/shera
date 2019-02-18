# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
import logging

from utils import (
    setup_redis, setup_queue, Popper
)
from rq.decorators import job

from reports import get_reports, render_reports

from sources import *

logger = logging.getLogger('shera')

def deliver_reports(contracts_path, reports_path,
        template, output_path, source, bucket=500):
    try:
        source_class = eval(source)
    except NameError as e:
        logger.error('%s source type not found' % str(source))

    reports = get_reports(contracts_path, reports_path)
    popper = Popper(reports)
    pops = popper.pop(bucket)
    while pops:
        j = push_reports.delay(pops, template, output_path, source_class)
        logger.info("Job id:%s | %s/%s" % (
            j.id, len(pops), len(popper.items))
        )
        pops = popper.pop(bucket)

@job(setup_queue(name='reports'), connection=setup_redis(), timeout=3600)
def push_reports(reports, template, output, source_class):
    O = source_class.setup_pool()
    start = datetime.now()
    try:
        render_reports(O, reports, template, output)
        O.send_reports(reports)
    except Exception as e:
        logger.error('Report push failed: %s' % str(e))
    stop = datetime.now()
    logger.info('Delivered reports in %s' % (stop - start))
    logger.info("%s delivered reports" % len(reports))
