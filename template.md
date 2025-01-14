# 🏛️ roofAI

everything AI about roofs. 🏛️

```bash
pip install roofAI
```

```mermaid
graph LR
    dataset_ingest["roofAI<br>dataset<br>ingest<br>source=AIRS|CamVid<br>&lt;dataset-object-name&gt;"]

    dataset_review["roofAI<br>dataset<br>review -<br>&lt;dataset-object-name&gt;"]

    semseg_train["semseg<br>train -<br>&lt;dataset-object-name&gt;<br>&lt;model-object-name&gt;"]

    semseg_predict[""]

    AIRS["AIRS"]:::folder
    CamVid["CamVid"]:::folder
    dataset_object_name["dataset object"]:::folder
    model_object_name["model object"]:::folder
    prediction_object_name["prediction object"]:::folder

    AIRS --> dataset_ingest
    CamVid --> dataset_ingest
    dataset_ingest --> dataset_object_name

    AIRS --> dataset_review
    CamVid --> dataset_review
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