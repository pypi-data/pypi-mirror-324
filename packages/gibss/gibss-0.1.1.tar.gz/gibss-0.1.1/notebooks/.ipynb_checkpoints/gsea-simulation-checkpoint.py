# ### GSEA simulation
# This is just a quick example of applying logistic SuSiE to GSEA. The gene sets are real, they come from MSigDB's "curated gene sets" database (C2). 
#

from gibss.logisticprofile import logistic_ser_hermite, fit_logistic_susie
import numpy as np
import jax.numpy as jnp
X = np.load('msigdb_c2.npy')
np.random.seed(1)
beta0 = -3
beta = np.zeros(X.shape[0])
beta[np.random.choice(beta.size, 5, replace=False)] = 2.
logit = beta @ X + beta0
y = np.random.binomial(1, 1/(1 + np.exp(-logit)))

# %time res = fit_logistic_susie(X, y, L=5, maxiter=20, serkwargs=dict(maxiter=1), warm_init = True)

# %time res = fit_logistic_susie(X, y, L=5, maxiter=20, serkwargs=dict(maxiter=1), warm_init = False)

# %time res = fit_logistic_susie(X[:500], y, L=5, maxiter=10, method='hermite_eb', cleanup=True)

np.where(beta != 0)

res.cs[0]

res.cs[1]

res.cs[2]

res.cs[3]

# %%time
# fit SER for marginal analysis
serfit = logistic_ser_hermite(
  coef_init = np.zeros((X.shape[0], 2)), 
  X = X.astype(float), 
  y = y.astype(float), 
  offset = 0., 
  prior_variance = 1.,
  m = 1
)
# extract relevant info from SER
marginal_results = dict(
  lbf=np.array(serfit.fits.lbf),
  effect=np.array(serfit.fits.beta)
)

# %%time
# fit SER for marginal analysis
serfit = logistic_ser_hermite(
  coef_init = np.zeros((X.shape[0], 2)), 
  X = X.astype(float), 
  y = y.astype(float), 
  offset = 0., 
  prior_variance = 1.,
  m = 1
)
serfit.alpha[0]

import jax
Xput = jax.device_put(X, jax.devices()[0])
yput = jax.device_put(y, jax.devices()[0])
coef_init = jax.device_put(np.zeros((X.shape[0], 2)), jax.devices()[0])

from functools import partial
serfun = partial(logistic_ser_hermite, **dict(m=1, prior_variance=1.0))

# %time a = serfun(coef_init, Xput, yput, 0.).alpha.block_until_ready()

from jax.tree_util import Partial
from jax import jit
serfun = jit(Partial(logistic_ser_hermite, **dict(m=1, prior_variance=1.0)))

# %time a = serfun(coef_init, Xput, yput, 0.).alpha.block_until_ready()

fit = serfun(np.zeros((X.shape[0], 2)), X, y, 0.)


# +
def make_ser_fitfun(X, y, coef_init, prior_variance):
    @jax.jit
    def serfitfun(psi):
        return logistic_ser_hermite(
            coef_init = coef_init,
            X = X, y=y, offset = psi,
            m=1, prior_variance = prior_variance
        )
    return serfitfun

def f1(psi, x):
    """
    forward selection scan
    """
    serfit = fitfun(psi)
    psi2 = psi + serfit.psi
    return psi2, serfit

def f2(psi, serfit):
    """
    subsequent iterations need to remove predictions first
    """
    psi2 = psi - serfit.psi
    serfit2 = fitfun(psi)
    psi2 = serfit2.psi
    return psi2, serfit2

from functools import partial
from dataclasses import dataclass

@partial(jax.tree_util.register_dataclass,
         data_fields=['tol', 'converged', 'maxiter', 'iter'], meta_fields=[])
@dataclass
class AdditiveState:
    tol: int
    converged: bool
    maxiter: int
    iter: int

def update_sers(val):
    state, (psi1, components1) = val
    psi2, components2 = jax.lax.scan(f2, psi, components)

    # update the optimization state
    diff = jnp.abs(psi2 - psi1).max()
    state2 = AdditiveState(state.tol, diff < state.tol, state.maxiter, state.iter + 1)
    return state2, (psi2, components2)
    
def check_not_converged(val):
    state, components = val
    return jax.lax.cond(
            state.converged | (state.iter >= state.maxiter),
            lambda: False, # stop the while loop
            lambda: True # stay in the while loop
    )


# +
# setup
coef_init = np.zeros((X.shape[0], 2))
fitfun = make_ser_fitfun(X, y, coef_init, 1.)
psi_init = np.zeros_like(y).astype(float)
L = 10
tol = 1e-5
maxiter = 10
# forward selection
psi, components = jax.lax.scan(f1, psi_init, np.arange(L))

# run gibss
state = AdditiveState(tol, False, maxiter, 1)
init_val = (state, (psi, components))
res = jax.lax.while_loop(check_not_converged, update_sers, init_val)
# %time res[1][1].alpha.block_until_ready()
# -



# +
import jax.numpy as jnp

def categorical_kl(pi1, pi2):
    return jnp.sum(pi1 * (jnp.log(pi1) - jnp.log(pi2)))

def categorical_kl_sym(pi1, pi2):
    return (categorical_kl(pi1, pi2) + categorical_kl(pi2, pi1))/2

pi1 = np.random.normal(size=10)**2
pi1 = pi1 / pi1.sum()

pi2 = np.random.normal(size=10)**2
pi2 = pi2 / pi2.sum()

categorical_kl_sym(pi1, pi1), categorical_kl_sym(pi1, pi2)
# -

serfit.lbf_ser

serfit2.log_bfs

gseafit = fit_logistic_susie(X, y, L=10)
