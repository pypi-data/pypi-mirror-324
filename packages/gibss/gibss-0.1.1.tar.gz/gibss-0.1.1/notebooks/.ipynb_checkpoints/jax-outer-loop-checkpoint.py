# # Using Jax to implement the outer loop of GIBSS
#
# Problem: when fitting GIBSS, we have already implemented the SER with fast, vectorized, JITed code. 
# However, there may be some overhead associated with passing the data between different calls to the SER. 
# We think we can achieve a significant speed-up using `jax.lax.scan` to handle fitting the sequence of $L$ SERs,
# and `jax.lax.while` to monitor convergence in the outer loop.
#
# Ultimately we found that the initial speedup we we observed was due to a bug in the code + smart compilation of the buggy code. 
# The bug was that when we iterate over the SERs, we were passing each SER the same linear prediction, rather than updating it sequentially. The compiler probably noticed this. Once we fixed the bug, the performance gain disappeared. However, now I am curious if such a "simultaneous update" approach could work. Obviously it does not work from a bad initialization (consider when the linear predictions for each SER are $0$, then the simultaneous update would return the same SER for each component. However, I wonder if there are conditions under which the simultaneous update is stable.
#
# A significant downside of the `jax.lax.scan` approach is that we allocate memory for all $L$ SERs, which can be very large. Even for a single SER, I'm concerned about memory usage when $X$ is large. E.g. for MsigDB C2 (5k gene sets x 20k genes) requires ~7gb of memory (I should do more formal profiling, but I was just reading the `Memory` for the corresponding python process in Activity Monitor). A solution to reduce the overhead is to carry out the computation for the SER in chunks, or to screen variables so that we only need to check a small fraction of them.

# ## A simple simulator

# +
import numpy as np

def sim(n, p):
    X = np.random.normal(size=(p, n))
    logit = -1 + X[0] + X[10]
    y = np.random.binomial(1, 1/(1 + np.exp(-logit)))
    return X, y


# -

# ## Jax implementation

# +
from gibss.susie import fit_susie
from gibss.logisticprofile import initialize_coef, logistic_ser_hermite
from jax.tree_util import Partial
import jax.numpy as jnp

serkwargs = dict(m=1, prior_variance=1.)
initfun = lambda X, y, psi: jnp.zeros((X.shape[0], 2))
serfun = Partial(logistic_ser_hermite, **serkwargs)

def test_new_outer_loop(X, y, L, maxiter):
    fit, state = fit_susie(X, y, L, serfun, initfun, serkwargs, -1., maxiter)
    fit.alpha.block_until_ready()


# -

# ## Reference implementation
#
# The base python implementation of the GIBSS outer loop is extremely simple. 
# Here we will use the JITed SER, but do the outer loop in python.
# We can compare performance to the optimized version.

# +
def gibss_outer_loop(X, y, L, maxiter=10):
    """
    Simplified implementation of the GIBSS outer loop.
    In a first pass fit L SERs. This step is analagous to forward stepwise selection.
    Iteratively refine the SER estimates by refitting while holding the others fixed.
    run for a fixed number of iterations
    """
    def serfun(psi):
        """
        logistic SER, BFs approximated with Laplace MAP (Gauss-Hermite quadrature with one quadrature point)
        the prior variance is fixed to 1.
        """
        return logistic_ser_hermite(
            np.zeros((X.shape[0], 2)),
            X, y, psi,
            m=1, prior_variance=1.
        )
        
    components = []
    psi = np.zeros_like(y)
    for _ in range(L):
        coef_init = np.zeros((X.shape[0], 2))
        component = serfun(psi)
        components.append(component)
        psi = psi + component.psi
        
    for i in range(maxiter - 1):
        for j in range(L):
            psi2 = psi - components[j].psi
            components[j] = serfun(psi2)
            psi3 = psi2 + components[j].psi
            psi = psi3

    return components

def test_gibss_outer_loop(X, y, L, maxiter):
    components = gibss_outer_loop(X, y, L, maxiter)
    components[0].alpha.block_until_ready()


# -

# ### A python outer loop, again

# +
from gibss.susie import ensure_dense_and_float, tree_stack, make_ser_fitfun, AdditiveState
from typing import Callable, Any
import numpy as np
import jax
    
