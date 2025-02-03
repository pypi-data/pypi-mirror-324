r'''
# dynatrace-automation-sitereliabilityguardian

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Automation::SiteReliabilityGuardian` v1.1.0.

## Description

Manage a Site Reliability Guardian in Dynatrace

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Automation::SiteReliabilityGuardian \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Automation-SiteReliabilityGuardian \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Automation::SiteReliabilityGuardian`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-automation-sitereliabilityguardian+v1.1.0).
* Issues related to `Dynatrace::Automation::SiteReliabilityGuardian` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

## License

Distributed under the Apache-2.0 License.
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

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnSiteReliabilityGuardian(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.CfnSiteReliabilityGuardian",
):
    '''A CloudFormation ``Dynatrace::Automation::SiteReliabilityGuardian``.

    :cloudformationResource: Dynatrace::Automation::SiteReliabilityGuardian
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        objectives: typing.Sequence[typing.Union["Objective", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Sequence[builtins.str],
        variables: typing.Sequence[typing.Union["Variable", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Automation::SiteReliabilityGuardian``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the Site Reliability Guardian.
        :param objectives: Objectives are means for measuring the performance, availability, capacity, and security of your services.
        :param tags: Define key/value pairs that further describe this guardian.
        :param variables: Define variables for dynamically defining DQL queries.
        :param description: The description of the Site Reliability Guardian.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0422fb6c65cee431f47d86c37f7abc0d35b737ccec2e54f2287f9fd4b88d1a03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSiteReliabilityGuardianProps(
            name=name,
            objectives=objectives,
            tags=tags,
            variables=variables,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrObjectId")
    def attr_object_id(self) -> builtins.str:
        '''Attribute ``Dynatrace::Automation::SiteReliabilityGuardian.ObjectId``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrObjectId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSiteReliabilityGuardianProps":
        '''Resource props.'''
        return typing.cast("CfnSiteReliabilityGuardianProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.CfnSiteReliabilityGuardianProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "objectives": "objectives",
        "tags": "tags",
        "variables": "variables",
        "description": "description",
    },
)
class CfnSiteReliabilityGuardianProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        objectives: typing.Sequence[typing.Union["Objective", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Sequence[builtins.str],
        variables: typing.Sequence[typing.Union["Variable", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a Site Reliability Guardian in Dynatrace.

        :param name: The name of the Site Reliability Guardian.
        :param objectives: Objectives are means for measuring the performance, availability, capacity, and security of your services.
        :param tags: Define key/value pairs that further describe this guardian.
        :param variables: Define variables for dynamically defining DQL queries.
        :param description: The description of the Site Reliability Guardian.

        :schema: CfnSiteReliabilityGuardianProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42d9185aa9afe3b9b806593fe5bc5152567b9523ffab8138990f6ee78f50f0e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument objectives", value=objectives, expected_type=type_hints["objectives"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "objectives": objectives,
            "tags": tags,
            "variables": variables,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Site Reliability Guardian.

        :schema: CfnSiteReliabilityGuardianProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def objectives(self) -> typing.List["Objective"]:
        '''Objectives are means for measuring the performance, availability, capacity, and security of your services.

        :schema: CfnSiteReliabilityGuardianProps#Objectives
        '''
        result = self._values.get("objectives")
        assert result is not None, "Required property 'objectives' is missing"
        return typing.cast(typing.List["Objective"], result)

    @builtins.property
    def tags(self) -> typing.List[builtins.str]:
        '''Define key/value pairs that further describe this guardian.

        :schema: CfnSiteReliabilityGuardianProps#Tags
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.List["Variable"]:
        '''Define variables for dynamically defining DQL queries.

        :schema: CfnSiteReliabilityGuardianProps#Variables
        '''
        result = self._values.get("variables")
        assert result is not None, "Required property 'variables' is missing"
        return typing.cast(typing.List["Variable"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Site Reliability Guardian.

        :schema: CfnSiteReliabilityGuardianProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteReliabilityGuardianProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.Objective",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "name": "name",
        "objective_type": "objectiveType",
        "auto_adaptive_threshold_enabled": "autoAdaptiveThresholdEnabled",
        "description": "description",
        "dql_query": "dqlQuery",
        "reference_slo": "referenceSlo",
        "target": "target",
        "warning": "warning",
    },
)
class Objective:
    def __init__(
        self,
        *,
        comparison_operator: "ObjectiveComparisonOperator",
        name: builtins.str,
        objective_type: "ObjectiveObjectiveType",
        auto_adaptive_threshold_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        dql_query: typing.Optional[builtins.str] = None,
        reference_slo: typing.Optional[builtins.str] = None,
        target: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param comparison_operator: 
        :param name: 
        :param objective_type: 
        :param auto_adaptive_threshold_enabled: Auto-adaptive thresholds are a dynamic approach to baselining where the reference value for detecting anomalies changes over time.
        :param description: 
        :param dql_query: 
        :param reference_slo: Please enter the metric key of your desired SLO. SLO metric keys have to start with 'func:slo.'
        :param target: 
        :param warning: 

        :schema: Objective
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdecc1a4f4d89018b12f12f2d60bb11179823dc2eb0cd45d43b1542dbba510f)
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument objective_type", value=objective_type, expected_type=type_hints["objective_type"])
            check_type(argname="argument auto_adaptive_threshold_enabled", value=auto_adaptive_threshold_enabled, expected_type=type_hints["auto_adaptive_threshold_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dql_query", value=dql_query, expected_type=type_hints["dql_query"])
            check_type(argname="argument reference_slo", value=reference_slo, expected_type=type_hints["reference_slo"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "name": name,
            "objective_type": objective_type,
        }
        if auto_adaptive_threshold_enabled is not None:
            self._values["auto_adaptive_threshold_enabled"] = auto_adaptive_threshold_enabled
        if description is not None:
            self._values["description"] = description
        if dql_query is not None:
            self._values["dql_query"] = dql_query
        if reference_slo is not None:
            self._values["reference_slo"] = reference_slo
        if target is not None:
            self._values["target"] = target
        if warning is not None:
            self._values["warning"] = warning

    @builtins.property
    def comparison_operator(self) -> "ObjectiveComparisonOperator":
        '''
        :schema: Objective#ComparisonOperator
        '''
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return typing.cast("ObjectiveComparisonOperator", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: Objective#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def objective_type(self) -> "ObjectiveObjectiveType":
        '''
        :schema: Objective#ObjectiveType
        '''
        result = self._values.get("objective_type")
        assert result is not None, "Required property 'objective_type' is missing"
        return typing.cast("ObjectiveObjectiveType", result)

    @builtins.property
    def auto_adaptive_threshold_enabled(self) -> typing.Optional[builtins.bool]:
        '''Auto-adaptive thresholds are a dynamic approach to baselining where the reference value for detecting anomalies changes over time.

        :schema: Objective#AutoAdaptiveThresholdEnabled
        '''
        result = self._values.get("auto_adaptive_threshold_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Objective#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dql_query(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Objective#DqlQuery
        '''
        result = self._values.get("dql_query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_slo(self) -> typing.Optional[builtins.str]:
        '''Please enter the metric key of your desired SLO.

        SLO metric keys have to start with 'func:slo.'

        :schema: Objective#ReferenceSlo
        '''
        result = self._values.get("reference_slo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Objective#Target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Objective#Warning
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Objective(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.ObjectiveComparisonOperator"
)
class ObjectiveComparisonOperator(enum.Enum):
    '''
    :schema: ObjectiveComparisonOperator
    '''

    GREATER_UNDERSCORE_THAN_UNDERSCORE_OR_UNDERSCORE_EQUAL = "GREATER_UNDERSCORE_THAN_UNDERSCORE_OR_UNDERSCORE_EQUAL"
    '''GREATER_THAN_OR_EQUAL.'''
    LESS_UNDERSCORE_THAN_UNDERSCORE_OR_UNDERSCORE_EQUAL = "LESS_UNDERSCORE_THAN_UNDERSCORE_OR_UNDERSCORE_EQUAL"
    '''LESS_THAN_OR_EQUAL.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.ObjectiveObjectiveType"
)
class ObjectiveObjectiveType(enum.Enum):
    '''
    :schema: ObjectiveObjectiveType
    '''

    DQL = "DQL"
    '''DQL.'''
    REFERENCE_UNDERSCORE_SLO = "REFERENCE_UNDERSCORE_SLO"
    '''REFERENCE_SLO.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-sitereliabilityguardian.Variable",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "name": "name"},
)
class Variable:
    def __init__(self, *, definition: builtins.str, name: builtins.str) -> None:
        '''
        :param definition: 
        :param name: 

        :schema: Variable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b055e3cfa80462a2182084357ceaa8ecca8e26edf513c5151f143e70ec1e45)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "name": name,
        }

    @builtins.property
    def definition(self) -> builtins.str:
        '''
        :schema: Variable#Definition
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: Variable#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Variable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSiteReliabilityGuardian",
    "CfnSiteReliabilityGuardianProps",
    "Objective",
    "ObjectiveComparisonOperator",
    "ObjectiveObjectiveType",
    "Variable",
]

publication.publish()

def _typecheckingstub__0422fb6c65cee431f47d86c37f7abc0d35b737ccec2e54f2287f9fd4b88d1a03(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    objectives: typing.Sequence[typing.Union[Objective, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Sequence[builtins.str],
    variables: typing.Sequence[typing.Union[Variable, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42d9185aa9afe3b9b806593fe5bc5152567b9523ffab8138990f6ee78f50f0e(
    *,
    name: builtins.str,
    objectives: typing.Sequence[typing.Union[Objective, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Sequence[builtins.str],
    variables: typing.Sequence[typing.Union[Variable, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdecc1a4f4d89018b12f12f2d60bb11179823dc2eb0cd45d43b1542dbba510f(
    *,
    comparison_operator: ObjectiveComparisonOperator,
    name: builtins.str,
    objective_type: ObjectiveObjectiveType,
    auto_adaptive_threshold_enabled: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    dql_query: typing.Optional[builtins.str] = None,
    reference_slo: typing.Optional[builtins.str] = None,
    target: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b055e3cfa80462a2182084357ceaa8ecca8e26edf513c5151f143e70ec1e45(
    *,
    definition: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
