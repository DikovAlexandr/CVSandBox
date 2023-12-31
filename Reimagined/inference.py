import torch
import torchvision
import numpy as np
import torch.nn as nn

from PIL import Image
from infer_utils import get_outputs
from torchvision.transforms import transforms as transforms
from class_names import INSTANCE_CATEGORY_NAMES as class_names


def get_bboxes_of_objects(input, weights, threshold):
    # Initialize the model
    model = torchvision.models.detection.maskrcnn_resnet50_fpn_v2(
        pretrained=False, num_classes=91
    )

    model.roi_heads.box_predictor.cls_score = nn.Linear(in_features=1024, out_features=len(class_names), bias=True)
    model.roi_heads.box_predictor.bbox_pred = nn.Linear(in_features=1024, out_features=len(class_names)*4, bias=True)
    model.roi_heads.mask_predictor.mask_fcn_logits = nn.Conv2d(256, len(class_names), kernel_size=(1, 1), stride=(1, 1))

    # Set the computation device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Initialize the model
    ckpt = torch.load(weights, map_location=device)
    model.load_state_dict(ckpt['model'])

    # Load the modle on to the computation device and set to eval mode
    model.to(device).eval()
    # print(model)

    # Transform to convert the image to tensor
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    image = Image.open(input)
    # Keep a copy of the original image for OpenCV functions and applying masks
    orig_image = image.copy()

    # Transform the image
    image = transform(image)
    # Add a batch dimension
    image = image.unsqueeze(0).to(device)

    masks, boxes, labels = get_outputs(image, model, threshold)
    print(boxes, labels)
    print(len(boxes), len(labels))

    return masks, boxes, labels

input = "input/inference_data/test_10.jpg"
weights = "weights/table_plot.pth"
threshold = 0.8
get_bboxes_of_objects = get_bboxes_of_objects(input, weights, threshold)