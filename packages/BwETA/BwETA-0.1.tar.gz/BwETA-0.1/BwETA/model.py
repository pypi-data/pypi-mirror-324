import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from layers import *

class TransformerModel(tf.keras.Model):
    def __init__(self, num_heads=8, attention_dim=512, vocab_size=5027,num_blocks=24, ff_dim=4096, dropout_rate=0.2,**kwargs):
        super(TransformerModel, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.attention_dim = attention_dim
        self.vocab_size = vocab_size
        self.num_blocks = num_blocks
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=attention_dim)
        self.positional_encoding = PositionalEncoding(attention_dim)
        self.blocks = [TransformerBlock(num_heads, attention_dim, ff_dim, dropout_rate) for _ in range(num_blocks)]
        self.final_layer = layers.Dense(vocab_size)  # Output layer for classification (adjust output size accordingly)

    def call(self, inputs,attention_mask = None,labels = None):
        class CustomModelOutput():
            def __init__(self,loss,logits):
                self.loss = loss
                self.logits = logits

        # All the input data checking is being done here---
        try:
            mask = inputs["attention_mask"]  # If needed for masking
            input = inputs["input_ids"]
        except Exception:
            input = inputs
            if attention_mask == None:
                if len(input.shape) == 2:
                    input_len = input.shape[1]
                    batch_size = input.shape[0]
                elif len(input.shape) == 1:
                    input_len = input.shape[0]
                    batch_size = 1
                mask = tf.ones((batch_size,input_len))
            else:
                mask = attention_mask

        #Here everything is getting casted---
        mask = tf.cast(mask, tf.int32)
        input = tf.cast(input, tf.int32)

        # This is the place for the layer and blocks to run--
        x = self.embedding(input)
        x = x + self.positional_encoding(x)
        # Only pass the mask to blocks if it's not None
        for block in self.blocks:
            x = block(x, mask=mask)  # Pass through each transformer block
        logits =  self.final_layer(x)

        if labels == None:
            return CustomModelOutput(None,logits)
        else:
            labels = labels[:, 1:]
            return CustomModelOutput(float(self.loss_fn(labels,logits[:, :-1, :])),logits)

    def generate(self, input, max_len, mask=None):
        try:
            input = input["input_ids"]
            input = tf.constant(input, dtype=tf.int32)
        except:
            input = tf.constant(input, dtype=tf.int32)
        for _ in range(max_len):
            output = self(input, mask)
            probs = tf.nn.softmax(output.logits, axis=-1)
            predicted_id = tf.argmax(probs[:, -1, :], axis=-1).numpy().flatten()

            # Reshape predicted_id to match the batch size for concatenation
            predicted_id = tf.expand_dims(predicted_id, axis=1)  # Shape: (batch_size, 1)
            predicted_id = tf.cast(predicted_id,dtype=tf.int32)
            # Concatenate along the sequence length axis (axis=1)
            input = tf.concat([input, predicted_id], axis=1)

        return input.numpy().flatten()

    def save_pretrained(self,path):
            self.save(f'{path}/tf_model.h5')
            with open(f'{path}/model_config.json', 'w') as f:
                f.write(self.to_json())

    def build_custom(self):
        input_ids = tf.random.uniform([1, 2], maxval=50257, dtype=tf.int32)
        attention_mask = tf.ones([1, 2], dtype=tf.int32)
        input_data = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
        self(input_data,labels=input_data['input_ids'])

    def get_config(self):
        config = super(TransformerModel, self).get_config()
        config.update({
            "num_heads": self.num_heads,
            "attention_dim": self.attention_dim,
            "vocab_size": self.vocab_size,
            "num_blocks": self.num_blocks,
            "ff_dim": self.ff_dim,
            "dropout_rate": self.dropout_rate
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)