# roofAI 🏛️

everything AI about roofs. 🏛️

🔷 [datasets](./roofAI/dataset) 🔷 [notebooks](./notebooks/) 🔷 [semseg](./roofAI/semseg) 🔷

```bash
🏛️  roofAI-3.205.1
🏛️  everything AI about roofs.

roofAI conda create_env [validate,~recreate]
 . create conda environment.
roofAI conda validate
 . validate conda environment.
QGIS seed
 . seed 🌱 QGIS.
QGIS expressions pull
 . pull QGIS expressions.
QGIS expressions push [push]
 . push QGIS expressions.
 📂 /Users/kamangir/Library/Application Support/QGIS/QGIS3/profiles/default/python/expressions
 📂 /Users/kamangir/git/roofAI/roofAI/QGIS/expressions
semseg predict \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,upload] \
	<model-object-name> \
	<dataset-object-name> \
	<prediction-object-name>
 . semseg[<model-object-name>].predict(<dataset-object-name>) -> <prediction-object-name>.
semseg train \
	[device=cpu|cuda,~download,dryrun,profile=FULL|QUICK|VALIDATION,register,suffix=<v1>,upload] \
	<dataset-object-name> \
	<model-object-name> \
	[--activation <sigmoid>] \
	[--classes <one+two+three+four>] \
	[--encoder_name <se_resnext50_32x4d>] \
	[--encoder_weights <imagenet>]
 . semseg.train(<dataset-object-name>) -> <model-object-name>.
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
	<object-name> \
	[--count <1>] \
	[--index <index>] \
	[--subset <subset>]
 . review <object-name>.
roofAI pytest \
	[dryrun,list,~log,plugin=<plugin-name>,warning] \
	[filename.py|filename.py::test]
 . pytest roofAI.
roofAI test [~dataset,dryrun,~semseg]
 . test roofAI.
```

[![image](https://github.com/kamangir/assets/blob/main/roofAI/2023-11-12-20-30-49-02592-predict.gif?raw=true)](./roofAI/semseg/)

---

To use on [AWS SageMaker](https://aws.amazon.com/sagemaker/) replace `<plugin-name>` with `roofAI` and follow [these instructions](https://github.com/kamangir/blue-plugin/blob/main/SageMaker.md).