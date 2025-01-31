# ### Logistic 1d
#
# Here we plan to have each SER contribute only the single effect, and not update the intercept.
# Each univariate regression only needs to solve a 1d optimization problem.
#
# Operationally, this is helpful because we don't need to worry about how the prior on the intercep, or inclusion of other covariates should influence the computation of the Bayes factor in each SER. Perhaps this should not concern us too much. We are already neglecting the uncertainty of the other predictions by only providing point estimates.
#
# On the other hand, it may be easier to imagine how to develop a method for estimating the effecs and Bayes factors in the presence of uncertainty for the simple 1d model.
#
# In order to include the intercept and other covariates in the additive model, we simply need to introduce a component to the additive model that does this fitting. 

# +
from typing import Any
from jax import Array
import jax.numpy as np
from functools import partial
from dataclasses import dataclass
import jax
import jax.numpy as jnp
from gibss.newton import newton_factory
import numpy as np
from jax.scipy.stats import norm

@partial(jax.tree_util.register_dataclass,
         data_fields=['psi', 'fit'], meta_fields=[])
@dataclass
class AdditiveComponent:
    psi: Array  # predictions
    fit: Any  # parameters

def nloglik(coef, x, y, offset, prior_variance=1.):
    """Logistic log-likelihood"""
    psi = offset + x @ coef
    ll = jnp.sum(y * psi - jnp.logaddexp(0, psi)) + norm.logpdf(coef, 0, jnp.sqrt(prior_variance)).sum()
    return -ll

def logistic_fixed_effect(coef_init, X, y, offset, prior_variance=0., newtonkwargs=dict(tol=1e-3, maxiter=500, alpha=0.8, gamma=-0.1)):
    # estimate the MLE
    fun = partial(nloglik, x=X, y=y, offset=offset, prior_variance=prior_variance)
    newton_solver = newton_factory(fun, **newtonkwargs)
    res = newton_solver(coef_init)
    psi = X @ res.x
    return AdditiveComponent(psi, res)


# -

X = np.random.normal(size=(10000, 10))
X[:, 0] = 1
beta = np.random.normal(size=10)
beta[0] = -2
psi = X @ beta
y = 1 / (1 + np.exp(-X@beta))
nloglik(np.zeros(10), X, y, 0.), nloglik(beta, X, y, 0., 100000.), nloglik(np.zeros(10), X, y, psi, 100000.)

from gibss.logistic import logistic_ser_hermite
serfit = logistic_ser_hermite(np.zeros((10, 1)), X.T, y, 0.)
serfit.psi.size

from gibss.logistic import make_logistic_fitfuns
f1, f2 = make_logistic_fitfuns(X.T, y, L=1)
r1=f1(np.zeros_like(y), None)
r2=f2(np.zeros_like(y), None)

from gibss.logistic import fit_logistic_susie1d
fit = fit_logistic_susie1d(X.T, y)

# %%time
fit = fit_logistic_susie1d(X.T, y)
fit[0][0].psi[0].block_until_ready()

# ### Example: gsea simulation

import numpy as np
import jax.numpy as jnp
X = np.load('msigdb_c2.npy')
np.random.seed(1)
beta0 = -3
beta = np.zeros(X.shape[0])
beta[np.random.choice(beta.size, 5, replace=False)] = 2.
logit = beta @ X + beta0
idx = np.where(beta !=0)[0]
y = np.random.binomial(1, 1/(1 + np.exp(-logit)))

from gibss.logistic import logistic_ser_hermite
from gibss.susie import make_fitfun
initfun = lambda X, y, psi, fit: jnp.zeros((X.shape[0], 1))
fitfun = make_fitfun(X, y, logistic_ser_hermite, initfun)
#fitfun(0., None)

# + active=""
# from gibss.logistic import make_logistic_fitfuns
# from gibss.susie import fit_additive, tree_stack
# serkwargs = dict(newtonkwargs=dict(tol=1e-3, maxiter=5, alpha=0.2, gamma=-0.1))
# fitfuns = make_logistic_fitfuns(X, y, L=2, prior_variance=1.0, serkwargs=serkwargs)
# components, state = fit_additive(fitfuns, maxiter=5, keep_intermediate=True, tol=0)
# -

