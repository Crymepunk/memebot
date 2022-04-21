#!/usr/bin/env python3
from alive_progress import alive_bar
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import pyttsx3
import argparse

parse = argparse.ArgumentParser()

parse.add_argument("--maxlength", "-m", help="max length of the output", type=int, default=0)
parse.add_argument("--tts", "-t", help="enable tts", action="store_true")
parse.add_argument("--input", "-i", type=str, help="input for the memebot")

ARG = parse.parse_args()


def compute(length):
    # Encode the input
    input_ids = tokenizer.encode(inp, return_tensors='tf')
    yield
    print("Encoded the input")
    # Generate the output
    greedy_output = model.generate(input_ids, max_length=length * 10, temperature=0.7, repetition_penalty=1.2, top_k=0.0, top_p=0.0)
    yield
    print("Generated the output")
    # Decode the output into text
    global output
    output = tokenizer.decode(greedy_output[0], skip_special_tokens=True)
    yield
    print("Decoded the output")

# Load the model
model = TFGPT2LMHeadModel.from_pretrained("gpt2")
# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# Load the TTS engine
engine = pyttsx3.init()

# Clear the terminal
print("\033[2J")
# Print divide line
if ARG.input == None:
    print("-" * 50 + " Input " + "-" * 50 + "\n")

# Input for the model
if ARG.input:
    # If input argument is given
    inp = ARG.input
else:
    # If input argument is not given
    inp = input("Enter a sentence: ")
    # Max length of the input
if ARG.maxlength != 0:
    # If max tokens argument is given
    max_length = ARG.maxlength
else:
    # If max tokens argument is not given
    if ARG.input:
        # If input argument is given
        max_length = ""
    else:
        # If input argument is not given
        max_length = input("Max length of the input (Enter for default): ")
if ARG.tts:
    # If tts argument is given
    tts = True
else:
    # If tts argument is not given
    if ARG.input:
        # If input argument is given
        tts = False
    else:
        # If input argument is not given
        tts = input("Enable TTS? (y/N): ")
        if tts.lower() == "y" or tts.lower() == "yes":
            tts = True
        else:
            tts = False

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

# Print divide line
print("\n" + "-" * 48 + " Generating " + "-" * 48 + "\n")
# Create Progress Bar
with alive_bar(3, title="Working...", stats=False) as bar:
    for i in compute(max_length):   
        bar()

# Print divide line
print("\n" + "-" * 50 + " Output " + "-" * 50 + "\n")
# Print the output
print(output)
# Print divide line
print("\n" + "-" * 108)
if tts == True:
    engine.say(output)
    engine.runAndWait()
    engine.stop()
