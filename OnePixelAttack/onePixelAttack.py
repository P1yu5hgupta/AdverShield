from torchvision import models
import torch
import cv2
import numpy as np
from scipy.optimize import differential_evolution
import torch.nn as nn
from torch.autograd import Variable
from OnePixelAttack.model import BasicCNN
import argparse

image_path = 'airplane.png'
d = 3
iters = 600
popsize = 10
model_path = './OnePixelAttack/cifar10_basiccnn.pth.tar'
cifar10_class_names = {0: 'airplane', 1: 'automobile', 2: 'bird', 3: 'cat',
                       4: 'deer', 5: 'dog', 6: 'frog', 7: 'horse', 8: 'ship', 9: 'truck'}
pred_adv = 0
prob_adv = 0
img = None
model = None
prob_orig = 0
pred_orig = 0


def preprocess(img):
    img = img.astype(np.float32)
    img /= 255.0
    img = img.transpose(2, 0, 1)
    return img


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def perturb(x):
    adv_img = img.copy()

    pixs = np.array(np.split(x, len(x)/5)).astype(int)
    loc = (pixs[:, 0], pixs[:, 1])
    val = pixs[:, 2:]
    adv_img[loc] = val

    return adv_img


def optimize(x):
    adv_img = perturb(x)

    inp = Variable(torch.from_numpy(preprocess(adv_img)).float().unsqueeze(0))
    out = model(inp)
    prob = softmax(out.data.numpy()[0])

    return prob[pred_orig]


def scale(x, scale=5):
    return cv2.resize(x, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


def callback(x, convergence):
    global pred_adv, prob_adv
    adv_img = perturb(x)

    inp = Variable(torch.from_numpy(preprocess(adv_img)).float().unsqueeze(0))
    out = model(inp)
    prob = softmax(out.data.numpy()[0])

    pred_adv = np.argmax(prob)
    prob_adv = prob[pred_adv]
    if pred_adv != pred_orig and prob_adv >= 0.9:
        print('Attack successful..')
        print('Prob [%s]: %f' % (cifar10_class_names[pred_adv], prob_adv))
        print()
        return True
    else:
        print('Prob [%s]: %f' %
              (cifar10_class_names[pred_orig], prob[pred_orig]))


def onePixelAttackUtil1(_image_path):
    image_path = "./OnePixelAttack/images/"+_image_path
    print('Request: One Pixel Attack Method')
    print("Predict: Image Received: %s" % (_image_path))
    orig = cv2.imread(image_path)[..., ::-1]
    orig = cv2.resize(orig, (32, 32))
    global img
    img = orig.copy()
    shape = orig.shape
    global model
    model = BasicCNN()
    saved = torch.load(model_path, map_location='cpu')
    model.load_state_dict(saved['state_dict'])
    model.eval()

    inp = Variable(torch.from_numpy(preprocess(img)).float().unsqueeze(0))
    global pred_orig
    global prob_orig
    prob_orig = softmax(model(inp).data.numpy()[0])
    pred_orig = np.argmax(prob_orig)
    print('Prediction before attack: %s' % (cifar10_class_names[pred_orig]))
    print('Probability: %f' % (prob_orig[pred_orig]))
    return cifar10_class_names[pred_orig], prob_orig[pred_orig]


def onePixelAttackUtil2(_image_path, _d):

    image_path = "./OnePixelAttack/images/"+_image_path
    d = _d
    print('Request: One Pixel Attack Method')
    print("Attack: Image Received: %s, Epsilon: %s" % (_image_path, d))
    orig = cv2.imread(image_path)[..., ::-1]
    orig = cv2.resize(orig, (32, 32))
    global img
    img = orig.copy()
    shape = orig.shape
    global model
    model = BasicCNN()
    saved = torch.load(model_path, map_location='cpu')
    model.load_state_dict(saved['state_dict'])
    model.eval()

    inp = Variable(torch.from_numpy(preprocess(img)).float().unsqueeze(0))
    global pred_orig
    global prob_orig
    prob_orig = softmax(model(inp).data.numpy()[0])
    pred_orig = np.argmax(prob_orig)
    print('Prediction before attack: %s' % (cifar10_class_names[pred_orig]))
    print('Probability: %f' % (prob_orig[pred_orig]))
    print()

    # while True:
    bounds = [(0, shape[0]-1), (0, shape[1]), (0, 255), (0, 255), (0, 255)] * d
    result = differential_evolution(
        optimize, bounds, maxiter=iters, popsize=popsize, tol=1e-5, callback=callback)

    adv_img = perturb(result.x)
    inp = Variable(torch.from_numpy(preprocess(adv_img)).float().unsqueeze(0))
    out = model(inp)
    prob = softmax(out.data.numpy()[0])
    print('Prob [%s]: %f --> Prob[%s]: %f' % (cifar10_class_names[pred_orig],
                                              prob_orig[pred_orig], cifar10_class_names[pred_adv], prob_adv))

    # cv2.imshow('adversarial image', scale(adv_img[..., ::-1]))

    finalImg = scale(adv_img[..., ::-1])
    # finalImg = cv2.resize(finalImg, (100, 100), interpolation=cv2.INTER_AREA)
    cv2.imwrite('./OnePixelAttack/adversarial.jpg', finalImg)
    cv2.imwrite('./static/images/onepixelattack/adversarial.jpg',
                finalImg)

    return (cifar10_class_names[pred_adv], prob_adv)
    exit(0)
