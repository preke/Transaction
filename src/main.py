# coding = utf-8
import pandas as pd
import numpy as np
import torch
import argparse
import os
import datetime
import traceback
import model



# CONFIG
DATA_PATH = '../Dyadic_PELD.tsv'

parser = argparse.ArgumentParser(description='')
args = parser.parse_args()

args.device        = 1
args.base          = 'BERT'

args.MAX_LEN       = 128 
args.batch_size    = 16
args.lr            = 5e-6
args.adam_epsilon  = 1e-8
args.epochs        = 50


seed_list = [42]#, 42, 123, 234, 345, 456, 567]
for seed in  seed_list:
    args.SEED          = seed
    args.result_name   = 'test_' + str(args.SEED) + '.csv'

    np.random.seed(args.SEED)
    torch.manual_seed(args.SEED)
    torch.cuda.manual_seed_all(args.SEED)

    ## LOAD DATA
    from dataload import load_data
    train_length, train_dataloader, valid_dataloader, test_dataloader = load_data(args, DATA_PATH)
    args.train_length = train_length

    ## TRAIN THE MODEL
    from model import Emo_Generation
    from train import train_model


    if args.base == 'RoBERTa':
        model = Emo_Generation.from_pretrained('roberta-base').cuda(args.device)
    else:
        model = Emo_Generation.from_pretrained('bert-base-uncased').cuda(args.device)
        
        
    train_model(model, args, train_dataloader, valid_dataloader, test_dataloader)







