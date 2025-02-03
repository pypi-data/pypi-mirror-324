import pytest
import numpy as np
import cvxpy as cp
from datetime import datetime
from ConvexTrader.Portfolio import Portfolio
from ConvexTrader.Trade import Trade, TradeType
from ConvexTrader.single_period_optimization import single_period_optimization
from ConvexTrader.portfolio_exceptions import ValidationError, OptimizationError


@pytest.fixture
def sample_portfolio():
    portfolio = Portfolio()
    trades = [
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY),
        Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.BUY),
        Trade("MSFT", 75, 300.0, datetime(2023, 1, 3), TradeType.BUY),
    ]
    for trade in trades:
        portfolio.execute_trade(trade)
    return portfolio


def test_single_period_optimization_basic(sample_portfolio):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = sample_portfolio.weights_vector
    gamma = 1.0

    def phi_trade(z):
        return cp.sum(cp.abs(z))

    def phi_hold(w):
        return cp.sum(cp.square(w))

    result = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    assert result is not None
    assert len(result) == len(w_t)


def test_validation_errors():
    w_t = np.array([0.5, 0.5])
    gamma = 1.0

    def phi_trade(z):
        return cp.sum(cp.abs(z))

    def phi_hold(w):
        return cp.sum(cp.square(w))

    # Test invalid returns type
    with pytest.raises(ValidationError, match="Expected returns must be"):
        single_period_optimization("invalid", w_t, gamma, phi_trade, phi_hold)

    # Test invalid weights type
    with pytest.raises(ValidationError, match="Portfolio weights must be"):
        single_period_optimization(
            np.array([0.1, 0.2]), "invalid", gamma, phi_trade, phi_hold
        )

    # Test dimension mismatch
    with pytest.raises(ValidationError, match="Dimension mismatch"):
        single_period_optimization(np.array([0.1]), w_t, gamma, phi_trade, phi_hold)

    # Test negative gamma
    with pytest.raises(ValidationError, match="Risk aversion parameter"):
        single_period_optimization(np.array([0.1, 0.2]), w_t, -1.0, phi_trade, phi_hold)


def test_optimization_errors():
    w_t = np.array([0.5, 0.5])
    r_t = np.array([0.1, 0.2])
    gamma = 1.0

    # Test invalid objective function
    def invalid_phi_trade(z):
        return "invalid"  # Non-CVXPY expression

    def phi_hold(w):
        return cp.sum(cp.square(w))

    with pytest.raises(OptimizationError, match="Invalid cost functions"):
        single_period_optimization(r_t, w_t, gamma, invalid_phi_trade, phi_hold)

    # Test solver failure with infinite values
    def phi_trade(z):
        return cp.sum(cp.abs(z))

    r_t_inf = np.array([np.inf, np.inf])
    with pytest.raises(OptimizationError, match="Invalid returns.*infinite"):
        single_period_optimization(r_t_inf, w_t, gamma, phi_trade, phi_hold)

    # Add test for NaN values
    r_t_nan = np.array([np.nan, np.nan])
    with pytest.raises(OptimizationError, match="Invalid returns.*NaN"):
        single_period_optimization(r_t_nan, w_t, gamma, phi_trade, phi_hold)


def test_zero_expected_returns(sample_portfolio):
    r_t = np.zeros(len(sample_portfolio.weights_vector))
    w_t = sample_portfolio.weights_vector
    gamma = 1.0

    def phi_trade(z):
        return cp.sum(cp.abs(z))

    def phi_hold(w):
        return cp.sum(cp.square(w))

    result = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    assert np.allclose(result, 0, atol=1e-3)


def test_high_risk_aversion(sample_portfolio):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = sample_portfolio.weights_vector
    gamma = 10.0

    def phi_trade(z):
        return cp.sum(cp.abs(z))

    def phi_hold(w):
        return cp.sum(cp.square(w))

    result = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    assert np.all(np.abs(result) < 0.2)  # Adjust threshold for high gamma


def test_low_risk_aversion(sample_portfolio):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = sample_portfolio.weights_vector
    gamma = 0.1

    def phi_trade(z):
        return cp.sum(cp.abs(z))

    def phi_hold(w):
        return cp.sum(cp.square(w))

    result = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    assert np.any(np.abs(result) > 0.1)  # Low gamma should allow larger trades
