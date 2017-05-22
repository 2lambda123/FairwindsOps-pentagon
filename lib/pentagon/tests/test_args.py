
# Copyright 2017 Reactive Ops Inc.
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import pentagon
import os
import logging
from pentagon.tests.test_base import TestPentagonProject


class TestPentagonProjectWithoutArgs(TestPentagonProject):
    name = 'test_pentagon_without_args'

    def setUp(self):
        self.p = pentagon.PentagonProject(self.name)

    def tearDown(self):
        self.p = None


class TestPentagonProjectWithAllArgs(TestPentagonProject):
    name = 'test_pentagon_with_all_args'
    args = {
        'configure': True,

        # 'repository_name': 'test-repository-name',
        # 'workspace_directory': 'test-workspace-direcotry',

        # need to test some of these without all of them
        'aws_access_key': 'test-aws-key',
        'aws_secret_key': 'test-aws-secret-key',
        'aws_default_region': 'test-aws-region',
        'aws_availability_zone_count': 5,
        'aws_availability_zones': 'test-aws-regiona,test-aws-regionb,test-aws-regionc',
        'vpc_name': 'test_vpc_name',
        'vpc_cidr_base': 'test_vpc_cidr_base',
        'vpc_id': 'test_vpc_id',
        # KOPS:
        'state_store_bucket': 'test-statestore-bucket',
        # Working Kubernetes
        'working_kubernetes_cluster_name': 'test-working-cluster-name',
        'working_kubernetes_dns_zone': 'test-working-cluster-dns-zone',
        'working_kubernetes_node_count': 3,
        'working_kubernetes_master_aws_zone': 'test-working-aws-master-zone',
        'working_kubernetes_master_node_type': 'test-working-master-node-type',
        'working_kubernetes_worker_node_type': 'test-working-worker-node-type',
        'working_kubernetes_v_log_level': 'test-working-v-log-level',
        'working_kubernetes_network_cidr': 'test-working-netwwork-cidr',
        # Production Kubernetes
        'production_kubernetes_cluster_name': 'test-production-cluster-name',
        'production_kubernetes_dns_zone': 'test-production-cluster-dns-zone',
        'production_kubernetes_node_count': 3,
        'production_kubernetes_master_aws_zone': 'test-production-aws-master-zone',
        'production_kubernetes_master_node_type': 'test-production-master-node-type',
        'production_kubernetes_worker_node_type': 'test-production-worker-node-type',
        'production_kubernetes_v_log_level': 'test-production-v-log-level',
        'production_kubernetes_network_cidr': 'test-production-netwwork-cidr',
        # ssh keys
        'admin_vpn_key': 'test-admin-vpn-key',
        'working_kube_key': 'test-working-kube-key',
        'production_kube_key': 'test-production-kube-key',
        'working_private_key': 'test-working-private-key',
        'production_private_key': 'test-production-private-key',
        }

    def setUp(self):
        self.p = pentagon.PentagonProject(self.name, self.args)

    def tearDown(self):
        self.p = None

    def test_configure_project(self):
        self.assertEqual(self.p._configure_project, True)

    def test_aws_availability_zones(self):
        self.assertIsInstance(self.p._aws_availability_zone_count, int)
        self.assertEqual(self.p._aws_default_region, self.args['aws_default_region'])
        self.assertEqual(self.p._aws_availability_zones, self.args['aws_availability_zones'])

    def test_vpc_name(self):
        self.assertEqual(self.p._vpc_name, self.args['vpc_name'])

    def test_kops_args(self):
        self.assertEqual(self.p._state_store_bucket, self.args['state_store_bucket'])

    def test_kubernetes_args(self):
        base_kube_args = [
            '_kubernetes_cluster_name',
            '_kubernetes_dns_zone',
            '_kubernetes_node_count',
            '_kubernetes_master_aws_zone',
            '_kubernetes_master_node_type',
            '_kubernetes_worker_node_type',
            '_kubernetes_v_log_level',
            '_kubernetes_network_cidr',
        ]

        for env in ['working', 'production']:
            for arg in base_kube_args:
                arg_name = '{}{}'.format(env, arg)
                attr_name = '_{}'.format(arg_name)
                pentagon_attribute = getattr(self.p, attr_name)
                self.assertEqual(pentagon_attribute, self.args.get(arg_name))


class TestPentagonProjectWithMinimalArgs(TestPentagonProject):
    name = 'test_pentagon_with_minimal_args'

    args = {
        'configure': True,
        # need to test some of these without all of them
        'aws_access_key': 'test-aws-key',
        'aws_secret_key': 'test-aws-secret-key',
        'aws_default_region': 'test-aws-region',
        'aws_availability_zone_count': 5,
        }

    def setUp(self):
        self.p = pentagon.PentagonProject(self.name, self.args)

    def tearDown(self):
        self.p = None

    def test_configure_project(self):
        self.assertEqual(self.p._configure_project, self.args['configure'])

    def test_aws_availability_zones(self):
        azs = "test-aws-regiona, test-aws-regionb, test-aws-regionc, test-aws-regiond, test-aws-regione"
        self.assertIsInstance(self.p._aws_availability_zone_count, int)
        self.assertEqual(self.p._aws_default_region, self.args['aws_default_region'])
        self.assertEqual(self.p._aws_availability_zones, azs)


class TestPentagon(TestPentagonProject):

    def test_noninteget_az_count(self):
        args = {
            'configure': True,
            'aws_default_region': 'test_default_region',
            'aws_availability_zone_count': 'not_an_integer'
        }
        with self.assertRaises(ValueError):
            p = pentagon.PentagonProject(self.name, args)
