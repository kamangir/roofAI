# creation

```bash
@select $(@ref roofAI_semseg_model_AIRS_o2)
roofAI inference create model .
roofAI inference create endpoint_config,suffix=pytorch .
roofAI inference create endpoint,config_suffix=pytorch,suffix=pytorch .
```

- model: `$(@ref roofAI_semseg_model_AIRS_o2)`.

- endpoint config: `config-$(@ref roofAI_semseg_model_AIRS_o2)-pytorch`.

- endpoint: `endpoint-$(@ref roofAI_semseg_model_AIRS_o2)-pytorch`.

# invoking

wip 🔥
