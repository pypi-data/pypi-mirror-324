# Author: Alex Wong
# multicollinearity.py
# 01/10/2025

import altair as alt
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor 

def check_multicollinearity(train_df: pd.DataFrame, threshold = None, vif_only = False):
    """
    Detects multicollinearity in the training dataset by computing the variance inflation factor (‘VIF’) and pairwise Pearson Correlation for each numeric feature. 

    Parameters
    ----------
    train_df : pd.DataFrame
         Training dataset

    threshold : int 
        Minimum threshold of VIF for a feature to be included in the returned dataframe. 
        Default is None.
    
    vif_only : Boolean
        If true, only a dataframe containing the VIF scores will be returned. Otherwise, the correlation chart is also returned.

    Returns
    -------
    pd.DataFrame
    A dataframe containing the VIF of all numeric features in train_df. 
    
    alt.Chart
        A chart that shows the pairwise Pearson Correlations of all numeric columns in train_df. 

    Examples
    --------
    >>> from linreg_ally.multicollinearity import check_multicollinearity
    >>> vif_df, corr_chart = check_multicollinearity(train_df)
    >>> vif_df = check_multicollinearity(train_df, threshold = 5, vif_only = True)  
    """
    # select only numeric columns in train_df
    train_df_numeric_only = train_df.select_dtypes(include='number')

    # Calculate VIF for each feature
    vif = [variance_inflation_factor(train_df_numeric_only, i) for i in range(len(train_df_numeric_only.columns))]
    vif_dict = {
        'Features': train_df_numeric_only.columns,
        'VIF': vif
    }
    vif_df = pd.DataFrame(vif_dict)

    # Calculate pairwise Pearson correlations
    corr_df = (train_df_numeric_only
               .corr('pearson', numeric_only=True)
               .abs()  # Use abs for negative correlation to stand out
               .stack()  # Get df into long format for altair
               .reset_index(name='corr'))  

    # Round the correlation values to 3 decimal places
    corr_df['corr'] = corr_df['corr'].round(3)

    # Create the correlation chart using Altair
    corr_chart = alt.Chart(corr_df).mark_circle().encode(
        x='level_0',
        y='level_1',
        size='corr',
        color='corr'
    )

    # Filter VIF dataframe by the threshold if provided
    if threshold is not None:
        vif_df = vif_df[vif_df['VIF'] >= threshold]

    # Return VIF dataframe or both VIF dataframe and correlation chart
    if vif_only:
        return vif_df
    else:
        return vif_df, corr_chart



    