# %%time
from gibss.logistic import fit_logistic_susie
serkwargs = dict(prior_variance=5., newtonkwargs=dict(tol=1e-3, maxiter=5, alpha=0.2, gamma=-0.1))

# %%time
fit1 = fit_logistic_susie(X, y, warm=True, L=10, maxiter=20, tol=1e-4, serkwargs=serkwargs, keep_intermediate=False)

# +
from gibss.utils import tree_stack

fixed_effect = fit1.components[0]
sers = tree_stack(fit1.components[1:])
credible_sets = [compute_cs(a) for a in sers.alpha]
# -

fixed_effects = fixed_effect.fit.x

fixed_effects = fixed_effect.fit.x
alpha = np.array(sers.alpha)
lbf = np.array(sers.fits.lbf)
beta = np.array(sers.fits.beta.shape)
prior_variance = np.array(sers.fits.prior_variance)
lbf_ser = np.array(sers.lbf_ser)
credible_sets = [compute_cs(a) for a in alpha]

from gibss.credible_sets import compute_cs
credible_sets = [compute_cs(a) for a in sers.alpha]

credible_sets[3]

idx

# +
from gibss.additive import fit_additive_model
from gibss.susie import make_fitfun
from gibss.logistic import logistic_ser_hermite, logistic_ser_hermite_init
from functools import partial
from gibss.logistic import make_fixed_fitfun

fixedfitfun = make_fixed_fitfun(X, y)
kwargs  = dict(
    prior_variance = float(10.),
    newtonkwargs=dict(tol=1e-2, maxiter=5, alpha=0.2, gamma=-0.1)
)
initfun = partial(logistic_ser_hermite_init, warm=True)
fitfun = make_fitfun(X, y, logistic_ser_hermite, initfun, kwargs)
fit = fitfun(-3., None)
# -

fit.

from gibss.additive import AdditiveModel, fit_additive_model
m0 = AdditiveModel(-3., None, [fitfun for _ in range(3)], None)
m1 = fit_additive_model([fitfun for _ in range(5)], tol=1e-5, maxiter=10, keep_intermediate=False)

from gibss.m1.components

# %%time
fit2 = fit_logistic_susie(
    X, y, method='hermite_eb', L=10, maxiter=20, tol=1e-4, keep_intermediate=False)

fit1.sers.lbf_ser

# %%time
from gibss.logisticprofile import fit_logistic_susie as fit2d
serkwargs = dict(m=1, prior_variance=5., newtonkwargs=dict(tol=1e-3, maxiter=5, alpha=0.2, gamma=-0.1))
fit2 = fit2d(X, y, L=10, maxiter=20, tol=1e-4, serkwargs=serkwargs)

fit2[0].lbf_ser

fit2[1]

fit1.sers.lbf_ser

# %%time
from gibss.logistic import fit_logistic_susie1d
serkwargs = dict(newtonkwargs=dict(tol=1e-3, maxiter=5, alpha=0.2, gamma=-0.1))
fit2 = fit_logistic_susie1d(X, y, L=10, method='hermite_eb', maxiter=20, tol=1e-4, serkwargs=serkwargs, keep_intermediate=True)
#fit1[1].lbf_ser.block_until_ready()

from gibss.susie import tree_unstack
sers = tree_unstack(fit1.sers)

sers[0]

fit2.sers.lbf_ser[:, 5]

fit1.sers.lbf_ser[:, 5]

np.set_printoptions(2)
fit2.sers.lbf_ser





fit1.sers.alpha.argmax(2)

fit1.fixed_effects.fit.x[:,0]

fit1.sers.fits.beta[0, :, 1]

# %%time
from gibss.logistic import fit_logistic_susie1d
serkwargs = dict(newtonkwargs=dict(tol=1e-3, maxiter=5, alpha=0.2, gamma=-0.1))
fit1 = fit_logistic_susie1d(X, y, L=10, maxiter=20, tol=1e-4, serkwargs=serkwargs)
#fit1[1].lbf_ser.block_until_ready()

fit1.fixed_effects.fit.x

