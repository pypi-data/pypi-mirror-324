# # Conditional normal means problem
#
# \\[
# \begin{aligned}
# \hat \beta | s, \theta &\sim N(\theta, s^2) \\
# \theta &\sim (1 - \pi_1)({\bf x}) \delta_0 + \pi_1 ({\bf x}) G(\cdot)
# \end{aligned}
# \\]
#
# We'll optimize in an iterative manner. Let $Z$ be a latent random variable where $\theta | Z=1 \sim G(\cdot)$.
# We will perform EM style updates where in the E step we compute the posterior assignments $p(Z=1 | y, {\bf x}0$,
# and in the $M$ step we will estimate the function $\pi_1({\bf x})$ using logistic SuSiE.

# We'll simulate under a simple example to start. Where $G = \delta_1$ so that $\theta = 1$ with probability $\pi_1({\bf x})$.
# In the situation where $G$ EM for the mixture model is simple. We can precompute the conditional likelihood $\ell_k = p(y| X, Z=k)$. 
# The E step corresponds to taking $\gamma_k = q(z =k) \propto  \exp (\ell_k) \pi_k$.
#
# The $M$ step, in the usual mixture model, is simply to take the mixture weights $\pi_k \propto \sum_i \gamma_{ik}$.
# However, we introduce dependence of the mixture weights on the covariates ${\bf x}$. We use logistic SuSiE to estimate $\pi_1({\bf x})$. In particular we use the (approximate) posterior mean of the log-odds as a point estimate.

# +
import numpy as np
from scipy.stats import norm
from scipy.special import logsumexp

n, p = 100000, 100
X = np.random.normal(size=(p, n))
logit = X[0] * 0 - 3
y = np.random.binomial(1, p=1/(1 + np.exp(-logit)))
beta = np.random.normal(size=n) + y
    

# +
# conditional likelihoods
L = np.array([
    norm.logpdf(beta, 0., 1.),
    norm.logpdf(beta, 1., 1.)])

# initialize pi
pi_init = np.ones(2) * 0.5
pi = pi_init
pi1 = []
for _ in range(1000):
    A = L + np.log(pi)[:, None]
    Gamma = np.exp(A - logsumexp(A, 0))  # E-step
    pi = Gamma.mean(1)  # m-step
    pi1.append(pi[1])
# -

import matplotlib.pyplot as plt
plt.plot(np.arange(1000), np.log(pi1) - np.log(1 - np.array(pi1)))
plt.xlabel("iteration")
plt.ylabel("log-odds")


# As a second example lets look at when $G$ is a normal mixture

# +
def categorical_kl(pi1, pi2):
    return np.sum(np.log(pi1/pi2, where=(pi1!= 0)) * pi1)

def categorical_kl_sym(pi1, pi2):
    return categorical_kl(pi1, pi2) + categorical_kl(pi2, pi1)

Estep = lambda Gamma: np.exp(Gamma - logsumexp(Gamma, 1)[:, None])

def em_mixture(beta, s2, sigma_grid, pi_init=None, maxiter=1000):
    L = norm.logpdf(beta[:, None], scale = np.sqrt(sigma_grid**2 + s2)[None])
    if pi_init is None:
        pi_init = np.ones(len(sigma_grid))/len(sigma_grid)
    pi = pi_init
    for _ in range(maxiter):
        pi_old = pi
        Gamma = Estep(L + np.log(pi)[None])
        pi = Gamma.mean(0)
        kl = categorical_kl_sym(pi_old, pi)
        if kl < 1e-10:
            break
    ell = logsumexp(L + np.log(pi)[None], 1)
    return pi, ell


# +
from scipy.stats import poisson

# real mixture weights are Poisson pmf
normalize = lambda x: x/x.sum()
pitrue = normalize(poisson.pmf(np.arange(10), mu=1))
#pitrue = np.ones(10)/10
#pitrue = normalize(np.arange(10))

n = 100000
sigma_grid = np.cumprod(np.ones(10) * np.sqrt(2))
s2 = 1
z = np.random.choice(np.arange(10), size=n, p=pitrue, replace=True)
beta = np.random.normal(size=n, scale=np.sqrt(sigma_grid[z]**2 + s2))
# -

pihat, ellhat = em_mixture(beta, 1., sigma_grid)
plt.plot(np.arange(10), pitrue)
plt.plot(np.arange(10), pihat)

# Now let's replace the M step with a logistic SuSiE fit

