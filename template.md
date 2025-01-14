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

--table--

---

--signature--