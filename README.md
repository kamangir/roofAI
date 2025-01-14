# 🏛️ roofAI

everything AI about roofs. 🏛️

```bash
pip install roofAI
```

```mermaid
graph LR
    dataset_ingest_AIRS["roofAI<br>dataset<br>ingest<br>source=AIRS<br>&lt;dataset-object-name&gt;"]
    dataset_ingest_CamVid["vanwatch<br>discover<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]

    dataset_review["vanwatch<br>discover<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]

    dataset_object_name["dataset object"]:::folder
    AIRS["AIRS"]:::folder
    CamVid["CamVid"]:::folder

    AIRS --> dataset_ingest_AIRS
    dataset_ingest_AIRS --> dataset_object_name

    CamVid --> dataset_ingest_CamVid
    dataset_ingest_CamVid --> dataset_object_name

    AIRS --> dataset_review
    CamVid --> dataset_review
    dataset_object_name --> dataset_review

    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

|   |   |
| --- | --- |
| 🏛️[`datasets`](https://github.com/kamangir/roofAI/blob/main/roofAI/dataset) [![image](https://github.com/kamangir/assets/blob/main/roofAI/AIRS-cache-v45--review-index-2.png?raw=true)](https://github.com/kamangir/roofAI/blob/main/roofAI/dataset) Semantic Segmentation Datasets | 🏛️[`semseg`](https://github.com/kamangir/roofAI/blob/main/roofAI/semseg) [![image](https://github.com/kamangir/roofAI/raw/main/assets/predict-00247.png)](https://github.com/kamangir/roofAI/blob/main/roofAI/semseg) A Semantic Segmenter based on [segmentation_models.pytorch](<https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb>). |

---


[![pylint](https://github.com/kamangir/roofAI/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/roofAI/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/roofAI/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/roofAI/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/roofAI/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/roofAI/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/roofAI.svg)](https://pypi.org/project/roofAI/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/roofAI)](https://pypistats.org/packages/roofAI)

built by 🌀 [`blue_options-4.187.1`](https://github.com/kamangir/awesome-bash-cli), based on 🏛️ [`roofAI-5.64.1`](https://github.com/kamangir/roofAI).
