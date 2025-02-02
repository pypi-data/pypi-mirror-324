import altair as alt
import pandas as pd
import numpy as np
import scipy.stats as stats

def qq_and_residuals_plot(y_actual, y_predicted, concatenate=True):
    """
    Generate a Q-Q plot (standardized residuals vs theoretical quantiles)
    and a Residuals vs. Fitted Values plot using Altair for regression diagnostics.

    Parameters
    ----------
    y_actual : array-like
        Actual observed values from the dataset. Must be numeric and have the same length as `y_predicted`.

    y_predicted : array-like
        Predicted (fitted) values from the regression model. Must be numeric and have the same length as `y_actual`.

    concatenate : bool, optional (default=True)
        If True, concatenates the Q-Q plot and Residuals vs. Fitted Values plot side by side.
        If False, returns the plots separately as individual Altair charts.

    Returns
    -------
    alt.Chart or tuple of alt.Chart
        - If `concatenate=True`, returns a concatenated Altair chart with both plots.
        - If `concatenate=False`, returns a tuple containing the Q-Q plot and Residuals vs. Fitted Values plot.

    Raises
    ------
    ValueError
        If `y_actual` or `y_predicted` are empty, have mismatched lengths, or contain fewer than two data points.
    
    TypeError
        If `y_actual` or `y_predicted` are not numeric.

    Examples
    --------
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> y_actual = np.random.normal(10, 2, 100)
    >>> y_predicted = y_actual + np.random.normal(0, 1, 100)
    >>> chart = qq_and_residuals_plot(y_actual, y_predicted, concatenate=True)
    >>> chart.display()
    """
    # Ensure inputs are NumPy arrays
    y_actual = np.array(y_actual)
    y_predicted = np.array(y_predicted)

    # Validate inputs
    if y_actual.size == 0 or y_predicted.size == 0:
        raise ValueError("Inputs must not be empty")
    if y_actual.size != y_predicted.size:
        raise ValueError("Inputs must have the same length")
    if y_actual.size < 2:
        raise ValueError("Insufficient data points for plotting")
    if not (np.issubdtype(y_actual.dtype, np.number) and np.issubdtype(y_predicted.dtype, np.number)):
        raise TypeError("Inputs must be numeric")

    # Calculate residuals
    residuals = y_actual - y_predicted
    standardized_residuals = (residuals - np.mean(residuals)) / np.std(residuals)

    # Create Q-Q plot data frame
    qq_theoretical, qq_sample = stats.probplot(standardized_residuals, dist="norm", fit=False)
    qq_df = pd.DataFrame({
        'Theoretical Quantiles': qq_theoretical,
        'Standardized Residuals': qq_sample
    })

    # Create reference line for Q-Q plot (45-degree line)
    qq_reference_line = alt.Chart(pd.DataFrame({
        'Theoretical Quantiles': [-3, 3],  # Typical range for normal quantiles
        'Standardized Residuals': [-3, 3]
    })).mark_line(color='red', strokeDash=[5, 5]).encode(
        x='Theoretical Quantiles',
        y='Standardized Residuals'
    )

    # Q-Q Plot
    qq_plot = alt.Chart(qq_df).mark_circle(size=60).encode(
        x=alt.X('Theoretical Quantiles', title='Theoretical Quantiles'),
        y=alt.Y('Standardized Residuals', title='Standardized Residuals')
    ).properties(title="Q-Q Plot", width=300, height=300) + qq_reference_line

    # Residuals vs Fitted Values data frame
    residuals_df = pd.DataFrame({
        'Fitted Values': y_predicted,
        'Residuals': residuals
    })

    # Create horizontal reference line at y = 0 for Residuals vs. Fitted Values
    residuals_reference_line = alt.Chart(pd.DataFrame({
        'Fitted Values': [y_predicted.min() - 2, y_predicted.max() + 2], #edited starting point
        'Residuals': [0, 0]
    })).mark_line(color='red', strokeDash=[5, 5]).encode(
        x='Fitted Values',
        y='Residuals'
    )

    # Residuals vs Fitted Values Plot
    residuals_plot = alt.Chart(residuals_df).mark_circle(size=60).encode(
        x=alt.X('Fitted Values', title='Fitted Values'),
        y=alt.Y('Residuals', title='Residuals')
    ).properties(title="Residuals vs. Fitted Values", width=300, height=300) + residuals_reference_line


    # Combine or return separately
    if concatenate:
        return alt.hconcat(qq_plot, residuals_plot).resolve_scale(y='independent')
    return qq_plot, residuals_plot
