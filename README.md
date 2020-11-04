# The Gap on Gap: Tackling the Problem of Differing Data Distributions in Bias-Measuring Datasets
Code and data for the paper "The Gap on Gap: Tackling the Problem of Differing Data Distributions in Bias-Measuring Datasets"
Work has been accepted to AFCI workshop at NeurIPS 2020 and can be found on [ArXiv](https://arxiv.org/abs/2011.01837).
For the full GAP dataset, please refer to the [original repository](https://github.com/google-research-datasets/gap-coreference).
Here, we follow their formatting and evaluation setup.

To evaluate your GAP outputs with Wt-bias metric, use the following command:    
```python gap_scorer.py --gold_tsv gap-test.tsv --system_tsv [your output file] --weights linear_weights_trimmed.json```     
```linear_weights_trimmed.json``` can be replaced with ```linear_weights.json``` to evaluate on W-bias instead.
Evaluation file was written in Python 3.

Annotations of all name spans in the test set can be found in json file ```gap-test-name-spans.json```
To re-compute the weights, please refer to the script ```compute_weights.sh``` which contains comments on all the necessary steps.
To re-compute the weights, Python 3 and Matlab with its Linprog package are required. Matlab version R2019b was used in our work.
