import torch
import torchvision
import torch.nn as nn

import sys
import os
import argparse

from src.utils import *
from src.data_handler import FaceLoader
from src.trainer import FaceTrainer

def parse_arguments(argv):

    parser = argparse.ArgumentParser()

    # set up root for training dataset
    parser.add_argument('--train_root', type=str, default=None)

    # set up root for training dataset (masked)
    # if you wnat to training with mask image, use this
    parser.add_argument('--epochs', type=int, default=None)
    parser.add_argument('--batch_size', type=int, default=None)
    parser.add_argument('--embedding_size', type=int, default=512)

    # set up root for saving model, log
    parser.add_argument('--save_root', type=str, default=None)

    # set up training model backbone
    # TODO: add more backbone network.
    parser.add_argument('--magnitude', type=str, default='ball', choices=['ball', 'linear', 'seg'])
    
    # set up training model head
    # TODO: add more network head
    parser.add_argument('--angular', type=str, default='cos', choices=['cos, sqcos'])
    
    parser.add_argument('--gpu_idx', type=str, default=0)

    return parser.parse_args(argv)

def main(args):
    
    # check cuda availablity
    os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu_idx
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # make save directory
    model_dir = args.save_root + '/model'
    make_dir(model_dir) 

    log_dir = args.save_root + '/log'
    make_dir(log_dir)
    
    data_loader = FaceLoader(args.train_root, args.batch_size)
    
    trainer = FaceTrainer(device, data_loader, args.magnitude, args.angular, log_dir, model_dir, args.batch_size, args.embedding_size)

    # train using trainer
    trainer.train(args.epochs)


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    main(args)
