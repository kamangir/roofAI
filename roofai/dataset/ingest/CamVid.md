# CamVid

`360 x 480` dataset ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial), [more info](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/).


## Content

In `./SegNet-Tutorial/CamVid/`, for `subset` in `[test, train, val]`,

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

more: [review.ipynb](../../../notebooks/dataset/review.ipynb): 

## Ingest

```bash
roofai dataset ingest \
    source=CamVid
```

## Review

```bash
roofai dataset review - \
    roofAI_ingest_CamVid_2025-01-13-w4lnfp
```

![image](https://github.com/kamangir/assets/blob/main/roofAI/0001TP_008850.png?raw=true)
