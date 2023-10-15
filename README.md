# roofAI 🏠

everything AI about roofs. 🏠

🔷 [datasets](./roofAI/ingest) 🔷 [notebooks](./notebooks/) 🔷 [semseg](./roofAI/semseg) 🔷

```bash
 > roof help verbose
🏠 roofAI-3.79.1
🏠 everything AI about roofs.

roofAI create_conda_env \
	[dryrun,~pip]
 . create conda environmnt.
roofAI ingest \
	[dryrun,source=CamVid|AIRS,sufix=<v1>,register,upload] \
	<object-name>
 . ingest -> <object-name>.
QGIS seed
 . seed 🌱 QGIS.
semseg predict \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,upload] \
	<model_object_name> \
	<dataset_object_name> \
	<prediction_object_name>
 . semseg[<model_object_name>].predict(<dataset_object_name>) -> <prediction_object_name>.
semseg train \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,register,upload] \
	<dataset_object_name> \
	<model_object_name> \
	[--activation <sigmoid>] \
	[--classes <one+two+three+four>] \
	[--encoder_name <se_resnext50_32x4d>] \
	[--encoder_weights <imagenet>]
 . semseg.train(<dataset_object_name>) -> <model_object_name>.
usage: python3 -m roofAI.semseg [-h] [--activation ACTIVATION] [--classes CLASSES] [--dataset_path DATASET_PATH] [--device DEVICE]
                                [--encoder_name ENCODER_NAME] [--encoder_weights ENCODER_WEIGHTS] [--model_path MODEL_PATH]
                                [--prediction_path PREDICTION_PATH] [--profile PROFILE]
                                task

roofAI.semseg-3.79.1

positional arguments:
  task                  predict|train

optional arguments:
  -h, --help            show this help message and exit
  --activation ACTIVATION
                        sigmoid or None for logits or softmax2d for multi-class segmentation
  --classes CLASSES     one+two+three+four
  --dataset_path DATASET_PATH
  --device DEVICE       cpu|cuda
  --encoder_name ENCODER_NAME
  --encoder_weights ENCODER_WEIGHTS
  --model_path MODEL_PATH
  --prediction_path PREDICTION_PATH
  --profile PROFILE     FULL|QUICK|VALIDATION
roofAI pytest \
	[dryrun,list,~log,plugin=<plugin-name>,warning] \
	[args]
 . pytest roofAI.
usage: python3 -m roofAI [-h] [--show_description SHOW_DESCRIPTION] task

roofAI-3.79.1

positional arguments:
  task                  version

optional arguments:
  -h, --help            show this help message and exit
  --show_description SHOW_DESCRIPTION
                        0|1
```