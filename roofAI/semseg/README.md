# `semseg`

A Semantic Segmenter based on [segmentation_models.pytorch](<https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb>). Also see [the notebooks](../../notebooks/).

## ingest

```bash
@select roofAI-dataset-$(@@timestamp)

roofAI dataset ingest \
    source=AIRS,upload . \
    --test_count 1000 \
    --train_count 8000 \
    --val_count 1000

roofAI dataset review - .
```

<details>
<summary>objects</summary>

`roofAI-dataset-2025-01-13-bbz4k3`

`roofAI-dataset-2025-01-13-gca7nz`

</details>

## train



```bash
roofAI semseg train \
    profile=FULL . - \
    --classes roof \
    --epoch_count 5
```

<details>
<summary>objects</summary>

5 epochs: `roofAI-dataset-2025-01-13-bbz4k3-train-2025-01-13-i8le50` 🎰

3 epochs: `roofAI-dataset-2025-01-13-gca7nz-train-2025-01-13-ukhtql` 🎰

</details>

🎰

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
    $TEST_roofAI_semseg_model_AIRS_full_v2 \
    $TEST_roofAI_ingest_AIRS_v2 \
    $(@timestamp)
```

![image](../../assets/predict-00247.png)

![image](https://github.com/kamangir/assets/blob/main/roofAI/2023-11-12-20-30-49-02592-predict.gif?raw=true)