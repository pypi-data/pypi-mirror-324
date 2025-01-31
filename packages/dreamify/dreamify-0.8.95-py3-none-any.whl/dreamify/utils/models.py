import random
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


def choose_model(model_name: str = None):
    # If no model name is given, choose randomly from the available models
    if model_name is None:
        model_name = random.choice([model.value for model in ModelType])

    model_name = model_name.lower()

    match model_name:
        case ModelType.VGG19.value:
            return VGG19(weights="imagenet", include_top=False)
        case ModelType.CONVNEXT_XL.value:
            return ConvNeXtXLarge(weights="imagenet", include_top=False)
        case ModelType.DENSENET121.value:
            return DenseNet121(weights="imagenet", include_top=False)
        case ModelType.EFFICIENTNET_V2L.value:
            return EfficientNetV2L(weights="imagenet", include_top=False)
        case ModelType.INCEPTION_RESNET_V2.value:
            return InceptionResNetV2(weights="imagenet", include_top=False)
        case ModelType.INCEPTION_V3.value:
            return InceptionV3(weights="imagenet", include_top=False)
        case ModelType.RESNET152V2.value:
            return ResNet152V2(weights="imagenet", include_top=False)
        case ModelType.XCEPTION.value:
            return Xception(weights="imagenet", include_top=False)
        case _:
            raise ValueError(f"Invalid model name: {model_name}")
