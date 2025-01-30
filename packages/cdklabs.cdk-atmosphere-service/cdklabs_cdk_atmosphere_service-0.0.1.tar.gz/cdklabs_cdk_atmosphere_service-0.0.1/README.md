# Atmosphere Service

> [API Reference](./API.md)

An HTTP service that manages a collection of pre-existing environments and allocates them to integration tests per request.

## Usage

```python
import aws_cdk as cdk
from cdklabs.cdk_atmosphere_service import AtmosphereService


app = cdk.App()
stack = cdk.Stack(app, "Stack")
AtmosphereService(stack, "AtmosphereService",
    config=ConfigurationData(
        environments=[Environment(
            account="1111",
            region="us-east-1",
            pool="release",
            admin_role_arn="arn:aws:iam::1111:role/Admin"
        )
        ]
    )
)
```
