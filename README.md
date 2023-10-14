# roofAI 🏠

everything AI about roofs. 🏠

> [datasets](./wiki/datasets.md)
> [notebooks](./notebooks/)
> [semseg](./roofAI/semseg/README.md)

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