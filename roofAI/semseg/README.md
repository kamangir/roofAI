# train

```bash
roofAI semseg train \
    profile=VALIDATION \
    $(@cache read roofAI_ingest_CamVid_v1) \
    roofAI-CamVid-semseg-model-$(@timestamp) \
    --classes car
```

![image](../../assets/augmented_dataset-00000.png)

`model.json`
```json
{
    "activation": "sigmoid",
    "classes": [
        "car"
    ],
    "encoder_name": "se_resnext50_32x4d",
    "encoder_weights": "imagenet"
}
```

https://arash-kamangir.medium.com/roofai-7-camvid-semseg-for-airs-train-51ff862fd8a6

# predict

```bash
roofAI semseg predict \
    profile=VALIDATION \
    $(@cache read roofAI_semseg_model_CamVid_v1) \
    $(@cache read roofAI_ingest_CamVid_v1) \
    roofAI-CamVid-semseg-prediction-$(@timestamp)
```

![image](../../assets/predict-00000.png)

https://arash-kamangir.medium.com/roofai-7-camvid-semseg-for-airs-2-4ad962c03b5b