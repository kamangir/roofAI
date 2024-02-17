import os
import glob
import json
from tqdm import tqdm
import sagemaker
import shutil
from abcli import file
from abcli.modules import objects
from abcli import logging
import logging

logger = logging.getLogger(__name__)


# https://github.com/aws/amazon-sagemaker-examples/blob/main/introduction_to_amazon_algorithms/semantic_segmentation_pascalvoc/semantic_segmentation_pascalvoc.ipynb
def upload(
    dataset_object_name: str,
    object_name,
    count: int = -1,
):
    dataset_object_path = objects.object_path(dataset_object_name)
    object_path = objects.object_path(object_name, create=True)

    logger.info(
        "uploading: {} -{}> {}".format(
            dataset_object_path,
            f"{count}-" if count != -1 else "",
            object_path,
        )
    )

    """
    Move the images into appropriate directory structure as described in the 
    [documentation](link-to-documentation). This is quite simply, moving the 
    training images to `train` directory and so on. Fortunately, the dataset's 
    annotations are already named in sync with the image names, satisfying one 
    requirement of the Amazon SageMaker Semantic Segmentation algorithm.
    """

    # Create directory structure mimicing the s3 bucket where data is to be dumped.
    VOC2012 = os.path.join(dataset_object_path, "pascal-voc/VOC2012")
    for sub_folder in "train,validation,train_annotation,validation_annotation".split(
        ","
    ):
        os.makedirs(os.path.join(object_path, f"data/{sub_folder}"), exist_ok=True)

    # Create a list of all training images.
    with open(VOC2012 + "/ImageSets/Segmentation/train.txt") as f:
        train_list = f.read().splitlines()

    if count != -1:
        train_list = train_list[:count]

    # Create a list of all validation images.
    with open(VOC2012 + "/ImageSets/Segmentation/val.txt") as f:
        val_list = f.read().splitlines()

    if count != -1:
        val_list = val_list[:count]

    # Move the jpg images in training list to train directory and png images to train_annotation directory.
    for i in tqdm(train_list):
        file.copy(
            VOC2012 + "/JPEGImages/" + i + ".jpg",
            os.path.join(object_path, "data/train/", i + ".jpg"),
            log=False,
            overwrite=False,
        )
        file.copy(
            VOC2012 + "/SegmentationClass/" + i + ".png",
            os.path.join(object_path, "data/train_annotation/", i + ".png"),
            log=False,
            overwrite=False,
        )

    # Move the jpg images in validation list to validation directory and png images to validation_annotation directory.
    for i in tqdm(val_list):
        file.copy(
            VOC2012 + "/JPEGImages/" + i + ".jpg",
            os.path.join(object_path, "data/validation/", i + ".jpg"),
            log=False,
            overwrite=False,
        )
        file.copy(
            VOC2012 + "/SegmentationClass/" + i + ".png",
            os.path.join(object_path, "data/validation_annotation/", i + ".png"),
            log=False,
            overwrite=False,
        )

    """
    Let us check if the move was completed correctly. If it was done correctly, the 
    number of jpeg images in `train` and png images in `train_annotation` must be the 
    same, and so in validation as well.
    """

    metadata = {"num": {}}
    metadata["num"]["train"] = len(
        glob.glob1(
            os.path.join(object_path, "data/train"),
            "*.jpg",
        )
    )
    metadata["num"]["val"] = len(
        glob.glob1(
            os.path.join(object_path, "data/validation"),
            "*.jpg",
        )
    )
    logger.info("{} train image(s)".format(metadata["num"]["train"]))
    assert metadata["num"]["train"] == len(
        glob.glob1(
            os.path.join(object_path, "data/train_annotation"),
            "*.png",
        )
    )
    logger.info("{} validation image(s)".format(metadata["num"]["val"]))
    assert metadata["num"]["val"] == len(
        glob.glob1(
            os.path.join(object_path, "data/validation_annotation"),
            "*.png",
        )
    )

    """
    Let us now upload our prepared datset to the S3 bucket that we decided to use in this notebook 
    earlier. Notice the following directory structure that is used.

    ```bash
    root 
    |-train/
    |-train_annotation/
    |-validation/
    |-validation_annotation/

    ```

    Notice also that all the images in the `_annotation` directory are all indexed PNG files. This 
    implies that the metadata (color mapping modes) of the files contain information on how to map 
    the indices to colors and vice versa. Having an indexed PNG is an advantage as the images will 
    be rendered by image viewers as color images, but the image themsevels only contain integers. 
    The integers are also within `[0, 1 ... c-1, 255]`  for a `c` class segmentation problem, with 
    `255` as 'hole' or 'ignore' class. We allow any mode that is a 
    [recognized standard](https://pillow.readthedocs.io/en/3.0.x/handbook/concepts.html#concept-modes) 
    as long as they are read as integers.

    While we recommend the format with default color mapping modes such as PASCAL, the algorithm also 
    allows users to specify their own label maps. Refer to the 
    [documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/semantic-segmentation.html#semantic-segmentation-inputoutput) 
    for more details. The label map for the PASCAL VOC dataset is the default, which is equivalent to:

    ```json
    {
        "scale": 1
    }
    ```

    This essentially tells the algorithm to directly use the image pixel value integers as labels. 
    Since we are using PASCAL dataset, let us create (recreate the default just for demonstration) a 
    label map for training channel and let the algorithm use the default (which is exactly the same)
    for the validation channel. If `label_map` is used, please pass it to the label_map channel.
    """

    label_map = {"scale": 1}
    with open(os.path.join(object_path, "data/train_label_map.json"), "w") as lmfile:
        json.dump(label_map, lmfile)

    sess = sagemaker.Session()

    abcli_s3_object_prefix = os.getenv(
        "$abcli_s3_object_prefix",
        "s3://kamangir/bolt",
    )
    bucket = abcli_s3_object_prefix.split("s3://", 1)[1].split("/")[0]
    prefix = "{}/{}".format(
        abcli_s3_object_prefix.split("s3://", 1)[1].split("/", 1)[1],
        object_name,
    )

    # Let us now upload our dataset, including our optional label map.
    metadata["bucket"] = bucket
    metadata["prefix"] = prefix
    logger.info(f"-> s3: bucket={bucket}, prefix={prefix}")

    metadata["channel"] = {}
    for channel in ["train", "train_annotation", "validation", "validation_annotation"]:
        metadata["channel"][channel] = sess.upload_data(
            path=os.path.join(object_path, "data/{}".format(channel)),
            bucket=bucket,
            key_prefix=prefix + "/{}".format(channel),
        )
        logger.info("train channel: {}".format(metadata["channel"][channel]))

    metadata["channel"]["label_map"] = sess.upload_data(
        path=os.path.join(object_path, "data/train_label_map.json"),
        bucket=bucket,
        key_prefix=prefix + "/label_map",
    )
    logger.info("label_map channel: {}".format(metadata["channel"]["label_map"]))

    file.save_yaml(os.path.join(object_path, "metadata.yaml"), metadata)
    logger.info(
        "-> {}".format(
            sess.upload_data(
                path=os.path.join(object_path, "metadata.yaml"),
                bucket=bucket,
                key_prefix=prefix,
            )
        )
    )

    return metadata
