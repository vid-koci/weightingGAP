# The Gap on Gap: Tackling the Problem of Differing Data Distributions in Bias-Measuring Datasets
Code and data for the paper "The Gap on Gap: Tackling the Problem of Differing Data Distributions in Bias-Measuring Datasets"
Work has been accepted to AAAI 2021 conference and AFCI workshop at NeurIPS 2020 and can be found on [ArXiv](https://arxiv.org/abs/2011.01837).
For the full GAP dataset, please refer to the [original repository](https://github.com/google-research-datasets/gap-coreference).
Here, we follow their formatting and evaluation setup.

## Motivation
[Webster et al. 2018](https://arxiv.org/abs/1810.05201) observe that certain unbiased baselines obtain GAP bias scores significantly different from 1.0, the unbiased score. We identify the patterns within the dataset that cause this and propose an alternative weighted Wt-Bias metric that alleviates this data imbalance that might affect evaluated models. For details, please refer to our [paper](https://arxiv.org/abs/2011.01837).

## How to use

To evaluate your GAP outputs with Wt-bias metric, use the following command:    
```python gap_scorer.py --gold_tsv gap-test.tsv --system_tsv [your output file] --weights linear_weights_trimmed.json```     
```linear_weights_trimmed.json``` can be replaced with ```linear_weights.json``` to evaluate on W-bias instead.
Evaluation file was written in Python 3.

Annotations of all name spans in the test set can be found in json file ```gap-test-name-spans.json```
To re-compute the weights, please refer to the script ```compute_weights.sh``` which contains comments on all the necessary steps.
To re-compute the weights, Python 3 and Matlab with its Linprog package are required. Matlab version R2019b was used in our work.

## How to Cite

```
@inproceedings{kocijan21aaai,
    title     = {The Gap on Gap: Tackling the Problem of Differing Data Distributions in Bias-Measuring Datasets},
    author    = {Vid Kocijan and
               Oana-Maria Camburu and
               Thomas Lukasiewicz},
    booktitle = {{Proceedings of the 35th AAAI}},
    month = {February},
    year = {2021}
}
'''
