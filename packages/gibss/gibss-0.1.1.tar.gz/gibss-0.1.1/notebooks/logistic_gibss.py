#%%
import numpy as np
from gibss.logisticprofile import logistic_susie
from gibss.logisticprofile import logistic_ser_hermite
from gibss.logisticprofile import initialize_coef
from gibss.logisticprofile import fit_null
from gibss.utils import todict

np.random.seed(3)
X = np.random.normal(size = (500, 2000))
x = X[0]
y = np.random.binomial(1, 1/(1 + np.exp(-(-1 + 0.5 * x))))
offset = 0.
prior_variance = 1.
nullfit = fit_null(y, 0.)

#%%
from gibss.logisticprofile import initialize_coef, logistic_ser_hermite, logistic_ser_lapmle, logistic_ser_wakefield, logistic_ser_lapmle_eb, logistic_ser_wakefield_eb
coef_init = initialize_coef(X, y, 0, 1.)
a = logistic_ser_hermite(coef_init, X, y, offset, prior_variance, m=5, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)
b = logistic_ser_wakefield(coef_init, X, y, offset, prior_variance, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)
c = logistic_ser_lapmle(coef_init, X, y, offset, prior_variance, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)
d = logistic_ser_wakefield_eb(coef_init, X, y, offset, prior_variance, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)
e = logistic_ser_lapmle_eb(coef_init, X, y, offset, prior_variance, maxiter=50, tol=1e-3, alpha=0.5, gamma=0.0)

#%%
A = logistic_susie(X, y, L=3, prior_variance=1, maxiter=10, tol=1e-3, method='hermite', serkwargs=dict(m=1, tol=1e-5))
B = logistic_susie(X, y, L=3, prior_variance=1, maxiter=10, tol=1e-3, method='lapmle', serkwargs=dict(tol=1e-5))
C = logistic_susie(X, y, L=3, prior_variance=1, maxiter=10, tol=1e-3, method='wakefield', serkwargs=dict(tol=1e-5))
D = logistic_susie(X, y, L=3, prior_variance=1, maxiter=10, tol=1e-3, method='lapmle_eb', serkwargs=dict(tol=1e-5))
E = logistic_susie(X, y, L=3, prior_variance=1, maxiter=10, tol=1e-3, method='wakefield_eb', serkwargs=dict(tol=1e-5))

#%%
import numpy as np
lbf = lambda fit: np.array([x.lbf_ser for x in fit.components])
prior_variance = lambda fit: np.array([x.prior_variance for x in fit.components])
alpha_max = lambda fit: np.array([x.alpha.max() for x in fit.components])
idx_max = lambda fit: np.array([x.alpha.argmax() for x in fit.components])

for fit in [A, B, C, D, E]:
    print(lbf(fit))
    print(prior_variance(fit))
    print(alpha_max(fit))
    print(idx_max(fit))
    print('')

#%%
from gibss.newton import newton_factory
from gibss.logisticprofile import nloglik_mle
from functools import partial
prnt = lambda x: print(f'x= {x.x}, \nf= {x.f}, \ng= {x.g}, \nnd= {x.nd}, \nstepsize= {x.stepsize}, \niter= {x.iter}')

results = {} 
for i in range(100):
    x0 = np.random.normal(size=x.size)
    loss = partial(nloglik_mle, x=x0, y=y, offset=0.)
    optimizer = newton_factory(loss, maxiter=100, tol=1e-10, alpha=0.8, gamma=0.0)
    param0 = np.zeros(2)
    param0[0] = np.log(y.mean()) - np.log(1 - y.mean())
    res = optimizer(param0)
    prnt(res)
    results[i] = dict(state=res, x0=x0, param0=param0)

#%%
nds = np.array([r['state'].nd for r in results.values()])
idx = nds.argmax()
results[idx]['state'].nd

x0 = results[idx]['x0']
param0 = results[idx]['param0']


#%%
from gibss.logisticprofile import fit_null, wakefield, logistic_ser_wakefield
from jax.tree_util import Partial

nullfit = fit_null(y, 0.)
wakefield(np.zeros(2), x, y, 0., 1., nullfit, 50)
coef_init = initialize_coef(X, y, 0, 1.)
serfit_wakefield1 = logistic_ser_wakefield(np.zeros_like(coef_init), X, y, 0., 100.0, maxiter=50, tol=1e-5, gamma=0.5, alpha=0.)
serfit_wakefield2 = logistic_ser_wakefield(coef_init, X, y, 0., 100.0, maxiter=50)

#%%

