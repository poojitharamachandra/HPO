# -*- coding: utf-8 -*-
"""hpo2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ayZhEffmqRrk_hVePfHATozroHdIwA4c
"""

import torch

import torch.nn as nn

import torchvision.transforms as transforms

import torchvision.datasets as dsets

from torch.utils.data import TensorDataset

from torch.autograd import Variable

from torch.utils.data.sampler import SubsetRandomSampler

import numpy as np

#!pip3 install torchvision

class CNNModel(nn.Module):

    def __init__(self):

        super(CNNModel, self).__init__()
        # Convolution 1

        self.cnn1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=0)

        self.relu1 = nn.ReLU()

        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

     

        # Convolution 2

        self.cnn2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=0)

        self.relu2 = nn.ReLU()

        self.maxpool2 = nn.MaxPool2d(kernel_size=2)
        
        
        # Convolution 3

        #self.cnn3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=0)

        #self.relu3 = nn.ReLU()

        #self.maxpool3 = nn.MaxPool2d(kernel_size=2)

        

        # Fully connected 1 (readout)
        #10 classes

        self.fc1 = nn.Linear(32* 5 * 5, 10) 

    

    def forward(self, x):

        # Convolution 1

        out = self.cnn1(x)

        out = self.relu1(out)

        out = self.maxpool1(out)     

        # Convolution 2 

        out = self.cnn2(out)

        out = self.relu2(out) 

        out = self.maxpool2(out)
        
        # Convolution 3 

        #out = self.cnn3(out)

        #out = self.relu3(out) 

        #out = self.maxpool3(out)

        

        # Resize

        # Original size: (100, 32, 7, 7)

        # out.size(0): 100

        # New out size: (100, 32*7*7)

        out = out.view(out.size(0), -1)


        # Linear function (readout)

        out = self.fc1(out)   

        return out

import os

import requests
import numpy as np
from torch.utils.data import Dataset
import torchvision.transforms as transforms



class KMNIST(Dataset):
    """
    Dataset class for use with pytorch for the Kuzushiji-MNIST dataset as given in
    Deep Learning for Classical Japanese Literature. Tarin Clanuwat et al. arXiv:1812.01718

    Kuzushiji-MNIST contains 70,000 28x28 grayscale images spanning 10 classes (one from each column of hiragana),
    and is perfectly balanced like the original MNIST dataset (6k/1k train/test for each class).
    """

    def __init__(self, data_dir='.', train: bool = True, transform=None):
        """
        :param data_dir: Directory of the data
        :param train: Use training or test set
        :param transform: pytorch transforms for data augmentation
        """

        self.__urls = [
            'http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-train-imgs.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-train-labels.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-test-imgs.npz',
            'http://codh.rois.ac.jp/kmnist/dataset/kmnist/kmnist-test-labels.npz',
        ]

        t_str = 'train' if train else 'test'
        imgs_fn = 'kmnist-{}-imgs.npz'.format(t_str)
        labels_fn = 'kmnist-{}-labels.npz'.format(t_str)

        if not os.path.exists(data_dir):
            os.mkdir(os.path.abspath(data_dir))
        if not os.path.exists(os.path.abspath(os.path.join(data_dir, imgs_fn))):
            self.__download(os.path.abspath(data_dir))

        imgs_fn = os.path.abspath(os.path.join(data_dir, imgs_fn))
        labels_fn = os.path.abspath(os.path.join(data_dir, labels_fn))

        self.images = np.load(imgs_fn)['arr_0']
        self.labels = np.load(labels_fn)['arr_0']
        self.n_classes = len(np.unique(self.labels))
        self.class_labels, self.class_frequency = np.unique(self.labels, return_counts=True)
        self.class_frequency = self.class_frequency / np.sum(self.class_frequency)
        self.data_dir = data_dir
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1  # only gray scale
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = np.expand_dims(self.images[idx], axis=-1)
        if self.transform:
            image = self.transform(image)

        label = np.int(self.labels[idx])
        return image, label

    def __download(self, data_dir):
        print('Datadir', data_dir)
        for url in self.__urls:
            fn = os.path.basename(url)
            req = requests.get(url, stream=True)
            print('Downloading {}'.format(fn))
            with open(os.path.join(data_dir, fn), 'wb') as fh:
                for chunck in req.iter_content(chunk_size=1024):
                    if chunck:
                        fh.write(chunck)
            print('done')
        print('All files downloaded')

train_dataset=KMNIST(transform=transforms.ToTensor())
test_dataset=KMNIST(train=False, transform=transforms.ToTensor())

