import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import get_scorer, get_scorer_names

def run_linear_regression(dataframe, target_column, numeric_feats, categorical_feats, drop_feats=None, test_size=0.2, random_state=None, scoring_metrics=['r2', 'neg_mean_squared_error']):
    """
    Performs linear regression with preprocessing using sklearn and outputs evaluation scoring metrics.
    
    Parameters
    ----------
    dataframe: `pandas.DataFrame`
        full dataset including features and target.
    target_column: `string`
        name of the target variable column.
    numeric_feats: `list`
        columns to apply StandardScaler.
    categorical_feats: `list`
        columns to apply OneHotEncoder.
    drop_feats: `list`, optional
        columns to drop (default None).
    test_size: `float`, optional
        proportion of the dataset to include in the test split (default 0.2).
    random_state: `int`, optional
        controls the shuffling applied to the data before the split (default None).
    scoring_metrics: `list`, optional
        scoring metrics to evaluate the model (default 'r2', 'neg_mean_squared_error').
    
    Returns
    -------
    tuple
        the fitted model
        DataFrames for the training and test features
        Series for the training and test labels
        dictionary of metric scores with metric names as keys
    
    Raises
    ------
    ValueError
        When `dataframe`, `target_column`, `test_size` or `scoring_metrics` is not within the range of acceptable values
    TypeError
        When `dataframe`, `random_state` or `scoring_metrics` is not the expected type
    
    Examples
    ---------
    >>> import pandas as pd
    >>> from linreg_ally.linreg_ally import run_linear_regression
    >>> df = pd.DataFrame({
    ...     "feature_1": [1, 2, 3, 4],
    ...     "feature_2": [0.5, 0.1, 0.4, 0.9],
    ...     "category": ["a", "b", "a", "b"],
    ...     "target": [1.0, 2.5, 3.4, 4.3]
    ... })
    >>> target_column = 'target'
    >>> numeric_feats = ['feature_1', 'feature_2']
    >>> categorical_feats = ['category']
    >>> drop_feats = []
    >>> best_model, X_train, X_test, y_train, y_test, scores = run_linear_regression(
    ...     df, target_column, numeric_feats, categorical_feats, drop_feats, scoring_metrics=['r2', 'neg_mean_squared_error']
    ... )
    >>> scores
    {'r2': 0.52, 'neg_mean_squared_error': 1.23}
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame.")
    
    if dataframe.shape[1] <= 1:
        raise ValueError("dataframe must contain more than one column.")
    
    if target_column not in dataframe.columns:
        raise ValueError(f"target_column '{target_column}' is not in the dataframe.")
    
    if not (0.0 < test_size < 1.0):
        raise ValueError("test_size must be between 0.0 and 1.0.")
    
    if random_state is not None and not isinstance(random_state, int):
        raise TypeError("random_state must be an integer.")
    
    if not isinstance(scoring_metrics, list) or not all(isinstance(metric, str) for metric in scoring_metrics):
        raise TypeError("scoring_metrics must be a list of strings.")
    
    if not all(metric in get_scorer_names() for metric in scoring_metrics):
        invalid_metrics = [metric for metric in scoring_metrics if metric not in get_scorer_names()]
        raise ValueError(f"The following scoring metrics are not valid: {', '.join(invalid_metrics)}")
    
    drop_feats = drop_feats if drop_feats is not None else []

    X = dataframe.drop(columns=[target_column])
    y = dataframe[target_column]

    preprocessor = preprocess(numeric_feats, categorical_feats, drop_feats)

    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    (best_model, scores) = fit_predict(pipe, X_train, X_test, y_train, y_test, scoring_metrics)

    print("Model Summary")
    print("------------------------")
    for metric, score in scores.items():
        print(f"Test {metric}: {score:.3f}")

    return best_model, X_train, X_test, y_train, y_test, scores

def preprocess(numeric_feats, categorical_feats, drop_feats):
    return make_column_transformer(
        (StandardScaler(), numeric_feats),
        (OneHotEncoder(), categorical_feats),
        ('drop', drop_feats)
    )

def fit_predict(pipeline, X_train, X_test, y_train, y_test, scoring_metrics):
    pipeline.fit(X_train, y_train)

    best_model = pipeline

    predictions = best_model.predict(X_test)

    scores = {}
    for metric in scoring_metrics:
        scorer = get_scorer(metric)
        scores[metric] = scorer._score_func(y_test, predictions)

    return (best_model, scores)