#%%
from gibss.logisticprofile import nloglik_mle
from jax.tree_util import Partial
nd_diffs = serfit_wakefield1.fits.state.nd - serfit_wakefield2.fits.state.nd
idx = np.abs(nd_diffs).argmax()
print(nd_diffs.max())
fit1 = wakefield(np.zeros(2), X[idx], y, 0., 100, nullfit, 50)
fit2 = wakefield(np.array([np.log(y.mean()) - np.log(1 - y.mean()), 0.0]), X[idx], y, 0., 100, nullfit, 50)
loss = Partial(nloglik_mle, x=X[idx], y=y, offset=0.)

#%%
def newton_save_iterates(x0, fun, niter=10):
    grad = jax.grad(fun)
    hess = jax.hessian(fun)
    step = partial(newton_step, fun=fun, grad=grad, hess=hess)
    state = NewtonState(x0, fun(x0), grad(x0), hess(x0), 1.0, np.inf, 1e-3, False, niter, 0)
    states = []
    for i in range(niter):
        state = step(state)
        states.append(state)
    return states

#%%
from functools import partial
from gibss.newton import NewtonState, newton_step
import jax

def newton_save_iterates(x0, fun, niter=10):
    grad = jax.grad(fun)
    hess = jax.hessian(fun)
    step = partial(newton_step, fun=fun, grad=grad, hess=hess)
    state = NewtonState(x0, fun(x0), grad(x0), hess(x0), 1.0, np.inf, 1e-3, False, niter, 0)
    states = []
    for i in range(niter):
        state = step(state)
        states.append(state)
    return states

n1 = newton_save_iterates(np.zeros(2), loss, 50)
n2 = newton_save_iterates(np.array([np.log(y.mean()) - np.log(1 - y.mean()), 0.0]), loss, 50)

n1x = np.array([s.x for s in n1])
n2x = np.array([s.x for s in n2])
#%%
print(f'nd= {serfit_wakefield1.fits.state.nd[idx]}, {serfit_wakefield2.fits.state.nd[idx]}')
print(f'iter = {serfit_wakefield1.fits.state.iter[idx]}, {serfit_wakefield2.fits.state.iter[idx]}')
print(f'f = {serfit_wakefield1.fits.state.f[idx]}, {serfit_wakefield2.fits.state.f[idx]}')


#%%
print(f'nd= {fit1.state.nd}, {fit2.state.nd}')
print(f'iter= {fit1.state.iter}, {fit2.state.iter}')
print(f'f= {fit1.state.f}, {fit2.state.f}')
print(f'x= {fit1.state.x}, {fit2.state.x}')
print(f'g= {fit1.state.g}, {fit2.state.g}')
print(f'h= {np.diag(fit1.state.h)}, {np.diag(fit2.state.h)}')

#%%
def prnt(state):
    print(f'nd= {state.nd}, iter= {state.iter}, stepsize= {state.stepsize} \nf= {state.f},\nx= {state.x},\ng= {state.g},\nh= {np.diag(state.h)}\n')

prnt(n2[0])
prnt(n2[20])
#%%
from functools import partial
from gibss.ser import ser
import jax

@partial(jax.jit, static_argnames = ['maxiter'])
def logistic_ser_wakefield(coef_init, X, y, offset, prior_variance, maxiter=50):
    vwakefield = jax.vmap(Partial(wakefield, maxiter=maxiter), in_axes=(0, 0, None, None, None, None))
    return ser(coef_init, X, y, offset, prior_variance, vwakefield, fit_null)

vwakefield = jax.vmap(Partial(wakefield, maxiter=50), in_axes=(0, 0, None, None, None, None))
@partial(jax.jit, static_argnames = ['maxiter'])
def logistic_ser_wakefield2(coef_init, X, y, offset, prior_variance, maxiter=50):
    return ser(coef_init, X, y, offset, prior_variance, vwakefield, fit_null)

logistic_ser_wakefield(coef_init, X, y, 0., 1.0)
logistic_ser_wakefield2(coef_init, X, y, 0., 1.0)
#%%
%timeit logistic_ser_wakefield(coef_init, X, y, 0., 1.0)
%timeit logistic_ser_wakefield2(coef_init, X, y, 0., 1.0)




#%%
grad = jax.grad(loss)
hess = jax.hessian(loss)

nd = lambda x: grad(x) @ hess(x) @ grad(x)/2

fit1 = wakefield(np.zeros(2), X[94], y, 0., 1., nullfit, 50)
ci = initialize_coef(X[94][None], y, 0., 100.)[0]
fit2 = wakefield(ci, X[94], y, 0., 1., nullfit, 50)
loss(np.zeros(2)), loss(fit1.state.x), loss(fit2.state.x)
nd(fit1.state.x), nd(fit2.state.x)

#%%
import numpy as np
import matplotlib.pyplot as plt

X, Y = np.meshgrid(
    np.linspace(-0.001, 0.001, 20) + fit1.state.x[0],
    np.linspace(-0.001, 0.001, 20) + fit1.state.x[1]
)
Z = loss(fit1.state.x) - jax.vmap(jax.vmap(loss))(np.stack([X, Y], axis=-1))
plt.contourf(X, Y, Z, levels=20)
plt.colorbar()

