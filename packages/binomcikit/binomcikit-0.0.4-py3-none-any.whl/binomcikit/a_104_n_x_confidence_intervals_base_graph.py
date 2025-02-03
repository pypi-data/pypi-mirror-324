from a_103_n_x_confidence_intrevals_base import *
import pandas as pd
from plotnine import (
    ggplot, aes, geom_errorbarh, geom_point, labs,
    scale_colour_manual, scale_shape_manual
)


def plotciexx(x, n, alp, e):
    """
    Plot confidence intervals with error bars and points for aberrations.

    Parameters:
    x (int): Number of successes
    n (int): Sample size
    alp (float): Alpha level (between 0 and 1)
    e (float or list): Error value(s). Can be single value or list of values
    """
    # Input validation
    if x < 0 or x > n orded.DataFrame()  # Initialize an empty DataFrame for lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    # Create the base plot
    p = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="x values", title="Exact method given x") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit', color='e'), size=0.5))

    # Add points for aberrations if they exist
    if not ldf.empty:
        p += geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                        size=4, color="red") + \
             scale_shape_manual(values=['o','s','^'])

    # Add color scale with standard matplotlib color names
    p += scale_colour_manual(values=["red", "blue", "green", "purple", "orange",
                                     "brown", "black", "gray", "magenta", "cyan"])

    p.show()
