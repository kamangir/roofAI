# CamVid

`360 x 480` dataset ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial), [more info](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/).

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
    $TEST_roofAI_ingest_CamVid_v1
```

![image](../../../assets/0001TP_009390.png)

## ingest

```bash
roofAI dataset ingest \
    source=CamVid
```