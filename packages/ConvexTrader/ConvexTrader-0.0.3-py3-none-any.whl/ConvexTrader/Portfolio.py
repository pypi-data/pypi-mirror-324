import numpy as np
import cvxpy as cp
from typing import List, Dict
from .Trade import Trade, TradeType
from .single_period_optimization import single_period_optimization
from .multi_period_optimization import multi_period_optimization
from .portfolio_exceptions import ValidationError, OptimizationError


class Portfolio:
    def __init__(self, gamma=0.5):
        """
        Initialize a portfolio with empty holdings, trades, symbols, and vectors for holdings and weights.
        - holdings: Dictionary to store the quantity of each stock symbol.
        - trades: List to store all trade transactions.
        - symbols: List to keep track of all unique stock symbols in the portfolio.
        - holdings_vector: Numpy array representing quantities of each stock in the same order as symbols.
        - weights_vector: Numpy array representing the proportion of each stock in the portfolio.
        - gamma: double representing the risk metric gamma, set to 0.5 automatically but can be customized by the user
        """
        self.holdings: Dict[str, int] = {}
        self.trades: List[Trade] = []
        self.symbols: List[str] = []
        self.holdings_vector: np.ndarray = np.array([])
        self.weights_vector: np.ndarray = np.array([])
        self.gamma = gamma

    def execute_trade(self, trade: Trade):
        """
        Executes a trade (buy or sell) by updating holdings and adjusting portfolio weights accordingly.
            trade: A Trade object containing trade details (symbol, quantity, trade_type).

        Args:
            trade: A Trade object containing trade details (symbol, quantity, trade_type)

        Raises:
            ValidationError: If there are insufficient shares for a sell trade
        """
        # Add the trade to the list of executed trades
        if not isinstance(trade, Trade):
            raise ValidationError(
                "Invalid trade object", details=f"Expected Trade, got {type(trade)}"
            )

        self.trades.append(trade)

        if trade.symbol not in self.symbols:
            self.symbols.append(trade.symbol)
            self.holdings_vector = np.append(self.holdings_vector, 0)
            self.weights_vector = np.append(self.weights_vector, 0)

        symbol_index = self.symbols.index(trade.symbol)

        if trade.trade_type == TradeType.BUY:
            self.holdings[trade.symbol] = (
                self.holdings.get(trade.symbol, 0) + trade.quantity
            )
            self.holdings_vector[symbol_index] += trade.quantity

        elif trade.trade_type == TradeType.SELL:
            if (
                trade.symbol not in self.holdings
                or self.holdings[trade.symbol] < trade.quantity
            ):
                raise ValidationError(
                    f"Insufficient shares to sell {trade.symbol}",
                    details=f"Requested: {trade.quantity}, Available: {self.holdings.get(trade.symbol, 0)}",
                )

            self.holdings[trade.symbol] -= trade.quantity
            self.holdings_vector[symbol_index] -= trade.quantity

            if self.holdings[trade.symbol] == 0:
                del self.holdings[trade.symbol]

        self.update_weights()

    def update_weights(self):
        """
        Updates the portfolio weights based on the current holdings.
        """
        total_holdings = np.sum(
            self.holdings_vector
        )  # Calculate total number of shares across all holdings

        if total_holdings > 0:
            # If total holdings are greater than zero, calculate the weight of each stock
            self.weights_vector = self.holdings_vector / total_holdings
        else:
            # If there are no holdings, set all weights to zero
            self.weights_vector = np.zeros(len(self.symbols))

    def get_weights(self) -> Dict[str, float]:
        """
        Returns a dictionary of stock symbols and their corresponding weights in the portfolio.
        """
        return {
            symbol: weight for symbol, weight in zip(self.symbols, self.weights_vector)
        }

    def total_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculates the total market value of the portfolio based on current stock prices.
        """
        # Create a vector of current prices in the same order as the symbols list
        prices_vector = np.array([current_prices[symbol] for symbol in self.symbols])
        # Return the dot product of the holdings vector and prices vector to get the portfolio's total value
        return np.dot(self.holdings_vector, prices_vector)

    def single_period_optimize(
        self, expected_returns: np.ndarray, gamma: float
    ) -> np.ndarray:
        """
        Solve the single-period optimization problem using the provided single_period_optimization function.

        Args:
            expected_returns: Numpy array of expected returns for each stock in the portfolio.
            gamma: Risk-aversion parameter.

        Returns:
            Numpy array: Optimal trade vector (z).

        Raises:
            ValidationError: If input parameters are invalid
            OptimizationError: If optimization fails
        """
        w_t = self.weights_vector

        def phi_trade(z):
            return cp.sum(cp.abs(z))

        def phi_hold(w):
            return cp.sum(cp.square(w))

        if len(expected_returns) != len(self.weights_vector):
            raise ValidationError(
                "Expected returns length mismatch",
                details=f"Expected {len(self.weights_vector)}, got {len(expected_returns)}",
            )
        if gamma < 0:
            raise ValidationError(
                "Invalid risk aversion parameter",
                details=f"gamma must be non-negative, got {gamma}",
            )

        result = single_period_optimization(
            expected_returns, w_t, gamma, phi_trade, phi_hold
        )

        if result is None:
            raise OptimizationError("Single-period optimization failed")

        return result

    def multi_period_optimize(
        self,
        H: int,
        r_t: np.ndarray,
        gamma_t: np.ndarray,
        psi_t: np.ndarray,
        phi_trade: List[np.ndarray],
        phi_hold: List[np.ndarray],
    ) -> np.ndarray:
        """
        Solve the multi-period optimization problem using the multi_period_optimization function.

        Args:
            H: Number of future periods to optimize.
            r_t: Matrix of expected returns, where each row corresponds to a future period.
            gamma_t: Vector of risk-aversion parameters for each period.
            psi_t: Vector of risk factors for each period.
            phi_trade: List of transaction cost vectors for each period.
            phi_hold: List of holding cost vectors for each period.

        Returns:
            Numpy array: Optimal trade vectors over all periods (z matrix).

        Raises:
            ValidationError: If input parameters are invalid
            OptimizationError: If optimization fails
        """
        if r_t.shape[1] != len(self.weights_vector):
            raise ValidationError(
                "Number of assets mismatch",
                details=f"Expected {len(self.weights_vector)} assets, got {r_t.shape[1]}",
            )
        if (
            len(gamma_t) != H
            or len(psi_t) != H
            or len(phi_trade) != H
            or len(phi_hold) != H
        ):
            raise ValidationError(
                "Input length mismatch",
                details=f"All period inputs must have length {H}",
            )

        result = multi_period_optimization(
            H, r_t, self, gamma_t, psi_t, phi_trade, phi_hold
        )

        if result is None:
            raise OptimizationError("Multi-period optimization failed")

        return result
