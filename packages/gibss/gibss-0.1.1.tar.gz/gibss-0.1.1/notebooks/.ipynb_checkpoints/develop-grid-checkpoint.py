# +
from gibss.logisticprofile import nloglik, nloglik_vmap, fit_null

import jax.numpy as jnp
from jax.scipy.stats import norm
from jax.scipy.special import logsumexp
import jax
import numpy as np
from functools import partial
from gibss.ser import ser, _ser
from jax.tree_util import Partial
from typing import Any
from dataclasses import dataclass
from gibss.newton import newton_factory
from gibss.gd_backtracking import gd_factory
from gibss.gibss import gibss

# new Univariate regression class records the prior variance
@partial(jax.tree_util.register_dataclass,
         data_fields=['logp', 'lbf', 'beta', 'prior_variance', 'state'], meta_fields=[])
@dataclass
class UnivariateRegression2:
    logp: float
    lbf: float
    beta: float
    prior_variance: float
    state: Any



# +
base_nodes, base_weights = np.polynomial.hermite.hermgauss(5)

def hermite_grid(coef_init, x, y, offset, nullfit, prior_variance_grid, maxiter=50, tol=1e-3, alpha=0.5, gamma=-0.1):
    def hermite_inner(coef_init, prior_variance):
        solver = newton_factory(
            Partial(nloglik, x=y, y=y, offset=offset, prior_variance=prior_variance))
        # ,maxiter=maxiter, tol=tol, alpha=alpha, gamma=gamma)
        state = solver(coef_init)
        params = state.x
        hessian = -state.h
    
        # set up quadrature
        mu = params[1]
        sigma = jnp.sqrt(-1/hessian[1,1])
        nodes = base_nodes * jnp.sqrt(2) * sigma + mu
        weights = base_weights / jnp.sqrt(jnp.pi)
    
        # compute logp
        coef_nodes = jnp.stack([jnp.ones_like(nodes) * params[0], nodes], axis=1)
        nll = -nloglik_vmap(coef_nodes, y, y, offset, prior_variance)
        logp = jax.scipy.special.logsumexp(nll - norm.logpdf(nodes, loc=mu, scale=sigma) + jnp.log(weights)) 
        lbf = logp - nullfit.logp
    
        # compute posterior mean of effect
        y2 = nodes * jnp.exp(y - logp)
        beta = jnp.sum(y2/norm.pdf(nodes, loc=mu, scale=sigma) * weights)
    
        return state.x, UnivariateRegression2(logp, lbf, beta, prior_variance, state)
    res = jax.lax.scan(hermite_inner, coef_init, prior_variance_grid)
    return(res[1])


# -

n = 10000
x = np.random.normal(size=n)
psi = -1 + x
y = np.random.binomial(1, 1/(1 + np.exp(-Psi))).astype(float)
offset = 0.
nullfit = fit_null(y, 0.)
prior_variance_grid = np.array([0.000001, 0.0001, 0.01, 0.1, 1., 10., 100., 1000.])
hermite_grid(np.zeros(2), x, y, 0. nullfit, prior_variance_grid

res[1].prior_variance

res[1].lbf

from gibss.logisticprofile import hermite_factory
fit_hermite = hermite_factory(1)
fit_hermite(np.zeros(2), X, Y, 0., nullfit, 1.0)


