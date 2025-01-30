r'''
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
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


class Allocate(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Allocate",
):
    '''(experimental) Allocate function.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocations: "Allocations",
        configuration: "Configuration",
        environments: "Environments",
        scheduler: "Scheduler",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocations: (experimental) Allocations storage.
        :param configuration: (experimental) Service configuration.
        :param environments: (experimental) Environments storage.
        :param scheduler: (experimental) Scheduler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0231988f16f79c5e9e91c43c21dcfa6daa31565b5fdaf3ffb135d19b57fca30e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AllocateProps(
            allocations=allocations,
            configuration=configuration,
            environments=environments,
            scheduler=scheduler,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "function"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.AllocateProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocations": "allocations",
        "configuration": "configuration",
        "environments": "environments",
        "scheduler": "scheduler",
    },
)
class AllocateProps:
    def __init__(
        self,
        *,
        allocations: "Allocations",
        configuration: "Configuration",
        environments: "Environments",
        scheduler: "Scheduler",
    ) -> None:
        '''(experimental) Properties for ``Allocate``.

        :param allocations: (experimental) Allocations storage.
        :param configuration: (experimental) Service configuration.
        :param environments: (experimental) Environments storage.
        :param scheduler: (experimental) Scheduler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca47cfce295459755d3e667cf175350e70ab6f0d62725812c126bcec42513f9)
            check_type(argname="argument allocations", value=allocations, expected_type=type_hints["allocations"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument scheduler", value=scheduler, expected_type=type_hints["scheduler"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocations": allocations,
            "configuration": configuration,
            "environments": environments,
            "scheduler": scheduler,
        }

    @builtins.property
    def allocations(self) -> "Allocations":
        '''(experimental) Allocations storage.

        :stability: experimental
        '''
        result = self._values.get("allocations")
        assert result is not None, "Required property 'allocations' is missing"
        return typing.cast("Allocations", result)

    @builtins.property
    def configuration(self) -> "Configuration":
        '''(experimental) Service configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("Configuration", result)

    @builtins.property
    def environments(self) -> "Environments":
        '''(experimental) Environments storage.

        :stability: experimental
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast("Environments", result)

    @builtins.property
    def scheduler(self) -> "Scheduler":
        '''(experimental) Scheduler.

        :stability: experimental
        '''
        result = self._values.get("scheduler")
        assert result is not None, "Required property 'scheduler' is missing"
        return typing.cast("Scheduler", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AllocateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Allocations(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Allocations",
):
    '''(experimental) Allocations table.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed1aba36a83cd8d657cc4eb45528c4ee3e1b22fa4146d6ce9a695085415faf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''
        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c8f95e4acd80d19711d0b00d7f265e32e0af0754a9e81ba7fbe0c9faa94a92)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(None, jsii.invoke(self, "grantReadWrite", [identity]))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "table"))


