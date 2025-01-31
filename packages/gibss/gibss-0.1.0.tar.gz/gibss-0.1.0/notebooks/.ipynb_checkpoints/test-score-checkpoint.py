# %% [markdown]
# ### Score based Bayes factor
#
# We are exploring the idea of using a score based approximation to the Bayes factor as a quick pre-screening when fitting logistic SuSiE via GIBSS. The idea is that a large fraction of variables are going to have posterior inclusion probabilities close to $0$. These variables will not contribute meaningfully to the outputs of the SER, and we can save substantially on computation by skipping them.
#
# The challenge is identifying a pre-screening step for variables. 
# Here we propose approximating the Bayes factor using a score based approximation.
# The can be computed cheapy compare to the more accurate Laplace approximation, because it does not involve optimization of each model, only a single gradient and hessian evaluation for each variable.

# %%
import numpy as np
import matplotlib.pyplot as plt

# simulate correlated X
A = np.exp(- 0.1 * (np.arange(100)[None] - np.arange(100)[:, None])**2)
X = A @ np.random.normal(size=(100, 1000))
plt.plot(np.corrcoef(X)[0])

# %%
from gibss.logisticprofile import fit_null, compute_lbf_score, logistic_ser_hermite

from gibss.logisticprofile import nloglik
import jax

causal = [10, 30, 50, 70]
b = np.ones(4) * 1
psi = -1 * b @ X[causal,]
y = np.random.binomial(1, 1/(1 + np.exp(-psi)))

nullfit = fit_null(y, 0.)
compute_lbf_score(x, y, 0., nullfit, 1.)
vcompute_lbf_score = jax.jit(jax.vmap(compute_lbf_score, (0, None, None, None, None)))
lbf_score = vcompute_lbf_score(X, y, 0., nullfit, 1.)

serfit = logistic_ser_hermite(np.zeros((100, 2)), X, y, 0., 1., 1)
plt.scatter(serfit.fits.lbf, lbf_score, c=np.isin(np.arange(100), causal))

# %% [markdown]
# I suspect that we could safely screen out variables where the score based Bayes factor approximation is $<1$. 

# %%
np.unique(np.stack([(serfit.fits.lbf < 0), (lbf_score < 0)]).T, axis=0, return_counts=True)


# %%
(fit.components[5].fits.lbf < 0).mean()

# %%
from gibss.logisticprofile import logistic_susie
from gibss.credible_sets import compute_cs

fit = logistic_susie(X, y, L=10, method='hermite', serkwargs=dict(prior_variance=1, m=1))

# %%
compute_cs(fit.components[0].alpha)

# %%
alpha = np.array(fit.components[0].alpha)
compute_cs(alpha)

# %%
from scipy.special import logsumexp
x = np.array([0., 2.5, 2.5])
np.exp(x - logsumexp(x))
