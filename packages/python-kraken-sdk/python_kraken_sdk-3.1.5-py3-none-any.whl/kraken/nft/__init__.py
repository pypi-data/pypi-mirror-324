#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
# pylint: disable=unused-import

"""This module provides the Kraken NFT clients"""

from kraken.nft.market import Market
from kraken.nft.trade import Trade

__all__ = [
    "Market",
    "Trade",
]
