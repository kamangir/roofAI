# 🏛️ roofAI

everything AI about roofs. 🏛️

```bash
pip install roofAI
```

```mermaid
graph LR
    dataset_ingest["roofAI dataset ingest source=AIRS|CamVid <dataset-object-name>"]

    dataset_review["roofAI dataset review~~- <dataset-object-name>"]

    semseg_train["semseg train~~- <dataset-object-name> <model-object-name>"]

    semseg_predict["semseg predict~~- <model-object-name> <dataset-object-name> <prediction-object-name>"]

    AIRS["AIRS"]:::folder
    CamVid["CamVid"]:::folder
    dataset_object_name["dataset object"]:::folder
    model_object_name["model object"]:::folder
    prediction_object_name["prediction object"]:::folder

    AIRS --> dataset_ingest
    CamVid --> dataset_ingest
    dataset_ingest --> dataset_object_name

    AIRS --> dataset_review
    dataset_object_name --> dataset_review

    dataset_object_name --> semseg_train
    semseg_train --> model_object_name

    model_object_name --> semseg_predict
    dataset_object_name --> semseg_predict
    semseg_predict --> prediction_object_name

    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

--table--

---

--signature--