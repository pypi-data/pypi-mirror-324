# ### Sparse logistic regression

import numpy as np
n=100000
p=10000
X = np.random.binomial(1, 0.1, size=(p, n))
# true effect size of one for X[0]
y = np.random.binomial(1, 1 / (1 + np.exp(-X[0])), size=n)
psi0 = np.zeros_like(y)

from scipy import sparse
X_sp = sparse.csr_matrix(X)

# +
# a flat array of values
X_sp.data[:10]

# a flat array indicating the column of each observation
X_sp.indices[:5], X_sp[0, X_sp.indices[:5]].toarray()

# index into the start of each row.
X_sp.indptr
# -

# make a list where each entry corresponds to a row
# each entry has the non-zero indices of the row
adj = np.split(X_sp.indices, X_sp.indptr)[1:]
[np.allclose(X[i, adj[i]], 1.) for i in range(10)]

# We can check that the MAP estimates for the big problem are the same as the MAP estimates for the small problem. We show for the causal variable `X[0]` and for a null variable `X[1]`

# +
from gibss.newton import newton_factory
from gibss.logistic import nloglik1d

idx = adj[0]
l1 = lambda b: nloglik1d(b, X[0, idx], y[idx], psi0[idx])
solver1 = newton_factory(l1)
fit1 = solver1(np.zeros(1))

l2 = lambda b: nloglik1d(b, X[0], y, psi0)
solver2 = newton_factory(l2)
fit2 = solver2(np.zeros(1))
fit1.x, fit2.x

# +
idx = adj[1]
l1 = lambda b: nloglik1d(b, X[1, idx], y[idx], psi0[idx])
solver1 = newton_factory(l1)
fit1 = solver1(np.zeros(1))

l2 = lambda b: nloglik1d(b, X[1], y, psi0)
solver2 = newton_factory(l2)
fit2 = solver2(np.zeros(1))
fit1.x, fit2.x
# -

# Although notice that solving the smaller problem, despite only requiring 10% of the data is not acutally much faster when using the JIT compiled code.

# %%timeit
fit1 = solver1(np.zeros(1)).x.block_until_ready()

# %%timeit
fit2 = solver2(np.zeros(1)).x.block_until_ready()

# Here we see that for Compressed row formate row operations are much faster than column operations.

# %%timeit 
# row sums
X_sp[0].sum()

# %%timeit 
# column sums
X_sp[:, 0].sum()

# ### Flattened implementation
# For a univariate logistic regression computing the liklelihood ratio against $b=0$, graident, and hessian only depend on the indices with nonzero $x$. Here we flatten the problem of solving $p$ sparse problems.
#
# ylong = y[X_sp.indices]
# xlong = X_sp.data
# psi0long = psi[X_sp.indices]
# partition = X_sp.indptr
# sizes = (np.roll(partition, -1) - partition)[:-1]

import numpy as np
indices = X_sp.indices
partition = X_sp.indptr
sizes = (np.roll(partition, -1) - partition)[:-1]


# +
def expand_b(bs, sizes):
    return np.concatenate([np.ones(m) * b for b, m in zip(bs, sizes)])

def split_sum(long, partition):
    return np.array([x.sum() for x in np.split(long, partition)[1:-1]])


# -

# test split_sum
bs = np.ones(p)
b = expand_b(bs, sizes)
#split_sum(b, partition) - sizes

def compute_lr(b, xlong, ylong, psi0long, tau=1.0):
    blong = expand_b(b, sizes)
    psilong = psi0long + blong
    lrlong = ylong * (psilong - psi0long) \
        - np.log(1 + np.exp(psilong)) \
        + np.log(1 + np.exp(psi0long))
    return split_sum(lrlong, partition) -0.5 * tau * b**2 + np.log(tau) - np.log(2 * np.pi)


def update_b(b, xlong, ylong, psi0long, tau=1.0):
    blong = expand_b(b, sizes)
    psilong = psi0long + blong
    lrlong = ylong * (psilong - psi0long) \
        - np.log(1 + np.exp(psilong)) \
        + np.log(1 + np.exp(psi0long)) 
        #-0.5 * tau * blong**2 + np.log(tau) - np.log(2 * np.pi)
    plong = 1 / (1 + np.exp(-psilong))
    gradlong = (ylong - plong) * xlong
    hesslong = - plong * (1 - plong) * xlong * xlong
    update_direction = -(split_sum(gradlong, partition) - tau * b) / (split_sum(hesslong, partition) - tau)
    return b + update_direction


xlong = X_sp.data
ylong = y[X_sp.indices]
psi0long = np.zeros_like(ylong)
b = np.zeros(p)

# %%time
for _ in range(3):
    b = update_b(b, xlong, ylong, psi0long, tau=1.0)
    print(f'b={b[0]}')

# ### Flattened implementation, jax
#
# Now can we make this faster with jax?

import jax.numpy as jnp
import jax
from functools import partial
import jax.numpy as jnp
import jax


