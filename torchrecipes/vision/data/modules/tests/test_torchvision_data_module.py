#!/usr/bin/env python3

import unittest
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional, Union

import torch
from hydra.core.config_store import ConfigStore
from hydra.experimental import compose, initialize
from hydra.utils import instantiate
from torchrecipes.vision.data.modules.torchvision_data_module import (
    TorchVisionDataModule,
    TorchVisionDataModuleConf,
)
from torchrecipes.vision.data.transforms.builder import (
    build_transforms_from_dataset_config,
)
from torchvision.datasets.mnist import MNIST
from torchvision.datasets.vision import VisionDataset


class TestTorchVisionDataModule(unittest.TestCase):
    data_path: str

    @classmethod
    def setUpClass(cls) -> None:
        data_path_ctx = TemporaryDirectory()
        cls.addClassCleanup(data_path_ctx.cleanup)
        cls.data_path = data_path_ctx.name

        # Download the torchvision MNIST dataset for testing
        MNIST(cls.data_path, train=True, download=True)
        MNIST(cls.data_path, train=False, download=True)

        # Create hydra config nodes
        cs = ConfigStore.instance()
        cs.store(name="torchvision_data_module", node=TorchVisionDataModuleConf)

    def test_init_datamodule_with_hydra(self) -> None:
        datasets_conf = self._get_datasets_config(download=False)
        with initialize():
            test_conf = compose(config_name="torchvision_data_module")
            test_conf.datasets = datasets_conf
            torchvision_data_module = instantiate(test_conf, _recursive_=False)
            self.assertIsInstance(torchvision_data_module, TorchVisionDataModule)

    def test_creating_datamodule(self) -> None:
        torchvision_data_module = self.get_torchvision_data_module()
        self.assertIsInstance(torchvision_data_module, TorchVisionDataModule)
        torchvision_data_module.setup()
        dataloder = torchvision_data_module.train_dataloader()
        img, _ = next(iter(dataloder))
        self.assertEqual(img.size(), torch.Size([1, 1, 64, 64]))

    def test_val_split(self) -> None:
        torchvision_data_module = self.get_torchvision_data_module(val_split=100)
        torchvision_data_module.setup()
        # pyre-ignore[6]: dataset has length
        self.assertEqual(len(torchvision_data_module.datasets["train"]), 59900)
        # pyre-ignore[6]: dataset has length
        self.assertEqual(len(torchvision_data_module.datasets["val"]), 100)

        torchvision_data_module = self.get_torchvision_data_module(val_split=0.1)
        torchvision_data_module.setup()
        # pyre-ignore[6]: dataset has length
        self.assertEqual(len(torchvision_data_module.datasets["train"]), 54000)
        # pyre-ignore[6]: dataset has length
        self.assertEqual(len(torchvision_data_module.datasets["val"]), 6000)

    def get_datasets_from_config(self) -> Dict[str, VisionDataset]:
        datasets_conf = self._get_datasets_config(download=False)
        datasets = {}
        for split, dataset_conf in datasets_conf.items():
            if dataset_conf is None:
                datasets[split] = None
            else:
                dataset_conf = dict(dataset_conf)
                dataset_conf = build_transforms_from_dataset_config(dataset_conf)
                datasets[split] = instantiate(dataset_conf, _recursive_=False)
        return datasets

    def get_torchvision_data_module(
        self,
        batch_size: int = 1,
        val_split: Optional[Union[int, float]] = None,
    ) -> TorchVisionDataModule:
        datasets = self.get_datasets_from_config()
        return TorchVisionDataModule(
            datasets=datasets,
            val_split=val_split,
            batch_size=batch_size,
        )

    def _get_datasets_config(self, download: bool = False) -> Dict[str, Any]:
        return {
            "train": {
                "_target_": "torchvision.datasets.mnist.MNIST",
                "train": True,
                "root": self.data_path,
                "download": download,
                "transform": [
                    {
                        "_target_": "torchvision.transforms.Resize",
                        "size": 64,
                    },
                    {
                        "_target_": "torchvision.transforms.ToTensor",
                    },
                ],
            },
            "val": None,
            "test": {
                "_target_": "torchvision.datasets.mnist.MNIST",
                "train": False,
                "root": self.data_path,
                "download": download,
                "transform": [
                    {
                        "_target_": "torchvision.transforms.Resize",
                        "size": 64,
                    },
                    {
                        "_target_": "torchvision.transforms.ToTensor",
                    },
                ],
            },
        }
