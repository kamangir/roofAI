"""
Copied with modification from ../../notebooks/semseg.ipynb
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time
from typing import List
import torch
from torch.utils.data import DataLoader
from abcli import file
from abcli import path
from abcli.plugins import cache
import segmentation_models_pytorch as smp
from segmentation_models_pytorch import utils
from roofAI.semseg.augmentation import (
    get_training_augmentation,
    get_validation_augmentation,
    get_preprocessing,
)
from roofAI.semseg.dataloader import Dataset
from roofAI.dataset import RoofAIDataset
from roofAI.semseg.model import SemSegModel
from roofAI.semseg.utils import visualize
from roofAI.semseg import Profile
import abcli.logging
import logging

logger = logging.getLogger()


class SemSegModelTrainer(object):
    def __init__(
        self,
        dataset_path: str,
        model_path: str,
        classes: List[str],
        in_notebook: bool = False,
        profile: Profile = Profile.VALIDATION,
    ):
        self.dataset = RoofAIDataset(dataset_path)

        self.dataset_path = self.dataset.dataset_path

        self.model_path = model_path
        path.create(self.model_path, log=True)

        self.in_notebook = in_notebook
        self.profile = profile

        logger.info(
            "{}: {} -{}-> {}".format(
                self.__class__.__name__,
                path.name(self.dataset_path),
                self.profile,
                path.name(self.model_path),
            )
        )

        self.x_train_dir = os.path.join(self.dataset_path, "train")
        self.y_train_dir = os.path.join(self.dataset_path, "trainannot")

        self.x_valid_dir = os.path.join(self.dataset_path, "val")
        self.y_valid_dir = os.path.join(self.dataset_path, "valannot")

        self.x_test_dir = os.path.join(self.dataset_path, "test")
        self.y_test_dir = os.path.join(self.dataset_path, "testannot")

        dataset = Dataset(
            self.x_train_dir,
            self.y_train_dir,
            classes=classes,
            count=self.profile.data_count,
        )

        image, mask = dataset[0]  # get some sample
        visualize(
            {
                "image": image,
                "mask": mask.squeeze(),
            },
            in_notebook=in_notebook,
            filename=os.path.join(model_path, "dataset.png"),
        )

        #### Visualize resulted augmented images and masks
        augmented_dataset = Dataset(
            self.x_train_dir,
            self.y_train_dir,
            augmentation=get_training_augmentation(),
            classes=classes,
            count=self.profile.data_count,
        )

        # same image with different random transforms
        for i in range(1 if profile == Profile.VALIDATION else 3):
            image, mask = augmented_dataset[0]
            visualize(
                {
                    "image": image,
                    "mask": mask.squeeze(-1),
                },
                in_notebook=in_notebook,
                filename=os.path.join(model_path, f"augmented_dataset-{i:05d}.png"),
            )

    def train(
        self,
        classes,
        encoder_name="se_resnext50_32x4d",
        encoder_weights="imagenet",
        activation="sigmoid",  # could be None for logits or 'softmax2d' for multi-class segmentation
        device="cpu",  # 'cuda'
        register: bool = False,
        suffix: str = "v1",
        in_notebook: bool = False,
    ):
        logger.info(
            "{}.train{} -{}:{}-> {}[{}]: {}".format(
                self.__class__.__name__,
                f"[{suffix}]" if suffix else "",
                device,
                activation,
                encoder_name,
                encoder_weights,
                ",".join(classes),
            )
        )

        start_time = time.time()

        # create segmentation model with pretrained encoder
        model = smp.FPN(
            encoder_name=encoder_name,
            encoder_weights=encoder_weights,
            classes=len(classes),
            activation=activation,
        ).to(device)

        preprocessing_fn = smp.encoders.get_preprocessing_fn(
            encoder_name,
            encoder_weights,
        )

        train_dataset = Dataset(
            self.x_train_dir,
            self.y_train_dir,
            augmentation=get_training_augmentation(),
            preprocessing=get_preprocessing(preprocessing_fn),
            classes=classes,
            count=self.profile.data_count,
        )

        valid_dataset = Dataset(
            self.x_valid_dir,
            self.y_valid_dir,
            augmentation=get_validation_augmentation(),
            preprocessing=get_preprocessing(preprocessing_fn),
            classes=classes,
            count=self.profile.data_count,
        )

        train_loader = DataLoader(
            train_dataset,
            batch_size=8,
            shuffle=True,
            num_workers=0,
        )
        valid_loader = DataLoader(
            valid_dataset,
            batch_size=1,
            shuffle=False,
            num_workers=0,
        )

        # Dice/F1 score - https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
        # IoU/Jaccard score - https://en.wikipedia.org/wiki/Jaccard_index

        loss = utils.losses.DiceLoss()
        metrics = [
            utils.metrics.IoU(threshold=0.5),
        ]

        optimizer = torch.optim.Adam(
            [
                dict(params=model.parameters(), lr=0.0001),
            ]
        )

        # create epoch runners
        # it is a simple loop of iterating over dataloader`s samples
        train_epoch = smp.utils.train.TrainEpoch(
            model,
            loss=loss,
            metrics=metrics,
            optimizer=optimizer,
            device=device,
            verbose=True,
        )

        valid_epoch = smp.utils.train.ValidEpoch(
            model,
            loss=loss,
            metrics=metrics,
            device=device,
            verbose=True,
        )

        max_score = 0
        model_filename = os.path.join(self.model_path, "model.pth")
        epic_logs = {}
        epic_list = range(0, self.profile.epoch_count)
        for i in epic_list:
            logger.info("epoch: #{}/{}".format(i + 1, self.profile.epoch_count))
            train_logs = train_epoch.run(train_loader)
            valid_logs = valid_epoch.run(valid_loader)

            epic_logs[i] = {"train": train_logs, "valid": valid_logs}

            # do something (save model, change lr, etc.)
            if max_score < valid_logs["iou_score"]:
                max_score = valid_logs["iou_score"]
                torch.save(model, model_filename)
                logger.info("-> {}".format(model_filename))

            if i == 25:
                optimizer.param_groups[0]["lr"] = 1e-5
                print("Decrease decoder learning rate to 1e-5!")

        file.save_json(
            os.path.join(self.model_path, "model.json"),
            {
                "activation": activation,
                "classes": classes,
                "elapsed_time": time.time() - start_time,
                "encoder_name": encoder_name,
                "encoder_weights": encoder_weights,
                "epics": epic_logs,
            },
        )

        fig = plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        for subset in "train,valid".split(","):
            plt.plot(
                epic_list,
                [epic_logs[epic][subset]["dice_loss"] for epic in epic_list],
                label=f"{subset} loss",
            )
        plt.xlabel("epic")
        plt.ylabel("dice-loss")
        plt.grid(True)
        plt.title(path.name(self.model_path))
        plt.legend()
        plt.subplot(1, 2, 2)
        for subset in "train,valid".split(","):
            plt.plot(
                epic_list,
                [epic_logs[epic][subset]["iou_score"] for epic in epic_list],
                label=f"{subset} iou",
            )
        plt.xlabel("epic")
        plt.ylabel("iou score")
        plt.ylim(0, 1)
        plt.grid(True)
        plt.legend()
        filename = os.path.join(self.model_path, "train-summary.png")
        file.prepare_for_saving(filename)
        plt.savefig(filename)
        logger.info(f"-> {filename}")
        if in_notebook:
            plt.show()
        plt.close()

        semseg_model = SemSegModel(model_filename)

        test_dataset = Dataset(
            self.x_test_dir,
            self.y_test_dir,
            augmentation=get_validation_augmentation(),
            preprocessing=get_preprocessing(preprocessing_fn),
            classes=classes,
            count=self.profile.data_count,
        )

        test_dataloader = DataLoader(test_dataset)

        # evaluate model on test set
        test_epoch = smp.utils.train.ValidEpoch(
            model=semseg_model.model,
            loss=loss,
            metrics=metrics,
            device=device,
        )

        logs = test_epoch.run(test_dataloader)

        # TODO: semseg_model.predict(...)

        if register:
            cache.write(
                f"roofAI_semseg_model_{self.dataset.source}_{suffix}",
                path.name(self.model_path),
            )

        return semseg_model