#%%
import optax
import jax
import jax.numpy as jnp
f = loss
solver = optax.lbfgs()
params = coef_init[0]
print('Objective function: ', f(params))
opt_state = solver.init(params)
value_and_grad = optax.value_and_grad_from_state(f)
for _ in range(20):
  value, grad = value_and_grad(params, state=opt_state)
  updates, opt_state = solver.update(
     grad, opt_state, params, value=value, grad=grad, value_fn=f
  )
  params = optax.apply_updates(params, updates)
  print('Objective function: ', f(params))

#%%
from gibss.logisticprofile import logistic_ser_hermite
serfit_hermite = logistic_ser_hermite(coef_init, X, y, 0., 100.0, 1)
#%%
coef_init = initialize_coef(X, y, 0, 1.)
serfit = logistic_ser_hermite(coef_init, X, y, 0., 1.0, 5)

#%%
from gibss.logisticprofile import logistic_ser_lapmle
from gibss.logisticprofile import logistic_ser_lapmle_eb
serfit_eb = logistic_ser_lapmle_eb(coef_init, X, y, 0., 100.0)
serfit = logistic_ser_lapmle(coef_init, X, y, 0., 100.0)

#%%
from gibss.logisticprofile import logistic_ser_wakefield
from gibss.logisticprofile import logistic_ser_wakefield_eb
serfit_eb_wakefield = logistic_ser_lapmle_eb(coef_init, X, y, 0., 100.0)
serfit_wakefield = logistic_ser_lapmle(coef_init, X, y, 0., 100.0)

#%%
y2 = np.random.binomial(1, np.mean(y) * np.ones_like(y))
serfit_eb = logistic_ser_lapmle_eb(coef_init, X, y2, 0., 100.0)
serfit = logistic_ser_lapmle(coef_init, X, y2, 0., 100.0)

#%%
susiefit = logistic_susie(X, y, L=1, maxiter=1, tol=1e-5)
susiedict = todict(susiefit) 

#%%
susiefit = logistic_susie(X, y, L=3, maxiter=10, tol=1e-5, method='lapmle')
susiedict = todict(susiefit) 

#%%
susiefit = logistic_susie(X, y, L=3, maxiter=50, tol=1e-5, method='lapmle_eb')
susiedict = todict(susiefit) 

    #%%
alpha = np.array([c.alpha for c in susiefit.components])
alpha.argmax(1)
alpha.max(1)

#%%
from gibss.logisticprofile import logistic_ser_lapmle_eb
serfun = logistic_ser_lapmle_eb
ser1 = serfun(coef_init, X, y, np.zeros_like(y), 1.0)
ser2 = serfun(coef_init, X, y, ser1.psi, 1.0)
ser3 = serfun(coef_init, X, y, ser1.psi + ser2.psi, 1.0)

for i in range(10):
    ser1 = serfun(coef_init, X, y, ser2.psi + ser3.psi, 1.0)
    ser2 = serfun(coef_init, X, y, ser1.psi + ser3.psi, 1.0)
    ser3 = serfun(coef_init, X, y, ser1.psi + ser2.psi, 1.0)

#%%
susiefit = logistic_susie(X, y, L=10, maxiter=50, tol=1e-5)
susiedict = todict(susiefit) 

# %%
from gibss.logisticprofile import initialize_coef, logistic_ser_hermite
coef_init = initialize_coef(X, y, 0., prior_variance)
component = logistic_ser_hermite(coef_init, X, y, np.zeros_like(y), 1e-10)

def fit_ser(psi, old_component):
    coef_init = old_component.fits.params
    # TODO: can we estimate the prior variance here using the last fit?
    # So at each iteration we fit with a fixed prior variance,
    # but we give the opportuity to update the prior variance before the next iteration.
    return logistic_ser_hermite(coef_init, X, y, psi, prior_variance)

component2 = fit_ser(-component.psi, component)


#%%
from gibss.gibss import gibss, gibss2
from gibss.logisticprofile import logistic_ser_lapmle_eb, initialize_coef

#%%
fit1 = gibss(X, y, L=3, maxiter=10, initfun=initialize_coef, serfun=logistic_ser_lapmle_eb, tol=1e-5)

#%%
fit2 = gibss2(X, y, L=3, maxiter=10, initfun=initialize_coef, serfun=logistic_ser_lapmle_eb, tol=1e-5)

# %%
fit3 = logistic_susie(X, y, L=3, maxiter=10, tol=1e-5, method='lapmle_eb')

# %%
fit4 = gibss(X, y, 3, 1.0, 10, 1e-5, initialize_coef, logistic_ser_lapmle_eb)

# %%
