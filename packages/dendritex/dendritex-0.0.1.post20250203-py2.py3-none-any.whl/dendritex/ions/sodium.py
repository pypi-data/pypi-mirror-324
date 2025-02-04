# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
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
# ==============================================================================

from __future__ import annotations

from typing import Union, Callable, Optional

import brainstate as bst
import brainunit as u

from dendritex._base import Ion

__all__ = [
    'Sodium',
    'SodiumFixed',
]


class Sodium(Ion):
    """Base class for modeling Sodium ion."""
    __module__ = 'dendritex.ions'


class SodiumFixed(Sodium):
    """
    Fixed Sodium dynamics.

    This calcium model has no dynamics. It holds fixed reversal
    potential :math:`E` and concentration :math:`C`.
    """
    __module__ = 'dendritex.ions'

    def __init__(
        self,
        size: bst.typing.Size,
        E: Union[bst.typing.ArrayLike, Callable] = 50. * u.mV,
        C: Union[bst.typing.ArrayLike, Callable] = 0.0400811 * u.mM,
        name: Optional[str] = None,
        **channels
    ):
        super().__init__(size, name=name, **channels)
        self.E = bst.init.param(E, self.varshape, allow_none=False)
        self.C = bst.init.param(C, self.varshape, allow_none=False)
