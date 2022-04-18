#!/usr/bin/env python3
from time import sleep
from alive_progress import alive_bar
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import tensorflow as tf

def compute(length):
    # Generate the output
    global greedy_output
    greedy_output = model.generate(input_ids, max_length=length * 10, temperature=0.7, repetition_penalty=1.2, top_k=0.0, top_p=0.0)
    yield

# Load the model
model = TFGPT2LMHeadModel.from_pretrained("gpt2")
# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Clear the terminal
print("\033[2J")
print("-" * 100)

# Input for the model
inp = input("Enter a sentence: ")
# Max length of the input
max_length = input("Max length of the input (Enter for default): ")
while True:
    if max_length == "":
        max_length = len(inp) * 10
    else:
        try:
            max_length = int(max_length)
            break
        except:
            print("Invalid input")
            continue
# Tokenize the input
input_ids = tokenizer.encode(inp, return_tensors='tf')
# Create Progress Bar
with alive_bar(1) as bar:
    for i in compute(max_length):
        bar()

print("-" * 100)
print(tokenizer.decode(greedy_output[0], skip_special_tokens=True))
