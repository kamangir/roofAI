"""
Writing helper class for data extraction, transformation and preprocessing  
https://pytorch.org/docs/stable/data

Copied with minor modification from ../../notebooks/semseg.ipynb
"""

import os
import cv2
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset

from blue_objects import path

from roofai.dataset.classes import RoofAIDataset


class Dataset(BaseDataset):
    """CamVid Dataset. Read images, apply augmentation and preprocessing transformations.

    Args:
        images_dir (str): path to images folder
        masks_dir (str): path to segmentation masks folder
        class_values (list): values of classes to extract from segmentation mask
        augmentation (albumentations.Compose): data transformation pipeline
            (e.g. flip, scale, etc.)
        preprocessing (albumentations.Compose): data preprocessing
            (e.g. normalization, shape manipulation, etc.)

    """

    def __init__(
        self,
        images_dir,
        masks_dir,
        classes=None,
        augmentation=None,
        preprocessing=None,
        count=-1,
    ):
        self.ids = os.listdir(images_dir)
        if count != -1:
            self.ids = self.ids[:count]

        self.images_fps = [os.path.join(images_dir, image_id) for image_id in self.ids]
        self.masks_fps = [os.path.join(masks_dir, image_id) for image_id in self.ids]

        # convert str names to class values on masks
        dataset = RoofAIDataset(path.parent(images_dir, 3))

        missing_classes = [cls for cls in classes if cls.lower() not in dataset.classes]
        assert not bool(
            missing_classes
        ), "{} class(es) are not found in the dataset: {}".format(
            len(missing_classes),
            ", ".join(missing_classes),
        )

        self.class_values = [dataset.classes.index(cls.lower()) for cls in classes]
        print(
            "{}: {} class(es): {}".format(
                self.__class__.__name__,
                len(self.class_values),
                ", ".join([str(value) for value in self.class_values]),
            )
        )
        assert self.class_values

        self.augmentation = augmentation
        self.preprocessing = preprocessing

        print(f"{self.__class__.__name__}: {len(self.ids)} item(s).")

    def __getitem__(self, i):
        # read data
        image = cv2.imread(self.images_fps[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.masks_fps[i], 0)

        # extract certain classes from mask (e.g. cars)
        masks = [(mask == v) for v in self.class_values]
        mask = np.stack(masks, axis=-1).astype("float")

        # apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=image, mask=mask)
            image, mask = sample["image"], sample["mask"]

        # apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=image, mask=mask)
            image, mask = sample["image"], sample["mask"]

        return image, mask

    def __len__(self):
        return len(self.ids)
