class PortfolioOptimizationError(Exception):
    """Base exception class for portfolio optimization errors"""

    def __init__(self, message="A portfolio optimization error occurred", details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class ValidationError(PortfolioOptimizationError):
    """Raised when input validation fails"""

    def __init__(self, message="Input validation failed", details=None):
        super().__init__(message=message, details=details)


class OptimizationError(PortfolioOptimizationError):
    """Raised when the optimization problem fails"""

    def __init__(self, message="Optimization problem failed to solve", details=None):
        super().__init__(message=message, details=details)
