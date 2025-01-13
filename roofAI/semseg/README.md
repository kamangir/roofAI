# `semseg`

A Semantic Segmenter based on [segmentation_models.pytorch](<https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb>). Also see [the notebooks](../../notebooks/).

## train

```bash
roofAI semseg train \
    profile=FULL \
    $(@ref roofAI_ingest_AIRS_v2) \
    $(@timestamp) \
    --classes roof
```

https://arash-kamangir.medium.com/roofai-17-train-on-airs-on-sagemaker-2-dd24082aca03

https://arash-kamangir.medium.com/roofai-20-refactors-on-sagemaker-9e295b84daea

![image](../../assets/christchurch_424-00000-00000.png)

![image](../../assets/train-summary.png)

`model.json` (example, shortened)
```json
{
    "activation": "sigmoid",
    "classes": [
        "roof"
    ],
    "elapsed_time": 361.5529091358185,
    "encoder_name": "se_resnext50_32x4d",
    "encoder_weights": "imagenet",
    "epics": {
        "0": {
            "train": {
                "dice_loss": 0.8440376162528992,
                "iou_score": 0.08718136921525002
            },
            "valid": {
                "dice_loss": 0.6924602970480918,
                "iou_score": 0.23197315189281645
            }
        },
        "9": {
            "train": {
                "dice_loss": 0.2785138368606567,
                "iou_score": 0.5775847971439362
            },
            "valid": {
                "dice_loss": 0.40588687658309924,
                "iou_score": 0.4811718734062814
            }
        }
    }
}
```

## predict

```bash
roofAI semseg predict \
    profile=FULL,upload \
    $(@ref roofAI_semseg_model_AIRS_full_v2) \
    $(@ref roofAI_ingest_AIRS_v2) \
    $(@timestamp)
```

![image](../../assets/predict-00247.png)

![image](https://github.com/kamangir/assets/blob/main/roofAI/2023-11-12-20-30-49-02592-predict.gif?raw=true)