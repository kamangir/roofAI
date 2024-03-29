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

![image](../../assets/christchurch_397.png)

```bash
roof dataset review open \
    $(@ref roofAI_ingest_AIRS_v2)
```

## ingest

```bash
roofAI dataset ingest \
    source=AIRS,register \
    - \
    --test_count 250 \
    --train_count 350 \
    --val_count 100
```

![image](../../assets/christchurch_424-00000-00000.png)

# CamVid

ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial),

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

## review

```bash
roof dataset review open \
    $(@ref roofAI_ingest_CamVid_v1)
```

![image](../../assets/0001TP_009390.png)

## ingest

```bash
roofAI dataset ingest \
    source=CamVid,register
```

# SageMaker

from [Semantic Segmentation on AWS Sagemaker](https://github.com/aws/amazon-sagemaker-examples/blob/main/introduction_to_amazon_algorithms/semantic_segmentation_pascalvoc/semantic_segmentation_pascalvoc.ipynb).

example datasets: `pascal-voc-v1-full-v2`,

```bash
sagesemseg upload_dataset - suffix=full-v2
```

and `pascal-voc-v1-debug-v2`,

```bash
sagesemseg upload_dataset - suffix=debug-v2 --count 16
```

for `subset` in `[train, validation]`,

- `{subset}` contains `.jpg`s.
- `{subset}_annotation` contains ... indexed `.png` files ... `[0, 1 ... c-1, 255]` for ... `c` class[es] ... `255` ... 'ignore' ... any mode that is a [recognized standard](https://pillow.readthedocs.io/en/3.0.x/handbook/concepts.html#concept-modes) [and] ... read as integers ...

image width = 500, and height = 375, while height seems to be flexible.

![image](https://github.com/kamangir/assets/blob/main/roofAI/christchurch_1011-00000-00000.png?raw=true)
