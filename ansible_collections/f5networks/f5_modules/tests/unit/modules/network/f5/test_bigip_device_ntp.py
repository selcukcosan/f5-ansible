# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_ntp import (
    Parameters, ModuleManager, ArgumentSpec
)
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock, patch
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        ntp = ['192.168.1.1', '192.168.1.2']
        args = dict(
            ntp_servers=ntp,
            timezone='Arctic/Longyearbyen'
        )

        p = Parameters(params=args)
        assert p.ntp_servers == ntp
        assert p.timezone == 'Arctic/Longyearbyen'

    def test_api_parameters(self):
        ntp = ['192.168.1.1', '192.168.1.2']
        args = dict(
            servers=ntp,
            timezone='Arctic/Longyearbyen'
        )

        p = Parameters(params=args)
        assert p.ntp_servers == ntp
        assert p.timezone == 'Arctic/Longyearbyen'


class TestModuleManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_ntp.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_device_ntp.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_update_ntp_servers(self, *args):
        ntp = ['10.1.1.1', '10.1.1.2']
        set_module_args(
            dict(
                ntp_servers=ntp,
                provider=dict(
                    server='localhost',
                    password='password',
                    user='admin'
                )
            )
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(params=load_fixture('load_ntp.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_one_of=self.spec.required_one_of
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['ntp_servers'] == ntp

    def test_update_timezone(self, *args):
        set_module_args(
            dict(
                timezone='Arctic/Longyearbyen',
                provider=dict(
                    server='localhost',
                    password='password',
                    user='admin'
                )
            )
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(params=load_fixture('load_ntp.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_one_of=self.spec.required_one_of
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['timezone'] == 'Arctic/Longyearbyen'

    def test_update_ntp_servers_and_timezone(self, *args):
        ntp = ['10.1.1.1', '10.1.1.2']
        set_module_args(
            dict(
                ntp_servers=ntp,
                timezone='Arctic/Longyearbyen',
                provider=dict(
                    server='localhost',
                    password='password',
                    user='admin'
                )
            )
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(params=load_fixture('load_ntp.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_one_of=self.spec.required_one_of
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.update_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['ntp_servers'] == ntp
        assert results['timezone'] == 'Arctic/Longyearbyen'

    def test_absent_ntp_servers(self, *args):
        ntp = []
        set_module_args(
            dict(
                ntp_servers=ntp,
                timezone='America/Los_Angeles',
                state='absent',
                provider=dict(
                    server='localhost',
                    password='password',
                    user='admin'
                )
            )
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(params=load_fixture('load_ntp.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_one_of=self.spec.required_one_of
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.absent_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is True
        assert results['ntp_servers'] == ntp
        assert not hasattr(results, 'timezone')

    def test_absent_timezone(self, *args):
        set_module_args(
            dict(
                timezone='',
                state='absent',
                provider=dict(
                    server='localhost',
                    password='password',
                    user='admin'
                )
            )
        )

        # Configure the parameters that would be returned by querying the
        # remote device
        current = Parameters(params=load_fixture('load_ntp.json'))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode,
            required_one_of=self.spec.required_one_of
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.absent_on_device = Mock(return_value=True)
        mm.read_current_from_device = Mock(return_value=current)

        results = mm.exec_module()
        assert results['changed'] is False
