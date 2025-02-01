import numpy as np
from scipy.special import logsumexp
from scipy.stats import norm
from gibss.logistic import SusieFit
from gibss.utils import tree_stack
from gibss.additive import fit_additive_model, update_additive_model
from gibss.logistic_sparse import make_fixed_fitfun, make_sparse_logistic_ser1d
from jax.tree_util import Partial


def categorical_kl(pi1, pi2):
    return np.sum(np.log(pi1 / pi2, where=(pi1 != 0)) * pi1)


def categorical_kl_sym(pi1, pi2):
    return categorical_kl(pi1, pi2) + categorical_kl(pi2, pi1)


Estep = lambda Gamma: np.exp(Gamma - logsumexp(Gamma, 1)[:, None])


def em_g_normal_mixture(betahat, shat, sigma_grid, pi_init=None, maxiter=1000):
    component_log_marginal = norm.logpdf(
        betahat[:, None], scale=np.sqrt((sigma_grid**2)[None] + (shat**2)[:, None])
    )
    if pi_init is None:
        pi_init = np.ones(len(sigma_grid)) / len(sigma_grid)
    pi = pi_init
    log_marginals = []
    for _ in range(maxiter):
        pi_old = pi
        Gamma = Estep(component_log_marginal + np.log(pi)[None])
        pi = Gamma.mean(0)  # M-step
        kl = categorical_kl_sym(pi_old, pi)
        if kl < 1e-10:
            break
        ell = logsumexp(component_log_marginal + np.log(pi)[None], 1)
        log_marginals.append(ell.sum())
    return pi, ell, component_log_marginal, log_marginals


def covariate_moderated_normal_mixture_logistic_susie_sparse(
    betahat,
    shat,
    X_sp,
    L=10,
    maxiter=100,
    sigma_grid=None,
    prior_variance=1.0,
    alpha=0.8,
    gamma=0.0,
):
    # fit a scale mixture of normals
    if sigma_grid is None:
        sigma_grid = np.cumprod(np.ones(12) * np.sqrt(2)) / 4
    pi, ell, component_log_marginal_g, log_marginals = em_g_normal_mixture(
        betahat, shat, sigma_grid
    )
    # use the larger components as alternative density (assuming small/null effect contribute mostly to the smallest componenet, but if the grid is too dense this may not be true)
    pi1 = pi[1:] / np.sum(pi[1:])
    L1 = logsumexp(component_log_marginal_g[:, 1:] + np.log(pi1)[None], 1)
    component_log_marginal = np.array([norm.logpdf(betahat, 0.0, shat), L1]).T

    # attach y to base fit funs on the fly
    base_fitfun = make_sparse_logistic_ser1d(X_sp, prior_variance, alpha, gamma)
    base_fixedfitfun = make_fixed_fitfun()

    def fitfuns(y):
        return [Partial(base_fixedfitfun, y=y)] + [
            Partial(base_fitfun, y=y) for _ in range(L)
        ]

    # Do EM for mixture model, in the M step update SuSiE fits.
    pi = np.ones((betahat.size, 2)) * 0.5
    Gamma = Estep(component_log_marginal + np.log(pi))
    y = Gamma[:, 1]  # get new data
    model = fit_additive_model(fitfuns(y))
    pi1 = 1 / (1 + np.exp(-model.psi))
    pi = np.array([1 - pi1, pi1]).T
    for _ in range(maxiter):
        pi_old = pi
        Gamma = Estep(component_log_marginal + np.log(pi))
        y = Gamma[:, 1]  # get new data
        model.fit_functions = fitfuns(y)
        model = update_additive_model(model, maxiter=5)
        pi1 = 1 / (1 + np.exp(-model.psi))
        pi = np.array([1 - pi1, pi1]).T
        kl = categorical_kl_sym(pi_old, pi)
        if kl < 1e-4:
            break

    fixed_effect = model.components[0]
    sers = tree_stack(model.components[1:])
    fit = SusieFit(fixed_effect, sers, model.state)
    return fit