class AtmosphereService(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.AtmosphereService",
):
    '''(experimental) Atmosphere service to allocate AWS environments on-demand.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        config: typing.Union["ConfigurationData", typing.Dict[builtins.str, typing.Any]],
        endpoint: typing.Optional[typing.Union["EndpointOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param config: (experimental) Service Configuration, stored in a dedicated s3 bucket.
        :param endpoint: (experimental) Options for the API endpoint.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad579ce9e0c037b640bf723f24cdf369e9d5886d908c76a2c1d31b4cf0b262a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AtmosphereServiceProps(config=config, endpoint=endpoint)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="allocate")
    def allocate(self) -> Allocate:
        '''(experimental) Provides access to the allocate function.

        :stability: experimental
        '''
        return typing.cast(Allocate, jsii.get(self, "allocate"))

    @builtins.property
    @jsii.member(jsii_name="allocations")
    def allocations(self) -> Allocations:
        '''(experimental) Provides access to the allocations table.

        :stability: experimental
        '''
        return typing.cast(Allocations, jsii.get(self, "allocations"))

    @builtins.property
    @jsii.member(jsii_name="cleanup")
    def cleanup(self) -> "Cleanup":
        '''(experimental) Provides access to the cleanup task.

        :stability: experimental
        '''
        return typing.cast("Cleanup", jsii.get(self, "cleanup"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "Configuration":
        '''(experimental) Provides access to the service configuration file.

        :stability: experimental
        '''
        return typing.cast("Configuration", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="deallocate")
    def deallocate(self) -> "Deallocate":
        '''(experimental) Provides access to the deaclloce function.

        :stability: experimental
        '''
        return typing.cast("Deallocate", jsii.get(self, "deallocate"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> "Endpoint":
        '''(experimental) Provides access to the API gateway endpoint.

        :stability: experimental
        '''
        return typing.cast("Endpoint", jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="environments")
    def environments(self) -> "Environments":
        '''(experimental) Provides access to the environments table.

        :stability: experimental
        '''
        return typing.cast("Environments", jsii.get(self, "environments"))

    @builtins.property
    @jsii.member(jsii_name="scheduler")
    def scheduler(self) -> "Scheduler":
        '''(experimental) Provides access to the scheduler.

        :stability: experimental
        '''
        return typing.cast("Scheduler", jsii.get(self, "scheduler"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.AtmosphereServiceProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "endpoint": "endpoint"},
)
class AtmosphereServiceProps:
    def __init__(
        self,
        *,
        config: typing.Union["ConfigurationData", typing.Dict[builtins.str, typing.Any]],
        endpoint: typing.Optional[typing.Union["EndpointOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for ``AtmosphereService``.

        :param config: (experimental) Service Configuration, stored in a dedicated s3 bucket.
        :param endpoint: (experimental) Options for the API endpoint.

        :stability: experimental
        '''
        if isinstance(config, dict):
            config = ConfigurationData(**config)
        if isinstance(endpoint, dict):
            endpoint = EndpointOptions(**endpoint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3160ca321214af3c273a63e391821048132dfdb3e763a6b9e2aaa3c62bc8d1d7)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
        }
        if endpoint is not None:
            self._values["endpoint"] = endpoint

    @builtins.property
    def config(self) -> "ConfigurationData":
        '''(experimental) Service Configuration, stored in a dedicated s3 bucket.

        :stability: experimental
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("ConfigurationData", result)

    @builtins.property
    def endpoint(self) -> typing.Optional["EndpointOptions"]:
        '''(experimental) Options for the API endpoint.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional["EndpointOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AtmosphereServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cleanup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Cleanup",
):
    '''(experimental) Provides a cleanup task.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocations: Allocations,
        configuration: "Configuration",
        environments: "Environments",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocations: (experimental) Allocations storage.
        :param configuration: (experimental) Service configuration.
        :param environments: (experimental) Environments storage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55675c03a7e6c56f8a2472e9483d31ad114a159de628f58087ee564262a8db8b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CleanupProps(
            allocations=allocations,
            configuration=configuration,
            environments=environments,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantRun")
    def grant_run(self, grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''
        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45cf22488ac93ee13f8a365a012255cac0cdbb57e092a655614a91c72afbcc1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRun", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.Cluster:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition, jsii.get(self, "task"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.CleanupProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocations": "allocations",
        "configuration": "configuration",
        "environments": "environments",
    },
)
class CleanupProps:
    def __init__(
        self,
        *,
        allocations: Allocations,
        configuration: "Configuration",
        environments: "Environments",
    ) -> None:
        '''(experimental) Properties for ``Cleanup``.

        :param allocations: (experimental) Allocations storage.
        :param configuration: (experimental) Service configuration.
        :param environments: (experimental) Environments storage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c74b92ac430746641057aea2b2edc3a36b24afa2bf517e3430155cc85470dd)
            check_type(argname="argument allocations", value=allocations, expected_type=type_hints["allocations"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocations": allocations,
            "configuration": configuration,
            "environments": environments,
        }

    @builtins.property
    def allocations(self) -> Allocations:
        '''(experimental) Allocations storage.

        :stability: experimental
        '''
        result = self._values.get("allocations")
        assert result is not None, "Required property 'allocations' is missing"
        return typing.cast(Allocations, result)

    @builtins.property
    def configuration(self) -> "Configuration":
        '''(experimental) Service configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("Configuration", result)

    @builtins.property
    def environments(self) -> "Environments":
        '''(experimental) Environments storage.

        :stability: experimental
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast("Environments", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CleanupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Configuration(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Configuration",
):
    '''(experimental) Service configuration construct.

    Configuration data will be written to a JSON file and stored in a dedicated s3 bucket.
    Logical components that needs access should use the ``grantRead`` method and then
    download the file whenever they need to.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data: typing.Union["ConfigurationData", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data: (experimental) Data of the configuration file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3a137cea4f61ae3a90cb488557fd8405310d92f6b9b740a202358a9d9aefff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfigurationProps(data=data)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''(experimental) Allow the given identity to download the configuration file(s).

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050bd4ac315624861f8343edea53907a87711715c01b0f0c350b5f37793e7ed0)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [identity]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) S3 Bucket where the configuration file is stored.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> "ConfigurationData":
        '''(experimental) Configuration data.

        :stability: experimental
        '''
        return typing.cast("ConfigurationData", jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''(experimental) S3 Object key of configuration file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.ConfigurationData",
    jsii_struct_bases=[],
    name_mapping={"environments": "environments"},
)
class ConfigurationData:
    def __init__(
        self,
        *,
        environments: typing.Sequence[typing.Union["Environment", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Configuration Data.

        :param environments: (experimental) List of environments, configured by the service operator.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994d0252650625fc7bb402f65ed22f2384ecf05802a7bac40df3d0aff9364ec0)
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environments": environments,
        }

    @builtins.property
    def environments(self) -> typing.List["Environment"]:
        '''(experimental) List of environments, configured by the service operator.

        :stability: experimental
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast(typing.List["Environment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigurationData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.ConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class ConfigurationProps:
    def __init__(
        self,
        *,
        data: typing.Union[ConfigurationData, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties of ``Configuration``.

        :param data: (experimental) Data of the configuration file.

        :stability: experimental
        '''
        if isinstance(data, dict):
            data = ConfigurationData(**data)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aabd37d225de3358f5386696f65c7892d9ad4258d83fd6a4dcf43b1321fd762)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
        }

    @builtins.property
    def data(self) -> ConfigurationData:
        '''(experimental) Data of the configuration file.

        :stability: experimental
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(ConfigurationData, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Deallocate(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Deallocate",
):
    '''(experimental) Deallocate function.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocations: Allocations,
        cleanup: Cleanup,
        environments: "Environments",
        scheduler: "Scheduler",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocations: (experimental) Allocations storage.
        :param cleanup: (experimental) Cleanup.
        :param environments: (experimental) Environments storage.
        :param scheduler: (experimental) Scheduler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bd226c207210cec55525d6fdf6170fcb1375ab842e6f9f58f99e9eff15fef7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DeallocateProps(
            allocations=allocations,
            cleanup=cleanup,
            environments=environments,
            scheduler=scheduler,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "function"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.DeallocateProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocations": "allocations",
        "cleanup": "cleanup",
        "environments": "environments",
        "scheduler": "scheduler",
    },
)
class DeallocateProps:
    def __init__(
        self,
        *,
        allocations: Allocations,
        cleanup: Cleanup,
        environments: "Environments",
        scheduler: "Scheduler",
    ) -> None:
        '''(experimental) Properties for ``Deallocate``.

        :param allocations: (experimental) Allocations storage.
        :param cleanup: (experimental) Cleanup.
        :param environments: (experimental) Environments storage.
        :param scheduler: (experimental) Scheduler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5710e05d2ce9cb3a48dd71a36e7533dfdd7957aab27d5e10a8a0e115b58dec)
            check_type(argname="argument allocations", value=allocations, expected_type=type_hints["allocations"])
            check_type(argname="argument cleanup", value=cleanup, expected_type=type_hints["cleanup"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument scheduler", value=scheduler, expected_type=type_hints["scheduler"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocations": allocations,
            "cleanup": cleanup,
            "environments": environments,
            "scheduler": scheduler,
        }

    @builtins.property
    def allocations(self) -> Allocations:
        '''(experimental) Allocations storage.

        :stability: experimental
        '''
        result = self._values.get("allocations")
        assert result is not None, "Required property 'allocations' is missing"
        return typing.cast(Allocations, result)

    @builtins.property
    def cleanup(self) -> Cleanup:
        '''(experimental) Cleanup.

        :stability: experimental
        '''
        result = self._values.get("cleanup")
        assert result is not None, "Required property 'cleanup' is missing"
        return typing.cast(Cleanup, result)

    @builtins.property
    def environments(self) -> "Environments":
        '''(experimental) Environments storage.

        :stability: experimental
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast("Environments", result)

    @builtins.property
    def scheduler(self) -> "Scheduler":
        '''(experimental) Scheduler.

        :stability: experimental
        '''
        result = self._values.get("scheduler")
        assert result is not None, "Required property 'scheduler' is missing"
        return typing.cast("Scheduler", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeallocateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Endpoint",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocate: Allocate,
        deallocate: Deallocate,
        allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocate: (experimental) Allocate function.
        :param deallocate: (experimental) Deallocate function.
        :param allowed_accounts: (experimental) List of accounts that are allowed to access the endpoint. Default: - only the service account is allowed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca446827c29368284848f097b7738220c25168c9f448b0d530fb25a21819b77a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EndpointProps(
            allocate=allocate, deallocate=deallocate, allowed_accounts=allowed_accounts
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="allocationResource")
    def allocation_resource(self) -> _aws_cdk_aws_apigateway_ceddda9d.Resource:
        '''(experimental) Allocation sub resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Resource, jsii.get(self, "allocationResource"))

    @builtins.property
    @jsii.member(jsii_name="allocationsResource")
    def allocations_resource(self) -> _aws_cdk_aws_apigateway_ceddda9d.Resource:
        '''(experimental) Allocations sub resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Resource, jsii.get(self, "allocationsResource"))

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> _aws_cdk_aws_apigateway_ceddda9d.RestApi:
        '''(experimental) Api Gateway rest api.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RestApi, jsii.get(self, "api"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.EndpointOptions",
    jsii_struct_bases=[],
    name_mapping={"allowed_accounts": "allowedAccounts"},
)
class EndpointOptions:
    def __init__(
        self,
        *,
        allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``Endpoint``.

        :param allowed_accounts: (experimental) List of accounts that are allowed to access the endpoint. Default: - only the service account is allowed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b787cf2495d75e1670561c2cbff54ad1b1dae00af5dfe265b744394d34f0eae)
            check_type(argname="argument allowed_accounts", value=allowed_accounts, expected_type=type_hints["allowed_accounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_accounts is not None:
            self._values["allowed_accounts"] = allowed_accounts

    @builtins.property
    def allowed_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of accounts that are allowed to access the endpoint.

        :default: - only the service account is allowed.

        :stability: experimental
        '''
        result = self._values.get("allowed_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.EndpointProps",
    jsii_struct_bases=[EndpointOptions],
    name_mapping={
        "allowed_accounts": "allowedAccounts",
        "allocate": "allocate",
        "deallocate": "deallocate",
    },
)
class EndpointProps(EndpointOptions):
    def __init__(
        self,
        *,
        allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        allocate: Allocate,
        deallocate: Deallocate,
    ) -> None:
        '''(experimental) Properties ``Endpoint``.

        :param allowed_accounts: (experimental) List of accounts that are allowed to access the endpoint. Default: - only the service account is allowed.
        :param allocate: (experimental) Allocate function.
        :param deallocate: (experimental) Deallocate function.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86cad33b3692a8b218c59deb676f5ad36b05a7ed72879ec9e6960bb6eac1098)
            check_type(argname="argument allowed_accounts", value=allowed_accounts, expected_type=type_hints["allowed_accounts"])
            check_type(argname="argument allocate", value=allocate, expected_type=type_hints["allocate"])
            check_type(argname="argument deallocate", value=deallocate, expected_type=type_hints["deallocate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocate": allocate,
            "deallocate": deallocate,
        }
        if allowed_accounts is not None:
            self._values["allowed_accounts"] = allowed_accounts

    @builtins.property
    def allowed_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of accounts that are allowed to access the endpoint.

        :default: - only the service account is allowed.

        :stability: experimental
        '''
        result = self._values.get("allowed_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allocate(self) -> Allocate:
        '''(experimental) Allocate function.

        :stability: experimental
        '''
        result = self._values.get("allocate")
        assert result is not None, "Required property 'allocate' is missing"
        return typing.cast(Allocate, result)

    @builtins.property
    def deallocate(self) -> Deallocate:
        '''(experimental) Deallocate function.

        :stability: experimental
        '''
        result = self._values.get("deallocate")
        assert result is not None, "Required property 'deallocate' is missing"
        return typing.cast(Deallocate, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.Environment",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "admin_role_arn": "adminRoleArn",
        "pool": "pool",
        "region": "region",
    },
)
class Environment:
    def __init__(
        self,
        *,
        account: builtins.str,
        admin_role_arn: builtins.str,
        pool: builtins.str,
        region: builtins.str,
    ) -> None:
        '''(experimental) Environment Configuration.

        :param account: (experimental) Account ID.
        :param admin_role_arn: (experimental) ARN of an Admin role in the account. This role must be pre-created and allow the service to assume it.
        :param pool: (experimental) Which pool does this environment belong to.
        :param region: (experimental) Region.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a87bacbf0242891798d37ad305b544c303701f0241297e41227ca500b7ce11)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument admin_role_arn", value=admin_role_arn, expected_type=type_hints["admin_role_arn"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "admin_role_arn": admin_role_arn,
            "pool": pool,
            "region": region,
        }

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Account ID.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_role_arn(self) -> builtins.str:
        '''(experimental) ARN of an Admin role in the account.

        This role must be pre-created
        and allow the service to assume it.

        :stability: experimental
        '''
        result = self._values.get("admin_role_arn")
        assert result is not None, "Required property 'admin_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool(self) -> builtins.str:
        '''(experimental) Which pool does this environment belong to.

        :stability: experimental
        '''
        result = self._values.get("pool")
        assert result is not None, "Required property 'pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Environment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Environments(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Environments",
):
    '''(experimental) Environments table.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af286d2ea4c54c2785f03940141fb188764383c9b3c5ae8228b05d10ffe4183c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''
        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06b815653296707b54cd26f26703388635a6a09a792f676670f66113bc6c456)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(None, jsii.invoke(self, "grantReadWrite", [identity]))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.Table:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.Table, jsii.get(self, "table"))


class Scheduler(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-atmosphere-service.Scheduler",
):
    '''(experimental) Scheduler layer.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocations: Allocations,
        environments: Environments,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocations: (experimental) Allocations storage.
        :param environments: (experimental) Environments storage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40aece8ad1893f263cfd7356f60acfc8002133bcf95ac34cf18fb30b3c359668)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SchedulerProps(allocations=allocations, environments=environments)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantSchedule")
    def grant_schedule(self, grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''
        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bbd16c51e251490c0c3d568f9acb6731ffb811106bd24f0c393b0079c37032)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantSchedule", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="allocationTimeoutFunction")
    def allocation_timeout_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "allocationTimeoutFunction"))

    @builtins.property
    @jsii.member(jsii_name="cleanupTimeoutFunction")
    def cleanup_timeout_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "cleanupTimeoutFunction"))

    @builtins.property
    @jsii.member(jsii_name="dlq")
    def dlq(self) -> _aws_cdk_aws_sqs_ceddda9d.Queue:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.Queue, jsii.get(self, "dlq"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-atmosphere-service.SchedulerProps",
    jsii_struct_bases=[],
    name_mapping={"allocations": "allocations", "environments": "environments"},
)
class SchedulerProps:
    def __init__(self, *, allocations: Allocations, environments: Environments) -> None:
        '''(experimental) Properties for ``Scheduler``.

        :param allocations: (experimental) Allocations storage.
        :param environments: (experimental) Environments storage.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce40a1273cc270334070329ce7a1c687d0f6736128a4b4f3302c9d74315d6220)
            check_type(argname="argument allocations", value=allocations, expected_type=type_hints["allocations"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocations": allocations,
            "environments": environments,
        }

    @builtins.property
    def allocations(self) -> Allocations:
        '''(experimental) Allocations storage.

        :stability: experimental
        '''
        result = self._values.get("allocations")
        assert result is not None, "Required property 'allocations' is missing"
        return typing.cast(Allocations, result)

    @builtins.property
    def environments(self) -> Environments:
        '''(experimental) Environments storage.

        :stability: experimental
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast(Environments, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchedulerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Allocate",
    "AllocateProps",
    "Allocations",
    "AtmosphereService",
    "AtmosphereServiceProps",
    "Cleanup",
    "CleanupProps",
    "Configuration",
    "ConfigurationData",
    "ConfigurationProps",
    "Deallocate",
    "DeallocateProps",
    "Endpoint",
    "EndpointOptions",
    "EndpointProps",
    "Environment",
    "Environments",
    "Scheduler",
    "SchedulerProps",
]

