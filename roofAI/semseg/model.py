from abcli import file
import torch
import abcli.logging
import logging

logger = logging.getLogger()


class SemSegModel(object):
    def __init__(self, filename: str):
        logger.info(
            "{}.load({})".format(
                self.__class__.__name__,
                filename,
            )
        )
        self.filename = filename
        self.model = torch.load(self.filename)

        success, metadata = file.load_json(
            file.set_extension(
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
    def signature(self):
        return "{}: {}[{}]-{}-> {}".format(
            self.__class__.__name__,
            self.encoder_name,
            self.encoder_weights,
            self.activation,
            ",".join(self.classes),
        )
