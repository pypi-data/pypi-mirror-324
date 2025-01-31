"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : financefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  financefunctions provides functionality for stock prices analysis
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# FUNCTIONS DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# Normalize function
# -------------------------------------------------------------
def norm(df: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """normalize the dataframe to first line

    Returns
    -------
    pandas datafrage
        normalized dataframe to first line
    """
    return df.ff.norm()


# -------------------------------------------------------------
# CAGR function
# -------------------------------------------------------------
def cagr(series: pd.Series) -> float:
    """calculate cagr (compound annual growth rate) of a series.

    Returns
    -------
    float
        float with cagr
    """
    return series.ff.cagr()
