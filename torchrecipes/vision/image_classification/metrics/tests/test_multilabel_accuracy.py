# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import testslide
import torch
from torchrecipes.vision.image_classification.metrics.multilabel_accuracy import (
    MultilabelAccuracy,
)


class TestMultilabelAccuracy(testslide.TestCase):
    def test_top_k(self) -> None:
        metric = MultilabelAccuracy(top_k=2)
        self.assertTrue(torch.equal(metric.compute(), torch.tensor(0.0)))

        preds = torch.tensor([[1.0, -1.0, 2.0]])
        target = torch.tensor([[0, 1.0, 0]])
        metric.update(preds, target)
        # none of the labels is in the top_k prediction
        self.assertTrue(torch.equal(metric.compute(), torch.tensor(0.0)))

        preds = torch.tensor([[1.0, -0.5, 2.0]])
        target = torch.tensor([[1, 1, 0]])
        metric.update(preds, target)
        # one of the labels is in the top_k prediction
        # one out of the two samples is correctly classified
        self.assertTrue(torch.equal(metric.compute(), torch.tensor(0.5)))

    def test_invalid_top_k(self) -> None:
        metric = MultilabelAccuracy(top_k=10)

        preds = torch.tensor([[1.0]])
        target = torch.tensor([[0]])
        with self.assertRaises(AssertionError):
            metric.update(preds, target)
