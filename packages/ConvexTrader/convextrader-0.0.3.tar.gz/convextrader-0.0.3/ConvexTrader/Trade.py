from enum import Enum, auto
from datetime import datetime
from .portfolio_exceptions import ValidationError


class TradeType(Enum):
    """
    Enum representing the type of trade, either a BUY or SELL.
    """

    BUY = auto()
    SELL = auto()


class Trade:
    """
    Represents a trade in a financial portfolio.

    A trade includes information about the stock symbol, the quantity of shares traded,
    the price per share, the date of the trade, and the type of trade (BUY or SELL).
    """

    def __init__(
        self,
        symbol: str,
        quantity: int,
        price: float,
        trade_date: datetime,
        trade_type: TradeType,
    ):
        """
        Initializes a Trade instance.

        Args:
            symbol (str): The ticker symbol of the stock being traded (e.g., 'AAPL', 'GOOGL').
            quantity (int): The number of shares being bought or sold.
            price (float): The price per share at which the trade was executed.
            trade_date (datetime): The date and time when the trade occurred.
            trade_type (TradeType): The type of trade, either `TradeType.BUY` or `TradeType.SELL`.

        Raises:
            ValidationError: If any of the input parameters are invalid.

        Example:
            Creating a buy trade for 10 shares of AAPL stock:

            >>> from datetime import datetime
            >>> trade = Trade(
            ...     symbol="AAPL",
            ...     quantity=10,
            ...     price=150.00,
            ...     trade_date=datetime.now(),
            ...     trade_type=TradeType.BUY
            ... )
        """
        if not isinstance(symbol, str) or not symbol:
            raise ValidationError(
                "Invalid symbol",
                details=f"Symbol must be non-empty string, got {type(symbol)}",
            )

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError(
                "Invalid quantity",
                details=f"Quantity must be positive integer, got {quantity}",
            )

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValidationError(
                "Invalid price", details=f"Price must be positive number, got {price}"
            )

        if not isinstance(trade_date, datetime):
            raise ValidationError(
                "Invalid trade date",
                details=f"Expected datetime object, got {type(trade_date)}",
            )

        if not isinstance(trade_type, TradeType):
            raise ValidationError(
                "Invalid trade type",
                details=f"Expected TradeType enum, got {type(trade_type)}",
            )

        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.trade_date = trade_date
        self.trade_type = trade_type

    def __repr__(self):
        """
        Returns a string representation of the Trade object.

        The representation includes the stock symbol, quantity, price,
        trade date, and type of trade.

        Returns:
            str: A formatted string representing the trade.

        Example:
            >>> repr(trade)
            '<Trade(symbol=AAPL, quantity=10, price=150.0, date=2024-11-25 15:30:00, type=BUY)>'
        """
        return (
            f"<Trade(symbol={self.symbol}, quantity={self.quantity}, price={self.price}, "
            f"date={self.trade_date.strftime('%Y-%m-%d %H:%M:%S')}, type={self.trade_type.name})>"
        )
