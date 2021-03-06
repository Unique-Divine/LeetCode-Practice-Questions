import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import numpy as np
from torch import Tensor
from torch.nn.modules.activation import LeakyReLU

class FFNNClassifier(nn.Module):
    """ Currently, the feed forward neural network is a part of the lightning 
    module. I'd like to separate the neural network out from thr training 
    procedure at some point, so I began moving some of the logic from 
    LitFFNN (class) in lit_modules.py to this file. """
    def __init__(self, 
                 input_dim: int, 
                 num_classes: int,
                 hidden_dim: int = None,
                 num_hidden_layers: int = 1
        ):
        super(FFNNClassifier, self).__init__()
        self.input_dim = input_dim
        self._hidden_dim = hidden_dim
        self.num_hidden_layers = num_hidden_layers
        self.num_classes = num_classes

        self.layers = nn.ModuleList()
        self._set_layers()

    #  ---------------------  Layer types  ---------------------  #

    def RegularizedLinear(
        self, in_dim: int, out_dim: int, dropout_pct=0.1) -> nn.Sequential:  
        return nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(in_features=in_dim, out_features=out_dim),
            nn.ReLU(),
            nn.Dropout(p=dropout_pct))

    #  ---------------------  Set layers  ---------------------  #

    def _set_input_layer(self):
        input_layer = self.RegularizedLinear(
            in_dim=self.input_dim, out_dim=self.hidden_dim)
        self.layers.append(input_layer)
    
    def _set_hidden_layers(self):
        for layer_idx in range(1, self.num_hidden_layers+1):
            hidden_layer = self.RegularizedLinear(
                in_dim=self.hidden_dim, out_dim=self.hidden_dim)
            self.layers.append(hidden_layer)

    def _set_output_layer(self):
        output_layer = nn.Linear(in_features=self.hidden_dim, 
                                    out_features=self.num_classes)
        self.layers.append(output_layer)

    def _set_layers(self):
        self._set_input_layer()
        self._set_hidden_layers()
        self._set_output_layer()
    
    @property
    def hidden_dim(self) -> int:
        def init_hidden_dim():
            self._hidden_dim = round(
                np.sqrt(self.input_dim * self.num_classes)
            )
        try: 
            hidden_dim_exists: bool = self._hidden_dim is not None
            assert hidden_dim_exists
            assert isinstance(self._hidden_dim, int)
        except:
            init_hidden_dim()
        return self._hidden_dim

    #  ---------------------  Forward pass  ---------------------  #

    def forward(self, x: Tensor) -> Tensor:
        for idx, layer in enumerate(self.layers):
            x = layer(x)
        logits = F.log_softmax(input=x, dim=1)
        return logits

class FFNNRegressor(nn.Module):
    """ Currently, the feed forward neural network is a part of the lightning 
    module. I'd like to separate the neural network out from thr training 
    procedure at some point, so I began moving some of the logic from 
    LitFFNN (class) in lit_modules.py to this file. """
    def __init__(self, 
                 input_dim: int, 
                 hidden_dim: int = None,
                 num_hidden_layers: int = 1
        ):
        super(FFNNRegressor, self).__init__()
        self.input_dim = input_dim
        self._hidden_dim = hidden_dim
        self.num_hidden_layers = num_hidden_layers

        self.layers = nn.ModuleList()
        self._set_layers()

    #  ---------------------  Layer types  ---------------------  #

    def RegularizedLinear(
        self, in_dim: int, out_dim: int, dropout_pct=0.1) -> nn.Sequential:  
        return nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(in_features=in_dim, out_features=out_dim),
            nn.ReLU(),
            nn.Dropout(p=dropout_pct))

    #  ---------------------  Set layers  ---------------------  #

    def _set_input_layer(self):
        input_layer = self.RegularizedLinear(
            in_dim=self.input_dim, out_dim=self.hidden_dim)
        self.layers.append(input_layer)
    
    def _set_hidden_layers(self):
        for layer_idx in range(1, self.num_hidden_layers+1):
            hidden_layer = self.RegularizedLinear(
                in_dim=self.hidden_dim, out_dim=self.hidden_dim)
            self.layers.append(hidden_layer)

    def _set_output_layer(self):
        output_layer = nn.Linear(in_features=self.hidden_dim, 
                                 out_features=1)
        self.layers.append(output_layer)

    def _set_layers(self):
        self._set_input_layer()
        self._set_hidden_layers()
        self._set_output_layer()
    
    @property
    def hidden_dim(self) -> int:
        def init_hidden_dim():
            self._hidden_dim = 100
        hidden_dim_exists: bool = self._hidden_dim is not None
        if hidden_dim_exists: 
            assert hidden_dim_exists
            assert isinstance(self._hidden_dim, int)
        else:
            init_hidden_dim()
        return self._hidden_dim

    #  ---------------------  Forward pass  ---------------------  #

    def forward(self, x: Tensor) -> Tensor:
        for idx, layer in enumerate(self.layers):
            x = layer(x)
        preds = x
        return preds