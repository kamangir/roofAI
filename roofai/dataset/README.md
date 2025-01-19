# datasets

`DatasetKind`s:

1. CamVid:
    - The [original CamVid dataset](./ingest/CamVid.md).
    - Generated by `roofai dataset ingest`.
    - Consumed by `roofai semseg train`.
1. AIRS: The [original AIRS dataset](./ingest/AIRS.md)
    - Should be ingested to be trained on ⬆️.
1. SageMaker: For [`sagesemseg`](https://github.com/kamangir/blue-sandbox/blob/main/blue_sandbox/sagesemseg/README.md), ingested from `AIRS` with `target=sagemaker`.

|   |   |
| --- | --- |
| [`AIRS`](./ingest/AIRS.md) [![image](https://github.com/kamangir/assets/blob/main/roofAI/AIRS-cache-v45--review-index-2.png?raw=true)](./ingest/AIRS.md) Aerial Imagery for Roof Segmentation from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation). | [`CamVid`](./ingest/CamVid.md) [![image](https://github.com/kamangir/assets/blob/main/roofAI/0001TP_008850.png?raw=true)](./ingest/CamVid.md) From [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial) |