def fit_susie2(X: np.ndarray, y: np.ndarray, L: int, serfun: Callable, initfun: Callable, serkwargs: dict, tol=1e-3, maxiter=10) -> Any:
    # initialization
    X = ensure_dense_and_float(X)
    y = ensure_dense_and_float(y)
    fitfun = make_ser_fitfun(X, y, serfun, initfun, serkwargs)
    psi_init = jnp.zeros_like(y).astype(float)

    psi = jnp.zeros_like(y)
    components = []
    for l in range(L):
        component = fitfun(psi)
        psi = psi + component.psi
        components.append(component)

    diff = jnp.inf
    for i in range(maxiter - 1):
        psi_old = psi
        for l in range(L):
            psi = psi - components[l].psi
            components[l] = fitfun(psi)
            psi = psi + components[l].psi
        # check convergence
        diff = jnp.abs(psi - psi_old).max()
        if diff < tol:
            break
    state = AdditiveState(tol, diff < tol, maxiter, i + 1)
    fit = tree_stack(components)
    return fit, state



# -

X, y = sim(1000, 10000)
fit, state = fit_susie(X, y, 2, serfun, initfun, serkwargs, -1., 2)
fit2, state2 = fit_susie2(X, y, 2, serfun, initfun, serkwargs, -1., 2)

fit.lbf_ser, fit2.lbf_ser

# ### Quick benchmark
# When $p$ is small, the reference implementation is faster. 
# This may be due to the overhead of needing to compile? That would suggest we are recompiling on every call.
# However, as $p$ gets large we see the JAX outer loop is faster.

X, y = sim(100, 10000)
# %time test_new_outer_loop(X, y, 1, 5)
# %time test_gibss_outer_loop(X, y, 1, 5)

X, y = sim(1000, 10000)
# %time test_new_outer_loop(X, y, 1, 5)
# %time test_gibss_outer_loop(X, y, 1, 5)

X, y = sim(10000, 10000)
# %time test_new_outer_loop(X, y, 1, 5)
# %time test_gibss_outer_loop(X, y, 1, 5)

# ### Comparing outputs

# we can use a small simulation here
X, y = sim(1000, 10000)

# %time test_new_outer_loop(X, y, 3, 20)
# %time test_gibss_outer_loop(X, y, 3, 20)

# good agreement after forward selection
# %time fit_fast, fit_fast_state = fit_susie(X, y, 3, serfun, initfun, serkwargs, -1., 1)
# %time fit_slow = gibss_outer_loop(X, y, 3, 1)
fit_fast.lbf_ser, np.array([c.lbf_ser for c in fit_slow])

# 2 iterations
# %time fit_fast, fit_fast_state = fit_susie(X, y, 3, serfun, initfun, serkwargs, -1., 5)
# %time fit_slow = gibss_outer_loop(X, y, 3, 5)
fit_fast.lbf_ser, np.array([c.lbf_ser for c in fit_slow])

# 20 iterations
# %time fit_fast, fit_fast_state = fit_susie(X, y, 3, serfun, initfun, serkwargs, -1., 20)
# %time fit_slow = gibss_outer_loop(X, y, 3, 20)
fit_fast.lbf_ser, np.array([c.lbf_ser for c in fit_slow])

# with jax.profiler.trace("/tmp/jax-trace", create_perfetto_link=True):
#     fit_fast, fit_fast_state = fit_susie(X, y, 3, serfun, initfun, serkwargs, -1., 20)

# with jax.profiler.trace("/tmp/jax-trace", create_perfetto_link=True):
#     fit_slow = gibss_outer_loop(X, y, 3, 20)

from gibss.logisticprofile import fit_logistic_susie
X, y = sim(1000, 10000)
# %time fit = fit_logistic_susie(X, y, L=3, method='hermite_eb', maxiter=10)

fit.lbf_ser

fit.outer_loop_state

a = dict(a=1, b=2)
a.update(dict(c=3))
a

serkwargs0 = dict(m=2)
serkwargs = dict(m=1, prior_variance=1.)
serkwargs.update(serkwargs0)
serkwargs


