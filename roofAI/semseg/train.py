import os
from roofAI.semseg.augmentation import get_training_augmentation
from roofAI.semseg.dataloader import Dataset
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
        in_notebook: bool = False,
        profile: Profile = Profile.VALIDATION,
    ):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.in_notebook = in_notebook
        self.profile = profile
        logger.info(
            "{}: {} -{}-> {}".format(
                self.__class__.__name__,
                self.dataset_path,
                self.profile,
                self.model_path,
            )
        )

        self.x_train_dir = os.path.join(self.dataset_path, "train")
        self.y_train_dir = os.path.join(self.dataset_path, "trainannot")

        self.x_valid_dir = os.path.join(self.dataset_path, "val")
        self.y_valid_dir = os.path.join(self.dataset_path, "valannot")

        self.x_test_dir = os.path.join(self.dataset_path, "test")
        self.y_test_dir = os.path.join(self.dataset_path, "testannot")

        if in_notebook:
            logger.info("data review")
            dataset = Dataset(
                self.x_train_dir,
                self.y_train_dir,
                classes=["car"],
                count=self.profile.data_count,
            )

            image, mask = dataset[0]  # get some sample
            visualize(
                image=image,
                cars_mask=mask.squeeze(),
            )

        if in_notebook:
            #### Visualize resulted augmented images and masks
            augmented_dataset = Dataset(
                self.x_train_dir,
                self.y_train_dir,
                augmentation=get_training_augmentation(),
                classes=["car"],
                count=self.profile.data_count,
            )

            # same image with different random transforms
            for _ in range(1 if profile == Profile.VALIDATION else 3):
                image, mask = augmented_dataset[0]
                visualize(image=image, mask=mask.squeeze(-1))
