# creation

```bash
@select $(@ref roofAI_semseg_model_AIRS_o2)
roofAI inference create model .
roofAI inference create endpoint_config,suffix=v1 .
roofAI inference create endpoint,config_suffix=v1,suffix=v1 .
```

- model: `$(@ref roofAI_semseg_model_AIRS_o2)`.

- endpoint config: `config-$(@ref roofAI_semseg_model_AIRS_o2)-v1`.

- endpoint: `endpoint-$(@ref roofAI_semseg_model_AIRS_o2)-v1`.

# invoking

wip 🔥
