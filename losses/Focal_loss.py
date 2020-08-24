import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, pos_ratio=None, alpha=1, gamma=2, **kwargs):
        super(FocalLoss, self).__init__()
        self.pos_ratio = pos_ratio
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        batch_size = inputs.shape[0]
        loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-loss)
        loss = self.alpha * (1-pt)**self.gamma * loss
        
        if self.pos_ratio is not None:
            weight = self.__ratio2weight(targets, self.pos_ratio)
            loss = (loss * weight)
        loss = loss.sum() / batch_size if self.reduction == 'mean' else loss.sum()
        return loss
