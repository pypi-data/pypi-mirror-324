# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

from licomp_dwheeler.dwheeler import LicompDw

ld = LicompDw()

def test_supported():
    assert len(ld.supported_licenses()) == 16
    
def test_license_is_supported():
    assert ld.license_supported("BSD-3-Clause")
    
def test_license_is_not_supported():
    assert not ld.license_supported("Some-license-that-does-not-exist")
    
def test_provisioning_is_supported():
    assert ld.provisioning_supported(provisioning=Provisioning.BIN_DIST)
    
def test_provisioning_is_not_supported():
    assert not ld.provisioning_supported(provisioning=Provisioning.LOCAL_USE)
    
def test_compat():
    ret = ld.outbound_inbound_compatibility("GPL-2.0-only", "BSD-3-Clause", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "yes"
    assert ret['status'] == "success"

def test_incompat_1():
    ret = ld.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "no"
    assert ret['status'] == "success"

def test_bad_prov():
    ret = ld.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.LOCAL_USE)
    logging.debug("ret: " + str(ret))
    assert ret['status'] == 'failure'

def test_incompat_3():
    ret = ld.outbound_inbound_compatibility("BSD-3-Clause", "DO_NO_EXIST", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_incompat_4():
    ret = ld.outbound_inbound_compatibility("DO_NO_EXIST", "GPL-2.0-only", usecase=UseCase.LIBRARY, provisioning=Provisioning.BIN_DIST)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

