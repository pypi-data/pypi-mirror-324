#%%
import numpy as np
from gibss.logistic import nloglik, nloglik_mle
from gibss.newton import newton_factory
from jax.tree_util import Partial

# simulate 
x = np.random.normal(size=(1000))
y = np.random.binomial(1, 1/(1 + np.exp(-(x * 1. - 1))))


# %%
import jax
f = Partial(nloglik, x=x, y=y, offset=-1., prior_variance=1.)
g = jax.grad(f)
hess = jax.hessian(f)
f(np.array([0.]))
g(np.array([0.]))
hess(np.array([0.]))

#%%
coef_init = np.array([0.])
offset = -1
solver = newton_factory(Partial(nloglik_mle, x=x, y=y, offset=offset),
                        maxiter=20, tol=1e-5, alpha=0.5, gamma=0.0)
state = solver(coef_init)

#%%
from gibss.logisticprofile import compute_wakefield_lbf
betahat = state.x[0]
s2 = 1/state.h[0, 0]
lbf = compute_wakefield_lbf(betahat, s2, 1.0)

#%%
from gibss.logistic import wakefield, fit_null
nullfit = fit_null(y, np.ones_like(y) * -1)
wakefield(np.array([0.]), x, y, 0., nullfit, 1.)

# %%
from gibss.logistic import logistic_ser_wakefield, logistic_ser_lapmle, logistic_ser_hermite
X = np.random.normal(size=(10, 1000))
X[0] = x
fit = logistic_ser_wakefield(np.zeros(10)[:, None], X, y, -1., 1.0)
lapfit = logistic_ser_lapmle(np.zeros(10)[:, None], X, y, -1., 1.)
hermfit = logistic_ser_hermite(np.zeros(10)[:, None], X, y, -1., 1., 11)
