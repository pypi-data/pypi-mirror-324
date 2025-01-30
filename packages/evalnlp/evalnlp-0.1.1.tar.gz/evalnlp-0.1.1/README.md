# evalNLP

**evalNLP** is a Python library offering advanced metrics for evaluating Automatic Speech Recognition (ASR) and translation models. This library is designed to meet the needs of researchers and developers working on Natural Language Processing tasks.

## Features

- **UWER**: Universal Word Error Rate, an enhanced metric for fair transcription evaluation, adapted to morphologically rich and low-resource languages.
It uses a revised version of the Levenshtein algorithm with weighted substitutions through a `cost_func` and segmentation operations with a `u_cost`.
 **For more details, see the paper:** [Universal-WER: Enhancing WER with Segmentation and Weighted Substitution for Varied Linguistic Contexts](https://aclanthology.org/2024.iwclul-1.3/).

- **UTER**: (Coming Soon) Universal Translation Error Rate, a robust metric for translation evaluation. It provides scores that closely align with human Direct Assessment (DA) evaluations, even for low-resource languages.


## Installation

Install evalNLP using pip: 

```bash
pip install evalnlp
```


## Usage

The `uwer` function is defined as:

```python
def uwer(ref: str, hyp: str, cost_func=None, u_cost=None):
```


By default:
- The substitution cost function (`cost_func`) uses the **Sorensen-Dice** similarity measure.
- You can also use an average-based function that combines **CER**, **similarity_rate_lcs**, **jaccard_coefficient_lcs**, **fuzzy_ratio**, and **Sorensen-Dice** by passing `"moyenne"` as the `cost_func` parameter.
- The union cost (`u_cost`) is defined as described in the paper.



The `uwer` function works with both **single strings** and **lists of strings**.


### Example with single strings:

```python
from evalnlp import uwer

reference = "This is a reference"
hypothesis = "This is a hypothesis"
score = uwer(reference, hypothesis)
print(f"UWER Score: {score}")
```

### Example with lists:

```python
from evalnlp import uwer

references = ["This is a reference", "Another reference"]
hypotheses = ["This is a hypothesis", "Another hypothesis"]
scores = uwer(references, hypotheses)
print(f"UWER Scores: {scores}")
```
