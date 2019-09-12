#
# Copyright 2019 Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
from typing import Iterable

import drgn
from drgn.helpers.linux.fs import d_path
import sdb

# TODO make this a pretty printer?
class Path(sdb.Command):
    """ display the path represented by a struct path """

    names = ["path"]

    def call(self, objs: Iterable[drgn.Object]) -> None:
        # TODO validate that each input is a struct path or struct path*
        for obj in objs:
            print(d_path(obj).decode("utf-8", "backslashreplace"))