publication.publish()

def _typecheckingstub__0231988f16f79c5e9e91c43c21dcfa6daa31565b5fdaf3ffb135d19b57fca30e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocations: Allocations,
    configuration: Configuration,
    environments: Environments,
    scheduler: Scheduler,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca47cfce295459755d3e667cf175350e70ab6f0d62725812c126bcec42513f9(
    *,
    allocations: Allocations,
    configuration: Configuration,
    environments: Environments,
    scheduler: Scheduler,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed1aba36a83cd8d657cc4eb45528c4ee3e1b22fa4146d6ce9a695085415faf9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c8f95e4acd80d19711d0b00d7f265e32e0af0754a9e81ba7fbe0c9faa94a92(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad579ce9e0c037b640bf723f24cdf369e9d5886d908c76a2c1d31b4cf0b262a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    config: typing.Union[ConfigurationData, typing.Dict[builtins.str, typing.Any]],
    endpoint: typing.Optional[typing.Union[EndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3160ca321214af3c273a63e391821048132dfdb3e763a6b9e2aaa3c62bc8d1d7(
    *,
    config: typing.Union[ConfigurationData, typing.Dict[builtins.str, typing.Any]],
    endpoint: typing.Optional[typing.Union[EndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55675c03a7e6c56f8a2472e9483d31ad114a159de628f58087ee564262a8db8b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocations: Allocations,
    configuration: Configuration,
    environments: Environments,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45cf22488ac93ee13f8a365a012255cac0cdbb57e092a655614a91c72afbcc1(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c74b92ac430746641057aea2b2edc3a36b24afa2bf517e3430155cc85470dd(
    *,
    allocations: Allocations,
    configuration: Configuration,
    environments: Environments,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3a137cea4f61ae3a90cb488557fd8405310d92f6b9b740a202358a9d9aefff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data: typing.Union[ConfigurationData, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050bd4ac315624861f8343edea53907a87711715c01b0f0c350b5f37793e7ed0(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994d0252650625fc7bb402f65ed22f2384ecf05802a7bac40df3d0aff9364ec0(
    *,
    environments: typing.Sequence[typing.Union[Environment, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aabd37d225de3358f5386696f65c7892d9ad4258d83fd6a4dcf43b1321fd762(
    *,
    data: typing.Union[ConfigurationData, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bd226c207210cec55525d6fdf6170fcb1375ab842e6f9f58f99e9eff15fef7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocations: Allocations,
    cleanup: Cleanup,
    environments: Environments,
    scheduler: Scheduler,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5710e05d2ce9cb3a48dd71a36e7533dfdd7957aab27d5e10a8a0e115b58dec(
    *,
    allocations: Allocations,
    cleanup: Cleanup,
    environments: Environments,
    scheduler: Scheduler,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca446827c29368284848f097b7738220c25168c9f448b0d530fb25a21819b77a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocate: Allocate,
    deallocate: Deallocate,
    allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b787cf2495d75e1670561c2cbff54ad1b1dae00af5dfe265b744394d34f0eae(
    *,
    allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86cad33b3692a8b218c59deb676f5ad36b05a7ed72879ec9e6960bb6eac1098(
    *,
    allowed_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    allocate: Allocate,
    deallocate: Deallocate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a87bacbf0242891798d37ad305b544c303701f0241297e41227ca500b7ce11(
    *,
    account: builtins.str,
    admin_role_arn: builtins.str,
    pool: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af286d2ea4c54c2785f03940141fb188764383c9b3c5ae8228b05d10ffe4183c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06b815653296707b54cd26f26703388635a6a09a792f676670f66113bc6c456(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40aece8ad1893f263cfd7356f60acfc8002133bcf95ac34cf18fb30b3c359668(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocations: Allocations,
    environments: Environments,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bbd16c51e251490c0c3d568f9acb6731ffb811106bd24f0c393b0079c37032(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce40a1273cc270334070329ce7a1c687d0f6736128a4b4f3302c9d74315d6220(
    *,
    allocations: Allocations,
    environments: Environments,
) -> None:
    """Type checking stubs"""
    pass
