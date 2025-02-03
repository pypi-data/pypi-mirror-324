import pytest
import numpy as np
from datetime import datetime
from ConvexTrader.Portfolio import Portfolio
from ConvexTrader.Trade import Trade, TradeType
from ConvexTrader.multi_period_optimization import multi_period_optimization
from ConvexTrader.portfolio_exceptions import ValidationError, OptimizationError


@pytest.fixture
def mock_portfolio():
    class MockPortfolio:
        def __init__(self):
            self.weights_vector = np.array([0.6, 0.4])

    return MockPortfolio()


@pytest.fixture
def basic_portfolio():
    portfolio = Portfolio()
    trade_date = datetime.now()
    portfolio.execute_trade(Trade("AAPL", 10, 150.0, trade_date, TradeType.BUY))
    portfolio.execute_trade(Trade("GOOGL", 20, 2500.0, trade_date, TradeType.BUY))
    return portfolio


def test_multi_period_optimization_basic(mock_portfolio):
    H = 3
    portfolio_size = 2

    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    z = multi_period_optimization(
        H, r_t, mock_portfolio, gamma_t, psi_t, phi_trade, phi_hold
    )
    assert z is not None
    assert z.shape == (portfolio_size, H - 1)


def test_multi_period_optimize_invalid_horizon(mock_portfolio):
    H = 1  # Invalid horizon
    with pytest.raises(ValidationError, match="Invalid horizon parameter"):
        multi_period_optimization(H, np.array([[]]), mock_portfolio, [], [], [], [])


def test_multi_period_optimize_invalid_returns_shape(basic_portfolio):
    H = 3
    r_t = np.array([[0.05], [0.04], [0.06]])  # Wrong shape
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    with pytest.raises(ValidationError, match="Number of assets mismatch"):
        basic_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )


def test_multi_period_optimize_invalid_gamma_length(basic_portfolio):
    H = 3
    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([0.5, 0.4])  # Wrong length
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    with pytest.raises(ValidationError, match="Input length mismatch"):
        basic_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )


def test_multi_period_optimize_invalid_psi_length(basic_portfolio):
    H = 3
    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25]])  # Wrong length
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    with pytest.raises(ValidationError, match="Input length mismatch"):  # Updated match
        basic_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )


def test_multi_period_optimize_invalid_phi_trade_length(basic_portfolio):
    H = 3
    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03])]  # Wrong length
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    with pytest.raises(ValidationError, match="Input length mismatch"):  # Updated match
        basic_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )


def test_multi_period_optimize_solver_failure(basic_portfolio):
    H = 3
    # Use NaN values which will trigger validation error
    r_t = np.array([[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]])
    gamma_t = np.array([1.0, 1.0, 1.0])
    psi_t = np.array([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]])
    phi_trade = [np.array([1.0, 1.0]) for _ in range(H)]
    phi_hold = [np.array([1.0, 1.0]) for _ in range(H)]

    with pytest.raises(
        OptimizationError, match="Invalid returns matrix.*Contains.*NaN"
    ):
        multi_period_optimization(
            H, r_t, basic_portfolio, gamma_t, psi_t, phi_trade, phi_hold
        )


def test_multi_period_optimize_empty_portfolio():
    portfolio = Portfolio()
    H = 3
    r_t = np.array([[0.05], [0.04], [0.06]])
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1], [0.15], [0.1]])
    phi_trade = [np.array([0.02]), np.array([0.01]), np.array([0.03])]
    phi_hold = [np.array([0.01]), np.array([0.01]), np.array([0.01])]

    with pytest.raises(ValidationError, match="Number of assets mismatch"):
        portfolio.multi_period_optimize(H, r_t, gamma_t, psi_t, phi_trade, phi_hold)


def test_multi_period_optimize_negative_gamma(basic_portfolio):
    H = 3
    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([-0.5, 0.4, 0.3])  # Negative gamma
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    with pytest.raises(
        ValidationError, match="risk aversion parameters"
    ):  # Updated match
        multi_period_optimization(
            H, r_t, basic_portfolio, gamma_t, psi_t, phi_trade, phi_hold
        )
