import sagemaker
import json
import time
from PIL import Image
from matplotlib import pyplot as plt
import PIL
import numpy as np
from abcli.elapsed_timer import ElapsedTimer
from abcli.modules import objects
from abcli.modules import host
from abcli import string
from abcli import path
from abcli import file
from abcli.plugins.storage import instance as storage
from notebooks_and_scripts.sagemaker import role
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class ImageDeserializer(sagemaker.deserializers.BaseDeserializer):
    """Deserialize a PIL-compatible stream of Image bytes into a numpy pixel array"""

    def __init__(self, accept="image/png"):
        self.accept = accept

    @property
    def ACCEPT(self):
        return (self.accept,)

    def deserialize(self, stream, content_type):
        """Read a stream of bytes returned from an inference endpoint.
        Args:
            stream (botocore.response.StreamingBody): A stream of bytes.
            content_type (str): The MIME type of the data.
        Returns:
            mask: The numpy array of class labels per pixel
        """
        try:
            return np.array(Image.open(stream))
        finally:
            stream.close()


class SageSemSegModel(object):
    def __init__(self):
        self.dataset_object_name = ""
        self.dataset_metadata = {}
        self.model_object_name = ""
        self.data_channels = {}

        timer = ElapsedTimer()
        self.session = sagemaker.Session()
        timer.stop()

        self.estimator = None

        self.training_image = sagemaker.image_uris.retrieve(
            "semantic-segmentation", self.session.boto_region_name
        )

        self.predictor = None

        logger.info(
            "{} init took {}, image: {}".format(
                self.__class__.__name__,
                timer.elapsed_pretty(include_ms=True),
                self.training_image,
            )
        )

    def train(
        self,
        dataset_object_name: str,
        model_object_name: str,
        epochs: int = 10,
        instance_type: str = "ml.p3.2xlarge",
    ) -> bool:
        self.dataset_object_name = dataset_object_name
        self.model_object_name = model_object_name

        if not storage.download_file(
            f"bolt/{dataset_object_name}/metadata.yaml", "object"
        ):
            return False

        metadata_filename = objects.path_of(
            object_name=dataset_object_name,
            filename="metadata.yaml",
        )
        success, self.dataset_metadata = file.load_yaml(metadata_filename)
        if not success:
            return False

        logger.info(
            "{}.train: {} -> {}".format(
                self.__class__.__name__,
                self.dataset_object_name,
                self.model_object_name,
            )
        )
        logger.info(
            "{}.metadata: {}".format(
                self.dataset_object_name,
                json.dumps(self.dataset_metadata, indent=4),
            )
        )

        self.estimator = sagemaker.estimator.Estimator(
            self.training_image,  # Container image URI
            role,  # Training job execution role with permissions to access our S3 bucket
            instance_count=1,
            instance_type=instance_type,
            volume_size=50,  # in GB
            max_run=360000,  # in seconds
            output_path=f"s3://kamangir/bolt/{model_object_name}",
            base_job_name=model_object_name,
            sagemaker_session=self.session,
        )

        num_classes = (
            21
            if "classes" not in self.dataset_metadata
            else len(self.dataset_metadata["classes"])
        )
        logger.info(f"num_classes: {num_classes}")

        self.estimator.set_hyperparameters(
            backbone="resnet-50",  # This is the encoder. Other option is resnet-101
            algorithm="fcn",  # This is the decoder. Other options are 'psp' and 'deeplab'
            use_pretrained_model="True",  # Use the pre-trained model.
            crop_size=240,  # Size of image random crop.
            num_classes=num_classes,  # Pascal has 21 classes. This is a mandatory parameter.
            epochs=epochs,  # Number of epochs to run.
            learning_rate=0.0001,
            optimizer="rmsprop",  # Other options include 'adam', 'rmsprop', 'nag', 'adagrad'.
            lr_scheduler="poly",  # Other options include 'cosine' and 'step'.
            mini_batch_size=16,  # Setup some mini batch size.
            validation_mini_batch_size=16,
            early_stopping=True,  # Turn on early stopping. If OFF, other early stopping parameters are ignored.
            early_stopping_patience=2,  # Tolerate these many epochs if the mIoU doens't increase.
            early_stopping_min_epochs=10,  # No matter what, run these many number of epochs.
            num_training_samples=self.dataset_metadata["num"][
                "train"
            ],  # num_training_samples,  # This is a mandatory parameter, 1464 in this case.
        )

        distribution = "FullyReplicated"
        self.data_channels = {
            "train": sagemaker.inputs.TrainingInput(
                self.dataset_metadata["channel"]["train"],
                distribution=distribution,
            ),
            "validation": sagemaker.inputs.TrainingInput(
                self.dataset_metadata["channel"]["validation"],
                distribution=distribution,
            ),
            "train_annotation": sagemaker.inputs.TrainingInput(
                self.dataset_metadata["channel"]["train_annotation"],
                distribution=distribution,
            ),
            "validation_annotation": sagemaker.inputs.TrainingInput(
                self.dataset_metadata["channel"]["validation_annotation"],
                distribution=distribution,
            ),
            # 'label_map': metadata["channel"]["label_map"], # label_map_channel
        }

        self.estimator.fit(self.data_channels, logs=True)

        return True

    def deploy(self, **kwargs):
        self.predictor = self.estimator.deploy(**kwargs)

        path.create(
            objects.path_of(
                object_name=self.model_object_name,
                filename="validation/",
            )
        )
        filename_raw = objects.path_of(
            object_name=self.model_object_name,
            filename="validation/test.jpg",
        )

        host.shell(
            f"wget -O {filename_raw} https://github.com/kamangir/blue-bracket/raw/main/images/helmet-1.jpg"
        )

        filename = objects.path_of(
            object_name=self.model_object_name,
            filename="validation/test_resized.jpg",
        )
        width = 800
        im = PIL.Image.open(filename_raw)
        aspect = im.size[0] / im.size[1]
        # https://stackoverflow.com/a/14351890/17619982
        im.thumbnail([width, int(width / aspect)], PIL.Image.LANCZOS)
        im.save(filename, "JPEG")
        plt.imshow(im)
        if host.is_jupyter():
            plt.show()
        plt.close()

        self.predictor.deserializer = ImageDeserializer(accept="image/png")

        self.predictor.serializer = sagemaker.serializers.IdentitySerializer(
            "image/jpeg"
        )

        with open(filename, "rb") as imfile:
            imbytes = imfile.read()

        # Extension exercise: Could you write a custom serializer which takes a filename as input instead?

        start_time = time.time()
        cls_mask = self.predictor.predict(imbytes)
        elapsed_time = time.time() - start_time

        logger.info(
            "{} -> {}: {}".format(
                string.pretty_duration(elapsed_time),
                string.pretty_shape_of_matrix(cls_mask),
                np.unique(cls_mask),
            )
        )

        plt.imshow(cls_mask, cmap="jet")
        plt.savefig(
            objects.path_of(
                object_name=self.model_object_name,
                filename="validation/output.jpg",
            )
        )
        if host.is_jupyter():
            plt.show()

    def delete_endpoint(self):
        self.predictor.delete_endpoint()
