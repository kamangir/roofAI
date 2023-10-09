# roofAI 🏠

everything AI about roofs. 🏠

```bash
 > roofAI help
🏠 roofAI-3.22.1
🏠 everything AI about roofs.

roofAI create_conda_env \
	[dryrun,~pip]
 . create conda environmnt.
eoofAI ingest \
	[CamVid] \
	<object-name>
 . ingest -> <object-name>.
QGIS seed
 . seed 🌱 QGIS.
 ```

## datasets

| info | screenshot | info | screenshot |
|---|---|---|---|
| AIRS (Aerial Imagery for Roof Segmentation), [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth, [ingest](https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968), train 🔥| ![image](./assets/AIRS.png) | Ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial) through `roofAI ingest CamVid <dataset_object>`. | ![image](./assets/CamVid.png) |

## notebooks

[`semseg.ipynb`](./notebooks/semseg.ipynb) - [segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch)-based segmentation.