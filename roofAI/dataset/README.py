list_of_datasets = {
    "AIRS": {
        "description": "Aerial Imagery for Roof Segmentation from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation).",
        "thumbnail": "../../assets/christchurch_397.png",
    },
    "CamVid": {
        "description": "From [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial)",
        "thumbnail": "../../assets/0001TP_009390.png",
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
