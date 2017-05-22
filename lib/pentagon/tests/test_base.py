
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


class TestPentagonProject(unittest.TestCase):
    name = "test-pentagon-base"

    def setUp(self):
        self.p = pentagon.PentagonProject(self.name)

    def tearDown(self):
        self.p = None

    def test_instance(self):
        self.assertIsInstance(self.p, pentagon.PentagonProject)

    def test_name(self):
        print ('test')
        self.assertEqual(self.p._name, self.name)

    def test_repository_name(self):
        self.assertEqual(self.p._repository_name, '{}-infrastructure'.format(self.name))

    def test_repository_directory(self):
        self.assertEqual(self.p._repository_directory, "{}/{}".format(self.p._project_directory, self.p._repository_name))

    def test_workspace_directory(self):
        self.assertEqual(self.p._workspace_directory, os.path.expanduser('~/workspace'))

    def test_projects_directory(self):
        self.assertEqual(self.p._projects_directory, '{}/projects'.format(self.p._workspace_directory))

    def test_project_directory(self):
        self.assertEqual(self.p._project_directory, '{}/projects/{}'.format(self.p._workspace_directory, self.p._name))

    def test_private_path(self):
        self.assertEqual(self.p._private_path, "{}/config/private/".format(self.p._repository_directory))
