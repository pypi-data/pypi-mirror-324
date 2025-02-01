# Copyright (c) 2021 Red Hat, Inc.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
from __future__ import absolute_import

import testtools


from tobiko.tests.faults.podified.ha import cloud_disruptions
from tobiko import podified


@podified.skip_if_not_podified
class DisruptPodifiedNodesTest(testtools.TestCase):
    """ HA Tests: run health check -> disruptive action -> health check
    disruptive_action: a function that runs some
    disruptive scenario on a node"""

    def test_kill_all_galera_services(self):
        # HealthCheck.run_before()
        cloud_disruptions.kill_all_galera_services()
        # HealthCheck.run_after()

    def test_remove_all_grastate_galera(self):
        # HealthCheck.run_before()
        cloud_disruptions.remove_all_grastate_galera()
        # HealthCheck.run_before()

    def test_remove_one_grastate_galera(self):
        # HealthCheck.run_before()
        cloud_disruptions.remove_one_grastate_galera()
        # HealthCheck.run_after()
