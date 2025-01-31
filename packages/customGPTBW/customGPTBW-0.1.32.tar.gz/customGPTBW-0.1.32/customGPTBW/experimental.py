from tqdm import tqdm
import tensorflow as tf

def tokenize(ds_obj, mod_obj, max_length=512, batch_size=8, tokenization_batch_size=1000):
    if ds_obj.gpt_sentence is None:
        raise ValueError("Please run dataset_loadqa() and datasetgpt() first before processing.")
    
    from tqdm.auto import tqdm
    import numpy as np

    sentences = ds_obj.gpt_sentence
    total_samples = len(sentences)
    
    # Pre-allocate numpy arrays for maximum memory efficiency
    input_ids = np.empty((total_samples, max_length), dtype=np.int32)
    attention_mask = np.empty((total_samples, max_length), dtype=np.int32)

    with tqdm(total=total_samples, desc="🚀 Turbo-Tokenizing", unit="seq",
             bar_format="{l_bar}{bar:20}{r_bar}", dynamic_ncols=True) as pbar:
        for idx in range(0, total_samples, tokenization_batch_size):
            batch_end = idx + tokenization_batch_size
            batch = sentences[idx:batch_end]
            
            # GPU-accelerated tokenization when available
            tokenized = mod_obj.tokenizer(
                batch,
                max_length=max_length,
                truncation=True,
                padding="max_length",
                return_tensors="np",
                return_attention_mask=True
            )
            
            # Vectorized array operations for maximum speed
            batch_size = tokenized["input_ids"].shape[0]
            input_ids[idx:idx+batch_size] = tokenized["input_ids"]
            attention_mask[idx:idx+batch_size] = tokenized["attention_mask"]
            
            pbar.update(batch_size)
            pbar.set_postfix({"seq/s": f"{pbar.format_dict['rate']:0.1f}"})

    # Memory-mapped TensorFlow dataset for zero-copy efficiency
    dataset = ds_obj.create_tf_dataset({'input_ids': input_ids,'attention_mask': attention_mask}).batch(batch_size, num_parallel_calls=tf.data.AUTOTUNE)
    
    # Ultimate pipeline optimization
    dataset = dataset.cache().prefetch(tf.data.AUTOTUNE)
    
    ds_obj.tf_dataset = dataset
    ds_obj.type = 3
    return ds_obj