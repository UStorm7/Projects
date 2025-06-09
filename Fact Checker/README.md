✅ Fact Verification with FLAN-T5-XL

A lightweight fact-checking tool that uses Google's FLAN-T5-XL large language model to determine if a given answer to a question is factually correct or not.

🧠 Objective

Use an LLM to return **YES** if an answer is factually correct for a given question, else return **NO**.

🧪 Model Used

- [`google/flan-t5-xl`](https://huggingface.co/google/flan-t5-xl) via Hugging Face Transformers

🚀 How It Works

1. The script takes in a `question` and an `answer` from the command line.
2. It forms a structured prompt using those inputs.
3. Passes the prompt to the FLAN-T5-XL model.
4. Decodes and cleans the model’s output to extract a binary response: **YES** or **NO**.

🛠️ Requirements

```bash
pip install torch transformers
```

▶️ Usage
```bash
python fact_checker.py "Who discovered gravity?" "Albert Einstein"
```

## Output
NO

⚠️ Notes
- The output is case-sensitive and restricted strictly to YES or NO
- Seed is fixed for reproducibility (torch.manual_seed(42)).
