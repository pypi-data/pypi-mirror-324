import numpy as np
import cvxpy as cp
from .portfolio_exceptions import ValidationError, OptimizationError


def validate_inputs(H, r_t, portfolio, gamma_t, psi_t, phi_trade, phi_hold):
    """Validate input parameters for multi-period optimization"""
    if not isinstance(H, int) or H <= 1:
        raise ValidationError(
            "Invalid horizon parameter", details=f"H must be integer > 1, got {H}"
        )

    n_assets = len(portfolio.weights_vector)

    if not isinstance(r_t, np.ndarray) or r_t.shape[0] != H:
        raise ValidationError(
            "Invalid returns matrix",
            details=f"Expected shape ({H}, n_assets), got {r_t.shape}",
        )

    if not isinstance(gamma_t, (list, np.ndarray)) or len(gamma_t) != H:
        raise ValidationError(
            "Invalid risk aversion parameters",
            details=f"Expected length {H}, got {len(gamma_t)}",
        )

    if not isinstance(psi_t, (list, np.ndarray)) or len(psi_t) != H:
        raise ValidationError(
            "Invalid risk factors", details=f"Expected length {H}, got {len(psi_t)}"
        )

    if not isinstance(phi_trade, (list, np.ndarray)) or len(phi_trade) != H:
        raise ValidationError(
            "Invalid trading costs",
            details=f"Expected length {H}, got {len(phi_trade)}",
        )

    if not isinstance(phi_hold, (list, np.ndarray)) or len(phi_hold) != H:
        raise ValidationError(
            "Invalid holding costs", details=f"Expected length {H}, got {len(phi_hold)}"
        )

    if not isinstance(H, int) or H <= 1:
        raise ValidationError(
            "Invalid horizon parameter", details=f"H must be integer > 1, got {H}"
        )

    if np.any(gamma_t < 0):  # Add validation for negative gamma
        raise ValidationError(
            "Invalid risk aversion parameters",
            details=f"Risk aversion must be non-negative",
        )


def multi_period_optimization(H, r_t, portfolio, gamma_t, psi_t, phi_trade, phi_hold):
    """
    Multi-period portfolio optimization.

    Args:
        H: Number of periods
        r_t: Returns matrix
        portfolio: Portfolio object
        gamma_t: Risk aversion parameters
        psi_t: Risk factors
        phi_trade: Trading costs
        phi_hold: Holding costs

    Returns:
        numpy.ndarray: Optimal trade vectors

    Raises:
        ValidationError: If input parameters are invalid
        OptimizationError: If optimization fails
    """
    try:
        validate_inputs(H, r_t, portfolio, gamma_t, psi_t, phi_trade, phi_hold)

        # Check for numerical issues
        if np.any(np.isinf(r_t)) or np.any(np.isnan(r_t)):
            raise OptimizationError(
                "Invalid returns matrix", details="Contains infinite or NaN values"
            )

        if np.any(np.isinf(psi_t)) or np.any(np.isnan(psi_t)):
            raise OptimizationError(
                "Invalid risk factors", details="Contains infinite or NaN values"
            )

        n_assets = len(portfolio.weights_vector)
        z = cp.Variable((n_assets, H - 1))

        constraints = []
        objective_terms = []
        prev_w = portfolio.weights_vector

        for i in range(1, H):
            try:
                cur_w = prev_w + z[:, i - 1]

                expected_return = cp.matmul(r_t[i], cur_w)
                risk = gamma_t[i] * cp.sum(cp.multiply(psi_t[i], cp.square(cur_w)))
                holding_cost = cp.sum(cp.multiply(phi_hold[i], cur_w))
                transaction_cost = cp.sum(
                    cp.multiply(phi_trade[i], cp.abs(z[:, i - 1]))
                )

                objective_terms.append(
                    expected_return - risk - holding_cost - transaction_cost
                )
                constraints.append(cp.sum(cur_w) == 1)
                prev_w = cur_w

            except Exception as e:
                raise OptimizationError(f"Error in period {i}", details=str(e))

        objective = cp.Maximize(cp.sum(objective_terms))
        problem = cp.Problem(objective, constraints)

        if not problem.is_dcp():
            raise OptimizationError("Problem does not satisfy DCP rules")

        try:
            problem.solve()
            if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
                raise OptimizationError(
                    "Optimization failed", details=f"Solver status: {problem.status}"
                )
            return z.value

        except cp.error.SolverError as e:
            raise OptimizationError("Solver error", details=str(e))

    except (ValidationError, OptimizationError):
        raise
    except Exception as e:
        raise OptimizationError("Unexpected optimization error", details=str(e))
