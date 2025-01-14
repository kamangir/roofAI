# AIRS

Aerial Imagery for Roof Segmentation, from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth.

## Content

For `subset` in `[test, train, val]`,

- `{subset}/image` contains `.tif`s, RGB.
- `{subset}/label` contains `.tif`s and `_vis.tif`, binary, RGB.
- `{subset}.txt`, `test.txt` missing.

more: [AIRS.ipynb](../../notebooks/dataset/custom/AIRS.ipynb).

## Ingest

```bash
roofAI dataset ingest \
    source=AIRS - \
    --test_count 250 \
    --train_count 350 \
    --val_count 100
```

🔥

## Review

```bash
roofAI dataset review - \
    $ROOFAI_AIRS_CACHE_OBJECT_NAME
```

![image](../../../assets/christchurch_397.png)

```bash
roofAI dataset review - \
    $TEST_roofAI_ingest_AIRS_v2
```

![image](../../../assets/christchurch_424-00000-00000.png)
