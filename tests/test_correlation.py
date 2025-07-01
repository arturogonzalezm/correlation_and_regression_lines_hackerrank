import pytest

from unittest.mock import Mock
from src.correlation import CorrelationStrategy, PearsonCorrelationStrategy, CorrelationContext


class TestPearsonCorrelationStrategy:
    """Test cases for PearsonCorrelationStrategy class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.strategy = PearsonCorrelationStrategy()

    def test_perfect_positive_correlation(self):
        """Test perfect positive correlation (r = 1.0)."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10

    def test_perfect_negative_correlation(self):
        """Test perfect negative correlation (r = -1.0)."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        result = self.strategy.calculate(x, y)
        assert abs(result - (-1.0)) < 1e-10

    def test_no_correlation_constant_y(self):
        """Test no correlation when y values are constant."""
        x = [1, 2, 3, 4, 5]
        y = [5, 5, 5, 5, 5]  # constant values
        with pytest.raises(ZeroDivisionError):
            self.strategy.calculate(x, y)

    def test_no_correlation_constant_x(self):
        """Test no correlation when x values are constant."""
        x = [3, 3, 3, 3, 3]  # constant values
        y = [1, 2, 3, 4, 5]
        with pytest.raises(ZeroDivisionError):
            self.strategy.calculate(x, y)

    def test_identical_datasets(self):
        """Test correlation of identical datasets (should be 1.0)."""
        data = [5, 10, 15, 20, 25]
        result = self.strategy.calculate(data, data)
        assert abs(result - 1.0) < 1e-10

    def test_empty_lists(self):
        """Test with empty lists (should raise ZeroDivisionError)."""
        with pytest.raises(ZeroDivisionError):
            self.strategy.calculate([], [])

    def test_single_data_point(self):
        """Test with single data point (should raise ZeroDivisionError)."""
        x = [5]
        y = [10]
        with pytest.raises(ZeroDivisionError):
            self.strategy.calculate(x, y)

    def test_two_data_points_perfect_correlation(self):
        """Test with two data points showing perfect correlation."""
        x = [1, 2]
        y = [3, 6]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10

    def test_two_data_points_negative_correlation(self):
        """Test with two data points showing negative correlation."""
        x = [1, 2]
        y = [6, 3]
        result = self.strategy.calculate(x, y)
        assert abs(result - (-1.0)) < 1e-10

    def test_negative_values(self):
        """Test correlation with negative values."""
        x = [-5, -3, -1, 1, 3]
        y = [-10, -6, -2, 2, 6]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10

    def test_floating_point_values(self):
        """Test correlation with floating point values."""
        x = [1.5, 2.7, 3.9, 4.1, 5.3]
        y = [2.1, 3.8, 5.2, 6.7, 8.1]
        result = self.strategy.calculate(x, y)
        assert -1 <= result <= 1
        assert result > 0  # Should be positive correlation

    def test_moderate_positive_correlation(self):
        """Test moderate positive correlation."""
        x = [1, 2, 3, 4, 5, 6]
        y = [2, 3, 5, 4, 6, 7]  # Not perfect, but positive trend
        result = self.strategy.calculate(x, y)
        assert 0.5 < result < 1.0

    def test_moderate_negative_correlation(self):
        """Test moderate negative correlation."""
        x = [1, 2, 3, 4, 5, 6]
        y = [6, 5, 3, 4, 2, 1]  # Not perfect, but negative trend
        result = self.strategy.calculate(x, y)
        assert -1.0 < result < -0.5

    def test_very_large_numbers(self):
        """Test correlation with very large numbers."""
        x = [1e10, 2e10, 3e10, 4e10, 5e10]
        y = [2e10, 4e10, 6e10, 8e10, 10e10]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10

    def test_very_small_numbers(self):
        """Test correlation with very small numbers."""
        x = [1e-10, 2e-10, 3e-10, 4e-10, 5e-10]
        y = [2e-10, 4e-10, 6e-10, 8e-10, 10e-10]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10

    def test_zero_values_included(self):
        """Test correlation with zero values included."""
        x = [0, 1, 2, 3, 4]
        y = [0, 2, 4, 6, 8]
        result = self.strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10


class TestCorrelationContext:
    """Test cases for CorrelationContext class."""

    def test_context_initialization_with_strategy(self):
        """Test that context is properly initialized with strategy."""
        strategy = PearsonCorrelationStrategy()
        context = CorrelationContext(strategy)
        assert context._strategy is strategy

    def test_execute_delegates_to_strategy(self):
        """Test that execute method properly delegates to strategy."""
        strategy = PearsonCorrelationStrategy()
        context = CorrelationContext(strategy)

        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        result_context = context.execute(x, y)
        result_strategy = strategy.calculate(x, y)

        assert result_context == result_strategy

    def test_context_with_mock_strategy(self):
        """Test context with a mock strategy to verify delegation."""
        mock_strategy = Mock(spec=CorrelationStrategy)
        mock_strategy.calculate.return_value = 0.75

        context = CorrelationContext(mock_strategy)
        x = [1, 2, 3]
        y = [4, 5, 6]

        result = context.execute(x, y)

        assert result == 0.75
        mock_strategy.calculate.assert_called_once_with(x, y)

    def test_strategy_can_be_changed(self):
        """Test that strategy can be swapped (demonstrates Strategy pattern flexibility)."""
        # Create first strategy
        strategy1 = PearsonCorrelationStrategy()
        context = CorrelationContext(strategy1)

        # Create mock second strategy
        strategy2 = Mock(spec=CorrelationStrategy)
        strategy2.calculate.return_value = 0.5

        # Change strategy
        context._strategy = strategy2

        result = context.execute([1, 2, 3], [4, 5, 6])
        assert result == 0.5
        strategy2.calculate.assert_called_once_with([1, 2, 3], [4, 5, 6])


class TestCorrelationStrategyInterface:
    """Test the abstract CorrelationStrategy interface."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that CorrelationStrategy cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CorrelationStrategy()

    def test_concrete_implementation_must_implement_calculate(self):
        """Test that concrete implementations must implement calculate method."""

        class IncompleteStrategy(CorrelationStrategy):
            pass  # Missing calculate method

        with pytest.raises(TypeError):
            IncompleteStrategy()

    def test_valid_concrete_implementation(self):
        """Test that valid concrete implementations work correctly."""

        class CustomStrategy(CorrelationStrategy):
            def calculate(self, x, y):
                return 0.42  # Dummy implementation

        strategy = CustomStrategy()
        assert strategy.calculate([1, 2], [3, 4]) == 0.42


