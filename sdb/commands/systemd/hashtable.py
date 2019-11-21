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

from typing import Iterable

import drgn
import sdb


class SystemdHashmap(sdb.Walker):
    names = ["systemd_hashmap"]
    input_type = "Hashmap *"

    def storage_ptr(self, hashmap_base: drgn.Object) -> drgn.Object:
        if (hashmap_base.has_indirect):
            return hashmap_base.indirect.storage
        else:
            return hashmap_base.direct.storage

    def n_buckets(self, hashmap_base: drgn.Object) -> int:
        if (hashmap_base.has_indirect):
            return int(hashmap_base.indirect.n_buckets)
        else:
            idx = hashmap_base.member_('type')
            return int(self.prog['hashmap_type_info'][idx].n_direct_buckets)

    def entry_size(self, hashmap_base: drgn.Object) -> int:
        idx = hashmap_base.member_('type')
        #return int(self.prog['hashmap_type_info'][idx].entry_size)

        #
        # The above should work, but sdb can't read the memory values required.
        #
        #    return int(self.prog['hashmap_type_info'][idx].entry_size)
        # _drgn.FaultError: could not find memory segment containing 0x43e148
        #
        # This seems to be an sdb thing, gdb works fine. Maybe something ASLR
        # related?
        #
        return 16

    def walk(self, obj: drgn.Object) -> Iterable[drgn.Object]:
        hashmap_base = obj.b
        entry_size = self.entry_size(hashmap_base)
        storage_ptr = drgn.reinterpret('uint8_t*', self.storage_ptr(hashmap_base))
        for idx in range(0, self.n_buckets(hashmap_base)):
            entry = drgn.reinterpret('struct plain_hashmap_entry', storage_ptr[idx*entry_size])
            # TODO official way of telling whether a slot is free is to look at the DIB. See
            # skip_free_buckets and hashmap_iterate_in_internal_order
            if entry.b.key != drgn.NULL(self.prog, entry.b.key.type_):
                #
                # TODO The key is stored separately from the value. Should we
                # return a value of some fake type that contains both key and
                # value?
                #
                yield entry.value
