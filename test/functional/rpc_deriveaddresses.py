#!/usr/bin/env python3
# Copyright (c) 2018 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the deriveaddresses rpc call."""
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_raises_rpc_error


class DeriveaddressesTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1
        self.supports_cli = 1

    def run_test(self):
        assert_raises_rpc_error(-5, "Invalid descriptor",
                                self.nodes[0].deriveaddresses, "a")

        descriptor = "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/0)"
        address = "bchreg:qzgrvmwc8vevauc25j86hgfpduz8j98yvvyr0qx0ew"

        assert_equal(self.nodes[0].deriveaddresses(descriptor), [address])

        descriptor_pubkey = "pkh(tpubD6NzVbkrYhZ4WaWSyoBvQwbpLkojyoTZPRsgXELWz3Popb3qkjcJyJUGLnL4qHHoQvao8ESaAstxYSnhyswJ76uZPStJRJCTKvosUCJZL5B/1/1/0)"
        address = "bchreg:qzgrvmwc8vevauc25j86hgfpduz8j98yvvyr0qx0ew"

        assert_equal(self.nodes[0].deriveaddresses(
            descriptor_pubkey), [address])

        ranged_descriptor = "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/*)"
        assert_equal(
            self.nodes[0].deriveaddresses(ranged_descriptor, 0, 2),
            [address, "bchreg:qz7mjsvr6gglnl389gnfxmqx0asxp0hcvqjx829c6k", "bchreg:qq9q9wefpjzuna7qhuzz7rvck9tuhrzp3gvrzd8kx2"])

        assert_raises_rpc_error(
            -8,
            "Range should not be specified for an un-ranged descriptor",
            self.nodes[0].deriveaddresses,
            "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/0)",
            0,
            2)

        assert_raises_rpc_error(
            -8,
            "Range must be specified for a ranged descriptor",
            self.nodes[0].deriveaddresses,
            "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/*)")

        assert_raises_rpc_error(
            -8,
            "Missing range end parameter",
            self.nodes[0].deriveaddresses,
            "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/*)",
            0)

        assert_raises_rpc_error(
            -8,
            "Range end should be equal to or greater than begin",
            self.nodes[0].deriveaddresses,
            "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/*)",
            2,
            0)

        assert_raises_rpc_error(
            -8,
            "Range should be greater or equal than 0",
            self.nodes[0].deriveaddresses,
            "pkh(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/*)",
            -1,
            0)

        combo_descriptor = "combo(tprv8ZgxMBicQKsPd7Uf69XL1XwhmjHopUGep8GuEiJDZmbQz6o58LninorQAfcKZWARbtRtfnLcJ5MQ2AtHcQJCCRUcMRvmDUjyEmNUWwx8UbK/1/1/0)"
        assert_equal(self.nodes[0].deriveaddresses(
            combo_descriptor), [address, address])

        hardened_without_privkey_descriptor = "pkh(tpubD6NzVbkrYhZ4WaWSyoBvQwbpLkojyoTZPRsgXELWz3Popb3qkjcJyJUGLnL4qHHoQvao8ESaAstxYSnhyswJ76uZPStJRJCTKvosUCJZL5B/1'/1/0)"
        assert_raises_rpc_error(-5,
                                "Cannot derive script without private keys",
                                self.nodes[0].deriveaddresses,
                                hardened_without_privkey_descriptor)

        bare_multisig_descriptor = "multi(1, tpubD6NzVbkrYhZ4WaWSyoBvQwbpLkojyoTZPRsgXELWz3Popb3qkjcJyJUGLnL4qHHoQvao8ESaAstxYSnhyswJ76uZPStJRJCTKvosUCJZL5B/1/1/0, tpubD6NzVbkrYhZ4WaWSyoBvQwbpLkojyoTZPRsgXELWz3Popb3qkjcJyJUGLnL4qHHoQvao8ESaAstxYSnhyswJ76uZPStJRJCTKvosUCJZL5B/1/1/1)"
        assert_raises_rpc_error(-5,
                                "Descriptor does not have a corresponding address",
                                self.nodes[0].deriveaddresses,
                                bare_multisig_descriptor)


if __name__ == '__main__':
    DeriveaddressesTest().main()
