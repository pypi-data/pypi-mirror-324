We use JAX to implement a simple, light weight newton optimizer. 
At a high level, the optimizer takes a function to be minimzed, uses JAX to compute the gradient and hessian,
and performs newton steps. 
For convex objectives, the newton *direction* is guarunteed to be a descent direction, meaning that there is a stepsize such that $x_{t+1} = x_t - \beta H_t^{-1}g_t$ will decrease the objective function. We start with a step size of $1$ and decay geometrically by a factor $\alpha \in (0, 1)$ until the function achieved a *sufficient decrease*. That means we require $f(x_{t+1}) < f(x_t) - \gamma ||g||_2^2$. 

The two parameters controlling the behavior of the optimizer are `alpha`, which control the decay of the stepsize in the backtracking line search, and `gamma` which controls the decrease criteria of accepting a proposed move. Selecting $\gamma = -\inf$ corresponds with always accepting the move. When a convex optimization problem is initialized sufficiently close to its optimum it can be shown that a step size of $\beta = 1$ is always decreasing. However, when initialzed far from the optimum there is no guaruntee. 

### Small, negative values of $\gamma$. 
In practice we find that due to numerical stablity issues can cause updates to slightly increase the objective, while substantially decreasing Newton's decrement, which provides an upper bound on the suboptimality of the solution. We monitor convergence by Newton's decrement, so we find it useful to set `gamma` to a small negative value, e.g. $0.1$. In practice, we find this prevents us from divergent behavior at poor initialization, without causing the algorithm to stall.
