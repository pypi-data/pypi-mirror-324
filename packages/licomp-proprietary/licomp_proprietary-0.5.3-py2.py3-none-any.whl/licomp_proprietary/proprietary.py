# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

from licomp_proprietary.config import licomp_proprietary_version
from licomp_proprietary.config import module_name
from licomp_proprietary.config import my_supported_api_version
from licomp_proprietary.config import disclaimer
from licomp_proprietary.config import original_data_url
from licomp_proprietary.config import module_url

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
PROPRIETARY_LICENSES_FILE_NAME = 'proprietary-licenses.json'
PROPRIETARY_LICENSES_FILE = os.path.join(DATA_DIR, PROPRIETARY_LICENSES_FILE_NAME)

class LicompProprietary(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.provisionings = [Provisioning.BIN_DIST, Provisioning.SOURCE_DIST]
        self.usecases = [UseCase.LIBRARY]
        with open(PROPRIETARY_LICENSES_FILE) as fp:
            self.data = json.load(fp)
            self.licenses = self.data['licenses']
        self.ret_statuses = {
            "Same": CompatibilityStatus.COMPATIBLE,
            "Yes": CompatibilityStatus.COMPATIBLE,
            "No": CompatibilityStatus.INCOMPATIBLE,
            "Unknown": CompatibilityStatus.UNKNOWN,
            "Check dependency": CompatibilityStatus.DEPENDS,
            "unsupported": CompatibilityStatus.UNSUPPORTED,
        }

    def supported_licenses(self):
        licenses = list(self.licenses.keys())
        licenses.extend(list(self.licenses['Proprietary-linked'].keys()))
        licenses.sort()
        return licenses

    def supported_provisionings(self):
        return self.provisionings

    def _outbound_inbound_compatibility(self, outbound, inbound, usecase, provisioning, modified):
        try:
            compat = self.licenses[outbound][inbound]
            return self.outbound_inbound_reply(self.ret_statuses[compat],
                                               f'Value from matrix: {compat}')
        except KeyError:
            return self.outbound_inbound_reply(CompatibilityStatus.UNSUPPORTED,
                                               f'No support for outbound:"{outbound}" using inbound:"{inbound}"')

    def name(self):
        return module_name

    def version(self):
        return licomp_proprietary_version

    def url(self):
        return module_url

    def data_url(self):
        return original_data_url

    def supported_api_version(self):
        return my_supported_api_version

    def supported_usecases(self):
        return self.usecases

    def disclaimer(self):
        return disclaimer
