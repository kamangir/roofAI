# roofAI 🏠

everything AI about roofs. 🏠

🔷 [datasets](./roofAI/dataset) 🔷 [notebooks](./notebooks/) 🔷 [semseg](./roofAI/semseg) 🔷

```bash
 > roof help
🏠 roofAI-3.125.1
🏠 everything AI about roofs.

roofAI create_conda_env \
	[dryrun,~pip]
 . create conda environmnt.
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
roofAI dataset ingest \
	[cache,~from_cache,source=AIRS,dryrun,open,register,suffix=<v1>,upload] \
	<object-name> \
	[--test_count <10>] \
	[--train_count <10>] \
	[--val_count <10>]
 . ingest AIRS -> <object-name>.
roofAI dataset ingest \
	[source=CamVid,dryrun,open,register,suffix=<v1>,upload] \
	<object-name>
 . ingest CamVid -> <object-name>.
roofAI dataset review \
	[download,dryrun,open] \
	<dataset_object_name> \
	[--count <1>] \
	[--index <index>] \
	[--subset <subset>]
 . review <dataset_object_name>.
roofAI pytest \
	[dryrun,list,~log,plugin=<plugin-name>,warning] \
	[filename.py|filename.py::test]
 . pytest roofAI.
roofAI test [~dataset,dryrun,~semseg]
 . test roofAI.
```