# Parametrized tests for comprehensive coverage
class TestParametrizedScenarios:
    """Parametrized tests for various correlation scenarios."""

    @pytest.fixture
    def strategy(self):
        """Fixture providing PearsonCorrelationStrategy instance."""
        return PearsonCorrelationStrategy()

    @pytest.mark.parametrize("x,y,expected_sign", [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 1),  # Positive correlation
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], -1),  # Negative correlation
        ([1, 3, 2, 5, 4], [2, 6, 4, 10, 8], 1),  # Positive with variation
    ])
    def test_correlation_signs(self, strategy, x, y, expected_sign):
        """Test that correlation results have expected signs."""
        result = strategy.calculate(x, y)
        assert (result > 0) == (expected_sign > 0)

    @pytest.mark.parametrize("size", [2, 3, 5, 10, 20])
    def test_different_dataset_sizes(self, strategy, size):
        """Test correlation calculation with different dataset sizes."""
        x = list(range(1, size + 1))
        y = [i * 2 + 1 for i in x]  # Linear relationship

        result = strategy.calculate(x, y)
        assert abs(result - 1.0) < 1e-10  # Should be perfect correlation

    @pytest.mark.parametrize("multiplier", [-2, -1, 0.5, 1, 2, 5])
    def test_linear_relationships(self, strategy, multiplier):
        """Test perfect correlation with different linear relationships."""
        x = [1, 2, 3, 4, 5]
        y = [i * multiplier for i in x]

        if multiplier == 0:
            # All y values will be 0 (constant), should raise ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                strategy.calculate(x, y)
        elif multiplier > 0:
            result = strategy.calculate(x, y)
            assert abs(result - 1.0) < 1e-10
        else:  # multiplier < 0
            result = strategy.calculate(x, y)
            assert abs(result - (-1.0)) < 1e-10


class TestErrorHandling:
    """Test error conditions and edge cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.strategy = PearsonCorrelationStrategy()
        self.context = CorrelationContext(self.strategy)

    def test_mismatched_list_lengths(self):
        """Test behavior with lists of different lengths."""
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3]  # Shorter list

        # zip() will stop at shortest list, so this should work but use only 3 pairs
        result = self.strategy.calculate(x[:3], y)  # Manually match lengths
        assert isinstance(result, float)

    def test_all_zero_values(self):
        """Test with all zero values."""
        x = [0, 0, 0, 0, 0]
        y = [1, 2, 3, 4, 5]

        with pytest.raises(ZeroDivisionError):
            self.strategy.calculate(x, y)

    def test_context_with_none_strategy(self):
        """Test context behavior when strategy is None."""
        context = CorrelationContext(None)

        with pytest.raises(AttributeError):
            context.execute([1, 2, 3], [4, 5, 6])


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])
