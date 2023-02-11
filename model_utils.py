import scipy.stats
import matplotlib.pyplot as plt
import numpy as np


def get_probs(pulls):
    pulls_pities = np.array(
        pulls[
            (pulls["rarity"] == 5)
            & (pulls["guaranteed"] == "f")
            & (pulls["type"] == "character")
        ]["pity"]
    )
    freqs = plt.hist(pulls_pities, bins=89)[0]
    probs = freqs / sum(freqs)

    return probs


def fit_mixture(probs, gaussian_mean, gaussian_var, cutoff):

    p = 0.009
    a = p / probs[0]
    print(a)
    a = 0.50
    output = []

    norm_fitted = scipy.stats.norm(gaussian_mean, gaussian_var)
    norm_discrete_sum = sum([norm_fitted.pdf(i) for i in range(cutoff, 89)])
    geom_discrete_sum = sum([((1 - p) ** i) * p for i in range(0, cutoff)])
    geom_scale = 1 / geom_discrete_sum

    print("gauss sum:", norm_discrete_sum)
    print("geom sum:", geom_discrete_sum)

    for i in range(89):
        if i < cutoff:
            output.append(a * geom_scale * ((1 - p) ** i) * p)
        else:
            output.append((1 - a) * norm_fitted.pdf(i))

    return output
