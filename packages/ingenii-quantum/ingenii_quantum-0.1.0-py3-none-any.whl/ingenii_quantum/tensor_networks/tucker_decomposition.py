from tensorly.decomposition import partial_tucker
import tensorly as tl
import torch
import torch.nn as nn
import numpy as np

def tucker_decomposition_conv_layer(layer, ranks):
    """ 
    Gets a convolutional layer, applies Tucker decomposition and returns the set of smaller layers.

    Args:
        layer (torch layer): convolutional layer to decompose
        ranks (tuple): Ranks of the Tucker decomposition

    Returns 
        nn.Sequential: object with the Tucker decomposition.
    """
    tensors, _ = \
        partial_tucker(tl.tensor(layer.weight.data), \
            ranks, modes=[0, 1], init='svd')
    core, [last, first] = tensors
    
    # A pointwise convolution that reduces the channels from S to R3
    first_layer = torch.nn.Conv2d(in_channels=first.shape[0], \
            out_channels=first.shape[1], kernel_size=1,
            stride=1, padding=0, dilation=layer.dilation, bias=False)

    # A regular 2D convolution layer with R3 input channels and R3 output channels
    core_layer = torch.nn.Conv2d(in_channels=core.shape[1], \
            out_channels=core.shape[0], kernel_size=layer.kernel_size,
            stride=layer.stride, padding=layer.padding, dilation=layer.dilation,
            bias=False)

    # A pointwise convolution that increases the channels from R4 to T
    last_layer = torch.nn.Conv2d(in_channels=last.shape[1], \
                                 out_channels=last.shape[0], kernel_size=1, stride=1,
                                 padding=0, dilation=layer.dilation, bias=True)

    if layer.bias is not None:
        last_layer.bias.data = layer.bias.data

    first_layer.weight.data = \
        torch.transpose(torch.tensor(first), 1, 0).unsqueeze(-1).unsqueeze(-1)
    last_layer.weight.data = torch.tensor(last).unsqueeze(-1).unsqueeze(-1)
    core_layer.weight.data = torch.tensor(core)

    new_layers = [first_layer, core_layer, last_layer]
    return nn.Sequential(*new_layers)

def count_params(network):
    '''
    Counts the number of parameters in the neural network

    Args:
        network (torch.nn): Neural network model
        
    Returns:
        float: Number of training parameters
    '''
    return np.sum(np.prod(p.size()) for p in network.parameters())

