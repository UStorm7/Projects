# BERT Sentence Similarity Analyzer

This program uses the `bert-base-uncased` model to compute and compare semantic similarity between two input sentences using two vector representations:
- **Max-pooled hidden states**
- **[CLS] token representation via pooler_output**

## Features
- Uses Hugging Face's `transformers` library.
- Handles tokenization, attention masking, and sentence vector extraction.
- Computes cosine similarity for both representations.
- Command-line interface with formatted sentence input.

## Example Usage

```bash
python assignment.py The cat is on the mat , A cat sits on the mat

## Dependencies
   - transformers

   - torch

   - numpy

Install with:
```bash
pip install transformers torch numpy

## Notes
   - The program uses AutoTokenizer and BertModel from Hugging Face.

   - Sentences must be entered with a space-separated comma, like: sentence1 , sentence2