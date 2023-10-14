# roofAI 🏠

everything AI about roofs. 🏠

```bash
 > roofAI help verbose
🏠 roofAI-3.34.1
🏠 everything AI about roofs.

roofAI create_conda_env \
	[dryrun,~pip]
 . create conda environmnt.
roofAI ingest \
	[CamVid] \
	<object-name>
 . ingest -> <object-name>.
QGIS seed
 . seed 🌱 QGIS.
semseg predict \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,~upload] \
	<model_object_name> \
	<dataset_object_name> \
	<prediction_object_name>
 . semseg[<model_object_name>].predict(<dataset_object_name>) -> <prediction_object_name>.
usage: python3 -m roofAI.semseg [-h] [--model_path MODEL_PATH] [--dataset_path DATASET_PATH] [--prediction_path PREDICTION_PATH] [--profile PROFILE] [--device DEVICE] task

roofAI-3.33.1.semseg

positional arguments:
  task                  predict

optional arguments:
  -h, --help            show this help message and exit
  --model_path MODEL_PATH
  --dataset_path DATASET_PATH
  --prediction_path PREDICTION_PATH
  --profile PROFILE     FULL|QUICK|VALIDATION
  --device DEVICE       cpu|cuda
usage: python3 -m roofAI [-h] [--show_description SHOW_DESCRIPTION] task

roofAI-3.33.1

positional arguments:
  task                  version

optional arguments:
  -h, --help            show this help message and exit
  --show_description SHOW_DESCRIPTION
                        0|1
 ```

## datasets

### AIRS (Aerial Imagery for Roof Segmentation)

from [kaggle](https://www.kaggle.com/datasets/atilol/aerialimageryforroofsegmentation), 457 km2, orthorectified, 220,000 buildings, gsd: 7.5 cm, 19.36 GB, + ground truth, [ingest](https://arash-kamangir.medium.com/roofai-1-airs-b440ebb54968), [t](https://arash-kamangir.medium.com/roofai-3-semseg-on-airs-6922fd046f5c)[r](https://arash-kamangir.medium.com/roofai-4-a-semseg-for-airs-1de6b932a782)[a](https://arash-kamangir.medium.com/roofai-5-a-semseg-for-airs-2-ffee45e902eb)[i](https://arash-kamangir.medium.com/roofai-6-camvid-semseg-for-airs-1-f7530374adef)[n](https://arash-kamangir.medium.com/roofai-7-camvid-semseg-for-airs-2-4ad962c03b5b)... 🔥

### CamVid

ingested from [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial),

```bash
roofAI ingest CamVid roofAI-CamVid-v2
```

| `AIRS` | `CamVid` | | |
|---|---|---|---|
| ![image](./assets/AIRS.png) | ![image](./assets/CamVid.png) | | |

## notebooks

1. [`semseg.ipynb`](./notebooks/semseg.ipynb) -> [predict.ipynb](./semseg/predict.ipynb) + [train.ipynb](./semseg/train.ipynb): [segmentation_models.pytorch](https://github.com/qubvel/segmentation_models.pytorch)-based segmentation.