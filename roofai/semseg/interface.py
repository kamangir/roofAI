import os.path
from typing import List
from roofai.semseg.model import SemSegModel
from roofai.semseg.train import SemSegModelTrainer
from roofai.semseg import Profile
from typing import Tuple, Any


def predict(
    model_path: str,
    dataset_path: str,
    prediction_path: str,
    device: str,
    profile: Profile = Profile.VALIDATION,
    in_notebook: bool = False,
):
    model = SemSegModel(
        model_filename=os.path.join(model_path, "model.pth"),
        profile=profile,
        device=device,
    )

    model.predict(
        dataset_path=dataset_path,
        output_path=prediction_path,
        in_notebook=in_notebook,
    )


def train(
    dataset_path: str,
    model_path: str,
    classes: List[str],
    encoder_name="se_resnext50_32x4d",
    encoder_weights="imagenet",
    activation="sigmoid",  # could be None for logits or 'softmax2d' for multi-class segmentation
    device="cpu",  # 'cuda'
    profile: Profile = Profile.VALIDATION,
    in_notebook: bool = False,
    epoch_count: int = -1,
) -> SemSegModel:
    trainer = SemSegModelTrainer(
        dataset_path=dataset_path,
        model_path=model_path,
        classes=classes,
        in_notebook=in_notebook,
        profile=profile,
    )

    model = trainer.train(
        classes=classes,
        encoder_name=encoder_name,
        encoder_weights=encoder_weights,
        activation=activation,
        device=device,
        in_notebook=in_notebook,
        epoch_count=epoch_count,
    )

    model.predict(
        dataset_path=dataset_path,
        output_path=model_path,
        in_notebook=in_notebook,
    )

    return model
