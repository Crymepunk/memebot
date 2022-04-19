#!/usr/bin/env python3
from alive_progress import alive_bar
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

def compute(length):
    # Encode the input
    input_ids = tokenizer.encode(inp, return_tensors='tf')
    yield
    print("Encoded the Input!")
    # Generate the output
    greedy_output = model.generate(input_ids, max_length=length * 10, temperature=0.7, repetition_penalty=1.2, top_k=0.0, top_p=0.0)
    yield
    print("Generated the Output!")
    # Decode the output into text
    global output
    output = tokenizer.decode(greedy_output[0], skip_special_tokens=True)
    yield
    print("Decoded the Output!")

# Load the model
model = TFGPT2LMHeadModel.from_pretrained("gpt2")
# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Clear the terminal
print("\033[2J")
# Print divide line
print("-" * 50 + " Input " + "-" * 50 + "\n")

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
