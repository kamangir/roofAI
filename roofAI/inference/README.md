```bash
@select $(@ref roofAI_semseg_model_AIRS_o2)
roofAI inference create model .
roofAI inference create endpoint_config,suffix=v1 .
roofAI inference create endpoint,config_suffix=v1,suffix=v1 .
```

wip 🔥
