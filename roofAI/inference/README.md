# creation

```bash
@select $(@ref roofAI_semseg_model_AIRS_o2)
roofAI inference create model .
roofAI inference create endpoint_config,suffix=v1 .
roofAI inference create endpoint,config_suffix=v1,suffix=v1 .
```

- model: `model-2023-12-03-11-24-39-75649`.

- endpoint config: `config-model-2023-12-03-11-24-39-75649-v1`.

- endpoint: `endpoint-model-2023-12-03-11-24-39-75649-v1`.

# invoking

wip 🔥
