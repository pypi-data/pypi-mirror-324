import pytest
import numpy as np
from datetime import datetime
from ConvexTrader.Portfolio import Portfolio
from ConvexTrader.Trade import Trade, TradeType
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


# Trade Tests
def test_trade_creation():
    trade = Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY)
    assert trade.symbol == "AAPL"
    assert trade.quantity == 100
    assert trade.price == 150.0
    assert trade.trade_date == datetime(2023, 1, 1)
    assert trade.trade_type == TradeType.BUY


def test_trade_validation_errors():
    with pytest.raises(ValidationError, match="Invalid symbol"):
        Trade("", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY)

    with pytest.raises(ValidationError, match="Invalid quantity"):
        Trade("AAPL", -100, 150.0, datetime(2023, 1, 1), TradeType.BUY)

    with pytest.raises(ValidationError, match="Invalid price"):
        Trade("AAPL", 100, -150.0, datetime(2023, 1, 1), TradeType.BUY)

    with pytest.raises(ValidationError, match="Invalid trade date"):
        Trade("AAPL", 100, 150.0, "2023-01-01", TradeType.BUY)

    with pytest.raises(ValidationError, match="Invalid trade type"):
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), "BUY")


# Portfolio Tests
def test_portfolio_creation():
    portfolio = Portfolio()
    assert len(portfolio.holdings) == 0
    assert len(portfolio.trades) == 0
    assert len(portfolio.symbols) == 0
    assert len(portfolio.holdings_vector) == 0
    assert len(portfolio.weights_vector) == 0


def test_execute_trade_validation(sample_portfolio):
    with pytest.raises(ValidationError, match="Invalid trade object"):
        sample_portfolio.execute_trade("invalid trade")


def test_insufficient_shares(sample_portfolio):
    with pytest.raises(ValidationError, match="Insufficient shares"):
        sell_trade = Trade("AAPL", 150, 160.0, datetime(2023, 1, 4), TradeType.SELL)
        sample_portfolio.execute_trade(sell_trade)


def test_sell_nonexistent_symbol(sample_portfolio):
    with pytest.raises(ValidationError, match="Insufficient shares"):
        sell_trade = Trade("INVALID", 50, 100.0, datetime(2023, 1, 4), TradeType.SELL)
        sample_portfolio.execute_trade(sell_trade)


# Optimization Tests
def test_single_period_validation(sample_portfolio):
    with pytest.raises(ValidationError, match="Expected returns length mismatch"):
        sample_portfolio.single_period_optimize(np.array([0.1]), 0.5)

    with pytest.raises(ValidationError, match="Invalid risk aversion parameter"):
        sample_portfolio.single_period_optimize(np.array([0.1, 0.2, 0.3]), -0.5)


def test_multi_period_validation(sample_portfolio):
    H = 3
    n_assets = len(sample_portfolio.weights_vector)

    with pytest.raises(ValidationError, match="Number of assets mismatch"):
        r_t = np.ones((H, n_assets + 1))
        gamma_t = np.ones(H)
        psi_t = np.ones(H)
        phi_trade = [np.ones(n_assets) for _ in range(H)]
        phi_hold = [np.ones(n_assets) for _ in range(H)]
        sample_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )

    with pytest.raises(ValidationError, match="Input length mismatch"):
        r_t = np.ones((H, n_assets))
        gamma_t = np.ones(H + 1)  # Wrong length
        sample_portfolio.multi_period_optimize(
            H, r_t, gamma_t, psi_t, phi_trade, phi_hold
        )


# Edge Cases
def test_empty_portfolio_weights():
    portfolio = Portfolio()
    weights = portfolio.get_weights()
    assert len(weights) == 0


def test_update_weights_empty_portfolio():
    portfolio = Portfolio()
    portfolio.update_weights()
    assert len(portfolio.weights_vector) == 0


def test_total_value_empty_portfolio():
    portfolio = Portfolio()
    assert portfolio.total_value({}) == 0


def test_sell_all_shares(sample_portfolio):
    sell_trade = Trade("AAPL", 100, 160.0, datetime(2023, 1, 4), TradeType.SELL)
    sample_portfolio.execute_trade(sell_trade)
    assert "AAPL" not in sample_portfolio.holdings
    assert sample_portfolio.holdings_vector[0] == 0


def test_portfolio_repr(sample_portfolio):
    trade = sample_portfolio.trades[0]
    assert isinstance(str(trade), str)
    assert "AAPL" in str(trade)
    assert "BUY" in str(trade)
