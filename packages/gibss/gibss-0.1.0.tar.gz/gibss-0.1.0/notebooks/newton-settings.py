# ### Optimization settings
#
# To run GIBSS we are fitting a large number of univariate regressions.
# Each newton step requires evaluating the likelihood, gradient, and hessian. 
# When we are using Gauss-Hermite quadrature we do not require a very precise approximation of the MAP, particularly if we are using multiple evaluation points.

# +
from gibss.logisticprofile import logistic_ser_hermite, logistic_ser_hermite_grid, fit_logistic_susie, fit_null
import numpy as np
import jax.numpy as jnp
import jax
    
jax.config.update("jax_enable_x64", True)

X = np.load('msigdb_c2.npy')
np.random.seed(1)
beta0 = -3
beta = np.zeros(X.shape[0])
beta[np.random.choice(beta.size, 5, replace=False)] = 1.
logit = beta @ X + beta0
y = np.random.binomial(1, 1/(1 + np.exp(-logit)))
idx = np.where(beta != 0)[0]

nullfit = fit_null(y, 0.)
# -

# ?jaxopt.LBFGS

# +
import jaxopt
from gibss.logisticprofile import nloglik
from jax.tree_util import Partial

fun = Partial(nloglik, x=X[2], y=y, offset=0., prior_variance=1.)
fun(np.zeros(2))
solver = jaxopt.LBFGS(fun=fun, )

def blocked_bfgs(x0):
    fit = solver.run(np.zeros(2))
    fit.params.block_until_ready()
    return fit

# %timeit blocked_bfgs(np.zeros(2))
bfgs_res = blocked_bfgs(np.zeros(2))
bfgs_res.params, fun(bfgs_res.params)

# +
import jaxopt
from gibss.logisticprofile import nloglik
from jax.tree_util import Partial

fun = Partial(nloglik, x=X[2], y=y, offset=0., prior_variance=1.)
fun(np.zeros(2))
solver = jaxopt.LBFGS(fun=fun, tol=0.1)
jsolver = jax.jit(lambda x0: solver.run(x0))

# %timeit jsolver(np.zeros(2)).params.block_until_ready()
bfgs_res = jsolver(np.zeros(2))
bfgs_res.params, fun(bfgs_res.params)
# -

bfgs_res.state.iter_num

from gibss.newton import newton_factory
newton_solver = jax.jit(newton_factory(fun, 50, tol=.1, gamma=-0.1))
# %timeit newton_solver(np.zeros(2)).x.block_until_ready()
newton_res = newton_solver(np.zeros(2))
newton_res.x, newton_res.f, newton_res.iter

# %timeit newton_solver(np.array([-3., 0.])).x.block_until_ready()
newton_res = newton_solver(np.array([-3., 0.]))
newton_res.x, newton_res.f, newton_res.iter

p = X.shape[0]
coef_init = jnp.stack([jnp.ones(p) * nullfit.state.x, jnp.zeros(p)], axis=1)
coef_init[:5]

# +
import jax
import jax.numpy as jnp
from gibss.logisticprofile import hermite_grid_factory
from jax.tree_util import Partial

m = 1
prior_variance_grid = np.cumprod(np.ones(24)* np.sqrt(2)) / 128
maxiter = 1
tol = 1e-1
alpha = 0.5
gamma = -0.1
offset = 0.

vhermite = jax.vmap(Partial(hermite_grid_factory(m), 
                            prior_variance_grid = prior_variance_grid, 
                            maxiter=maxiter, tol=tol, alpha=alpha, gamma=gamma),
                    in_axes=(0, 0, None, None, None))
nullfit = fit_null(y, offset)  # fit null model
# initialize with null coef
p = X.shape[0]
coef_init = jnp.stack([jnp.ones(p) * nullfit.state.x, jnp.zeros(p)], axis=1)
# %time gridfits = vhermite(coef_init, X, y, offset, nullfit)  
# %time gridfits.state.iter.block_until_ready()
# -

nullfit = fit_null(y, offset)  # fit null model
p = X.shape[0]
coef_init = jnp.stack([jnp.ones(p) * nullfit.state.x, jnp.zeros(p)], axis=1)
fit0 = logistic_ser_hermite(np.zeros((p, 2)), X, y, 0., 1., m=1, alpha=0.1, tol=0.1)
fit1 = logistic_ser_hermite(coef_init, X, y, 0., 1., m=1, alpha=0.1, tol=0.1)

fit1.fits.state.x

# +
from gibss.newton import newton_step, NewtonState
from gibss.logisticprofile import nloglik

fun = Partial(nloglik, x=X[2], y=y, offset=0., prior_variance=1.)
grad = jax.grad(fun)
hess = jax.hessian(fun)

def newton_step_scan(state, x):
    state = newton_step(state, fun, grad, hess)
    return state, state
    
def newton(x0, tol=1e-3, niter=10, alpha=0.5, gamma=-0.1):
    f = fun(x0)
    g = grad(x0)
    H = hess(x0)
    direction = -jax.scipy.linalg.solve(H, g)
    state = NewtonState(x0, f, g, H, direction, 1.0, np.inf, tol, False, alpha, gamma, maxiter, 0)
    _, states = jax.lax.scan(newton_step_scan, state, np.arange(niter))
    return states

iters = newton(np.zeros(2), niter=100, alpha=0.1)
# -

from gibss.logisticprofile import hermite_factory
fun = hermite_factory(5)
fit = fun(np.zeros(2), X[2], y, 0., nullfit, 1., maxiter=100, tol=0.1, alpha=0.1, gamma=-0.1)


# ?logistic_ser_hermite

# +
def fit_blocked(f, *args, **kwargs):
    fit = f(*args, **kwargs)
    fit.fits.lbf.block_until_ready()
    return fit

coef_init = np.zeros((X.shape[0], 2))
coef_init[:, 0] = -3
# -

# %time ser1 = fit_blocked(logistic_ser_hermite, coef_init, X, y, 0., 1., m=5, maxiter=5, tol=3e-1)

# %time ser2 = fit_blocked(logistic_ser_hermite, coef_init, X, y, 0., 1., m=5, maxiter=5, tol=1e-3)

pvg = np.cumprod(np.ones(12) * 2) / 128 
# %time ser2 = fit_blocked(logistic_ser_hermite_grid, coef_init, X, y, offset=0., prior_variance_grid=pvg, m=1, maxiter=1, tol=1e-3)


