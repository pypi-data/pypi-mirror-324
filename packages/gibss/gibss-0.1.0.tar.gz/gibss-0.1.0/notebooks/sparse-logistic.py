# ### Sparse logistic regression

import numpy as np
n=10000
p=1000
X = np.random.binomial(1, 0.1, size=(p, n))
# true effect size of one for X[0]
y = np.random.binomial(1, 1 / (1 + np.exp(-X[0])), size=n)
psi0 = np.zeros_like(y)

from scipy import sparse
X_sp = sparse.csr_matrix(X)

# %%time
from gibss.logistic_sparse import fit_logistic_susie2
from gibss.utils import tree_stack
fit = fit_logistic_susie2(X_sp, y, L=5, maxiter=20, tol=1e-6)
#sers = tree_stack(fit.components[1:])

# +
from gibss.credible_sets import compute_cs
from gibss.logistic import SusieSummary
from gibss.utils import npize

def summarize_susie(fit):
    fixed_effects = np.array(fit.fixed_effect.fit.x)
    alpha = np.array(fit.sers.fit.alpha)
    lbf = np.array(fit.sers.fit.lbf)
    beta = np.array(fit.sers.fit.b)
    prior_variance = np.array(fit.sers.fit.prior_variance)
    lbf_ser = np.array(fit.sers.fit.lbf_ser)
    credible_sets = [compute_cs(a).__dict__ for a in alpha]
    res = SusieSummary(
        fixed_effects,
        alpha,
        lbf,
        beta,
        prior_variance,
        lbf_ser,
        credible_sets,
        npize(fit.state.__dict__)
    )
    return res

fit2 = summarize_susie(fit)
# -

fit2.credible_sets[1]

from jax.tree_util import tree_map
tree_map(type, fit2)

from jax.tree_util import tree_map
from jax import Array


# %%time
from gibss.logistic import fit_logistic_susie2
fit2 = fit_logistic_susie2(X, y, L=5, maxiter=20, prior_variance=1.)

fit.state

sers.fit.lbf_ser[0]

nd = -(sers.fit.optstate.g**2 / sers.fit.optstate.h)

fit2.prior_variance

fit2.lbf[0, 0], sers.fit.lbf[0, 0]

# +
import matplotlib.pyplot as plt 
import numpy as np    

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

sc = plt.scatter(fit2.beta[0], sers.fit.b[0], c=np.log(nd[0]))
abline(1, 0)
plt.colorbar(sc)
plt.show()
# -

sers.fit.alpha.max(1)

sc = plt.scatter(fit2.lbf[1], sers.fit.lbf[1], c=np.log(nd[1]))
abline(1, 0)
plt.colorbar(sc)
plt.show()

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
         data_fields=['x', 'f', 'g', 'h', 'stepsize'], meta_fields=[])
@dataclass
class OptState:
    x: ArrayLike
    f: ArrayLike
    g: ArrayLike
    h: ArrayLike
    stepsize: ArrayLike    
    
@partial(jax.tree_util.register_dataclass,
         data_fields=['b', 'llr', 'lbf', 'alpha', 'pi', 'prior_variance', 'optstate'], meta_fields=[])
@dataclass
class SparseSER:
    b: ArrayLike
    llr: ArrayLike
    lbf: ArrayLike
    alpha: ArrayLike
    pi: ArrayLike
    prior_variance: float
    optstate: OptState
        
def _get_sizes(partition):
    return (jnp.roll(partition, -1) - partition)[:-1]
        
