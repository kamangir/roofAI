"""
Copied with modification from ../../notebooks/semseg.ipynb
"""

import os
import time
import numpy as np
import torch
import cv2
from tqdm import tqdm
from scipy import ndimage
import segmentation_models_pytorch as smp
from shapely.geometry import Polygon

from blue_options import string
from blue_objects import file, path
from blue_objects.graphics.gif import generate_animated_gif

from roofai.semseg.augmentation import get_validation_augmentation, get_preprocessing
from roofai.dataset.classes import RoofAIDataset
from roofai.semseg.dataloader import Dataset
from roofai.semseg.utils import visualize
from roofai.semseg import Profile
from roofai.logger import logger


class SemSegModel:
    def __init__(
        self,
        model_filename: str,
        profile: Profile = Profile.VALIDATION,
        device="cpu",  # 'cuda'
        tolerance: float = 2,
    ):
        self.profile = profile
        self.filename = model_filename
        self.tolerance = tolerance
        self.device = device

        logger.info(
            "{}.load({}) on {}: {}".format(
                self.__class__.__name__,
                self.filename,
                self.device,
                self.profile,
            )
        )

        self.model = torch.load(self.filename).to(self.device)

        success, metadata = file.load_json(
            file.add_extension(
                self.filename,
                "json",
            )
        )
        assert success

        self.encoder_name = metadata["encoder_name"]
        self.encoder_weights = metadata["encoder_weights"]
        self.classes = metadata["classes"]
        self.activation = metadata["activation"]

        logger.info(self.signature)

    @property
    def object_name(self):
        return path.name(file.path(self.filename))

    def predict(
        self,
        dataset_path,
        output_path,
        in_notebook: bool = False,
    ):
        dataset = RoofAIDataset(dataset_path)

        logger.info(
            "{}.predict({}:{}) -{}-> {}".format(
                self.__class__.__name__,
                dataset.source,
                dataset.dataset_path,
                self.device,
                output_path,
            )
        )

        x_test_dir = os.path.join(dataset.dataset_path, "test")
        y_test_dir = os.path.join(dataset.dataset_path, "testannot")

        # test dataset without transformations for image visualization
        test_dataset_vis = Dataset(
            x_test_dir,
            y_test_dir,
            classes=self.classes,
            count=self.profile.data_count,
        )

        preprocessing_fn = smp.encoders.get_preprocessing_fn(
            self.encoder_name,
            self.encoder_weights,
        )

        test_dataset = Dataset(
            x_test_dir,
            y_test_dir,
            augmentation=get_validation_augmentation(),
            preprocessing=get_preprocessing(preprocessing_fn),
            classes=self.classes,
            count=self.profile.data_count,
        )

        list_of_images = []
        index_list = (
            [np.random.choice(len(test_dataset))]
            if self.profile == Profile.VALIDATION
            else range(len(test_dataset))
        )
        for n in tqdm(index_list):
            image_vis = test_dataset_vis[n][0].astype("uint8")
            image, gt_mask = test_dataset[n]

            gt_mask = gt_mask.squeeze()

            start_time = time.time()
            x_tensor = torch.from_numpy(image).to(self.device).unsqueeze(0)
            pr_mask = self.model.predict(x_tensor)
            pr_mask = pr_mask.squeeze().cpu().numpy().round()
            elapsed_time = time.time() - start_time
            logger.info(
                "took {}".format(
                    string.pretty_duration(
                        elapsed_time,
                        include_ms=True,
                    )
                )
            )

            label_mask, label_count = ndimage.label(pr_mask)
            logger.info(f"{label_count} object(s) found.")
            list_of_contours = []
            for label in range(1, label_count + 1):
                mask = label_mask == label

                contour, _ = cv2.findContours(
                    mask.astype(np.uint8),
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE,
                )

                if contour[0].shape[0] <= 4:
                    continue

                polygon = Polygon(
                    [
                        (x, y)
                        for x, y in zip(
                            contour[0][:, 0, 0],
                            contour[0][:, 0, 1],
                        )
                    ]
                )
                polygon = polygon.simplify(self.tolerance)

                list_of_contours.append(
                    (
                        list(polygon.exterior.xy[0]),
                        list(polygon.exterior.xy[1]),
                    )
                )

            file.save_json(
                os.path.join(output_path, f"predict-{n:05d}.json"),
                {
                    "count": label_count,
                    "contour": list_of_contours,
                    "device": self.device,
                    "elapsed_time": elapsed_time,
                },
            )

            filename = os.path.join(output_path, f"predict-{n:05d}.png")
            visualize(
                {
                    "image": image_vis,
                    "groundtruth": gt_mask,
                    "prediction": pr_mask,
                },
                in_notebook=in_notebook,
                filename=filename,
                description=[
                    f"model: {self.object_name}",
                    self.signature,
                    f"device: {self.device}",
                    f"{label_count} object(s)",
                    "took {}".format(
                        string.pretty_duration(
                            elapsed_time,
                            include_ms=True,
                            short=True,
                            largest=True,
                        )
                    ),
                ],
                list_of_contours=list_of_contours,
            )
            list_of_images += [filename]

        generate_animated_gif(
            list_of_images,
            os.path.join(output_path, "predict.gif"),
            frame_duration=500,
        )

    @property
    def signature(self):
        return "{}: {}[{}]-{}-> {}: {:.2f}".format(
            self.__class__.__name__,
            self.encoder_name,
            self.encoder_weights,
            self.activation,
            ",".join(self.classes),
            self.tolerance,
        )
