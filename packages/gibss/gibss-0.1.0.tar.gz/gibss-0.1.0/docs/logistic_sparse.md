
# Logistic SuSiE sparse module

When the independent variable in a simple univariate regression problem is sparse, the likelihood ratio will depend only on the observations $i$ with non-zero $x_i$. When we are comparing against a simple null model, the Bayes factor can be expressed as the integrated likelihood ratio over the prior on the regression coefficient. Thus we can compute the posterior summaries for each univariate regression using only the observations with non-zero $X$. When $X$ is very sparse, this reduced data procedure is much faster and more memory efficient.

The `gibss.logistic_sparse` module implements simultaneous optimization of $p$ sparse regression problems. More ore less, you should think of the core of this module as applying Newton's method to $p$ sparse problems simultaneously using efficient sparse matrix computations. However, we wanted to speedups from JIT compilation, and I experienced some friction working with the JAX sparse library (probably user error). Because the updates are quite simple to write, I end up working directly on compressed/flattened data that you would find e.g. in a compressed sparse row (CSR) or compressed sparse column (CSC) format matrix.

### log likelihood ratio

Given the data $({\bf y}, {\bf x}, \psi_0)$ where $y_i \in \{0, 1\}$ is the dependent variable, $x_i \in \mathbb R$ the independent variable, and $\psi_{0i} \in \mathbb R$ a fixed offset term, the logistic log likelihood is
$$
\ell(b) := \log p({\bf y}| b,  {\bf x}, \psi_0) = \sum_i y (bx_i + \psi_{0i}) - \log(1 + \exp(bx_i + \psi_{0i}))
$$

The log likelihood ratio against the null $b=0$ is then

$$
\gamma(b) := \ell(b) - \ell(0) = \sum_{i: x_i \neq 0} y (bx_i + \psi_{0i}) - \log(1 + \exp(bx_i + \psi_{0i}))
$$

We can compute the MAP estimate for $b$ by

$$
\hat b_{\text{MAP}} = \arg \max_b \gamma(b) + \log p(b)
$$

and the Bayes factor comparing the model where $b \sim p$ against the simple null model $b=0$ by

$$
\text{BF} = \int_{\mathbb R} \exp\{\gamma(b)\}p(b) db
$$

### CSR Format
There are various formats for sparse matrices. Here we describe one of them. The compressed sparse row format stores a sparse matrix using vectors. We use the names of attributes from the CSR matrix implementation in `scipy.sparse`. We provide examples for the matrix `X_sp = [[., 1, ., 3, 1], [2, ., ., 4, .]]`.

1. `data` First a data vector which stores all the non-zero elements of the array. Importantly data are stored row by row. So that `X_sp` would have `data = [1, 3, 1, 2, 4]`. 
2. `indices` Is a vector of length equal length to `data`. It contains the column number for each data point. `indices = [1, 3, 4, 0, 3]`
3. `indptr` indicates where in `indices` encode the ranges for each row. `indptr = [0, 3, 5]`. So that `0:3` correspond to the data in the first row, `3:5` in the second.

### Limitations

This implementation works on all of the data at once stored in a single array. It makes a compromise of also making expanded versions of the data `ylong = y[indices]`, `psi0long = pis0[indices]`. For sparse problems with the proportion of non-zero elements $< 1/3$. The tradeoff is terms of total memory usage is good, because the alternative is to represent `X` with a dense matrix.

If you have very large problems, you may consider modifying the approach here to run on subsets of the variables. This strategy would be amenable to parallelization across multiple processes, and does not require storing the entire `X` in a contiguous block of memory.