from jax.tree_util import tree_map
fit_np = tree_map(np.array, fit1)

fit_np

[print(f'top var = {a}, lbf = {b}, causal={np.isin(idx, a).astype(int)}') for a, b in zip(fit1[1].alpha.argmax(1), fit1[1].lbf_ser)]

fit1[1].fits.state.x.shape

from gibss.logistic import logistic_ser_hermite
serfit = logistic_ser_hermite(np.zeros((1000, 1)), X, y.astype(float), offset=0., m=int(1), prior_variance=1.0)
serfit.lbf_ser

# %%timeit
serfit = logistic_ser_hermite(np.zeros((1000, 1)), X, y.astype(float), offset=-3., m=int(1), prior_variance=1.0, newtonkwargs=dict(maxiter=5, alpha=0.5, gamma=-0.1))
serfit.lbf_ser.block_until_ready()

from gibss.logistic import make_logistic_fitfuns
f1, f2 = make_logistic_fitfuns(X, y, L=1)
r1=f1(np.zeros_like(y), None)
r2=f2(np.zeros_like(y), None)

# %%timeit
r2=f2(np.ones_like(y) * -3, None)
r2.lbf_ser.block_until_ready()

# %%time
from gibss.logisticprofile import logistic_ser_hermite as logistic_ser_hermite2
serfit2 = logistic_ser_hermite2(np.zeros((1000, 2)), X, y.astype(float), offset=0., m=int(1), prior_variance=1.0)
serfit2.lbf_ser.block_until_ready()

X.shape, y.size



# %%time
from gibss.logisticprofile import fit_logistic_susie
fit2 = fit_logistic_susie(X, y, L=5, maxiter=20)
fit2[0].lbf_ser.block_until_ready()

fit2[1]

mle = logistic_fixed_effect(np.zeros(10), X, y, 0., float(1e6))
l2 = logistic_fixed_effect(np.zeros(10), X, y, 0., 1.)
null = logistic_fixed_effect(np.zeros(10), X, y, psi, float(1e6))
intercept_only = logistic_fixed_effect(np.zeros(1), X[:, [0]], y, 0., float(1e6))

from jax.scipy.stats import norm
1/jnp.sqrt(2 * jnp.pi), norm.logpdf(0, 0, 1/jnp.sqrt(2*jnp.pi))

# ### Univariate regression and SER

# +
offset = 0.
prior_variance=1.
newtonkwargs=dict(maxiter=20)
x = X[:, 0]
fun = partial(nloglik, x=x[:, None], y=y, offset=offset, prior_variance=prior_variance)
newton_solver = newton_factory(fun, **newtonkwargs)
res = newton_solver(np.zeros(1))

def fit_newton(coef_init, x, y, offset, prior_variance, newtonkwargs = dict(maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)):
    fun = partial(nloglik, x=x[:, None], y=y, offset=offset, prior_variance=prior_variance)
    newton_solver = newton_factory(fun, **newtonkwargs)
    return newton_solver(coef_init)

fit_newton(np.zeros(1), x, y, 0., 1.)
# -

# %timeit fit_newton(np.zeros(1), x, y, 0., 1.)

# %timeit fit_newton(np.zeros(1), x, y, np.zeros_like(y), 1.)

# +
from gibss.logistic import hermite_factory
from jax.tree_util import Partial

hermite = hermite_factory(1)
res = hermite(np.zeros(1), np.ones_like(y), y, 0., 1.)

# +
m = 1
prior_variance = 1
newtonkwargs=dict(maxiter=20)
offset = 0.
from gibss.ser import SER

def logistic_ser_hermite(coef_init, X, y, offset, m=1, prior_variance=1.0, newtonkwargs=dict()):
    vhermite = jax.vmap(Partial(hermite_factory(m), y=y, offset=offset, prior_variance=prior_variance, newtonkwargs=newtonkwargs), in_axes=(0, 0))
    fits = vhermite(coef_init, X)
    logp = -fits.state.f
    ll0 = jnp.sum(y * offset - jnp.logaddexp(0, offset))
    lbf = -fits.state.f - ll0
    alpha = jnp.exp(lbf - jax.scipy.special.logsumexp(lbf))
    psi = X.T @ (alpha * fits.beta)
    return SER(psi, alpha, lbf, prior_variance, fits)

