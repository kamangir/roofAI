import os.path
from typing import List
from roofAI.semseg.model import SemSegModel
from roofAI.semseg.train import SemSegModelTrainer
from roofAI.semseg import Profile
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
    register: bool = False,
    suffix: str = "v1",
    profile: Profile = Profile.VALIDATION,
    in_notebook: bool = False,
) -> Tuple[bool, Any]:
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
        register=register,
        suffix=suffix,
        in_notebook=in_notebook,
    )

    model.predict(
        dataset_path=dataset_path,
        output_path=os.path.join(dataset_path, "_validation"),
        in_notebook=in_notebook,
    )

    return model
