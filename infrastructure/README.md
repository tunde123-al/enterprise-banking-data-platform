# Infrastructure

| Path | Status | Purpose |
| --- | --- | --- |
| [`arm_templates/`](arm_templates) | Template written; **not deployed** from this repository | Foundation resources: ADLS Gen2 storage account with `raw`/`bronze`/`silver`/`gold` containers, Key Vault, Data Factory, Synapse workspace |

The ARM template is the only infrastructure-as-code in this repository. It is validated as
JSON by the test suite and CI, but it has not been deployed or verified against an Azure
subscription. Terraform is not implemented; any files under `infrastructure/terraform/`
are empty placeholders.

## Deploying (requires your own Azure subscription)

```bash
az deployment group create \
  --resource-group <your-resource-group> \
  --template-file infrastructure/arm_templates/template.json \
  --parameters @infrastructure/arm_templates/parameters.json
```

`sqlAdministratorLoginPassword` is a `securestring` parameter with no default and is
deliberately absent from `parameters.json`; the CLI prompts for it. In a pipeline, pass it
from a secret store or a Key Vault reference. Never commit a value.
