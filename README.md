# roofAI 🏠

everything AI about roofs. 🏠

🔷 [datasets](./roofAI/ingest) 🔷 [notebooks](./notebooks/) 🔷 [semseg](./roofAI/semseg) 🔷

```bash
 > roof help
🏠 roofAI-3.85.1
🏠 everything AI about roofs.

roofAI create_conda_env \
	[dryrun,~pip]
 . create conda environmnt.
roofAI ingest \
	[cache,dryrun,~from_cache,source=CamVid|AIRS,suffix=<v1>,register,upload] \
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
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,register,suffix=<v1>,upload] \
	<dataset_object_name> \
	<model_object_name> \
	[--activation <sigmoid>] \
	[--classes <one+two+three+four>] \
	[--encoder_name <se_resnext50_32x4d>] \
	[--encoder_weights <imagenet>]
 . semseg.train(<dataset_object_name>) -> <model_object_name>.
roofAI pytest \
	[dryrun,list,~log,plugin=<plugin-name>,warning] \
	[args]
 . pytest roofAI.
roofAI test [dryrun]
 . test roofAI.
```