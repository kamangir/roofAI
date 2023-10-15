import os.path
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
) -> bool:
    model = SemSegModel(
        model_filename=os.path.join(model_path, "model.pth"),
        profile=profile,
    )

    model.predict(
        dataset_path=dataset_path,
        output_path=prediction_path,
        device=device,
        in_notebook=in_notebook,
    )

    return True


def train(
    dataset_path: str,
    model_path: str,
    profile: Profile = Profile.VALIDATION,
    in_notebook: bool = False,
    **kwargs,
) -> Tuple[bool, Any]:
    trainer = SemSegModelTrainer(
        dataset_path=dataset_path,
        model_path=model_path,
        in_notebook=in_notebook,
        profile=profile,
    )

    model = trainer.train(**kwargs)

    return True, model
