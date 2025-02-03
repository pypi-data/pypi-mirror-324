# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp.interface import Licomp
from licomp.interface import Provisioning
#from licomp.interface import Modification
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

from licomp_proprietary.proprietary import LicompProprietary

lp = LicompProprietary()

def test_supported():
    assert len(lp.supported_licenses()) > 60
    
def test_license_is_supported():
    assert lp.license_supported("BSD-3-Clause")
    
def test_license_is_not_supported():
    assert not lp.license_supported("Some-license-that-does-not-exist")
    
def test_provisioning_is_supported():
    assert lp.provisioning_supported(provisioning=Provisioning.BIN_DIST)
    
def test_provisioning_is_not_supported():
    assert not lp.provisioning_supported(provisioning=Provisioning.LOCAL_USE)
    
def test_compat():
    ret = lp.outbound_inbound_compatibility("Proprietary-linked", "BSD-3-Clause", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "yes"
    assert ret['status'] == "success"

def test_incompat_1():
    ret = lp.outbound_inbound_compatibility("Proprietary-linked", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "no"
    assert ret['status'] == "success"

def test_bad_prov():
    ret = lp.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.LOCAL_USE)
    logging.debug("ret: " + str(ret))
    assert ret['status'] == 'failure'

def test_incompat_3():
    ret = lp.outbound_inbound_compatibility("BSD-3-Clause", "DO_NO_EXIST", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_incompat_4():
    ret = lp.outbound_inbound_compatibility("DO_NO_EXIST", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_api_version():
    licomp_api_version = lp.api_version()
    lp_api_version = lp.supported_api_version()
    logging.debug(f'versions: {licomp_api_version} {lp_api_version}')
    assert licomp_api_version.split('.')[0] == lp_api_version.split('.')[0]
    assert licomp_api_version.split('.')[1] == lp_api_version.split('.')[1]

