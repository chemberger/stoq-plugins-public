#   Copyright 2014-2018 PUNCH Cyber Analytics Group
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Overview
========

Identify file types from their TrID signature

"""

import tempfile
from typing import Dict, Optional
from subprocess import check_output
from configparser import ConfigParser

from stoq.plugins import WorkerPlugin
from stoq.exceptions import StoqPluginException
from stoq import Payload, RequestMeta, WorkerResponse


class TridPlugin(WorkerPlugin):
    def __init__(self, config: ConfigParser, plugin_opts: Optional[Dict]) -> None:
        super().__init__(config, plugin_opts)

        if plugin_opts and 'trid_defs' in plugin_opts:
            trid_defs = plugin_opts['trid_defs']
        elif config.has_option('options', 'trid_defs'):
            trid_defs = config.get('options', 'trid_defs')
        self.trid_defs = trid_defs

        if plugin_opts and 'bin_path' in plugin_opts:
            bin_path = plugin_opts['bin_path']
        elif config.has_option('options', 'bin_path'):
            bin_path = config.get('options', 'bin_path')
        self.bin_path = bin_path

    def scan(self, payload: Payload, request_meta: RequestMeta) -> WorkerResponse:
        """
        Scan a payload using TRiD

        """
        results = {}

        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(payload.content)
            temp_file.flush()
            try:
                cmd = [self.bin_path, f"-d:{self.trid_defs}", temp_file.name]
                trid_results = check_output(cmd).splitlines()
            except Exception as err:
                raise StoqPluginException(f'Failed gathering TRiD data: {err}')

        for line in trid_results[6:]:
            if line.startswith('Warning'.encode()):
                break
            line = line.decode().split()
            if line:
                ext = line[1].strip('(.)')
                results[ext] = {'likely': line[0], 'type': ' '.join(line[2:])}

        return WorkerResponse(results)
