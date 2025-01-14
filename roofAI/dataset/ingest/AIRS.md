# AIRS

Aerial Imagery for Roof Segmentation, from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth.

[review](../../notebooks/dataset/custom/AIRS.ipynb): for `subset` in `[test, train, val]`,

- `{subset}/image` contains `.tif`s, RGB.
- `{subset}/label` contains `.tif`s and `_vis.tif`, binary, RGB.
- `{subset}.txt`, `test.txt` missing.

related,

- https://medium.com/@arash-kamangir/roofai-1-airs-b440ebb54968
- https://arash-kamangir.medium.com/roofai-9-ingesting-airs-2-e71dca1d28d2

## review

```bash
roof dataset review open \
    $(@ref roofAI_ingest_AIRS_cache)
```

![image](../../../assets/christchurch_397.png)

```bash
roof dataset review open \
    $TEST_roofAI_ingest_AIRS_v2
```

### ingest

```bash
roofAI dataset ingest \
    source=AIRS \
    - \
    --test_count 250 \
    --train_count 350 \
    --val_count 100
```

![image](../../assets/christchurch_424-00000-00000.png)