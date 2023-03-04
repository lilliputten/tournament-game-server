# -*- coding:utf-8 -*-
# @module gameHelpers
# @since 2023.03.04, 21:43
# @changed 2023.03.04, 21:43


def determineGameWinner(gameRecord):
    partners = gameRecord['partners']
    # partnersInfo = gameRecord['partnersInfo']
    return partners[0]


__all__ = [  # Exporting objects...
    'determineGameWinner',
]
