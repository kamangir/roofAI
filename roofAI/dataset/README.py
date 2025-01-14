list_of_datasets = {
    "AIRS": {
        "description": "Aerial Imagery for Roof Segmentation from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation).",
        "thumbnail": "https://github.com/kamangir/assets/blob/main/roofAI/AIRS-cache-v45--review-index-2.png?raw=true",
    },
    "CamVid": {
        "description": "From [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial)",
        "thumbnail": "https://github.com/kamangir/assets/blob/main/roofAI/0001TP_008850.png?raw=true",
    },
}


items = [
    "[`{}`](./ingest/{}.md) [![image]({})](./ingest/{}.md) {}".format(
        dataset_name,
        dataset_name,
        details["thumbnail"],
        dataset_name,
        details["description"],
    )
    for dataset_name, details in list_of_datasets.items()
]
