# roofAI 🏠

everything AI about roofs. 🏠

🔷 [datasets](./roofAI/ingest) 🔷 [notebooks](./notebooks/) 🔷 [semseg](./roofAI/semseg) 🔷

```bash
 > roofAI help verbose
🏠 roofAI-3.51.1
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
semseg train \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,register,~upload] \
	<dataset_object_name> \
	<model_object_name> \
	[--activation <sigmoid>] \
	[--classes <one+two+three+four>] \
	[--encoder_name <se_resnext50_32x4d>] \
	[--encoder_weights <imagenet>]
 . semseg.train(<dataset_object_name>) -> <model_object_name>.
usage: python3 -m roofAI.semseg [-h] [--model_path MODEL_PATH] [--dataset_path DATASET_PATH] [--prediction_path PREDICTION_PATH] [--profile PROFILE] [--device DEVICE] [--dataset_is_camvid DATASET_IS_CAMVID] [--encoder_name ENCODER_NAME]
                                [--encoder_weights ENCODER_WEIGHTS] [--classes CLASSES] [--activation ACTIVATION]
                                task

roofAI-3.51.1.semseg

positional arguments:
  task                  predict

optional arguments:
  -h, --help            show this help message and exit
  --model_path MODEL_PATH
  --dataset_path DATASET_PATH
  --prediction_path PREDICTION_PATH
  --profile PROFILE     FULL|QUICK|VALIDATION
  --device DEVICE       cpu|cuda
  --dataset_is_camvid DATASET_IS_CAMVID
                        0|1|-1
  --encoder_name ENCODER_NAME
  --encoder_weights ENCODER_WEIGHTS
  --classes CLASSES     one+two+three+four
  --activation ACTIVATION
                        sigmoid or None for logits or softmax2d for multi-class segmentation
usage: python3 -m roofAI [-h] [--show_description SHOW_DESCRIPTION] task

roofAI-3.51.1

positional arguments:
  task                  version

optional arguments:
  -h, --help            show this help message and exit
  --show_description SHOW_DESCRIPTION
                        0|1
 ```