import numpy as np
import cvxpy as cp
from .portfolio_exceptions import ValidationError, OptimizationError


def validate_inputs(r_t, w_t, gamma):
    """Validate input parameters"""
    if not isinstance(r_t, (list, np.ndarray)):
        raise ValidationError(
            "Expected returns must be a numpy array or list", details=f"Got {type(r_t)}"
        )

    if not isinstance(w_t, (list, np.ndarray)):
        raise ValidationError(
            "Portfolio weights must be a numpy array or list",
            details=f"Got {type(w_t)}",
        )

    if len(r_t) != len(w_t):
        raise ValidationError(
            "Dimension mismatch between returns and weights",
            details=f"Returns: {len(r_t)}, Weights: {len(w_t)}",
        )

    if gamma < 0:
        raise ValidationError(
            "Risk aversion parameter must be non-negative", details=f"Got gamma={gamma}"
        )


def validate_cost_functions(trade_cost, hold_cost):
    """Validate that cost functions return valid CVXPY expressions"""
    if not isinstance(trade_cost, cp.Expression):
        raise OptimizationError(
            "Invalid cost functions",
            details="Trading cost must return CVXPY expression",
        )
    if not isinstance(hold_cost, cp.Expression):
        raise OptimizationError(
            "Invalid cost functions",
            details="Holding cost must return CVXPY expression",
        )


def single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold):
    """
    Solve single-period portfolio optimization problem.

    Args:
        r_t: Expected returns vector
        w_t: Current portfolio weights
        gamma: Risk aversion parameter
        phi_trade: Trading cost function
        phi_hold: Holding cost function

    Returns:
        numpy.ndarray: Optimal trade vector

    Raises:
        ValidationError: If input parameters are invalid
        OptimizationError: If optimization problem fails
    """
    try:
        validate_inputs(r_t, w_t, gamma)

        # Check for numerical issues
        if np.any(np.isinf(r_t)) or np.any(np.isnan(r_t)):
            raise OptimizationError(
                "Invalid returns", details="Contains infinite or NaN values"
            )

        n = len(r_t)
        z_t = cp.Variable(n)

        # Validate objective function components
        try:
            trade_cost = 0.01 * phi_trade(z_t)
            hold_cost = 0.01 * phi_hold(w_t + z_t)
            validate_cost_functions(trade_cost, hold_cost)
        except Exception as e:
            raise OptimizationError("Invalid cost functions", details=str(e))

        trade_cost = 0.01 * phi_trade(z_t)
        hold_cost = 0.01 * phi_hold(w_t + z_t)

        sigma_t = np.eye(n)
        risk = gamma * (cp.quad_form(w_t + z_t, sigma_t) / n)

        objective = cp.Maximize(r_t.T @ z_t - risk - trade_cost - hold_cost)

        constraints = [cp.sum(w_t + z_t) == 1, z_t >= -w_t]

        if np.allclose(r_t, 0):
            constraints.append(cp.norm(z_t, 1) <= 1e-3)

        problem = cp.Problem(objective, constraints)

        if not problem.is_dcp():
            raise OptimizationError("Problem does not satisfy DCP rules")

        try:
            problem.solve()

            if problem.status == cp.OPTIMAL:
                return z_t.value
            else:
                raise OptimizationError(
                    "Optimization failed", details=f"Solver status: {problem.status}"
                )

        except cp.error.SolverError as e:
            raise OptimizationError("Solver failed", details=str(e))

    except (ValidationError, OptimizationError):
        raise
    except Exception as e:
        raise OptimizationError("Unexpected error during optimization", details=str(e))