def make_sparse_logistic_ser1d(X_sp, y):
    partition = X_sp.indptr
    sizes = _get_sizes(partition)
    indices = X_sp.indices
    xlong = X_sp.data
    ylong = y[X_sp.indices]
    
    def _splitsum(long):
        cumsum = jnp.cumsum(long)[partition[1:] - 1]
        carry, splitsum = jax.lax.scan(lambda carry, x: (x, x-carry), 0, cumsum)
        return splitsum
        
    def _compute_llr(blong, xlong, ylong, psilong, psi0long, tau=1.0):
        psilong = psi0long + blong
        lrlong = ylong * (psilong - psi0long) \
            - jnp.log(1 + jnp.exp(psilong)) \
            + jnp.log(1 + jnp.exp(psi0long))
        return _splitsum(lrlong)
    
    def decay_stepsize_opt_state(old_opt_state, alpha=0.5):
            return OptState(
                old_opt_state.x,
                old_opt_state.f,
                old_opt_state.g,
                old_opt_state.h,
                old_opt_state.stepsize * alpha
            )
        
    def merge_optstate(old_state, new_state):
        return jax.lax.cond(
                (old_state.f < new_state.f),
                lambda old, new: new,
                lambda old, new: decay_stepsize_opt_state(old, 0.5),
                old_state, new_state
        )
    merge_opstate_vmap = jax.vmap(merge_optstate, 0, 0)
        
    @jax.jit
    def update_b(state, psi0):
        # propose newton step
        psi0long = psi0[indices]
        tau = 1/state.prior_variance
        blong = jnp.repeat(state.b, sizes)
        psilong = psi0long + blong
        plong = 1 / (1 + jnp.exp(-psilong))
        gradlong = (ylong - plong) * xlong
        hesslong = - plong * (1 - plong) * xlong * xlong
        g = (_splitsum(gradlong) - tau * state.b) # gradient of log p(y, b)
        h = (_splitsum(hesslong) - tau) # hessian of logp(y, b) < 0
        update_direction = - g / h
        b = state.b + update_direction * state.optstate.stepsize
        llr = _compute_llr(blong, xlong, ylong, psilong, psi0long, tau) \
            - 0.5 * tau * b**2 + jnp.log(tau) - jnp.log(2 * jnp.pi)
        
        # pick between states
        optstate = OptState(b, llr, g, h, jnp.ones_like(llr))
        optstate = merge_opstate_vmap(state.optstate, optstate)
        
        # ser computations
        lbf = optstate.f \
            + 0.5 * (jnp.log(2 * jnp.pi) - jnp.log(-optstate.h))
        lbf = logsumexp(lbf + jnp.log(state.pi))
        alpha = jnp.exp(lbf - logsumexp(lbf))
        state = SparseResults(optstate.x, optstate.f, lbf, alpha, state.pi, state.prior_variance, optstate)
        return state

    def logistic_ser_1d(psi, fit):
        if fit is None:
            p = X_sp.shape[0]
            opt0 = OptState(np.ones(p), -np.inf * np.ones(p), np.ones(p), np.ones(p), np.ones(p))
            state0 = SparseResults(np.zeros(p), 0, 0, 0, np.ones(p)/p,  1., opt0)
            state = update_b(state0, psi)
        else:
            state = update_b(fit.fit, psi)
        psi = state.alpha * state.b
        return AdditiveComponent(psi, state)
    
    return logistic_ser_1d


# -

logistic_ser_1d = make_sparse_logistic_ser1d(X_sp, y)

fit = None
for i in range(5):
    fit = logistic_ser_1d(np.zeros(X_sp.shape[0]), fit)
    print(f'b={fit.fit.b[0]}')

from gibss.additive import AdditiveComponent
# ?AdditiveComponent

# +
# %%time
psi0long = np.zeros_like(ylong)
opt0 = OptState(np.ones(p), -np.inf * np.ones(p), np.ones(p), np.ones(p), np.ones(p))
state0 = SparseResults(np.zeros(p), 0, 0, 0, np.ones(p)/p,  1., opt0)

state = state0
for _ in range(5):
    state = update_b(state, psi0)
    
    print(f'b={state.b[0]}')
# -

opt0 = OptState(None, None, None, None, np.ones(p)*.6)
state0 = SparseResults(np.ones(p)-4, 0, 0, 0, np.ones(p)/p,  1., opt0)
state = update_b(state0, xlong, ylong, psi0long)
new_state = update_b(state, xlong, ylong, psi0long)
(new_state.llr >= state.llr).sum()

# +

#merge_state_vmap = jax.vmap(merge_state, 0, 0)
# -

merge_opstate_vmap = jax.vmap(merge_optstate, 0, 0)
merged_optstate = merge_opstate_vmap(state.optstate, new_state.optstate)

merged_optstate

merge_state_vmap(state, new_state)

from gibss.logistic import logistic_ser_hermite

# %%time 
serfit = logistic_ser_hermite(np.zeros((X.shape[0], 1)), X, y, 0., newtonkwargs=dict(maxiter=5))
serfit.alpha[0].block_until_ready()

state.logp[:10]

serfit.fits.lbf[:10]

state.b[:10] - serfit.fits.state.x.flatten()[:10]

state.h[:10] + serfit.fits.state.h.flatten()[:10]


