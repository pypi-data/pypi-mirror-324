from tqdm import tqdm
import tensorflow as tf
import shutil
import sys
import os

def tokenize(ds_obj,mod_obj,max_length=512,batch_size=8):
    if ds_obj.gpt_sentence == None:
        raise ValueError("Please run dataset_loadqa() and datasetgpt() first before processing.")
    
    def tokenize_func(ds, padding=True, truncation=True, return_tensors='tf', max_length=max_length):

        return mod_obj.tokenizer(ds_obj.gpt_sentence, padding=True, truncation=True, return_tensors='tf', max_length=max_length)
    
    dataset = tf.data.Dataset.from_tensor_slices(ds_obj)
    dataset = dataset.map(tokenize_func, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    ds_obj.tf_dataset = dataset
    ds_obj.type = 3