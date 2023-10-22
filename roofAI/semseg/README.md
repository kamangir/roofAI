# train

```bash
roofAI semseg train \
    profile=DECENT,register,suffix=v1 \
    $(@ref roofAI_ingest_AIRS_v1) \
    $(@timestamp) \
    --classes roof
```

![image](../../assets/christchurch_424-00000-00000.png)

![image](../../assets/train-summary.png)

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

# predict

```bash
roofAI semseg predict \
    profile=VALIDATION \
    $(@ref roofAI_semseg_model_AIRS_v1) \
    $(@ref roofAI_ingest_AIRS_v1)
```

![image](../../assets/predict-00000.png)

