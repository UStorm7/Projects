import sys
import torch
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

transformers.logging.set_verbosity_error()
transformers.utils.logging.disable_progress_bar()

def clean_decoded_output(decoded_output):
    cleaned = decoded_output.strip().upper()
    cleaned = re.findall(r'\bYES\b|\bNO\b', cleaned)
    return cleaned[0] if cleaned else "NO"

def llm_function(model,tokenizer,a,b):

    # 1. Properly formulating the prompt
    prompt = (
    "Task: You are a fact-checking assistant. "
    "Given a question and an answer, output only YES if the answer is factually correct, otherwise NO. "
    "Answer strictly based on facts.\n"
    f"Question: {a}\nAnswer: {b}\nOutput:"
)

    # 2. Tokenizing the prompt
    inputs = tokenizer(prompt, return_tensors="pt")

    # 3. Passing to model
    outputs = model.generate(**inputs)

    # 4. Decoding
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 5. Cleaning output
    cleaned_output = clean_decoded_output(decoded)
    return cleaned_output


if __name__ == '__main__':
    input_data_one = sys.argv[1].strip()
    input_data_two = sys.argv[2].strip()

    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl")
    
    a = input_data_one
    b = input_data_two
    
    torch.manual_seed(42)
    out = llm_function(model,tokenizer,a,b)
    print(out.strip())