@jax.jit
def update_b(b, xlong, ylong, psi0long, partition, tau=1.0):
    blong = jnp.repeat(b, sizes)
    psilong = psi0long + blong
    plong = 1 / (1 + jnp.exp(-psilong))
    gradlong = (ylong - plong) * xlong
    hesslong = - plong * (1 - plong) * xlong * xlong
    update_direction = -(split_sum2(gradlong, partition) - tau * b) / (split_sum2(hesslong, partition) - tau)
    return b + update_direction


# %%time
xlong = X_sp.data
ylong = y[X_sp.indices]
psi0long = np.zeros_like(ylong)
b = np.zeros(p)
for _ in range(5):
    b = update_b(b, xlong, ylong, psi0long, partition, tau=1.0)
    print(f'b={b[0]}')

# +
import jax.numpy as jnp
import jax
from functools import partial
import jax.numpy as jnp
import jax
from dataclasses import dataclass
from jax.typing import ArrayLike
from jax.scipy.special import logsumexp

@partial(jax.tree_util.register_dataclass,
         data_fields=['b', 'g', 'h', 'llr', 'lbf', 'alpha', 'pi', 'prior_variance', 'stepsize'], meta_fields=[])
@dataclass
class SparseResults:
    b: ArrayLike
    g: ArrayLike
    h: ArrayLike
    llr: ArrayLike
    lbf: ArrayLike
    alpha: ArrayLike
    pi: ArrayLike
    prior_variance: float
    stepsize: ArrayLike

@jax.jit
def _splitsum(long):
    cumsum = jnp.cumsum(long)[partition[1:] - 1]
    carry, splitsum = jax.lax.scan(lambda carry, x: (x, x-carry), 0, cumsum)
    return splitsum
    
@jax.jit    
def _get_sizes(partition):
    return (jnp.roll(partition, -1) - partition)[:-1]
    
def _compute_llr(blong, xlong, ylong, psilong, psi0long, tau=1.0):
    psilong = psi0long + blong
    lrlong = ylong * (psilong - psi0long) \
        - jnp.log(1 + jnp.exp(psilong)) \
        + jnp.log(1 + jnp.exp(psi0long))
    return _splitsum(lrlong)

@jax.jit
def update_b(state, xlong, ylong, psi0long):
    tau = 1/state.prior_variance
    blong = jnp.repeat(state.b, sizes)
    psilong = psi0long + blong
    plong = 1 / (1 + jnp.exp(-psilong))
    gradlong = (ylong - plong) * xlong
    hesslong = - plong * (1 - plong) * xlong * xlong
    g = (_splitsum(gradlong) - tau * state.b) # gradient of log p(y, b)
    h = (_splitsum(hesslong) - tau) # hessian of logp(y, b) < 0
    update_direction = - g / h
    b = state.b + update_direction * state.stepsize
    llr = _compute_llr(blong, xlong, ylong, psilong, psi0long, tau)
    lbf = (llr - 0.5 * tau * b**2 + jnp.log(tau) - jnp.log(2 * jnp.pi)) \
        + 0.5 * (jnp.log(2 * jnp.pi) - jnp.log(-h))
    lbf = logsumexp(lbf + jnp.log(state.pi))
    alpha = jnp.exp(lbf - logsumexp(lbf))
    proposed_state = SparseResults(b, g, h, llr, lbf, alpha, state.pi, state.prior_variance, 1.)


# +
# %%time
xlong = X_sp.data
ylong = y[X_sp.indices]
psi0long = np.zeros_like(ylong)
state0 = SparseResults(np.zeros(p), 0, 0, 0, 0, 0, np.ones(p)/p,  1., 1.)
partition = X_sp.indptr
sizes = _get_sizes(partition)

state = state0
for _ in range(5):
    state = update_b(state, xlong, ylong, psi0long)
    print(f'b={state.b[0]}')
# -

state0 = SparseResults(np.ones(p)-4, 0, 0, 0, 0, 0, np.ones(p)/p,  1., .6)
state = update_b(state0, xlong, ylong, psi0long)
new_state = update_b(state, xlong, ylong, psi0long)
(new_state.llr > state.llr).sum()


def decay_stepsize(old_state):
    return SparseResult(
        old_state.b,
        old_state.g,
        old_state.h,
        old_state.llr,
        old_state.lbf,
        old_state.alpha,
        old_state.pi,
        old_state.prior_variance,
        old_state.stepsize / 2,
    )
def merge_state(old_state, new_state):
    
    jax.lax.cond(old_state.llr =< new_state.llr,
                 new_state, 



from gibss.logistic import logistic_ser_hermite

# %%time 
serfit = logistic_ser_hermite(np.zeros((X.shape[0], 1)), X, y, 0., newtonkwargs=dict(maxiter=5))
serfit.alpha[0].block_until_ready()

state.logp[:10]

serfit.fits.lbf[:10]

state.b[:10] - serfit.fits.state.x.flatten()[:10]

state.h[:10] + serfit.fits.state.h.flatten()[:10]


