#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2016-09-25 12:21:49 +0100 (Sun, 25 Sep 2016)
#
#  https://github.com/harisekhon/nagios-plugins
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/harisekhon
#

"""

Nagios Plugin to check the deployed version of an RabbitMQ matches what's expected via the Management REST API

Requires the management plugin to be loaded.

This is also used in the accompanying test suite to ensure we're checking the right version of RabbitMQ
for compatibility for all my other RabbitMQ nagios plugins.

Tested on RabbitMQ 3.4.4, 3.5.7, 3.6.6

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import os
import sys
import traceback
srcdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(srcdir, 'pylib')
sys.path.append(libdir)
try:
    # pylint: disable=wrong-import-position
    from harisekhon.utils import log, qquit, support_msg_api, jsonpp
    from harisekhon import RestVersionNagiosPlugin
except ImportError as _:
    print(traceback.format_exc(), end='')
    sys.exit(4)

__author__ = 'Hari Sekhon'
__version__ = '0.3'


class CheckRabbitMQVersion(RestVersionNagiosPlugin):

    def __init__(self):
        # Python 2.x
        super(CheckRabbitMQVersion, self).__init__()
        # Python 3.x
        # super().__init__()
        self.name = 'RabbitMQ'
        self.default_port = 15672
        self.default_user = 'guest'
        self.default_password = 'guest'
        self.path = 'api/overview'

    def parse(self, req):
        try:
            json_data = json.loads(req.content)
            if log.isEnabledFor(logging.DEBUG):
                print(jsonpp(json_data))
                print('=' * 80)
            return json_data['rabbitmq_version']
        except (KeyError, ValueError) as _:
            qquit('UNKNOWN', str(_) + support_msg_api())


if __name__ == '__main__':
    CheckRabbitMQVersion().main()
