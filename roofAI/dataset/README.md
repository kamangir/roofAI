# datasets

## AIRS

Aerial Imagery for Roof Segmentation, from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth.

[review](../../notebooks/dataset/custom/AIRS.ipynb): for `subset` in `[test, train, val]`,

- `{subset}/image` contains `.tif`s, RGB.
- `{subset}/label` contains `.tif`s and `_vis.tif`, binary, RGB.
- `{subset}.txt`, `test.txt` missing.

related,

- https://medium.com/@arash-kamangir/roofai-1-airs-b440ebb54968
- https://arash-kamangir.medium.com/roofai-9-ingesting-airs-2-e71dca1d28d2

### review

```bash
roof dataset review open \
    $(@ref roofAI_ingest_AIRS_cache)
```

![image](../../assets/christchurch_397.png)

```bash
roof dataset review open \
    $(@ref roofAI_ingest_AIRS_v2)
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

## CamVid

`360 x 480`, [more info](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/), ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial),

[review](../../notebooks/dataset/review.ipynb): files are in `./SegNet-Tutorial/CamVid/`, where, for `subset` in `[test, train, val]`,

- `{subset}/` contains `.png`s: RGB.
- `{subset}annot/` contains `.png`s: RGB, three channels identical, `0-11` corresponding to the following classes. `Dataset` filters the required `classes` for a train.

```python
CLASSES = [
    "sky",
    "building",
    "pole",
    "road",
    "pavement",
    "tree",
    "signsymbol",
    "fence",
    "car",
    "pedestrian",
    "bicyclist",
    "unlabelled",
]
```

- `{subset}.txt` is likely unused.

related,

- https://arash-kamangir.medium.com/roofai-6-camvid-semseg-for-airs-1-f7530374adef
- https://arash-kamangir.medium.com/roofai-8-ingesting-airs-1f0efa4bd8a1

### review

```bash
roof dataset review open \
    $(@ref roofAI_ingest_CamVid_v1)
```

![image](../../assets/0001TP_009390.png)

### ingest

```bash
roofAI dataset ingest \
    source=CamVid
```
