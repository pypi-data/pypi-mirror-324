# -------------------------------------------------------------------------------
# Name:        didtools (diffindiff)
# Purpose:     Creating data for Difference-in-Differences Analysis
# Author:      Thomas Wieland (geowieland@googlemail.com)
# Version:     1.0.1
# Last update: 29.01.2025 18:17
# Copyright (c) 2025 Thomas Wieland
#-------------------------------------------------------------------------------

import pandas as pd
import numpy as np


def is_balanced (
    data,
    unit_col,
    time_col,
    outcome_col,
    other_cols = None
    ):

    """
    Funktion prueft ob die Daten ausbalanciert sind (gleich viele
    Beobachtungen fuer jede Kombination aus unit und time)
    """

    unit_freq = data[unit_col].nunique()
    # Anzahl Untersuchungseinheiten
    time_freq = data[time_col].nunique()
    # Anzahl Zeitpunkte
    unitxtime = unit_freq*time_freq
    # Wie viele Zeilen sollten es theoretisch sein? (Kartesisches Produkt Einheit x Zeit)

    if other_cols is None:
        cols_relevant = [unit_col, time_col, outcome_col]
    else:
        cols_relevant = [unit_col, time_col, outcome_col] + other_cols
        # "unit_col", "outcome_col" und "treatment_col" sind jeweils Strings,
        # aus denen eine Liste generiert wird. "other_cols" ist bereits eine Liste.
        # Beide werden verknuepft mit "+"

    data_relevant = data[cols_relevant]
    # nur der relevante Teil der Daten


    if unitxtime != len(data_relevant.notna()):
    # Wenn das df nicht so lang ist wie es sein sollte (fuer jede Kombination
    # aus unit und time ein Eintrag), dann ist der Datensatz nicht balanced
        return False
    else:
        return True


def is_missing(
    data,
    drop_missing: bool = True,
    missing_replace_by_zero: bool = False):

    """
    Funktion prueft ob es fehlende Werte gibt und schmeisst auf Wunsch
    die jeweiligen Zeilen raus
    """

    missing_outcome = data.isnull().any()
    # Prueft bei jeder (any) Spalte ob NAs dabei sind

    missing_outcome_var = any(missing_outcome == True)
    # mindestens einer True

    if missing_outcome_var == True:
        missing_true_vars = [name for name, value in missing_outcome.items() if value]
        # Name der Variablen, bei denen der Wert = True ist (d.h. wo NAs dabei sind)
    else:
        missing_true_vars = []
        # leere Liste

    if drop_missing:
        if missing_replace_by_zero:
            missing_replace_by_zero = False
            # nur eins von beidem moeglich ;)
        data = data.dropna(subset = missing_true_vars)
        # Alle Zeilen raus, in denen es in den spezifischen Spalten NAs gibt
        
    if missing_replace_by_zero:
        data[missing_true_vars] = data[missing_true_vars].fillna(0)
        # Alle fehlenden Werte auf 0 setzen

    return [missing_outcome_var, missing_true_vars, data]
    # Ausgabe als Liste mit 3 Eintraegen:
    # [0] Ergebnis der Pruefung (True oder False)
    # [1] Liste der Variablen, die fehlende Werte enthalten
    # [2] Datensatz, ggf. bereinigt


def is_simultaneous(
    data,
    unit_col,
    time_col,
    treatment_col
    ):

    """
    Funktion prueft ob die Intervention simultan (simultaneous) oder gestaffelt
    (staggered) einsetzt
    """

    # Identifizierung Interventions- und Kontrollgruppe:
    data_isnotreatment = is_notreatment(data, unit_col, treatment_col)
    # Analyse Datensatz mit is_notreatment()
    treatment_group = data_isnotreatment[1]
    # Extahieren Interventionsgruppe
    data_TG = data[data[unit_col].isin(treatment_group)]
    # nur Interventionsgruppe, denn bei der Kontrollgruppe gibt es ja keine Intervention

    data_TG_pivot = data_TG.pivot_table (index = time_col, columns = unit_col, values = treatment_col)
    # Pivot-Tabelle: Jede Untersuchungseinheit = 1 Spalte, Zeilen = Zeit

    col_identical = (data_TG_pivot.nunique(axis=1) == 1).all()
    # es wird geprueft, ob es JE ZEILE nur EINEN Wert gibt (1 ODER 0)
    # Wenn ja, dann ist der Treatment-Status an diesem Tag fuer alle
    # Untersuchungseinheiten identisch. Gepruef werden alle (.all())

    return col_identical


def is_notreatment(
    data,
    unit_col,
    treatment_col):

    """
    Funktion prueft ob es no-Treatment-Kontrollgruppe im Datensatz gibt
    anhand der Summe der Interventionsspalte je Untersuchungseinheit
    """

    data_relevant = data[[unit_col, treatment_col]]
    # Datensatz in kurz

    treatment_timepoints = data_relevant.groupby(unit_col).sum(treatment_col)
    # Summe der Treatment-Spalte (1/0) auf Ebene Untersuchungseinheiten
    treatment_timepoints = treatment_timepoints.reset_index()
    # alte Spaltennamen wieder

    no_treatment = (treatment_timepoints[treatment_col] == 0).any()
    # Gibt es zumindest einen Wert von 0 (=keine Intervention)?

    treatment_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] > 0, unit_col]
    control_group = treatment_timepoints.loc[treatment_timepoints[treatment_col] == 0, unit_col]
    # Interventions- und Kontrollgruppe jeweils in eine eigene Liste

    return [no_treatment, treatment_group, control_group]


def date_counter(df, date_col, new_col = "date_counter"):
    
    dates = df[date_col].unique()
    # Alle einzelnen Datumswerte
    #return(dates)

    date_counter = pd.DataFrame({
       'date': dates,
        new_col: range(1, len(dates) + 1)
        })
    # DataFrame, um Datum und den Zaehler zu kombinieren

    df = df.merge(
        date_counter,
        left_on = date_col,
        right_on = "date")
    
    return df