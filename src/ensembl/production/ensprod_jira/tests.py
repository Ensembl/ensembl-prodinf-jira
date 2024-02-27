# See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from ensembl.production.ensprod_jira.models import KnownBug, RRBug
from collections import namedtuple
User = get_user_model()


class JiraExportTest(APITestCase):

    def testAlive(self):
        filter_on = [
            'versions_list',
        ]
        filter_on.sort()
        expect = list(KnownBug.filter_on)
        expect.sort()
        self.assertListEqual(filter_on, expect)
        filter_on = [
            'key',
            'summary',
            'description',
        ]
        filter_on.sort()
        expect = list(RRBug.filter_on)
        expect.sort()
        self.assertListEqual(filter_on, expect)

