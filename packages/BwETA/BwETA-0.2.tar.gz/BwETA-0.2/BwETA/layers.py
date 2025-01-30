#@title Model everything
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, embedding_dim):
        super(PositionalEncoding, self).__init__()
        self.embedding_dim = embedding_dim

    def call(self, inputs):
        sequence_length = tf.shape(inputs)[1]
        embedding_dim = self.embedding_dim

        position = tf.range(sequence_length, dtype=tf.float32)[:, tf.newaxis]  # (seq_len, 1)
        
        # Calculate the number of terms needed to cover all dimensions when interleaved
        num_terms = (embedding_dim + 1) // 2
        
        div_term = tf.exp(
            tf.range(0, num_terms, dtype=tf.float32) * 
            -(tf.math.log(10000.0) / embedding_dim)
        )  # (num_terms,)
        
        # Compute sin and cos values
        sin_values = tf.sin(position * div_term)  # (seq_len, num_terms)
        cos_values = tf.cos(position * div_term)  # (seq_len, num_terms)
        
        # Interleave sin and cos values to form the positional encoding matrix
        pos_enc = tf.stack([sin_values, cos_values], axis=-1)  # (seq_len, num_terms, 2)
        pos_enc = tf.reshape(pos_enc, [sequence_length, 2 * num_terms])  # (seq_len, 2*num_terms)
        
        # Slice to the original embedding dimension in case it's odd
        pos_enc = pos_enc[:, :embedding_dim]
        
        # Expand dimensions to match batch size and add to inputs
        pos_enc = tf.expand_dims(pos_enc, 0)  # (1, seq_len, embedding_dim)
        pos_enc = tf.tile(pos_enc, [tf.shape(inputs)[0], 1, 1])  # (batch_size, seq_len, embedding_dim)
        
        return inputs + pos_enc


class TransformerBlock(layers.Layer):
    def __init__(self, num_heads, attention_dim, ff_dim=512, dropout_rate=0.1,**kwargs):
        super(TransformerBlock, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.attention_dim = attention_dim
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate

        # Multi-Head Attention Layer
        self.attention = layers.MultiHeadAttention(num_heads=num_heads, key_dim=attention_dim,causal=True)

        
        self.ffn1 = layers.Dense(ff_dim, activation=tf.keras.activations.gelu)
        self.ffn2 = layers.Dense(attention_dim)

        # Layer Normalization
        self.norm1 = layers.LayerNormalization()
        self.norm2 = layers.LayerNormalization()

        # Dropout layers
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)


    def call(self, inputs, mask):
        attn_output = self.attention(inputs, inputs, inputs, attention_mask=mask)
        attn_output = self.dropout1(attn_output)
        out1 = self.norm1(inputs + attn_output)  # Add & Norm

        # Apply Feed-Forward Network
        ffn_output = self.ffn1(out1)
        ffn_output = self.ffn2(ffn_output)
        ffn_output = self.dropout2(ffn_output)
        out2 = self.norm2(out1 + ffn_output)  # Add & Norm

        return out2