# +
from scipy import sparse

n, p = 10000, 100
X = np.random.binomial(1, p=0.1, size=(p, n))
X_sp = sparse.csr_matrix(X)
logit = 3 * X[:3].sum(0) - 2
z = np.random.binomial(1, p=1/(1+np.exp(-logit)))
betahat = np.random.normal(size=n) + z

# + active=""
# from gibss.logistic_sparse import fit_logistic_susie
# from scipy import sparse
# from tqdm import tqdm
#
# L = np.array([
#     norm.logpdf(betahat, 0., 1.),
#     norm.logpdf(betahat, 1., 1.)]).T
#
# # initialize pi
# pi_init = np.ones(2) * 0.5
# pi = pi_init
# pi1 = []
# for _ in range(10):
#     Gamma = Estep(L + np.log(pi))
#     y = Gamma[:, 1]
#     X_sp = sparse.csr_matrix(X)
#     fit = fit_logistic_susie(X_sp, y, L=10)
#     logit = fit.fixed_effect.psi + fit.sers.psi.sum(0)
#     pi1 = 1/(1 + np.exp(-logit))
#     pi = np.array([1-pi1, pi1]).T
#     #pi = Gamma.mean(1)  # m-step
#     #pi1.append(pi[1])

# +
from gibss.additive import fit_additive_model, update_additive_model
from gibss.logistic_sparse import make_fixed_fitfun, make_sparse_logistic_ser1d
from jax.tree_util import Partial
from tqdm import tqdm

prior_variance=1.0
alpha = 0.8
gamma = 0.0
L=5

base_fitfun = make_sparse_logistic_ser1d(X_sp, prior_variance, alpha, gamma)
base_fixedfitfun = make_fixed_fitfun()
# attach y to base fit funs on the fly
def fitfuns(y, L=10):
    return [Partial(base_fixedfitfun, y=y)] + [Partial(base_fitfun, y=y) for _ in range(L)]

# precompute conditional log-likelihoods
L = np.array([
    norm.logpdf(betahat, 0., 1.),
    norm.logpdf(betahat, 1., 1.)]).T

# initialize with hard assignments
y = (betahat/s2 > 2).astype(float)
model = fit_additive_model(fitfuns(y))
pi1 = 1/(1 + np.exp(-model.psi))
pi = np.array([1-pi1, pi1]).T

for _ in tqdm(range(100)):
    Gamma = Estep(L + np.log(pi))
    y = Gamma[:, 1] # get new data
    model.fit_functions = fitfuns(y)
    model = update_additive_model(model, maxiter=5)
    pi1 = 1/(1 + np.exp(-model.psi))
    pi = np.array([1-pi1, pi1]).T

# +
from gibss.logistic import SusieFit
from gibss.utils import tree_stack

fixed_effect = model.components[0]
sers = tree_stack(model.components[1:])
fit = SusieFit(fixed_effect, sers, model.state)
# -

fit.sers.fit.alpha.argmax(1), fit.sers.fit.lbf_ser, fit.s

fit.fixed_effect.fit.x, fit.sers.fit.b

fit.sers.fit.b[np.arange(10), fit.sers.fit.alpha.argmax(1)]

plt.scatter((z > 0).astype(float), pi1)

y = (betahat/s2 > 2).astype(float)
hard_threshold_model = fit_additive_model(fitfuns(y))
fixed_effect = model.components[0]
sers = tree_stack(model.components[1:])
hard_threshold_fit = SusieFit(fixed_effect, sers, model.state)

hard_threshold_fit.sers.fit.alpha.argmax(1)

hard_threshold_fit.sers.fit.b[np.arange(10), hard_threshold_fit.sers.fit.alpha.argmax(1)]

fit.sers.fit.alpha.argmax(1)
fit.sers.fit.lbf[:, :3]

    Gamma = Estep(L + np.log(pi))
    y = Gamma[:, 1]
    logit = fit.fixed_effect.psi + fit.sers.psi.sum(0)
    pi1 = 1/(1 + np.exp(-logit))
    pi = np.array([1-pi1, pi]).T

X_sp.shape

from gibss.logistic_sparse import fit_logistic_susie
from scipy import sparse
X_sp = sparse.csr_matrix(X)
fit = fit_logistic_susie(X_sp, y, L=10)

logit = fit.fixed_effect.psi + fit.sers.psi.sum(0)
pi1 = 1/(1 + np.exp(-logit))

# ?fit_logistic_susie


