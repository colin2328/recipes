# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


# pyre-strict
import os

import hydra
from pytorch_lightning.trainer import Trainer
from torchrecipes.text.doc_classification.conf.common import (
    AdamWConf,
    ClassificationHeadConf,
    DocClassificationTransformConf,
    XLMREncoderConf,
    XLMRClassificationModelConf,
    SST2DatasetConf,
    LabelTransformConf,
)
from torchrecipes.text.doc_classification.datamodule.doc_classification import (
    DocClassificationDataModule,
    DocClassificationDataModuleConf,
)
from torchrecipes.text.doc_classification.module.doc_classification import (
    DocClassificationModule,
    DocClassificationModuleConf,
)
from torchrecipes.text.doc_classification.tests.common.assets import _DATA_DIR_PATH
from torchrecipes.text.doc_classification.transform.doc_classification_text_transform import (
    DocClassificationTextTransformConf,
)
from torchrecipes.utils.task_test_base import TaskTestCaseBase


class TestDocClassificationModule(TaskTestCaseBase):
    def setUp(self) -> None:
        self.base_dir = os.path.join(os.path.dirname(__file__), "data")

    def get_transform_conf(self) -> DocClassificationTransformConf:
        doc_transform_conf = DocClassificationTextTransformConf(
            vocab_path="https://download.pytorch.org/models/text/xlmr.vocab.pt",
            spm_model_path="https://download.pytorch.org/models/text/xlmr.sentencepiece.bpe.model",
        )
        label_transform_conf = LabelTransformConf(label_names=["0", "1"])
        return DocClassificationTransformConf(
            transform=doc_transform_conf, label_transform=label_transform_conf
        )

    def get_standard_task(self) -> DocClassificationModule:
        module_conf = DocClassificationModuleConf(
            model=XLMRClassificationModelConf(
                encoder_conf=XLMREncoderConf(),
                head=ClassificationHeadConf(
                    num_classes=2,
                    input_dim=768,
                ),
                freeze_encoder=True,
                checkpoint="https://download.pytorch.org/models/text/xlmr.base.encoder.pt",
            ),
            optim=AdamWConf(),
        )
        transform_conf = self.get_transform_conf()
        num_classes = len(transform_conf.label_transform.label_names)  # pyre-ignore
        return hydra.utils.instantiate(
            module_conf,
            transform=transform_conf.transform,
            num_classes=num_classes,
            _recursive_=False,
        )

    def get_datamodule(self) -> DocClassificationDataModule:
        transform_conf = self.get_transform_conf()
        dataset_conf = SST2DatasetConf(root=_DATA_DIR_PATH, validate_hash=False)
        datamodule_conf = DocClassificationDataModuleConf(
            transform=transform_conf,
            dataset=dataset_conf,
            batch_size=8,
        )
        return hydra.utils.instantiate(
            datamodule_conf,
            _recursive_=False,
        )

    def test_python_conf(self) -> None:
        # pyre-fixme[16]: `TestDocClassificationModule` has no attribute `datamodule`.
        self.datamodule = self.get_datamodule()
        task = self.get_standard_task()
        trainer = Trainer(fast_dev_run=True)
        trainer.fit(task, datamodule=self.datamodule)

        pred1 = task.forward({"text": ["hello world", "how are you?"]})
        pred2 = task.forward(
            {"text": ["hello world", "how are you?"], "label": ["1", "0"]}
        )
        self.assertTrue(pred1 is not None)
        self.assertTrue(pred2 is not None)
