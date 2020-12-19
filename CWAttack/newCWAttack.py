import numpy as np
import json
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as Data
import cv2
import torchvision.utils
from torchvision import models
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.autograd import Variable
import warnings
warnings.filterwarnings("ignore")

device = "cpu"
IMG_SIZE = 224
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

class_idx = json.load(open("./CWAttack/data/imagenet_class_index.json"))
idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
])

model = models.inception_v3(pretrained=True).to(device)
model.eval()


def imshow(img):
    npimg = img.numpy()
    adv = np.transpose(npimg, (1, 2, 0))
    adv = cv2.convertScaleAbs(adv, alpha=(255.0))
    adv = adv[..., ::-1]
    return adv


def cw_l2_attack(model, images, labels, max_iter, targeted=False, c=1e-4, kappa=0, learning_rate=0.01):
    if(max_iter == 0):
        return images
    images = images.to(device)
    labels = labels.to(device)

    def f(x):

        outputs = model(x)
        one_hot_labels = torch.eye(len(outputs[0]))[labels].to(device)

        i, _ = torch.max((1-one_hot_labels)*outputs, dim=1)
        j = torch.masked_select(outputs, one_hot_labels.byte())

        if targeted:
            return torch.clamp(i-j, min=-kappa)

        else:
            return torch.clamp(j-i, min=-kappa)

    w = torch.zeros_like(images, requires_grad=True).to(device)

    optimizer = optim.Adam([w], lr=learning_rate)

    prev = 1e10
    for step in range(max_iter):

        a = 1/2*(nn.Tanh()(w) + 1)

        loss1 = nn.MSELoss(reduction='sum')(a, images)
        loss2 = torch.sum(c*f(a))

        cost = loss1 + loss2

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

        print('- Learning Progress : %2.2f %%        ' %
              ((step+1)/max_iter*100), end='\r')

    attack_images = 1/2*(nn.Tanh()(w) + 1)

    return attack_images


def cwAttack(image_path="./monkey.jpg", itr=4):
    print("True Image & True Label")
    image_path = "./CWAttack/images/"+image_path
    print(image_path)
    orig = cv2.imread(image_path)[..., ::-1]
    orig = cv2.resize(orig, (IMG_SIZE, IMG_SIZE))
    img = orig.copy().astype(np.float32)

    img /= 255.0
    img = (img - mean)/std
    img = img.transpose(2, 0, 1)

    images = Variable(torch.from_numpy(img).to(
        device).float().unsqueeze(0), requires_grad=True)
    images = images.to(device)

    outputs = model(images)

    _, labels = torch.max(outputs.data, 1)
    print(idx2label[labels.item()])

    print("Attack Image & Predicted Label")

    model.eval()

    images = cw_l2_attack(model, images, labels, itr, targeted=False, c=0.1)
    outputs = model(images)

    _, pre = torch.max(outputs.data, 1)

    adv = imshow(torchvision.utils.make_grid(
        images.cpu().data, normalize=True))
    cv2.imwrite("./CWAttack/cwAdversarial.jpg", adv)
    cv2.imwrite("./static/images/cwattack/adversarial.jpg", adv)
    print()
    result = idx2label[pre.item()]
    result = result.split("_")
    result = " ".join(result)
    return result
