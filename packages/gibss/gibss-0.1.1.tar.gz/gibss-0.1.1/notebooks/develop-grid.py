# ### Fitting regularization path for logistic SuSiE
# Fit logistic SER at a grid of prior variance values and pick the setting that maximizes the marginal likelihood.

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



# -

def hermite_grid_factory(m):
    base_nodes, base_weights = np.polynomial.hermite.hermgauss(m)
    def hermite_grid(coef_init, x, y, offset, nullfit, prior_variance_grid, maxiter=50, tol=1e-3, alpha=0.5, gamma=-0.1):
        def hermite_inner(coef_init, prior_variance):
            solver = newton_factory(
                Partial(nloglik, x=x, y=y, offset=offset, prior_variance=prior_variance),
                maxiter=maxiter, tol=tol, alpha=alpha, gamma=gamma
            )
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
            nll = -nloglik_vmap(coef_nodes, x, y, offset, prior_variance)
            logp = jax.scipy.special.logsumexp(nll - norm.logpdf(nodes, loc=mu, scale=sigma) + jnp.log(weights)) 
            lbf = logp - nullfit.logp
        
            # compute posterior mean of effect
            tmp = nodes * jnp.exp(nll - logp)
            beta = jnp.sum(tmp/norm.pdf(nodes, loc=mu, scale=sigma) * weights)
            return state.x, UnivariateRegression2(logp, lbf, beta, prior_variance, state)
            
        res = jax.lax.scan(hermite_inner, coef_init, prior_variance_grid)
        return(res[1])
    return hermite_grid


# I imagine there is some strategy to interpolate between grid points, but I also don't think that it will gain us much. The approach to the SER is this: we fit each variable along the same fixed path, compute the SER under each, and simply select the setting of prior variance that maximizes the evidence for an effect.

# a simple simulation
X = np.random.normal(size=(100, 10000))
y1 = np.random.binomial(1, 1/(1 + np.exp(1 - X[0]))) # non-null y
y2 = np.random.binomial(1, 0.1, size=10000) # null y
prior_variance_grid = np.cumprod(np.ones(12) * 2) / 512

hermite_grid = hermite_grid_factory(5)
nullfit1 = fit_null(y1, 0.)
gridfit1 = hermite_grid(np.zeros(2), X[0], y1, 0., nullfit1, prior_variance_grid)
nullfit2 = fit_null(y2, 0.)
gridfit2 = hermite_grid(np.zeros(2), X[0], y2, 0., nullfit2, prior_variance_grid)

# +
from functools import partial

@partial(jax.jit, static_argnames = ['m', 'maxiter'])
def logistic_ser_hermite_grid(coef_init, X, y, offset, prior_variance_grid, m, maxiter=50, tol=1e-3, alpha=0.5, gamma=-0.1):
    vhermite = jax.vmap(Partial(hermite_grid_factory(5), 
                                prior_variance_grid = prior_variance_grid, 
                                maxiter=5, tol=1e-3, alpha=0.5, gamma=-0.1),
                        in_axes=(0, 0, None, None, None))
    nullfit = fit_null(y, 0.)  # fit null model
    gridfits = vhermite(np.zeros((100, 2)), X, y, 0., nullfit)  # fit univariate models 
    best_prior_variance = jax.scipy.special.logsumexp(gridfits.lbf - jnp.log(X.shape[0]), axis=0).argmax()
    fits = jax.tree.map(lambda x: x[:, best_prior_variance], gridfits)
    return _ser(fits, X)

ser1 = logistic_ser_hermite_grid(np.zeros((100,2)), X, y1, 0., prior_variance_grid, 5)
ser2 = logistic_ser_hermite_grid(np.zeros((100,2)), X, y2, 0., prior_variance_grid, 5)
ser1.fits.prior_variance[0], ser2.fits.prior_variance[0]
# -

ser1.lbf_ser, ser2.lbf_ser



@partial(jax.jit, static_argnames = ['m', 'maxiter'])
def logistic_ser_hermite_grid(coef_init, X, y, offset, prior_variance_grid, m, maxiter=50, tol=1e-3, alpha=0.5, gamma=-0.1):
    vhermite = jax.vmap(Partial(hermite_grid_factory(m), prior_variance_grid = prior_variance_grid, maxiter=maxiter, tol=tol, alpha=alpha, gamma=gamma), in_axes=(0, 0, None, None, None))
    return ser(coef_init, X, y, offset, vhermite, fit_null)


n = 10000
x = np.random.normal(size=n)
psi = -1 + 1. * x
y = np.random.binomial(1, 1/(1 + np.exp(-psi))).astype(float)
offset = 0.
nullfit = fit_null(y, 0.)
prior_variance_grid = np.array([0.000001, 0.0001, 0.01, 0.1, 1., 10., 100., 1000.])
gridfit = hermite_grid(np.zeros(2), x, y, 0., nullfit, prior_variance_grid)

from gibss.logisticprofile import hermite_factory
fit_hermite = hermite_factory(1)
fit1 = fit_hermite(np.zeros(2), x, y, 0., nullfit, 1.0)



fit1.beta

import matplotlib.pyplot as plt
np.set_printoptions(precision=3)

np.array(gridfit.lbf)

plt.plot(np.log10(prior_variance_grid), np.array(gridfit.lbf))

gridfit.prior_variance



gridfit.state.iter

gridfit.state.iter



# +
import numpy as np
from scipy import sparse

def ensure_dense_and_float(matrix):
    # Check if the input is a sparse matrix
    if sparse.issparse(matrix):
        # Convert sparse matrix to a dense array
        matrix = matrix.toarray()
        # Provide a message to the user
        print("Input is a sparse matrix. Converting to a dense array.")
    
    # Ensure the matrix is a numpy array (in case it's a list or other type)
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Input must be a sparse matrix or a numpy array.")
    
    # Ensure the matrix is of float type
    if not np.issubdtype(matrix.dtype, np.floating):
        matrix = matrix.astype(float)
        print("Converting matrix to float type.")
    return matrix



# -

Xsp[0]


