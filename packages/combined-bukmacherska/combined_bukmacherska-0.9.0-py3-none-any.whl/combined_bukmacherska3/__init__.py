"""
__init__.py for the combined_bukmacherska3 package.

This package provides various mathematical, statistical, and machine learning functions
for sports analytics, including predictive models and visualization tools.

Modules:
- `math_utils`: Mathematical and statistical functions
- `team_analysis`: Functions for analyzing team performance
- `time_analysis`: Temporal and tactical analysis functions
- `ml_models`: Machine learning models and prediction functions
- `advanced_strategies`: Advanced strategies for game analysis
- `visualizations`: Functions for generating different types of plots
"""

from .combined_bukmacherska3 import (
    EULER_CONSTANT,
    gamma_function,
    beta_function,
    normal_pdf,
    mean,
    variance,
    std_dev,
    poisson_pmf,
    factorial_n,
    exponential_pdf,
    laplace_distribution,
    pareto_distribution,
    bernoulli_trial,
    poisson_distribution,
    srednia_goli_dom,
    skutecznosc_obron,
    przewiduj_gole_po_kartkach,
    agresja_druzyny,
    przewidywane_kontuzje,
    analiza_formy_zawodnika,
    wytrzymalosc_zawodnika,
    analiza_goli_w_minutach,
    pressing_vs_kontratak,
    analiza_wplywu_czasu_na_zmeczenie,
    tempo_druzyny,
    regresja_logistyczna,
    random_forest_predykcja,
    lstm_model,
    svm_model,
    xgboost_model,
    autoencoder_wynik,
    analiza_gry_w_powietrzu,
    efektywnosc_strefowa,
    analiza_ruchu_wyjscie_z_obrony,
    kontrola_posiadania,
    wykres_liniowy,
    wykres_slupkowy,
    wykres_obszarowy_3d
)