serfit = logistic_ser_hermite(np.zeros((10, 1)), X.T, y, 0., 1.)

# +
from gibss.susie import fit_additive
from gibss.logistic import logistic_fixed_effect, logistic_ser_hermite
                      
def make_logistid_1d_fitfuns(X, y, L=5, prior_variance=1.0, fixedkwargs=dict(), serkwargs=dict()):
    @jax.jit
    def fixedfitfun(psi, old_fit):
        # update default arguments
        kwargs = dict(
            prior_variance = float(1e6),
            newtonkwargs=dict(tol=1e-3, maxiter=500, alpha=0.8, gamma=-0.1)
        )
        kwargs.update(fixedkwargs)
        # TODO: take Z as an argument
        coef_init = jnp.zeros(1) 
        Z = np.ones((y.size, 1))

        # Fit fixed effects
        return logistic_fixed_effect(
            coef_init = coef_init,
            X = Z, y = y, offset = psi,
            **kwargs
        )
    @jax.jit
    def serfitfun(psi, old_fit):
        # update default arguments
        kwargs = dict(
            prior_variance = float(1.),
            newtonkwargs=dict(tol=1e-3, maxiter=500, alpha=0.8, gamma=-0.1)
        )
        kwargs.update(serkwargs)

        # fit SER
        coef_init = np.zeros((X.shape[0], 1))
        return logistic_ser_hermite(
            coef_init = coef_init,
            X = X, y=y, offset = psi,
            **kwargs
        )
    return ([fixedfitfun] + [serfitfun for _ in range(L)])

def fit_logistic_susie1d(X, y, L=5, prior_variance=1):
    fitfuns = make_logistid_1d_fitfuns(X.T, y, L=5, prior_variance=1.)
    return fit_additive(fitfuns)


# -

# %%time
res = fit_additive(fitfuns)
res[0][0].psi.block_until_ready()

X.shape

# ?logistic_ser_hermite

from gibss.logistic import nloglik_vmap
nloglik(np.zeros(1), y[:,None], y, 0., 1/jnp.sqrt(2 * jnp.pi))

logodds = lambda y: np.log(y.mean()/(1 - y.mean()))
logodds(y)

jnp.logaddexp(0, 0)

from gibss.logistic import logistic_ser_hermite
logistic_ser_hermite(np.zeros((10, 1)), X.T, y, 0., 1., 1)

X.shape

l2.fit.x/beta # shrunk

null.fit.x # near 0

p = y.mean()
intercept_only.fit.x/ np.log(p/(1-p))

# ### Estimate prior variance

# +
from gibss.logistic import hermite_grid_factory
import numpy as np

hermite_grid = hermite_grid_factory(1)
x = np.random.normal(size=10000)
y = np.random.binomial(1, 1/(1 + np.exp(-x)))
prior_variance_grid = np.cumprod(np.ones(24) * np.sqrt(2)) / 1024
# -

res = hermite_grid(np.zeros(1), x, y, 0., prior_variance_grid)
res.lbf

from gibss.logistic import logistic_ser_hermite_grid
m=1
offset=0
X = np.random.normal(size=(10, 10000))
X[0] = x / 1.0
sergrid = logistic_ser_hermite_grid(np.zeros((10, 1)), X, y, 0.)

sergrid.prior_variance

import jax
from jax.tree_util import Partial
m=1
offset=0
X = np.random.normal(size=(10, 10000))
X[0] = x
vhermite = jax.vmap(
    Partial(hermite_grid_factory(m), 
            y=y, 
            offset=offset, 
            prior_variance_grid=prior_variance_grid), in_axes=(0, 0)
)
gridfits = vhermite(np.zeros((10, 1)), X)
best_prior_variance = jax.scipy.special.logsumexp(gridfits.lbf, axis=0).argmax()
prior_variance_grid[best_prior_variance]

import matplotlib.pyplot as plt
k=12
plt.plot(prior_variance_grid[k:],jax.scipy.special.logsumexp(gridfits.lbf, axis=0)[k:])

# ?hermite_grid


