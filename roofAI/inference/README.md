# creation

create a model 1️⃣, then create an endpoint config 2️⃣, then create an endpoint 3️⃣,

```bash
@select $(@ref roofAI_semseg_model_AIRS_o2)
roofAI inference create model .
roofAI inference create endpoint_config,suffix=pytorch .
roofAI inference create endpoint,config_suffix=pytorch,suffix=pytorch .
```

- model: `$(@ref roofAI_semseg_model_AIRS_o2)`.

- endpoint config: `config-$(@ref roofAI_semseg_model_AIRS_o2)-pytorch`.

- endpoint: `endpoint-$(@ref roofAI_semseg_model_AIRS_o2)-pytorch`, also `$(roofAI_inference_default_endpoint)`.

# invoking

wip 🔥

```bash
cloudwatch browse endpoint
```

```bash
roof inference invoke \
  profile=VALIDATION - \
  $(@ref roofAI_ingest_AIRS_v2)
```
