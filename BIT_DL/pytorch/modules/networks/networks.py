# Copyright 2019 The Texar Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Various neural networks and related utilities.
"""
from BIT_DL.pytorch.modules.networks.network_base import FeedForwardNetworkBase
from BIT_DL.pytorch.utils.utils import get_output_size

__all__ = [
    "FeedForwardNetwork",
]


class FeedForwardNetwork(FeedForwardNetworkBase):
    r"""Feed-forward neural network that consists of a sequence of layers.

    Args:
        layers (list, optional): A list of :torch_nn:`Linear`
            instances composing the network. If not given, layers are created
            according to :attr:`hparams`.
        hparams (dict, optional): Embedder hyperparameters. Missing
            hyperparameters will be set to default values. See
            :meth:`default_hparams` for the hyperparameter structure and
            default values.

    See :meth:`forward` for the inputs and outputs.

    Example:

        .. code-block:: python

            hparams = { # Builds a two-layer dense NN
                "layers": [
                    { "type": "Dense", "kwargs": { "units": 256 },
                    { "type": "Dense", "kwargs": { "units": 10 }
                ]
            }
            nn = FeedForwardNetwork(hparams=hparams)

            inputs = torch.randn([64, 100])
            outputs = nn(inputs)
            # outputs == Tensor of shape [64, 10]
    """

    def __init__(self, layers=None, hparams=None):
        super().__init__(hparams=hparams)

        self._build_layers(layers=layers, layer_hparams=self._hparams.layers)

    @staticmethod
    def default_hparams():
        r"""Returns a dictionary of hyperparameters with default values.

        .. code-block:: python

            {
                "layers": [],
                "name": "NN"
            }

        Here:

        `"layers"`: list
            A list of layer hyperparameters. See
            :func:`~BIT_DL.pytorch.core.get_layer` for details on layer
            hyperparameters.

        `"name"`: str
            Name of the network.
        """
        return {
            "layers": [],
            "name": "NN"
        }

    @property
    def output_size(self) -> int:
        r"""The feature size of network layers output. If output size is
        only determined by input, the feature size is equal to ``-1``.
        """
        for i, layer in enumerate(reversed(self._layers)):
            size = get_output_size(layer)
            size_ext = getattr(layer, 'output_size', None)
            if size_ext is not None:
                size = size_ext
            if size is None:
                break
            if size > 0:
                return size
            elif i == len(self._layers) - 1:
                return -1

        raise ValueError("'output_size' can not be calculated because "
                         "'FeedForwardNetwork' contains submodule "
                         "whose output size cannot be determined.")
