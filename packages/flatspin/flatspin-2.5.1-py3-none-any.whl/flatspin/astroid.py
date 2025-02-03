"""
Generalized Stoner-Wohlfarth Astroid
"""
import numpy as np
import importlib.resources
from .data import read_csv, filter_df

def rotate_points(x, y, theta):
    return (x * np.cos(theta) - y * np.sin(theta),
            x * np.sin(theta) + y * np.cos(theta))

def gsw(h_par, b=1.0, c=1.0, beta=3.0, gamma=3.0, hc=1.0):
    """ Generalized Stoner-Wohlfarth Astroid (explicit form) """
    h_par = h_par / (b * hc)
    h_perp = c * hc * (1 - (h_par**2)**(1/gamma))**(beta/2)
    return h_perp

def gsw_par(h_perp, b=1.0, c=1.0, beta=3.0, gamma=3.0, hc=1.0):
    """ Generalized Stoner-Wohlfarth Astroid (explicit form, par version) """
    h_perp = h_perp / (c * hc)
    h_par = b * hc * (1 - (h_perp**2)**(1/beta))**(gamma/2)
    return h_par

def gsw_implicit(h_par, h_perp, b=1.0, c=1.0, beta=3.0, gamma=3.0, hc=1.0):
    """ Generalized Stoner-Wohlfarth Astroid (implicit form) """
    h_par = h_par / (b * hc)
    h_perp = h_perp / (c * hc)
    return (h_par**2)**(1/gamma) + (h_perp**2)**(1/beta) - 1

def gsw_astroid(b=1.0, c=1.0, beta=3.0, gamma=3.0, hc=1.0,
                rotation=0, resolution=361, angle_range=(0, 2*np.pi)):
    """ Generate samples from the Generalized Stoner-Wohlfarth Astroid """

    thetas = np.linspace(angle_range[0], angle_range[1], resolution)

    h_par = b * hc * np.cos(thetas)
    h_perp = gsw(h_par, b, c, beta, gamma, hc)
    h_perp[(thetas % (2*np.pi)) > np.pi] *= -1

    h_par, h_perp = rotate_points(h_par, h_perp, np.deg2rad(rotation))

    return np.column_stack([h_par, h_perp])

def _read_astroid_db():
    file = importlib.resources.files('flatspin').joinpath("astroids.csv")
    with file.open() as fp:
        return read_csv(fp)

db = _read_astroid_db()
"""pd.DataFrame: Astroid database table.

   :meta hide-value:
"""

def astroid_params(**filter):
    """ Lookup parameters from the astroid database.

    Parameters
    ----------
    **filter : dict
        column=value to match one row from the database.
        Consult ``astroid.db.columns`` for available column names.


    Examples
    --------
    >>> astroid_params(shape="stadium", width=220, height=80, thickness=20)
    {'hc': 0.1898446831994154,
    'sw_b': 0.3656109262423056,
    'sw_c': 1.0,
    'sw_beta': 1.6801798570360171,
    'sw_gamma': 2.749154122977873}

    Raises
    ------
    ValueError
        If there are none or multiple matches.

    """
    df = filter_df(db, **filter)

    if len(df) > 1:
        raise ValueError("Filter matches multiple astroids (consult astroid.db)")

    if len(df) == 0:
        raise ValueError("Filter matched no astroids (consult astroid.db)")

    params = df.iloc[0]

    return dict(
        hc=float(params.hc),
        sw_b=float(params.b),
        sw_c=float(params.c),
        sw_beta=float(params.beta),
        sw_gamma=float(params.gamma),
    )
