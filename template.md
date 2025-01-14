# 🏛️ roofAI

everything AI about roofs. 🏛️

```bash
pip install roofAI
```

```mermaid
graph LR
    dataset_ingest["vanwatch<br>discover<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]
    dataset_review["vanwatch<br>discover<br>target=&lt;target&gt;<br>&lt;object-name&gt;"]
    dataset_object_name["geojson"]:::folder
    AIRS["geojson"]:::folder
    CamVid["geojson"]:::folder

    AIRS -> dataset_ingest
    CamVid -> dataset_ingest
    dataset_ingest --> dataset_object_name

    AIRS -> dataset_ingest
    CamVid -> dataset_ingest
    dataset_object_name --> dataset_review

    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

--table--

---

--signature--