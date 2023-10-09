import abcli.logging
import logging

logger = logging.getLogger()


class SemSegModel(object):
    def __init__(self):
        ...

    @staticmethod
    def load(model_filename: str):
        logger.info(f"SemSegModel.load({model_filename})")
        ...

    @staticmethod
    def train(
        dataset_path: str,
        model_path: str,
    ):
        model = SemSegModel()

        logger.info(f"{model.__class__.__name__}.train: {dataset_path} -> {model_path}")

        return model