criterion = nn.CrossEntropyLoss()

def prepare_cnn(cfg):
  print(cfg)
  cfg = {k : cfg[k] for k in cfg if cfg[k]}
  print(cfg)
  run_cnn(**cfg)

#!apt-get install build-essential swig

#trace=[[]]
#index=0
f= open("results.txt","w+")
d= open("data_to_plot.txt","w+")

def train(train_loader,test_loader,model,optimizer):
          iter=0
          model.train()
          #print(model)
          for i, (images, labels) in enumerate(train_loader):
              if torch.cuda.is_available():
                  images = Variable(images.cuda())
                  labels = Variable(labels.cuda())

              else:
                  images = Variable(images)
                  labels = Variable(labels)

              optimizer.zero_grad()
              outputs = model(images)
              loss = criterion(outputs, labels)
              loss.backward()
              optimizer.step()
              iter+=1
              if iter % 50 == 0:
                    accuracy=test(test_loader,model)
                    
          
          return loss.item(),accuracy

def test(test_loader,model):
        model.eval()
        correct = 0
        total = 0
        for images, labels in test_loader:              
            if torch.cuda.is_available():
                 images = Variable(images.cuda())
            else:
                 images = Variable(images)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            if torch.cuda.is_available():
                  correct += (predicted.cpu() == labels.cpu()).sum()
            else:
                  correct += (predicted == labels).sum() 
                      
        accuracy = 100 * correct / total   
        return accuracy

def run_cnn(cfg):
    
  print("Running:",cfg)
  
  learning_rate = cfg["lr"]
  
  epochs=15
  
  model = CNNModel()
  
  if torch.cuda.is_available():
      model.cuda()
      
  batch_size=cfg["batch_size"]
  
  optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, 
                             betas=(0.9, 0.999), eps=1e-08, weight_decay=0.0001, amsgrad=False)
  train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, 
                                           shuffle=True)
  test_loader = torch.utils.data.DataLoader(dataset=test_dataset,  batch_size=batch_size,
                                          shuffle=False )
  for epoch in range(epochs):      
          loss,accuracy =  train(train_loader,test_loader,model,optimizer)
          print('Epoch: {}. Loss: {}. Accuracy: {}'.format(epoch, loss, accuracy))
          f.write('Epoch: {}. Loss: {}. Accuracy: {}'.format(epoch, loss, accuracy))
  print("[",learning_rate,batch_size,accuracy,"]")
  print("Loss:",loss)
  output=[lr,batch_size,accuracy]
  d.write("[")
  d.write("%f"%learning_rate)
  d.write("%d"%batch_size)
  d.write("%f"%accuracy)
  d.write("]")
  d.write("\n")
  #trace[index]=output
  #index+=1
  return loss

#!curl https://raw.githubusercontent.com/automl/smac3/master/requirements.txt | xargs -n 1 -L 1 pip install

#!pip install smac

# Import ConfigSpace and different types of parameters
from smac.configspace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter, \
    UniformFloatHyperparameter, UniformIntegerHyperparameter
from ConfigSpace.conditions import InCondition

# Import SMAC-utilities
from smac.tae.execute_func import ExecuteTAFuncDict
from smac.scenario.scenario import Scenario
from smac.facade.smac_facade import SMAC

cs = ConfigurationSpace()

lr = UniformFloatHyperparameter("lr", 0.0001, 0.1, default_value=0.001)
cs.add_hyperparameter(lr)

batch_size = CategoricalHyperparameter("batch_size", [32,64,128, 256], default_value=128)
cs.add_hyperparameter(batch_size)

# Scenario object
scenario = Scenario({"run_obj": "quality",   # we optimize quality (alternatively runtime)
                     "runcount-limit": 200,  # maximum function evaluations
                     "cs": cs,               # configuration space
                     "deterministic": "true",
                     #"abort_on_first_run_crash": "false"
                     })

# Optimize, using a SMAC-object
#print("Optimizing! Depending on your machine, this might take a few minutes.")
smac = SMAC(scenario=scenario, rng=np.random.RandomState(42),
        tae_runner=run_cnn)

print("Searching for incumbent config!")

smac.solver.intensifier.tae_runner.use_pynisher = False

incumbent = smac.optimize()

print("incumbent configuration:")
f.write("incumbent configuration:\n")


inc_value = run_cnn(incumbent)

print("Optimized loss Value: %.2f" % (inc_value))

f.close()
d.close()