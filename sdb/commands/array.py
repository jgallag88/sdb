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

# pylint: disable=missing-docstring

import argparse
from typing import Iterable

import drgn
import sdb

class Array(sdb.Command):
    # pylint: disable=too-few-public-methods

    names = ["array"]

    def _init_argparse(self, parser: argparse.ArgumentParser) -> None:
        # TODO allow 'count' to be omitted if input type is proper array
        parser.add_argument("count", type=int, metavar="<count>")

    def call(self, objs: Iterable[drgn.Object]) -> Iterable[drgn.Object]:
        for obj in objs:
            for idx in range(self.args.count):
                try:
                    yield obj[idx]
                except TypeError as err:
                    raise sdb.CommandError(self.name, str(err))
