from enum import Enum

from tensorflow.keras.applications import (
    VGG19,
    ConvNeXtXLarge,
    DenseNet121,
    EfficientNetV2L,
    InceptionResNetV2,
    InceptionV3,
    ResNet152V2,
    Xception,
)


class ModelType(Enum):
    VGG19 = "vgg19"
    CONVNEXT_XL = "convnext_xl"
    DENSENET121 = "densenet121"
    EFFICIENTNET_V2L = "efficientnet_v2l"
    INCEPTION_RESNET_V2 = "inception_resnet_v2"
    INCEPTION_V3 = "inception_v3"
    RESNET152V2 = "resnet152v2"
    XCEPTION = "xception"


def get_layer_settings(model_name: ModelType, layer_settings=None):
    if layer_settings is None:
        if model_name == ModelType.INCEPTION_V3:
            layer_settings = {
                "mixed4": 1.0,
                "mixed5": 1.5,
                "mixed6": 2.0,
                "mixed7": 2.5,
            }
        elif model_name == ModelType.VGG19:
            layer_settings = {
                "block5_conv3": 1.0,
                "block5_conv2": 1.5,
                "block4_conv3": 2.0,
                "block3_conv3": 2.5,
            }
        elif model_name == ModelType.DENSENET121:
            layer_settings = {
                "conv5_block16_1_conv": 1.0,
                "conv4_block24_1_conv": 1.5,
                "conv3_block16_1_conv": 2.0,
                "conv2_block12_1_conv": 2.5,
            }
        elif model_name == ModelType.EFFICIENTNET_V2L:
            layer_settings = {
                "block7a_project_bn": 1.0,
                "block6a_expand_activation": 1.5,
                "block5a_expand_activation": 2.0,
                "block4a_expand_activation": 2.5,
            }
        elif model_name == ModelType.INCEPTION_RESNET_V2:
            layer_settings = {
                "mixed_7a": 1.0,
                "mixed_6a": 1.5,
                "mixed_5a": 2.0,
                "mixed_4a": 2.5,
            }
        elif model_name == ModelType.RESNET152V2:
            layer_settings = {
                "conv5_block3_out": 1.0,
                "conv4_block6_out": 1.5,
                "conv3_block4_out": 2.0,
                "conv2_block3_out": 2.5,
            }
        elif model_name == ModelType.XCEPTION:
            layer_settings = {
                "block14_sepconv2_act": 1.0,
                "block13_sepconv2_act": 1.5,
                "block12_sepconv2_act": 2.0,
                "block11_sepconv2_act": 2.5,
            }
        elif model_name == ModelType.CONVNEXT_XL:
            layer_settings = {
                "stage4_block2_depthwise_conv": 1.0,
                "stage3_block2_depthwise_conv": 1.5,
                "stage2_block2_depthwise_conv": 2.0,
                "stage1_block2_depthwise_conv": 2.5,
            }
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    return layer_settings


def choose_model(model_name: str = None):
    if model_name is None:
        model_name = random.choice([model.value for model in ModelType])

    model_name = model_name.lower()

    match model_name:
        case ModelType.VGG19.value:
            return VGG19(weights="imagenet", include_top=False), get_layer_settings(
                model_name
            )
        case ModelType.CONVNEXT_XL.value:
            return ConvNeXtXLarge(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.DENSENET121.value:
            return DenseNet121(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.EFFICIENTNET_V2L.value:
            return EfficientNetV2L(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.INCEPTION_RESNET_V2.value:
            return InceptionResNetV2(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.INCEPTION_V3.value:
            return InceptionV3(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.RESNET152V2.value:
            return ResNet152V2(
                weights="imagenet", include_top=False
            ), get_layer_settings(model_name)
        case ModelType.XCEPTION.value:
            return Xception(weights="imagenet", include_top=False), get_layer_settings(
                model_name
            )
        case _:
            raise ValueError(f"Invalid model name: {model_name}")


__all__ = [choose_model]
