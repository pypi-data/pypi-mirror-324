#%%
import jax
import jax.numpy as jnp
from jax.scipy.special import logsumexp
import numpy as np
from gibss.newton import newton_factory


#%% quadratic objective, converges in one step
f = lambda x: x @ x
x0 = np.ones(10)
fopt = newton_factory(f, tol=1e-3, maxiter=10)
res = fopt(x0)
res.iter == 1, res.converged

#%%
from gibss.logisticprofile import nloglik_mle
from functools import partial
x = np.random.normal(size=1000)
y = np.random.binomial(1, 1/(1 + np.exp(-(x - 1))))
x0 = np.array([-1., 0.])
f = partial(nloglik_mle, x=x, y=y, offset=0.)
fopt = newton_factory(f, tol=1e-5, maxiter=5000, gamma=0.0)
res = fopt(x0)
f(x0), f(res.x), res.nd, res.iter

#%%
np.random.seed(2)
mu = np.random.normal(size=5)
f = lambda x: (x - mu) @ (x - mu) + jnp.sum(jnp.abs(x))
x0 = np.zeros(5)
fopt = newton_factory(f, tol=1e-3, maxiter=5000, gamma=0.0)
res = fopt(x0)
f(x0), f(res.x), res.nd

# %%
a = np.random.normal(size=100)
f = lambda x: logsumexp(x + a) + logsumexp(x) * 1e12
x0 = np.exp(np.random.normal(size=100))
x0 = jnp.log(x0 / x0.sum())
fopt = newton_factory(f, tol=1e-3, maxiter=100, gamma=0)  
res = fopt(x0)
f(x0), f(res.x)

# %% Compare newton with convergence monitoring to not
from gibss.newton import newton_factory, newton_lite_factory
from gibss.logisticprofile import nloglik, nloglik_vmap, fit_null, logistic_ser_hermite, UnivariateRegression
from gibss.ser import ser
from jax.tree_util import Partial
from jax.scipy.stats import norm
import jax
import jax.numpy as jnp
import numpy as np
from functools import partial

def hermite_factory2(m):
    base_nodes, base_weights = np.polynomial.hermite.hermgauss(m)
    def hermite(coef_init, x, y, offset, prior_variance, nullfit, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0):
        solver = newton_lite_factory(Partial(nloglik, x=x, y=y, offset=offset, prior_variance=prior_variance), niter=maxiter, tol=tol, alpha=alpha, gamma=gamma)
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
        y = -nloglik_vmap(coef_nodes, x, y, offset, prior_variance)
        logp = jax.scipy.special.logsumexp(y - norm.logpdf(nodes, loc=mu, scale=sigma) + jnp.log(weights)) 
        lbf = logp - nullfit.logp

        # compute posterior mean of effect
        y2 = nodes * jnp.exp(y - logp)
        beta = jnp.sum(y2/norm.pdf(nodes, loc=mu, scale=sigma) * weights)
        return UnivariateRegression(logp, lbf, beta, state)
    
    hermite_jit = jax.jit(hermite)
    return hermite_jit

vhermite = jax.vmap(partial(hermite_factory2(1), maxiter=5, tol=1e-3, alpha=0.5, gamma=0), in_axes=(0, 0, None, None, None, None))
@partial(jax.jit)
def logistic_ser_hermite2(coef_init, X, y, offset, prior_variance):
    return ser(coef_init, X, y, offset, prior_variance, vhermite, fit_null)

X = np.random.binomial(1, 0.2, size=(300, 40000))
x = X[0]
logit = -1 + 0.5 * x
y = np.random.binomial(1, 1/(1 + np.exp(-logit)))

a = logistic_ser_hermite(np.zeros((300, 2)), X, y, np.zeros_like(y), 1.0, m=1, maxiter=10)
b = logistic_ser_hermite2(np.zeros((300, 2)), X, y, np.zeros_like(y), 1.0)

# %%
