list_of_datasets = {
    "AIRS": {
        "description": "Aerial Imagery for Roof Segmentation, from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth.",
        "thumbnail": "../../assets/christchurch_397.png",
    },
    "CamVid": {
        "description": "From [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial)",
        "thumbnail": "../../assets/0001TP_009390.png",
    },
}


items = [
    "[`{}`](./ingest/{}) [![image]({})](./ingest/{}) {}".format(
        dataset_name,
        dataset_name,
        details["thumbnail"],
        dataset_name,
        details["description"],
    )
    for dataset_name, details in list_of_datasets.items()
]
