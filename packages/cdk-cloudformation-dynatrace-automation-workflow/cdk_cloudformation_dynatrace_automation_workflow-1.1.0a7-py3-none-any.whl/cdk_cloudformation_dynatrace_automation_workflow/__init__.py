r'''
# dynatrace-automation-workflow

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Automation::Workflow` v1.1.0.

## Description

The Workflows app is a powerful tool that lets you automatically act on monitoring data

## References

* [Source](https://docs.dynatrace.com/docs/platform-modules/automations/workflows)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Automation::Workflow \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Automation-Workflow \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Automation::Workflow`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-automation-workflow+v1.1.0).
* Issues related to `Dynatrace::Automation::Workflow` should be reported to the [publisher](https://docs.dynatrace.com/docs/platform-modules/automations/workflows).

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


class CfnWorkflow(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.CfnWorkflow",
):
    '''A CloudFormation ``Dynatrace::Automation::Workflow``.

    :cloudformationResource: Dynatrace::Automation::Workflow
    :link: https://docs.dynatrace.com/docs/platform-modules/automations/workflows
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        tasks: typing.Sequence[typing.Union["Task", typing.Dict[builtins.str, typing.Any]]],
        title: builtins.str,
        actor: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        is_private: typing.Optional[builtins.bool] = None,
        owner: typing.Optional[builtins.str] = None,
        throttle: typing.Optional[typing.Union["ThrottleRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger: typing.Optional[typing.Union["TriggerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Automation::Workflow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param tasks: The tasks to run for every execution of this workflow.
        :param title: The title / name of the workflow.
        :param actor: The user context the executions of the workflow will happen with.
        :param description: An optional description for the workflow.
        :param is_private: Defines whether this workflow is private to the owner or not.
        :param owner: The ID of the owner of this workflow.
        :param throttle: 
        :param trigger: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad52f4bb59e1412243694ac8412c386467d2bde67a5a6212c6f3175e65243ef8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkflowProps(
            tasks=tasks,
            title=title,
            actor=actor,
            description=description,
            is_private=is_private,
            owner=owner,
            throttle=throttle,
            trigger=trigger,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Dynatrace::Automation::Workflow.Id``.

        :link: https://docs.dynatrace.com/docs/platform-modules/automations/workflows
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerType")
    def attr_owner_type(self) -> builtins.str:
        '''Attribute ``Dynatrace::Automation::Workflow.OwnerType``.

        :link: https://docs.dynatrace.com/docs/platform-modules/automations/workflows
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerType"))

    @builtins.property
    @jsii.member(jsii_name="attrSchemaVersion")
    def attr_schema_version(self) -> jsii.Number:
        '''Attribute ``Dynatrace::Automation::Workflow.SchemaVersion``.

        :link: https://docs.dynatrace.com/docs/platform-modules/automations/workflows
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrSchemaVersion"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnWorkflowProps":
        '''Resource props.'''
        return typing.cast("CfnWorkflowProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.CfnWorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "tasks": "tasks",
        "title": "title",
        "actor": "actor",
        "description": "description",
        "is_private": "isPrivate",
        "owner": "owner",
        "throttle": "throttle",
        "trigger": "trigger",
    },
)
class CfnWorkflowProps:
    def __init__(
        self,
        *,
        tasks: typing.Sequence[typing.Union["Task", typing.Dict[builtins.str, typing.Any]]],
        title: builtins.str,
        actor: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        is_private: typing.Optional[builtins.bool] = None,
        owner: typing.Optional[builtins.str] = None,
        throttle: typing.Optional[typing.Union["ThrottleRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        trigger: typing.Optional[typing.Union["TriggerRequest", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The Workflows app is a powerful tool that lets you automatically act on monitoring data.

        :param tasks: The tasks to run for every execution of this workflow.
        :param title: The title / name of the workflow.
        :param actor: The user context the executions of the workflow will happen with.
        :param description: An optional description for the workflow.
        :param is_private: Defines whether this workflow is private to the owner or not.
        :param owner: The ID of the owner of this workflow.
        :param throttle: 
        :param trigger: 

        :schema: CfnWorkflowProps
        '''
        if isinstance(throttle, dict):
            throttle = ThrottleRequest(**throttle)
        if isinstance(trigger, dict):
            trigger = TriggerRequest(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3cb61ba0d3e04154ca9161f8c951d8257bd962f019fc52c033f81d5f38c75a)
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument actor", value=actor, expected_type=type_hints["actor"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_private", value=is_private, expected_type=type_hints["is_private"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tasks": tasks,
            "title": title,
        }
        if actor is not None:
            self._values["actor"] = actor
        if description is not None:
            self._values["description"] = description
        if is_private is not None:
            self._values["is_private"] = is_private
        if owner is not None:
            self._values["owner"] = owner
        if throttle is not None:
            self._values["throttle"] = throttle
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def tasks(self) -> typing.List["Task"]:
        '''The tasks to run for every execution of this workflow.

        :schema: CfnWorkflowProps#Tasks
        '''
        result = self._values.get("tasks")
        assert result is not None, "Required property 'tasks' is missing"
        return typing.cast(typing.List["Task"], result)

    @builtins.property
    def title(self) -> builtins.str:
        '''The title / name of the workflow.

        :schema: CfnWorkflowProps#Title
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actor(self) -> typing.Optional[builtins.str]:
        '''The user context the executions of the workflow will happen with.

        :schema: CfnWorkflowProps#Actor
        '''
        result = self._values.get("actor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the workflow.

        :schema: CfnWorkflowProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_private(self) -> typing.Optional[builtins.bool]:
        '''Defines whether this workflow is private to the owner or not.

        :schema: CfnWorkflowProps#IsPrivate
        '''
        result = self._values.get("is_private")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The ID of the owner of this workflow.

        :schema: CfnWorkflowProps#Owner
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def throttle(self) -> typing.Optional["ThrottleRequest"]:
        '''
        :schema: CfnWorkflowProps#Throttle
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional["ThrottleRequest"], result)

    @builtins.property
    def trigger(self) -> typing.Optional["TriggerRequest"]:
        '''
        :schema: CfnWorkflowProps#Trigger
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["TriggerRequest"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.Condition",
    jsii_struct_bases=[],
    name_mapping={"states": "states", "custom": "custom", "else_": "else"},
)
class Condition:
    def __init__(
        self,
        *,
        states: typing.Any,
        custom: typing.Optional[builtins.str] = None,
        else_: typing.Optional["ConditionElse"] = None,
    ) -> None:
        '''
        :param states: key/value pairs where the key is the name of another task and the value the status it needs to be for the current task to get executed. Possible values are SUCCESS, ERROR, ANY, OK (Success or Skipped) and NOK (Error or Cancelled)
        :param custom: A custom condition that needs to be met for the current task to get executed.
        :param else_: Possible values are SKIP and STOP.

        :schema: Condition
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cc246049e0a855d1dbd011e308740e1d2546740127d5246313238e6d2c5101)
            check_type(argname="argument states", value=states, expected_type=type_hints["states"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument else_", value=else_, expected_type=type_hints["else_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "states": states,
        }
        if custom is not None:
            self._values["custom"] = custom
        if else_ is not None:
            self._values["else_"] = else_

    @builtins.property
    def states(self) -> typing.Any:
        '''key/value pairs where the key is the name of another task and the value the status it needs to be for the current task to get executed.

        Possible values are SUCCESS, ERROR, ANY, OK (Success or Skipped) and NOK (Error or Cancelled)

        :schema: Condition#States
        '''
        result = self._values.get("states")
        assert result is not None, "Required property 'states' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def custom(self) -> typing.Optional[builtins.str]:
        '''A custom condition that needs to be met for the current task to get executed.

        :schema: Condition#Custom
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def else_(self) -> typing.Optional["ConditionElse"]:
        '''Possible values are SKIP and STOP.

        :schema: Condition#Else
        '''
        result = self._values.get("else_")
        return typing.cast(typing.Optional["ConditionElse"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Condition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.ConditionElse")
class ConditionElse(enum.Enum):
    '''Possible values are SKIP and STOP.

    :schema: ConditionElse
    '''

    SKIP = "SKIP"
    '''SKIP.'''
    STOP = "STOP"
    '''STOP.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.DavisEventName",
    jsii_struct_bases=[],
    name_mapping={"match": "match", "name": "name"},
)
class DavisEventName:
    def __init__(self, *, match: "DavisEventNameMatch", name: builtins.str) -> None:
        '''
        :param match: 
        :param name: 

        :schema: DavisEventName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831d9bb89102d87447360e35c5d74721996b23457d1878d57c422b02720b0442)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
            "name": name,
        }

    @builtins.property
    def match(self) -> "DavisEventNameMatch":
        '''
        :schema: DavisEventName#Match
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("DavisEventNameMatch", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: DavisEventName#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DavisEventName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.DavisEventNameMatch"
)
class DavisEventNameMatch(enum.Enum):
    '''
    :schema: DavisEventNameMatch
    '''

    CONTAINS = "CONTAINS"
    '''Contains.'''
    EQUALS = "EQUALS"
    '''Equals.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.DavisProblemCategories",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "custom": "custom",
        "error": "error",
        "info": "info",
        "monitoring_unavailable": "monitoringUnavailable",
        "resource": "resource",
        "slowdown": "slowdown",
    },
)
class DavisProblemCategories:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.bool] = None,
        custom: typing.Optional[builtins.bool] = None,
        error: typing.Optional[builtins.bool] = None,
        info: typing.Optional[builtins.bool] = None,
        monitoring_unavailable: typing.Optional[builtins.bool] = None,
        resource: typing.Optional[builtins.bool] = None,
        slowdown: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param availability: 
        :param custom: 
        :param error: 
        :param info: 
        :param monitoring_unavailable: 
        :param resource: 
        :param slowdown: 

        :schema: DavisProblemCategories
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d902c56b3688527d823253e297ceb958423b25e36efc1e82345f91c6726605b8)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
            check_type(argname="argument info", value=info, expected_type=type_hints["info"])
            check_type(argname="argument monitoring_unavailable", value=monitoring_unavailable, expected_type=type_hints["monitoring_unavailable"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument slowdown", value=slowdown, expected_type=type_hints["slowdown"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if custom is not None:
            self._values["custom"] = custom
        if error is not None:
            self._values["error"] = error
        if info is not None:
            self._values["info"] = info
        if monitoring_unavailable is not None:
            self._values["monitoring_unavailable"] = monitoring_unavailable
        if resource is not None:
            self._values["resource"] = resource
        if slowdown is not None:
            self._values["slowdown"] = slowdown

    @builtins.property
    def availability(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Availability
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Custom
        '''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Error
        '''
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def info(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Info
        '''
        result = self._values.get("info")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def monitoring_unavailable(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#MonitoringUnavailable
        '''
        result = self._values.get("monitoring_unavailable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slowdown(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: DavisProblemCategories#Slowdown
        '''
        result = self._values.get("slowdown")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DavisProblemCategories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "categories": "categories",
        "custom_filters": "customFilters",
        "entity_tags": "entityTags",
        "entity_tags_match": "entityTagsMatch",
        "event_type": "eventType",
        "names": "names",
        "on_problem_close": "onProblemClose",
        "query": "query",
    },
)
class EventTriggerConfig:
    def __init__(
        self,
        *,
        categories: typing.Optional[typing.Union[DavisProblemCategories, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_filters: typing.Optional[builtins.str] = None,
        entity_tags: typing.Any = None,
        entity_tags_match: typing.Optional["EventTriggerConfigEntityTagsMatch"] = None,
        event_type: typing.Optional["EventTriggerConfigEventType"] = None,
        names: typing.Optional[typing.Sequence[typing.Union[DavisEventName, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_problem_close: typing.Optional[builtins.bool] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''If specified the workflow is getting triggered based on events.

        :param categories: 
        :param custom_filters: 
        :param entity_tags: 
        :param entity_tags_match: 
        :param event_type: 
        :param names: 
        :param on_problem_close: 
        :param query: 

        :schema: EventTriggerConfig
        '''
        if isinstance(categories, dict):
            categories = DavisProblemCategories(**categories)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d48ac179ac2036ca8752ab6a9c54a9032cd695bd658ddf6061dc12400114dc2)
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument custom_filters", value=custom_filters, expected_type=type_hints["custom_filters"])
            check_type(argname="argument entity_tags", value=entity_tags, expected_type=type_hints["entity_tags"])
            check_type(argname="argument entity_tags_match", value=entity_tags_match, expected_type=type_hints["entity_tags_match"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument names", value=names, expected_type=type_hints["names"])
            check_type(argname="argument on_problem_close", value=on_problem_close, expected_type=type_hints["on_problem_close"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if categories is not None:
            self._values["categories"] = categories
        if custom_filters is not None:
            self._values["custom_filters"] = custom_filters
        if entity_tags is not None:
            self._values["entity_tags"] = entity_tags
        if entity_tags_match is not None:
            self._values["entity_tags_match"] = entity_tags_match
        if event_type is not None:
            self._values["event_type"] = event_type
        if names is not None:
            self._values["names"] = names
        if on_problem_close is not None:
            self._values["on_problem_close"] = on_problem_close
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def categories(self) -> typing.Optional[DavisProblemCategories]:
        '''
        :schema: EventTriggerConfig#Categories
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[DavisProblemCategories], result)

    @builtins.property
    def custom_filters(self) -> typing.Optional[builtins.str]:
        '''
        :schema: EventTriggerConfig#CustomFilters
        '''
        result = self._values.get("custom_filters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_tags(self) -> typing.Any:
        '''
        :schema: EventTriggerConfig#EntityTags
        '''
        result = self._values.get("entity_tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def entity_tags_match(self) -> typing.Optional["EventTriggerConfigEntityTagsMatch"]:
        '''
        :schema: EventTriggerConfig#EntityTagsMatch
        '''
        result = self._values.get("entity_tags_match")
        return typing.cast(typing.Optional["EventTriggerConfigEntityTagsMatch"], result)

    @builtins.property
    def event_type(self) -> typing.Optional["EventTriggerConfigEventType"]:
        '''
        :schema: EventTriggerConfig#EventType
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional["EventTriggerConfigEventType"], result)

    @builtins.property
    def names(self) -> typing.Optional[typing.List[DavisEventName]]:
        '''
        :schema: EventTriggerConfig#Names
        '''
        result = self._values.get("names")
        return typing.cast(typing.Optional[typing.List[DavisEventName]], result)

    @builtins.property
    def on_problem_close(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: EventTriggerConfig#OnProblemClose
        '''
        result = self._values.get("on_problem_close")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''
        :schema: EventTriggerConfig#Query
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerConfigEntityTagsMatch"
)
class EventTriggerConfigEntityTagsMatch(enum.Enum):
    '''
    :schema: EventTriggerConfigEntityTagsMatch
    '''

    ALL = "ALL"
    '''All.'''
    ANY = "ANY"
    '''Any.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerConfigEventType"
)
class EventTriggerConfigEventType(enum.Enum):
    '''
    :schema: EventTriggerConfigEventType
    '''

    BIZEVENTS = "BIZEVENTS"
    '''bizevents.'''
    EVENTS = "EVENTS"
    '''events.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerRequest",
    jsii_struct_bases=[],
    name_mapping={
        "is_active": "isActive",
        "trigger_configuration": "triggerConfiguration",
    },
)
class EventTriggerRequest:
    def __init__(
        self,
        *,
        is_active: typing.Optional[builtins.bool] = None,
        trigger_configuration: typing.Optional[typing.Union["EventTriggerRequestTriggerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param is_active: If specified the workflow is getting triggered based on a schedule.
        :param trigger_configuration: 

        :schema: EventTriggerRequest
        '''
        if isinstance(trigger_configuration, dict):
            trigger_configuration = EventTriggerRequestTriggerConfiguration(**trigger_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc35e00561e260314ae6b5443e50d36c74e6d19079dbc121cdfc1a8b5798fbaa)
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument trigger_configuration", value=trigger_configuration, expected_type=type_hints["trigger_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_active is not None:
            self._values["is_active"] = is_active
        if trigger_configuration is not None:
            self._values["trigger_configuration"] = trigger_configuration

    @builtins.property
    def is_active(self) -> typing.Optional[builtins.bool]:
        '''If specified the workflow is getting triggered based on a schedule.

        :schema: EventTriggerRequest#IsActive
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trigger_configuration(
        self,
    ) -> typing.Optional["EventTriggerRequestTriggerConfiguration"]:
        '''
        :schema: EventTriggerRequest#TriggerConfiguration
        '''
        result = self._values.get("trigger_configuration")
        return typing.cast(typing.Optional["EventTriggerRequestTriggerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventTriggerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerRequestTriggerConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class EventTriggerRequestTriggerConfiguration:
    def __init__(
        self,
        *,
        type: typing.Optional["EventTriggerRequestTriggerConfigurationType"] = None,
        value: typing.Optional[typing.Union[EventTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: 
        :param value: 

        :schema: EventTriggerRequestTriggerConfiguration
        '''
        if isinstance(value, dict):
            value = EventTriggerConfig(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1016836b8242730f92c1d6f0b512904d37d32840940b2980b0f86e5e4449ada)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional["EventTriggerRequestTriggerConfigurationType"]:
        '''
        :schema: EventTriggerRequestTriggerConfiguration#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["EventTriggerRequestTriggerConfigurationType"], result)

    @builtins.property
    def value(self) -> typing.Optional[EventTriggerConfig]:
        '''
        :schema: EventTriggerRequestTriggerConfiguration#Value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[EventTriggerConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventTriggerRequestTriggerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.EventTriggerRequestTriggerConfigurationType"
)
class EventTriggerRequestTriggerConfigurationType(enum.Enum):
    '''
    :schema: EventTriggerRequestTriggerConfigurationType
    '''

    DAVIS_HYPHEN_EVENT = "DAVIS_HYPHEN_EVENT"
    '''davis-event.'''
    DAVIS_HYPHEN_PROBLEM = "DAVIS_HYPHEN_PROBLEM"
    '''davis-problem.'''
    EVENT = "EVENT"
    '''event.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.Position",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class Position:
    def __init__(self, *, x: jsii.Number, y: jsii.Number) -> None:
        '''Layouting information about the task tile when visualized.

        If not specified Dynatrace will position the task tiles automatically

        :param x: x-coordinate for layouting.
        :param y: y-coordinate for layouting.

        :schema: Position
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6573d3df138f683eae6f279629ddd29a2bf2c935828c071628f6395e1a359e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "x": x,
            "y": y,
        }

    @builtins.property
    def x(self) -> jsii.Number:
        '''x-coordinate for layouting.

        :schema: Position#X
        '''
        result = self._values.get("x")
        assert result is not None, "Required property 'x' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def y(self) -> jsii.Number:
        '''y-coordinate for layouting.

        :schema: Position#Y
        '''
        result = self._values.get("y")
        assert result is not None, "Required property 'y' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Position(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.Retry",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "delay": "delay",
        "failed_loop_iterations_only": "failedLoopIterationsOnly",
    },
)
class Retry:
    def __init__(
        self,
        *,
        count: typing.Optional[builtins.str] = None,
        delay: typing.Optional[builtins.str] = None,
        failed_loop_iterations_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configure whether to automatically rerun the task on failure.

        If not specified no retries will be attempted

        :param count: Specifies a maximum number of times that a task can be repeated in case it fails on execution. You can specify either a number between 1 and 99 here or use an expression
        :param delay: Specifies a delay in seconds between subsequent task retries. You can specify either a number between 1 and 3600 here or an expression ({{...}})
        :param failed_loop_iterations_only: Specifies whether retrying the failed iterations or the whole loop.

        :schema: Retry
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2be2e9fbb6f7408a362116c4b917b4931654fb953d57c5766c77e2732e3e81)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument failed_loop_iterations_only", value=failed_loop_iterations_only, expected_type=type_hints["failed_loop_iterations_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if delay is not None:
            self._values["delay"] = delay
        if failed_loop_iterations_only is not None:
            self._values["failed_loop_iterations_only"] = failed_loop_iterations_only

    @builtins.property
    def count(self) -> typing.Optional[builtins.str]:
        '''Specifies a maximum number of times that a task can be repeated in case it fails on execution.

        You can specify either a number between 1 and 99 here or use an expression

        :schema: Retry#Count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Specifies a delay in seconds between subsequent task retries.

        You can specify either a number between 1 and 3600 here or an expression ({{...}})

        :schema: Retry#Delay
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failed_loop_iterations_only(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether retrying the failed iterations or the whole loop.

        :schema: Retry#FailedLoopIterationsOnly
        '''
        result = self._values.get("failed_loop_iterations_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Retry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.ScheduleFilterParameters",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "earliest_start": "earliestStart",
        "earliest_start_time": "earliestStartTime",
        "exclude_dates": "excludeDates",
        "include_dates": "includeDates",
        "until": "until",
    },
)
class ScheduleFilterParameters:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        earliest_start: typing.Optional[datetime.datetime] = None,
        earliest_start_time: typing.Optional[builtins.str] = None,
        exclude_dates: typing.Optional[typing.Sequence[datetime.datetime]] = None,
        include_dates: typing.Optional[typing.Sequence[datetime.datetime]] = None,
        until: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''
        :param count: 
        :param earliest_start: 
        :param earliest_start_time: 
        :param exclude_dates: 
        :param include_dates: 
        :param until: 

        :schema: ScheduleFilterParameters
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b58d2cea081d793b14223c37515e566da2f92bbe5e847aac88f40f4071eb04)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument earliest_start", value=earliest_start, expected_type=type_hints["earliest_start"])
            check_type(argname="argument earliest_start_time", value=earliest_start_time, expected_type=type_hints["earliest_start_time"])
            check_type(argname="argument exclude_dates", value=exclude_dates, expected_type=type_hints["exclude_dates"])
            check_type(argname="argument include_dates", value=include_dates, expected_type=type_hints["include_dates"])
            check_type(argname="argument until", value=until, expected_type=type_hints["until"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if earliest_start is not None:
            self._values["earliest_start"] = earliest_start
        if earliest_start_time is not None:
            self._values["earliest_start_time"] = earliest_start_time
        if exclude_dates is not None:
            self._values["exclude_dates"] = exclude_dates
        if include_dates is not None:
            self._values["include_dates"] = include_dates
        if until is not None:
            self._values["until"] = until

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: ScheduleFilterParameters#Count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def earliest_start(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: ScheduleFilterParameters#EarliestStart
        '''
        result = self._values.get("earliest_start")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def earliest_start_time(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScheduleFilterParameters#EarliestStartTime
        '''
        result = self._values.get("earliest_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_dates(self) -> typing.Optional[typing.List[datetime.datetime]]:
        '''
        :schema: ScheduleFilterParameters#ExcludeDates
        '''
        result = self._values.get("exclude_dates")
        return typing.cast(typing.Optional[typing.List[datetime.datetime]], result)

    @builtins.property
    def include_dates(self) -> typing.Optional[typing.List[datetime.datetime]]:
        '''
        :schema: ScheduleFilterParameters#IncludeDates
        '''
        result = self._values.get("include_dates")
        return typing.cast(typing.Optional[typing.List[datetime.datetime]], result)

    @builtins.property
    def until(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: ScheduleFilterParameters#Until
        '''
        result = self._values.get("until")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleFilterParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.ScheduleRequest",
    jsii_struct_bases=[],
    name_mapping={
        "trigger": "trigger",
        "filter_parameters": "filterParameters",
        "input": "input",
        "is_active": "isActive",
        "next_execution": "nextExecution",
        "rule": "rule",
        "timezone": "timezone",
    },
)
class ScheduleRequest:
    def __init__(
        self,
        *,
        trigger: typing.Any,
        filter_parameters: typing.Optional[typing.Union[ScheduleFilterParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        input: typing.Any = None,
        is_active: typing.Optional[builtins.bool] = None,
        next_execution: typing.Optional[datetime.datetime] = None,
        rule: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param trigger: 
        :param filter_parameters: 
        :param input: 
        :param is_active: 
        :param next_execution: 
        :param rule: 
        :param timezone: Timezone identifier, e.g. Europe/London.

        :schema: ScheduleRequest
        '''
        if isinstance(filter_parameters, dict):
            filter_parameters = ScheduleFilterParameters(**filter_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6389793d73515428e762f74210985e23465436f5043d26877e26d25c33e84bc2)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument filter_parameters", value=filter_parameters, expected_type=type_hints["filter_parameters"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument next_execution", value=next_execution, expected_type=type_hints["next_execution"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if filter_parameters is not None:
            self._values["filter_parameters"] = filter_parameters
        if input is not None:
            self._values["input"] = input
        if is_active is not None:
            self._values["is_active"] = is_active
        if next_execution is not None:
            self._values["next_execution"] = next_execution
        if rule is not None:
            self._values["rule"] = rule
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def trigger(self) -> typing.Any:
        '''
        :schema: ScheduleRequest#Trigger
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def filter_parameters(self) -> typing.Optional[ScheduleFilterParameters]:
        '''
        :schema: ScheduleRequest#FilterParameters
        '''
        result = self._values.get("filter_parameters")
        return typing.cast(typing.Optional[ScheduleFilterParameters], result)

    @builtins.property
    def input(self) -> typing.Any:
        '''
        :schema: ScheduleRequest#Input
        '''
        result = self._values.get("input")
        return typing.cast(typing.Any, result)

    @builtins.property
    def is_active(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: ScheduleRequest#IsActive
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def next_execution(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: ScheduleRequest#NextExecution
        '''
        result = self._values.get("next_execution")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def rule(self) -> typing.Optional[builtins.str]:
        '''
        :schema: ScheduleRequest#Rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Timezone identifier, e.g. Europe/London.

        :schema: ScheduleRequest#Timezone
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.Task",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "name": "name",
        "active": "active",
        "concurrency": "concurrency",
        "condition": "condition",
        "description": "description",
        "input": "input",
        "position": "position",
        "retry": "retry",
        "timeout": "timeout",
        "with_items": "withItems",
    },
)
class Task:
    def __init__(
        self,
        *,
        action: "TaskAction",
        name: builtins.str,
        active: typing.Optional[builtins.bool] = None,
        concurrency: typing.Optional[jsii.Number] = None,
        condition: typing.Optional[typing.Union[Condition, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        input: typing.Any = None,
        position: typing.Optional[typing.Union[Position, typing.Dict[builtins.str, typing.Any]]] = None,
        retry: typing.Optional[typing.Union[Retry, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        with_items: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Currently known and supported values are dynatrace.automations:http-function, dynatrace.automations:run-javascript and dynatrace.automations:execute-dql-query.
        :param name: The name of the task.
        :param active: Specifies whether a task should be skipped as a no operation or not.
        :param concurrency: Required if 'WithItems' is specified. By default loops execute sequentially with concurrency set to 1. You can increase how often it runs in parallel
        :param condition: 
        :param description: A description for this task.
        :param input: 
        :param position: 
        :param retry: 
        :param timeout: Specifies a default task timeout in seconds. 15 * 60 (15min) is used when not set.
        :param with_items: Iterates over items in a list, allowing actions to be executed repeatedly. Example: Specifying item in [1, 2, 3] here will execute the task three times for the numbers 1, 2 and 3 - with the current number available for scripting using the expression {{ _.item }}

        :schema: Task
        '''
        if isinstance(condition, dict):
            condition = Condition(**condition)
        if isinstance(position, dict):
            position = Position(**position)
        if isinstance(retry, dict):
            retry = Retry(**retry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9c5156931844403dd132cb1f75aa0b9ca1542d84d215c98679ab4b47047441)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument with_items", value=with_items, expected_type=type_hints["with_items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if active is not None:
            self._values["active"] = active
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if condition is not None:
            self._values["condition"] = condition
        if description is not None:
            self._values["description"] = description
        if input is not None:
            self._values["input"] = input
        if position is not None:
            self._values["position"] = position
        if retry is not None:
            self._values["retry"] = retry
        if timeout is not None:
            self._values["timeout"] = timeout
        if with_items is not None:
            self._values["with_items"] = with_items

    @builtins.property
    def action(self) -> "TaskAction":
        '''Currently known and supported values are dynatrace.automations:http-function, dynatrace.automations:run-javascript and dynatrace.automations:execute-dql-query.

        :schema: Task#Action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("TaskAction", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the task.

        :schema: Task#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether a task should be skipped as a no operation or not.

        :schema: Task#Active
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def concurrency(self) -> typing.Optional[jsii.Number]:
        '''Required if 'WithItems' is specified.

        By default loops execute sequentially with concurrency set to 1. You can increase how often it runs in parallel

        :schema: Task#Concurrency
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def condition(self) -> typing.Optional[Condition]:
        '''
        :schema: Task#Condition
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[Condition], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for this task.

        :schema: Task#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(self) -> typing.Any:
        '''
        :schema: Task#Input
        '''
        result = self._values.get("input")
        return typing.cast(typing.Any, result)

    @builtins.property
    def position(self) -> typing.Optional[Position]:
        '''
        :schema: Task#Position
        '''
        result = self._values.get("position")
        return typing.cast(typing.Optional[Position], result)

    @builtins.property
    def retry(self) -> typing.Optional[Retry]:
        '''
        :schema: Task#Retry
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional[Retry], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Specifies a default task timeout in seconds.

        15 * 60 (15min) is used when not set.

        :schema: Task#Timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def with_items(self) -> typing.Optional[builtins.str]:
        '''Iterates over items in a list, allowing actions to be executed repeatedly.

        Example: Specifying item in [1, 2, 3] here will execute the task three times for the numbers 1, 2 and 3 - with the current number available for scripting using the expression {{ _.item }}

        :schema: Task#WithItems
        '''
        result = self._values.get("with_items")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Task(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.TaskAction")
class TaskAction(enum.Enum):
    '''Currently known and supported values are dynatrace.automations:http-function, dynatrace.automations:run-javascript and dynatrace.automations:execute-dql-query.

    :schema: TaskAction
    '''

    DYNATRACE_PERIOD_AUTOMATIONS_HTTP_HYPHEN_FUNCTION = "DYNATRACE_PERIOD_AUTOMATIONS_HTTP_HYPHEN_FUNCTION"
    '''dynatrace.automations:http-function.'''
    DYNATRACE_PERIOD_AUTOMATIONS_RUN_HYPHEN_JAVASCRIPT = "DYNATRACE_PERIOD_AUTOMATIONS_RUN_HYPHEN_JAVASCRIPT"
    '''dynatrace.automations:run-javascript.'''
    DYNATRACE_PERIOD_AUTOMATIONS_EXECUTE_HYPHEN_DQL_HYPHEN_QUERY = "DYNATRACE_PERIOD_AUTOMATIONS_EXECUTE_HYPHEN_DQL_HYPHEN_QUERY"
    '''dynatrace.automations:execute-dql-query.'''
    DYNATRACE_PERIOD_SITE_PERIOD_RELIABILITY_PERIOD_GUARDIAN_VALIDATE_HYPHEN_GUARDIAN_HYPHEN_ACTION = "DYNATRACE_PERIOD_SITE_PERIOD_RELIABILITY_PERIOD_GUARDIAN_VALIDATE_HYPHEN_GUARDIAN_HYPHEN_ACTION"
    '''dynatrace.site.reliability.guardian:validate-guardian-action.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.ThrottleLimitEvent",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "time_left_in_seconds": "timeLeftInSeconds",
        "timestamp": "timestamp",
    },
)
class ThrottleLimitEvent:
    def __init__(
        self,
        *,
        limit: jsii.Number,
        time_left_in_seconds: jsii.Number,
        timestamp: datetime.datetime,
    ) -> None:
        '''
        :param limit: 
        :param time_left_in_seconds: 
        :param timestamp: 

        :schema: ThrottleLimitEvent
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8c5ad3498215a6a3e93fa5339fd3ebc92974d089b2685d00a8b64efbd4357d)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument time_left_in_seconds", value=time_left_in_seconds, expected_type=type_hints["time_left_in_seconds"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "limit": limit,
            "time_left_in_seconds": time_left_in_seconds,
            "timestamp": timestamp,
        }

    @builtins.property
    def limit(self) -> jsii.Number:
        '''
        :schema: ThrottleLimitEvent#Limit
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_left_in_seconds(self) -> jsii.Number:
        '''
        :schema: ThrottleLimitEvent#TimeLeftInSeconds
        '''
        result = self._values.get("time_left_in_seconds")
        assert result is not None, "Required property 'time_left_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timestamp(self) -> datetime.datetime:
        '''
        :schema: ThrottleLimitEvent#Timestamp
        '''
        result = self._values.get("timestamp")
        assert result is not None, "Required property 'timestamp' is missing"
        return typing.cast(datetime.datetime, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThrottleLimitEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.ThrottleRequest",
    jsii_struct_bases=[],
    name_mapping={"is_limit_hit": "isLimitHit", "limit_events": "limitEvents"},
)
class ThrottleRequest:
    def __init__(
        self,
        *,
        is_limit_hit: builtins.bool,
        limit_events: typing.Optional[typing.Sequence[typing.Union[ThrottleLimitEvent, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param is_limit_hit: 
        :param limit_events: 

        :schema: ThrottleRequest
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd54022dfb5341aabf6ac2e0b9bd517f03924859f59497dd09ba71a9074ec7b)
            check_type(argname="argument is_limit_hit", value=is_limit_hit, expected_type=type_hints["is_limit_hit"])
            check_type(argname="argument limit_events", value=limit_events, expected_type=type_hints["limit_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_limit_hit": is_limit_hit,
        }
        if limit_events is not None:
            self._values["limit_events"] = limit_events

    @builtins.property
    def is_limit_hit(self) -> builtins.bool:
        '''
        :schema: ThrottleRequest#IsLimitHit
        '''
        result = self._values.get("is_limit_hit")
        assert result is not None, "Required property 'is_limit_hit' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def limit_events(self) -> typing.Optional[typing.List[ThrottleLimitEvent]]:
        '''
        :schema: ThrottleRequest#LimitEvents
        '''
        result = self._values.get("limit_events")
        return typing.cast(typing.Optional[typing.List[ThrottleLimitEvent]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThrottleRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-automation-workflow.TriggerRequest",
    jsii_struct_bases=[],
    name_mapping={"event_trigger": "eventTrigger", "schedule": "schedule"},
)
class TriggerRequest:
    def __init__(
        self,
        *,
        event_trigger: typing.Optional[typing.Union[EventTriggerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union[ScheduleRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configures how executions of the workflows are getting triggered.

        If no trigger is specified it means the workflow is getting manually triggered

        :param event_trigger: 
        :param schedule: 

        :schema: TriggerRequest
        '''
        if isinstance(event_trigger, dict):
            event_trigger = EventTriggerRequest(**event_trigger)
        if isinstance(schedule, dict):
            schedule = ScheduleRequest(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7834acff965719d9323cc66f8fd6d11c6b002a504d5872b18a4419daa6a4983)
            check_type(argname="argument event_trigger", value=event_trigger, expected_type=type_hints["event_trigger"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_trigger is not None:
            self._values["event_trigger"] = event_trigger
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def event_trigger(self) -> typing.Optional[EventTriggerRequest]:
        '''
        :schema: TriggerRequest#EventTrigger
        '''
        result = self._values.get("event_trigger")
        return typing.cast(typing.Optional[EventTriggerRequest], result)

    @builtins.property
    def schedule(self) -> typing.Optional[ScheduleRequest]:
        '''
        :schema: TriggerRequest#Schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[ScheduleRequest], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggerRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnWorkflow",
    "CfnWorkflowProps",
    "Condition",
    "ConditionElse",
    "DavisEventName",
    "DavisEventNameMatch",
    "DavisProblemCategories",
    "EventTriggerConfig",
    "EventTriggerConfigEntityTagsMatch",
    "EventTriggerConfigEventType",
    "EventTriggerRequest",
    "EventTriggerRequestTriggerConfiguration",
    "EventTriggerRequestTriggerConfigurationType",
    "Position",
    "Retry",
    "ScheduleFilterParameters",
    "ScheduleRequest",
    "Task",
    "TaskAction",
    "ThrottleLimitEvent",
    "ThrottleRequest",
    "TriggerRequest",
]

publication.publish()

def _typecheckingstub__ad52f4bb59e1412243694ac8412c386467d2bde67a5a6212c6f3175e65243ef8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    tasks: typing.Sequence[typing.Union[Task, typing.Dict[builtins.str, typing.Any]]],
    title: builtins.str,
    actor: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    is_private: typing.Optional[builtins.bool] = None,
    owner: typing.Optional[builtins.str] = None,
    throttle: typing.Optional[typing.Union[ThrottleRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger: typing.Optional[typing.Union[TriggerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3cb61ba0d3e04154ca9161f8c951d8257bd962f019fc52c033f81d5f38c75a(
    *,
    tasks: typing.Sequence[typing.Union[Task, typing.Dict[builtins.str, typing.Any]]],
    title: builtins.str,
    actor: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    is_private: typing.Optional[builtins.bool] = None,
    owner: typing.Optional[builtins.str] = None,
    throttle: typing.Optional[typing.Union[ThrottleRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger: typing.Optional[typing.Union[TriggerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cc246049e0a855d1dbd011e308740e1d2546740127d5246313238e6d2c5101(
    *,
    states: typing.Any,
    custom: typing.Optional[builtins.str] = None,
    else_: typing.Optional[ConditionElse] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831d9bb89102d87447360e35c5d74721996b23457d1878d57c422b02720b0442(
    *,
    match: DavisEventNameMatch,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d902c56b3688527d823253e297ceb958423b25e36efc1e82345f91c6726605b8(
    *,
    availability: typing.Optional[builtins.bool] = None,
    custom: typing.Optional[builtins.bool] = None,
    error: typing.Optional[builtins.bool] = None,
    info: typing.Optional[builtins.bool] = None,
    monitoring_unavailable: typing.Optional[builtins.bool] = None,
    resource: typing.Optional[builtins.bool] = None,
    slowdown: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d48ac179ac2036ca8752ab6a9c54a9032cd695bd658ddf6061dc12400114dc2(
    *,
    categories: typing.Optional[typing.Union[DavisProblemCategories, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_filters: typing.Optional[builtins.str] = None,
    entity_tags: typing.Any = None,
    entity_tags_match: typing.Optional[EventTriggerConfigEntityTagsMatch] = None,
    event_type: typing.Optional[EventTriggerConfigEventType] = None,
    names: typing.Optional[typing.Sequence[typing.Union[DavisEventName, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_problem_close: typing.Optional[builtins.bool] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc35e00561e260314ae6b5443e50d36c74e6d19079dbc121cdfc1a8b5798fbaa(
    *,
    is_active: typing.Optional[builtins.bool] = None,
    trigger_configuration: typing.Optional[typing.Union[EventTriggerRequestTriggerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1016836b8242730f92c1d6f0b512904d37d32840940b2980b0f86e5e4449ada(
    *,
    type: typing.Optional[EventTriggerRequestTriggerConfigurationType] = None,
    value: typing.Optional[typing.Union[EventTriggerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6573d3df138f683eae6f279629ddd29a2bf2c935828c071628f6395e1a359e(
    *,
    x: jsii.Number,
    y: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2be2e9fbb6f7408a362116c4b917b4931654fb953d57c5766c77e2732e3e81(
    *,
    count: typing.Optional[builtins.str] = None,
    delay: typing.Optional[builtins.str] = None,
    failed_loop_iterations_only: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b58d2cea081d793b14223c37515e566da2f92bbe5e847aac88f40f4071eb04(
    *,
    count: typing.Optional[jsii.Number] = None,
    earliest_start: typing.Optional[datetime.datetime] = None,
    earliest_start_time: typing.Optional[builtins.str] = None,
    exclude_dates: typing.Optional[typing.Sequence[datetime.datetime]] = None,
    include_dates: typing.Optional[typing.Sequence[datetime.datetime]] = None,
    until: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6389793d73515428e762f74210985e23465436f5043d26877e26d25c33e84bc2(
    *,
    trigger: typing.Any,
    filter_parameters: typing.Optional[typing.Union[ScheduleFilterParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    input: typing.Any = None,
    is_active: typing.Optional[builtins.bool] = None,
    next_execution: typing.Optional[datetime.datetime] = None,
    rule: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9c5156931844403dd132cb1f75aa0b9ca1542d84d215c98679ab4b47047441(
    *,
    action: TaskAction,
    name: builtins.str,
    active: typing.Optional[builtins.bool] = None,
    concurrency: typing.Optional[jsii.Number] = None,
    condition: typing.Optional[typing.Union[Condition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    input: typing.Any = None,
    position: typing.Optional[typing.Union[Position, typing.Dict[builtins.str, typing.Any]]] = None,
    retry: typing.Optional[typing.Union[Retry, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    with_items: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8c5ad3498215a6a3e93fa5339fd3ebc92974d089b2685d00a8b64efbd4357d(
    *,
    limit: jsii.Number,
    time_left_in_seconds: jsii.Number,
    timestamp: datetime.datetime,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd54022dfb5341aabf6ac2e0b9bd517f03924859f59497dd09ba71a9074ec7b(
    *,
    is_limit_hit: builtins.bool,
    limit_events: typing.Optional[typing.Sequence[typing.Union[ThrottleLimitEvent, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7834acff965719d9323cc66f8fd6d11c6b002a504d5872b18a4419daa6a4983(
    *,
    event_trigger: typing.Optional[typing.Union[EventTriggerRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[ScheduleRequest, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
