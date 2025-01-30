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

from .._jsii import *

import aws_cdk.aws_imagebuilder as _aws_cdk_aws_imagebuilder_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8
from ..constructs import (
    Ec2ImagePipeline as _Ec2ImagePipeline_08b5ca60,
    Ec2ImagePipelineBaseProps as _Ec2ImagePipelineBaseProps_b9c7b595,
)
from ..interfaces import LambdaConfiguration as _LambdaConfiguration_618c7638


class Ec2LinuxImagePipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-proserve-lib.patterns.Ec2LinuxImagePipeline",
):
    '''(experimental) A pattern to build an EC2 Image Pipeline specifically for Linux.

    This pattern contains opinionated code and features to help create a linux
    pipeline. This pattern further simplifies setting up an image pipeline by
    letting you choose specific operating systems and features.

    The example below shows how you can configure an image that contains the AWS
    CLI and retains the SSM agent on the image. The image will have a 100GB root
    volume.

    :stability: experimental

    Example::

        import { Ec2LinuxImagePipeline } from '@cdklabs/cdk-proserve-lib/patterns';
        
        new Ec2LinuxImagePipeline(this, 'ImagePipeline', {
          version: '0.1.0',
          operatingSystem:
            Ec2LinuxImagePipeline.OperatingSystem.RED_HAT_ENTERPRISE_LINUX_8_9,
          rootVolumeSize: 100,
            buildConfiguration: {
              start: true,
              waitForCompletion: true
            },
          features: [
            Ec2LinuxImagePipeline.Feature.AWS_CLI,
            Ec2LinuxImagePipeline.Feature.RETAIN_SSM_AGENT
          ]
        );
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        extra_components: typing.Optional[typing.Sequence[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]] = None,
        extra_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        features: typing.Optional[typing.Sequence["Ec2LinuxImagePipeline.Feature"]] = None,
        operating_system: typing.Optional["Ec2LinuxImagePipeline.OperatingSystem"] = None,
        root_volume_size: typing.Optional[jsii.Number] = None,
        version: builtins.str,
        build_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_618c7638, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) A pattern to build an EC2 Image Pipeline specifically for Linux.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID.
        :param extra_components: (experimental) Additional components to install in the image. These will be added after the default Linux components.
        :param extra_device_mappings: (experimental) Additional EBS volume mappings to add to the image. These will be added in addition to the root volume.
        :param features: (experimental) A list of features to install.
        :param operating_system: (experimental) The operating system to use for the image pipeline.
        :param root_volume_size: (experimental) Size for the root volume in GB. Default: 10 GB. Default: 10
        :param version: (experimental) Version of the image pipeline. This must be updated if you make underlying changes to the pipeline configuration.
        :param build_configuration: (experimental) Configuration options for the build process.
        :param description: (experimental) Description of the image pipeline.
        :param encryption: (experimental) KMS key for encryption.
        :param instance_types: (experimental) Instance types for the Image Builder Pipeline. Default: [t3.medium]
        :param lambda_configuration: (experimental) Optional Lambda configuration settings.
        :param vpc_configuration: (experimental) VPC configuration for the image pipeline.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe75b8964707df740912e083b8358a4e940f27f7259ab820504b6c2ada0e612)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2LinuxImagePipelineProps(
            extra_components=extra_components,
            extra_device_mappings=extra_device_mappings,
            features=features,
            operating_system=operating_system,
            root_volume_size=root_volume_size,
            version=version,
            build_configuration=build_configuration,
            description=description,
            encryption=encryption,
            instance_types=instance_types,
            lambda_configuration=lambda_configuration,
            vpc_configuration=vpc_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="imagePipelineArn")
    def image_pipeline_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imagePipelineArn"))

    @image_pipeline_arn.setter
    def image_pipeline_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480b8d9ad288b00a9019dff6ab448fa0084409e75666e22ebc710de08d511ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePipelineArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imagePipelineTopic")
    def image_pipeline_topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, jsii.get(self, "imagePipelineTopic"))

    @image_pipeline_topic.setter
    def image_pipeline_topic(self, value: _aws_cdk_aws_sns_ceddda9d.ITopic) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c054b2b518ad1fdc972c31ac61f4ccead58620ac1a7b23a125009d747bc370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePipelineTopic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="latestAmi")
    def latest_ami(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "latestAmi"))

    @latest_ami.setter
    def latest_ami(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e396117a6c4ae570f398094ede114baa7576df8e02406727ef327dda84877bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestAmi", value) # pyright: ignore[reportArgumentType]

    @jsii.enum(
        jsii_type="@cdklabs/cdk-proserve-lib.patterns.Ec2LinuxImagePipeline.Feature"
    )
    class Feature(enum.Enum):
        '''
        :stability: experimental
        '''

        AWS_CLI = "AWS_CLI"
        '''
        :stability: experimental
        '''
        NICE_DCV = "NICE_DCV"
        '''
        :stability: experimental
        '''
        RETAIN_SSM_AGENT = "RETAIN_SSM_AGENT"
        '''
        :stability: experimental
        '''
        STIG = "STIG"
        '''
        :stability: experimental
        '''
        SCAP = "SCAP"
        '''
        :stability: experimental
        '''

    @jsii.enum(
        jsii_type="@cdklabs/cdk-proserve-lib.patterns.Ec2LinuxImagePipeline.OperatingSystem"
    )
    class OperatingSystem(enum.Enum):
        '''
        :stability: experimental
        '''

        RED_HAT_ENTERPRISE_LINUX_8_9 = "RED_HAT_ENTERPRISE_LINUX_8_9"
        '''
        :stability: experimental
        '''
        AMAZON_LINUX_2 = "AMAZON_LINUX_2"
        '''
        :stability: experimental
        '''
        AMAZON_LINUX_2023 = "AMAZON_LINUX_2023"
        '''
        :stability: experimental
        '''


@jsii.data_type(
    jsii_type="@cdklabs/cdk-proserve-lib.patterns.Ec2LinuxImagePipelineProps",
    jsii_struct_bases=[_Ec2ImagePipelineBaseProps_b9c7b595],
    name_mapping={
        "version": "version",
        "build_configuration": "buildConfiguration",
        "description": "description",
        "encryption": "encryption",
        "instance_types": "instanceTypes",
        "lambda_configuration": "lambdaConfiguration",
        "vpc_configuration": "vpcConfiguration",
        "extra_components": "extraComponents",
        "extra_device_mappings": "extraDeviceMappings",
        "features": "features",
        "operating_system": "operatingSystem",
        "root_volume_size": "rootVolumeSize",
    },
)
class Ec2LinuxImagePipelineProps(_Ec2ImagePipelineBaseProps_b9c7b595):
    def __init__(
        self,
        *,
        version: builtins.str,
        build_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_618c7638, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
        extra_components: typing.Optional[typing.Sequence[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]] = None,
        extra_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        features: typing.Optional[typing.Sequence[Ec2LinuxImagePipeline.Feature]] = None,
        operating_system: typing.Optional[Ec2LinuxImagePipeline.OperatingSystem] = None,
        root_volume_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for creating a Linux STIG Image Pipeline.

        :param version: (experimental) Version of the image pipeline. This must be updated if you make underlying changes to the pipeline configuration.
        :param build_configuration: (experimental) Configuration options for the build process.
        :param description: (experimental) Description of the image pipeline.
        :param encryption: (experimental) KMS key for encryption.
        :param instance_types: (experimental) Instance types for the Image Builder Pipeline. Default: [t3.medium]
        :param lambda_configuration: (experimental) Optional Lambda configuration settings.
        :param vpc_configuration: (experimental) VPC configuration for the image pipeline.
        :param extra_components: (experimental) Additional components to install in the image. These will be added after the default Linux components.
        :param extra_device_mappings: (experimental) Additional EBS volume mappings to add to the image. These will be added in addition to the root volume.
        :param features: (experimental) A list of features to install.
        :param operating_system: (experimental) The operating system to use for the image pipeline.
        :param root_volume_size: (experimental) Size for the root volume in GB. Default: 10 GB. Default: 10

        :stability: experimental
        '''
        if isinstance(build_configuration, dict):
            build_configuration = _Ec2ImagePipeline_08b5ca60.BuildConfigurationProps(**build_configuration)
        if isinstance(lambda_configuration, dict):
            lambda_configuration = _LambdaConfiguration_618c7638(**lambda_configuration)
        if isinstance(vpc_configuration, dict):
            vpc_configuration = _Ec2ImagePipeline_08b5ca60.VpcConfigurationProps(**vpc_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d272e504a6fabc4b04d50467e7c5293e2777ed064ddb4c6626d553e16c42dd65)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument build_configuration", value=build_configuration, expected_type=type_hints["build_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument lambda_configuration", value=lambda_configuration, expected_type=type_hints["lambda_configuration"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            check_type(argname="argument extra_components", value=extra_components, expected_type=type_hints["extra_components"])
            check_type(argname="argument extra_device_mappings", value=extra_device_mappings, expected_type=type_hints["extra_device_mappings"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument root_volume_size", value=root_volume_size, expected_type=type_hints["root_volume_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if build_configuration is not None:
            self._values["build_configuration"] = build_configuration
        if description is not None:
            self._values["description"] = description
        if encryption is not None:
            self._values["encryption"] = encryption
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if lambda_configuration is not None:
            self._values["lambda_configuration"] = lambda_configuration
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration
        if extra_components is not None:
            self._values["extra_components"] = extra_components
        if extra_device_mappings is not None:
            self._values["extra_device_mappings"] = extra_device_mappings
        if features is not None:
            self._values["features"] = features
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if root_volume_size is not None:
            self._values["root_volume_size"] = root_volume_size

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Version of the image pipeline.

        This must be updated if you make
        underlying changes to the pipeline configuration.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_configuration(
        self,
    ) -> typing.Optional[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps]:
        '''(experimental) Configuration options for the build process.

        :stability: experimental
        '''
        result = self._values.get("build_configuration")
        return typing.cast(typing.Optional[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the image pipeline.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) KMS key for encryption.

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Instance types for the Image Builder Pipeline.

        Default: [t3.medium]

        :stability: experimental
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lambda_configuration(self) -> typing.Optional[_LambdaConfiguration_618c7638]:
        '''(experimental) Optional Lambda configuration settings.

        :stability: experimental
        '''
        result = self._values.get("lambda_configuration")
        return typing.cast(typing.Optional[_LambdaConfiguration_618c7638], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps]:
        '''(experimental) VPC configuration for the image pipeline.

        :stability: experimental
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps], result)

    @builtins.property
    def extra_components(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]]:
        '''(experimental) Additional components to install in the image.

        These will be added after the default Linux components.

        :stability: experimental
        '''
        result = self._values.get("extra_components")
        return typing.cast(typing.Optional[typing.List[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]], result)

    @builtins.property
    def extra_device_mappings(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty]]:
        '''(experimental) Additional EBS volume mappings to add to the image.

        These will be added in addition to the root volume.

        :stability: experimental
        '''
        result = self._values.get("extra_device_mappings")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty]], result)

    @builtins.property
    def features(self) -> typing.Optional[typing.List[Ec2LinuxImagePipeline.Feature]]:
        '''(experimental) A list of features to install.

        :stability: experimental
        '''
        result = self._values.get("features")
        return typing.cast(typing.Optional[typing.List[Ec2LinuxImagePipeline.Feature]], result)

    @builtins.property
    def operating_system(
        self,
    ) -> typing.Optional[Ec2LinuxImagePipeline.OperatingSystem]:
        '''(experimental) The operating system to use for the image pipeline.

        :stability: experimental
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[Ec2LinuxImagePipeline.OperatingSystem], result)

    @builtins.property
    def root_volume_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Size for the root volume in GB.

        Default: 10 GB.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("root_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2LinuxImagePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2LinuxImagePipeline",
    "Ec2LinuxImagePipelineProps",
]

publication.publish()

def _typecheckingstub__cfe75b8964707df740912e083b8358a4e940f27f7259ab820504b6c2ada0e612(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    extra_components: typing.Optional[typing.Sequence[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]] = None,
    extra_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    features: typing.Optional[typing.Sequence[Ec2LinuxImagePipeline.Feature]] = None,
    operating_system: typing.Optional[Ec2LinuxImagePipeline.OperatingSystem] = None,
    root_volume_size: typing.Optional[jsii.Number] = None,
    version: builtins.str,
    build_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_618c7638, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480b8d9ad288b00a9019dff6ab448fa0084409e75666e22ebc710de08d511ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c054b2b518ad1fdc972c31ac61f4ccead58620ac1a7b23a125009d747bc370(
    value: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e396117a6c4ae570f398094ede114baa7576df8e02406727ef327dda84877bda(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d272e504a6fabc4b04d50467e7c5293e2777ed064ddb4c6626d553e16c42dd65(
    *,
    version: builtins.str,
    build_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.BuildConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_configuration: typing.Optional[typing.Union[_LambdaConfiguration_618c7638, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_Ec2ImagePipeline_08b5ca60.VpcConfigurationProps, typing.Dict[builtins.str, typing.Any]]] = None,
    extra_components: typing.Optional[typing.Sequence[typing.Union[_Ec2ImagePipeline_08b5ca60.Component, _aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent]]] = None,
    extra_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.InstanceBlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    features: typing.Optional[typing.Sequence[Ec2LinuxImagePipeline.Feature]] = None,
    operating_system: typing.Optional[Ec2LinuxImagePipeline.OperatingSystem] = None,
    root_volume_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
