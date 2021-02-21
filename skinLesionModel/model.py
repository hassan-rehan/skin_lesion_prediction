# python libraties
import os, cv2
import numpy as np
from PIL import Image

# pytorch libraries
import torch
from torch import nn
from torch.autograd import Variable
from torchvision import models,transforms

def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False

def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
    # Initialize these variables which will be set in this if statement. Each of these
    #   variables is model specific.
    model_ft = None
    input_size = 0

    if model_name == "resnet":
        """ Resnet18, resnet34, resnet50, resnet101
        """
        model_ft = models.resnet50(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
        input_size = 224


    elif model_name == "vgg":
        """ VGG11_bn
        """
        model_ft = models.vgg11_bn(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
        input_size = 224


    elif model_name == "densenet":
        """ Densenet121
        """
        model_ft = models.densenet121(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_ftrs, num_classes)
        input_size = 224

    elif model_name == "inception":
        """ Inception v3
        Be careful, expects (299,299) sized images and has auxiliary output
        """
        model_ft = models.inception_v3(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        # Handle the auxilary net
        num_ftrs = model_ft.AuxLogits.fc.in_features
        model_ft.AuxLogits.fc = nn.Linear(num_ftrs, num_classes)
        # Handle the primary net
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs,num_classes)
        input_size = 299

    else:
        print("Invalid model name, exiting...")
        exit()
    return model_ft, input_size

def choose_model(model_name):
    # resnet,vgg,densenet,inception
    model_name = model_name
    num_classes = 7
    feature_extract = False
    # Initialize the model for this run
    model_ft,input_size = initialize_model(model_name, num_classes, feature_extract, use_pretrained=True)
    # Define the device:
    device = torch.device('cuda:0')
    # Put the model on the device:
    model = model_ft.to(device)
    current_path = os.path.dirname(__file__)
    model.load_state_dict(torch.load(os.path.join(current_path,'skin_lesion')))
    model.eval()
    return model,input_size,device

def compute_img_mean_std(image):
  img_h, img_w = 224, 224
  img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
  img = cv2.resize(img, (img_h, img_w))
  img = img.astype(np.float32) / 255.
  
  pixels = img.ravel()  # resize to one row
  mean=np.mean(pixels)
  stdev=np.std(pixels)

  print("normMean = {}".format(mean))
  print("normStd = {}".format(stdev))
  return mean,stdev

def predict(img,model,input_size,device):
    norm_mean,norm_std = compute_img_mean_std(img)
    transform = transforms.Compose(
                                    [transforms.Resize((input_size,input_size)),transforms.RandomHorizontalFlip(),
                                    transforms.RandomVerticalFlip(),transforms.RandomRotation(20),
                                    transforms.ColorJitter(brightness=0.1, contrast=0.1, hue=0.1),
                                    transforms.ToTensor(), transforms.Normalize(norm_mean, norm_std)]
                                    )
    image=Image.open(img)
    image = transform(image)
    with torch.no_grad():
        image = Variable(image).to(device)
        image = image.unsqueeze(0)
        outputs = model(image)
        prediction = outputs.max(1, keepdim=True)[1]
        return int(prediction[0][0])