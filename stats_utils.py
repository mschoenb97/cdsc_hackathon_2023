""" Goodness of fit utilities """

import numpy as np


def get_null_pdf(*, prob, pity_cutoff):
    """res[i] = probability you get desired draw on ith try, where desired draw has probability p.
    We also assume that we have a guaranteed success after `pity_cutoff` trials
    """

    res = [0] * (pity_cutoff + 2)
    total_prob = 0
    current_prob = prob

    for i in range(1, pity_cutoff + 1):
        res[i] = current_prob
        total_prob += current_prob
        current_prob *= 1 - prob

    res[pity_cutoff + 1] = 1 - total_prob

    return np.array(res)


def data_for_metric(data, *, prob, pity_cutoff):

    null_pdf = get_null_pdf(prob=prob, pity_cutoff=pity_cutoff)
    expected_counts = null_pdf * len(data)

    true_counts_dict = data["pity"].value_counts().to_dict()
    true_counts = []

    for i in range(len(expected_counts)):
        true_counts.append(true_counts_dict.get(i, 0))

    return np.array(true_counts), np.array(expected_counts)


def null_metric(data, *, prob, pity_cutoff):

    true_counts, expected_counts = data_for_metric(
        data, prob=prob, pity_cutoff=pity_cutoff
    )

    total = true_counts.sum()

    abs_difference = np.absolute(true_counts - expected_counts).sum()
    abs_difference /= total

    return abs_difference
