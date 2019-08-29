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
from drgn.helpers.linux.list import list_for_each_entry
import sdb

class HList(sdb.Walker):
    """ walk a linux list_head """

    names = ["list"]
    input_type = "struct list_head *"

    # TODO validate 'type' and 'member' passed in, and handle errors nicely
    # for instance, passing "asdf for a type will complain with a SyntaxError ?

    def _init_argparse(self, parser: argparse.ArgumentParser) -> None:
        # TODO nargs=2 is gross workaround for fact that we don't have real lexing
        parser.add_argument("type", nargs=2, help="type of the struct used for entries in the hlist")
        parser.add_argument("member", help="name of the hlist_node member within the struct")

    def walk(self, obj: drgn.Object) -> Iterable[drgn.Object]:
        yield from list_for_each_entry(" ".join(self.args.type), obj, self.args.member)
