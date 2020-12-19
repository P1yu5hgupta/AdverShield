import torch
from torch.autograd import Variable
from torchvision import models
import torch.nn as nn
from torchvision import transforms
import numpy as np
import cv2
import argparse
from BIAttack.imagenet_labels import classes
import warnings
warnings.filterwarnings('ignore')

IMG_SIZE = 224
model_name = "resnet18"


def iterativeAttack(image_path="goldfish.jpg", eps=200, num_iter=10):
    image_path = "./BIAttack/images/"+image_path
    print('Iterative Method')
    print('Model: %s' % (model_name))
    print('Image: % s' % (image_path))
    print('Epsilon Value: %s Number of Iterations: %s' % (eps, num_iter))
    orig = cv2.imread(image_path)[..., ::-1]
    orig = cv2.resize(orig, (IMG_SIZE, IMG_SIZE))
    img = orig.copy().astype(np.float32)

    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    img /= 255.0
    img = (img - mean)/std
    img = img.transpose(2, 0, 1)

    model = getattr(models, model_name)(pretrained=True)
    model.eval()
    criterion = nn.CrossEntropyLoss()

    device = 'cpu'

    # prediction before attack
    inp = Variable(torch.from_numpy(img).to(
        device).float().unsqueeze(0), requires_grad=True)
    orig = torch.from_numpy(img).float().to(device).unsqueeze(0)

    out = model(inp)
    pred = np.argmax(out.data.cpu().numpy())

    prediction = classes[pred].split(',')[0]
    print('Prediction before attack: %s' % (classes[pred].split(',')[0]))

    inp = Variable(torch.from_numpy(img).to(
        device).float().unsqueeze(0), requires_grad=True)
    alpha = 10

    print('eps [%d]' % (eps))
    print('Iter [%d]' % (num_iter))
    print('-'*20)

    attack = ""
    for i in range(num_iter):
        out = model(inp)
        loss = criterion(out, Variable(
            torch.Tensor([float(pred)]).to(device).long()))

        loss.backward()

        perturbation = (alpha/255.0) * torch.sign(inp.grad.data)
        perturbation = torch.clamp((inp.data + perturbation) - orig, min=-eps/255.0, max=eps/255.0)
        inp.data = orig + perturbation

        inp.grad.data.zero_()

        pred_adv = np.argmax(model(inp).data.cpu().numpy())
        attack = classes[pred_adv].split(',')[0]
        print("Iter [%3d/%3d]:  Prediction: %s"
              % (i, num_iter, classes[pred_adv].split(',')[0]))

    adv = inp.data.cpu().numpy()[0]
    pert = (adv-img).transpose(1, 2, 0)
    adv = adv.transpose(1, 2, 0)
    adv = (adv * std) + mean
    adv = adv * 255.0
    adv = adv[..., ::-1]
    adv = np.clip(adv, 0, 255).astype(np.uint8)
    pert = pert * 255
    pert = np.clip(pert, 0, 255).astype(np.uint8)

    cv2.imwrite("./BIAttack/adversarial.jpg", adv)
    cv2.imwrite("./BIAttack/perturbation.jpg", pert)

    cv2.imwrite("./static/images/biattack/adversarial.jpg", adv)
    cv2.imwrite("./static/images/biattack/perbutation.jpg", pert)

    return prediction, attack
    # cv2.imshow("perbutation", pert)
    # cv2.imshow('adversarial image', adv)


if __name__ == '__main__':
    iterativeAttack()
