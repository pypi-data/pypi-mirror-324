# %% [markdown]
# # Ser with score based screening step
#
# When fitting GIBSS, a lot of computational effort is spent fitting models that contribute very little to the final output.
# Here we explore screening variables with a score based approximation of the Bayes factor, and only following up with plausible candidates.

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


# %% [markdown]
# Here is how we implement the score based Bayes factor in `gibss.logisticprofile`.
# `logisticprofile` maximizes over the intercept. 
#
# When we compute the standard deviation for $\hat b$ we compute $\sqrt{H^{-1}_{11}}$. 
#
# This comes from the asymptotic distribution of the MLE $\hat b \sim N(b, H^{-1})$, and marginalizing over the estimated intercept.
#
#
# The score based Bayes factor is
#
# \\[
# \begin{aligned}
# \frac{\int e^{\log p(y, b | x)} db}{p(y, b=0| x)}
# = \int \exp \left\{g b - \frac{1}{2} \tau b^2 \right\}db = \sqrt\frac{2\pi}{\tau} e^{g^2/2\tau}
# \end{aligned}
# \\]
# Where we write $g = \frac{d}{db} \log p(y, b | x)$ and $\tau = - \frac{d^2}{db^2} \log p(y, b | x)$ 

# %%
def compute_lbf_score(x, y, offset, nullfit, prior_variance):
    # evaluate the gradient and the hessian at the null
    b = jnp.array([nullfit.beta, 0.])
    grad = jax.grad(nloglik)(b, x, y, 0., prior_variance)    
    hess = jax.hessian(nloglik)(b, x, y, 0., prior_variance)

    # approximate the log BF with a quadratic approximation of log p(y, b) about b=0
    tau = jnp.linalg.det(hess) / hess[0, 0]  # 1 / H^{-1}_{11}
    lbf = 0.5 * jnp.log(2 * jnp.pi) -0.5 * jnp.log(tau) + 0.5 * grad[1]**2 / tau
    return lbf    


# %%
from gibss.logisticprofile import fit_null, compute_lbf_score, logistic_ser_hermite
from gibss.logisticprofile import nloglik
import jax

causal = [10, 30, 50, 70]
b = np.ones(4) * 1
psi = -1 * b @ X[causal,]
y = np.random.binomial(1, 1/(1 + np.exp(-psi)))

nullfit = fit_null(y, 0.)
compute_lbf_score(X[0], y, 0., nullfit, 1.)
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

# %% [markdown]
# ### Incorporate into SER procedure

# %%
from gibss.logisticprofile import initialize_coef, logistic_ser_hermite
from jax.tree_util import Partial
import jax.numpy as jnp
import numpy as np

serkwargs = dict(m=1, prior_variance=1.)
initfun = lambda X, y, psi: jnp.zeros((X.shape[0], 2))
serfun = Partial(logistic_ser_hermite, **serkwargs)

# %%
import numpy as np

def sim(n, p):
    X = np.random.normal(size=(p, n))
    logit = -1 + X[0] + X[10]
    y = np.random.binomial(1, 1/(1 + np.exp(-logit)))
    return X, y

# X, y = sim(1000, 1000)


# %%
vcompute_lbf_score = jax.jit(jax.vmap(compute_lbf_score, (0, None, None, None, None)))
lbf_score = vcompute_lbf_score(X, y, 0., nullfit, 1.)

# %%
big_lbf = lbf_score > jnp.log(lbf_score.size)
size = int(2**jnp.ceil(jnp.log2(big_lbf.sum()))) # power of 2
idx = jnp.argpartition(-lbf_score, 64)[:32]

# %%
fitsub = serfun(np.zeros((idx.size, 2)), X[idx], y.astype(float), 0.)
fit = serfun(np.zeros((X.shape[0], 2)), X, y.astype(float), 0.)

# %%
fit.fits.lbf[idx] - fitsub.fits.lbf

# %%
(fit.psi - fitsub.psi).max()

# %%
fit.alpha[idx].max()

# %%
plt.scatter(fit.alpha[idx], fitsub.alpha)

# %%
plt.scatter(np.arange(1000), fit.psi-fitsub.psi)

# %%
