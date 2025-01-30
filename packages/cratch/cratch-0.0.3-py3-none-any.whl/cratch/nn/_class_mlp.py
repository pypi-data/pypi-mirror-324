#coding:UTF-8

"""
# Name    : _class_mlp.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool of MLP.
"""

import torch.nn as nn
from collections import OrderedDict

#-----------------------------------------------------------------------------#
class MLP(nn.Module):
    """
    Multi Layer Perceptron class

    Parameters
    ----------
    num_input : int
        number of input data
    num_output: int
        number of output data
    num_neuron: int or list (same length of num_hidden)
        number of neuron
    num_hidden: int
        numbe or hidden layers
    activation: func (torch.nn module)
        activation function
        default function is nn.SiLU()

    Examples
    --------
    >>> import torch.nn as nn
    >>> import cratch
    >>> num_input = 5
    >>> num_output = 1
    >>> num_neuron = 3
    >>> num_hidden = 5
    >>> activation = nn.SiLU
    >>> net = cratch.nn.MLP(num_input, num_output, num_neuron, num_hidden, activation)
    >>> net
    MLP(
      (layers): Sequential(
        (input_hid): Linear(in_features=5, out_features=3, bias=True)
        (act_fnc_00): SiLU()
        (hid_hid_01): Linear(in_features=3, out_features=3, bias=True)
        (act_fnc_01): SiLU()
        (hid_hid_02): Linear(in_features=3, out_features=3, bias=True)
        (act_fnc_02): SiLU()
        (hid_hid_03): Linear(in_features=3, out_features=3, bias=True)
        (act_fnc_03): SiLU()
        (hid_hid_04): Linear(in_features=3, out_features=3, bias=True)
        (act_fnc_04): SiLU()
        (hid_output): Linear(in_features=3, out_features=1, bias=True)
      )
    )
    """
    def __init__(self, num_input, num_output, num_neuron=0,\
                 num_hidden=0, activation=nn.SiLU):
        super(MLP, self).__init__()
        self.num_input = num_input
        self.num_output = num_output
        self.num_neuron = num_neuron
        self.num_hidden = num_hidden
        self.activation = activation

        if num_hidden != 0:
            if type(num_neuron) != list:
                num_neuron = [num_neuron] * num_hidden

            elif num_hidden != len(num_neuron):
                print('Please check list of num_neuron')
                exit()

        if num_hidden == 0:
            layers = [('input_output', nn.Linear(num_input, num_output))]

        else:
            layers = [('input_hid', nn.Linear(num_input, num_neuron[0]))]
            layers.append(('act_fnc_00', activation()))
            if num_hidden > 1:
                for i in range(1, num_hidden):
                    layers.append( ('hid_hid_%02d' %\
                        i, nn.Linear(num_neuron[i-1], num_neuron[i])))
                    layers.append(('act_fnc_%02d' % i, activation()))
                layers.append(('hid_output', \
                    nn.Linear(num_neuron[i], num_output)))
            else:
                layers.append(('hid_output', \
                    nn.Linear(num_neuron[0], num_output)))
        layer_dict = OrderedDict(layers)
        self.layers = nn.Sequential(layer_dict)

    def forward(self, x):
        out = self.layers(x)
        return out

#-----------------------------------------------------------------------------#
