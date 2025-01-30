#-------------------------------------------------------------------------------
# Name:        didanalysis (diffindiff)
# Purpose:     Analysis functions for difference-in-differences analyses
# Author:      Thomas Wieland (geowieland@googlemail.com)
# Version:     1.0.1
# Last update: 29.01.2025 18:18
# Copyright (c) 2025 Thomas Wieland
#-------------------------------------------------------------------------------


import pandas as pd
from statsmodels.formula.api import ols
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from diffindiff import didtools


class did_model:
# Definition Klasse "did_model"
    def __init__(
        self,
        did_modelresults,
        did_modelconfig,
        did_modeldata,
        did_modelpredictions,
        did_fixed_effects,
        did_individual_effects,
        did_group_effects,
        did_model_statistics,
        did_olsmodel
        ):
    # Die "did_model"-Klasse ist eigentlich eine Liste mit 9 Eintraegen:
    # [0] model_results = Modellergebnisse (oben zusammengestellt als dict)
    # [1] model_config = Modellkonfiguration (oben zusammengestellt als dict)
    # [2] data = Datensatz des Nutzers, ggf. erweitert mit log Y (pandas df)
    # [3] model_predictions = Vorhergesagte Werte des Modells (pandas df)
    # [4] fixed_effects = Feste Effekte des Modells (Liste; leer, wenn keine FE)
    # [5] individual_effects = Individuelle Zeittrends bzw. Treatment-Effekte (Liste; leer, wenn keine da)
    # [6] group_effects = Gruppenspezifische Zeittrends bzw. Treatment-Effekte (Liste; leer, wenn keine da)
    # [7] model_statistics = Modellstatistiken u.a. R-Quadrat
    # [8] olsmodel = OLS-Modell Objekt

        self.data = [
            did_modelresults, 
            did_modelconfig, 
            did_modeldata, 
            did_modelpredictions, 
            did_fixed_effects,
            did_individual_effects,
            did_group_effects, 
            did_model_statistics, 
            did_olsmodel
            ]


    def treatment_statistics(self):

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] 
        # (hier: Modellkonfiguration aus create_data zzgl. weiterer Infos aus did_analysis)
        model_data = self.data[2]
        # Auslesen des data frames aus self.data[2] (hier: Modelldaten y und X)

        treatment_col = model_config["treatment_col"]
        # Spalte mit Treatment (1/0)
        time_col = model_config["time_col"]
        # Spalte mit Zeitpunkten
        after_treatment_period = model_config["after_treatment_period"]
        # Gibt es eine after treatment period? True/False
        unit_col = model_config["unit_col"]
        # Spalte mit Untersuchungseinheiten

        treatment_timepoints = model_data.groupby(unit_col)[treatment_col].sum()
        treatment_timepoints = pd.DataFrame(treatment_timepoints)
        treatment_timepoints = treatment_timepoints.reset_index()
        # Summe der Treatment-Spalte nach Untersuchungseinheit = Treatmentzeitraum je Untersuchungseinheit

        study_period_start = pd.to_datetime(min(model_data[time_col]))
        #study_period_start = datetime.strptime(min(model_data[time_col]), "%Y-%m-%d")
        study_period_start = study_period_start.date()
        #study_period_end = datetime.strptime(max(model_data[time_col]), "%Y-%m-%d")
        study_period_end = pd.to_datetime(max(model_data[time_col]))
        study_period_end = study_period_end.date()
        study_period_N = study_period_end-study_period_start
        study_period_N = study_period_N.days+1      
        # Laenge des gesamten Untersuchungszeitraums
        treatment_period_start = pd.to_datetime(min(model_data[model_data[treatment_col] == 1][time_col]))
        treatment_period_end = pd.to_datetime(max(model_data[model_data[treatment_col] == 1][time_col]))
        treatment_period_N = treatment_period_end-treatment_period_start
        treatment_period_N = treatment_period_N.days+1  
        # Laenge des gesamten Behandlungszeitraums
        after_treatment_period_start = None
        after_treatment_period_end = None
        after_treatment_period_N = None
        if after_treatment_period:
            after_treatment_period_start = treatment_period_end+pd.Timedelta(days=1)
            after_treatment_period_start = pd.to_datetime(after_treatment_period_start)
            after_treatment_period_end = pd.to_datetime(study_period_end)
            # sicherheitshalber beides konvertieren in datetime
            after_treatment_period_N = after_treatment_period_end-after_treatment_period_start
            after_treatment_period_N = after_treatment_period_N.days+1
            after_treatment_period_start = after_treatment_period_start.strftime("%Y-%m-%d")
            after_treatment_period_end = after_treatment_period_end.strftime("%Y-%m-%d")
        # Laenge der After-Treatment-Periode
        study_period_start = study_period_start.strftime("%Y-%m-%d")
        study_period_end = study_period_end.strftime("%Y-%m-%d")
        treatment_period_start = treatment_period_start.strftime("%Y-%m-%d")
        treatment_period_end = treatment_period_end.strftime("%Y-%m-%d")
        period_study = [study_period_start, study_period_end, study_period_N]
        period_treatment = [treatment_period_start, treatment_period_end, treatment_period_N]
        period_after_treatment = [after_treatment_period_start, after_treatment_period_end, after_treatment_period_N]
        time_periods = [period_study, period_treatment, period_after_treatment]
        # Zusammenstellung aller Infos als Liste

        treatment_group = np.array(treatment_timepoints[treatment_timepoints[treatment_col] > 0][unit_col])
        control_group = np.array(treatment_timepoints[treatment_timepoints[treatment_col] == 0][unit_col])
        groups = [treatment_group, control_group]
        # Liste mit 2 Eintraegen: 1. Behandlungsgruppe, 2. Kontrollgruppe (jeweils UID der Untersuchungseinheit)

        treatment_group_size = len(treatment_group)
        control_group_size = len(control_group)
        all_units = treatment_group_size+control_group_size
        treatment_group_share = treatment_group_size/all_units
        control_group_share = control_group_size/all_units
        group_sizes = [treatment_group_size, control_group_size, all_units, treatment_group_share, control_group_share]
        # Gruppengroessen absolut und relativ

        average_treatment_time = treatment_timepoints[treatment_timepoints[unit_col].isin(treatment_group)][treatment_col].mean()
        # Durchschnittliche Treatment-Zeit (nur unterschiedlich bei staggered adoption)
       

        return [
            group_sizes,
            average_treatment_time, 
            groups, 
            treatment_timepoints, 
            time_periods
            ]
        # Ausgabe als Liste mit 5 Eintraegen


    def summary(self):
        
        model_results = self.data[0]
        # Auslesen des dictionaries aus self.data[0] (hier: Modellkoeffizienten)
        # (verschachteltes dictionary)

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] 
        # (hier: Modellkonfiguration aus create_data zzgl. weiterer Infos aus did_analysis)

        model_data = self.data[2]
        # Auslesen des data frames aus self.data[2] (hier: Modelldaten y und X)

        outcome_col_original = model_config["outcome_col"]
        # Name von y im Original

        model_statistics = self.data[7]
        # 7. Element: Modellstatistiken


        # Tests:
        modeldata_isbalanced = didtools.is_balanced (
            data = model_data,
            unit_col = model_config["unit_col"],
            time_col = model_config["time_col"],
            outcome_col = model_config["outcome_col"]
            )
        # Pruefung ob Paneldaten balanced sind

        modeldata_isnotreatment = didtools.is_notreatment(
            data = model_data,
            unit_col = model_config["unit_col"],
            treatment_col = model_config["treatment_col"]
            )
        # Pruefung ob es eine No-Treatment-Kontrollgruppe gibt

        modeldata_issimultaneous = didtools.is_simultaneous(
            data = model_data,
            unit_col = model_config["unit_col"],
            time_col = model_config["time_col"],
            treatment_col = model_config["treatment_col"]
            )
        # Pruefung ob Intervention simultan oder gestaffelt (staggered)

        treatment_statistics = self.treatment_statistics()
        # Berechnung Statistiken
        

        print ("Difference-in-Differences Analysis")
        print ("===============================================================")

        # Block Modellergebnisse:
        if model_config["ITE"] is False and model_config["GTE"] is False: 
            print ("Average treatment effect:   " + str(round(model_results["ATE"]["ATE"], 3)) + "  SE=" + str(round(model_results["ATE"]["ATE_SE"], 3)) + "  t=" + str(round(model_results["ATE"]["ATE_t"], 3)) + "  p=" + str(round(model_results["ATE"]["ATE_p"], 3)))

        if model_config["ITE"]:
            individual_treatment_effects = self.data[5][1]
            # Auslesen individual_effects[1] = individual_treatment_effects = Individuelle Treatment-Effekte
            print ("Individual treatment effects:")
            coef_min = min(individual_treatment_effects["coef"])
            coef_min_SE = individual_treatment_effects[individual_treatment_effects["coef"] == coef_min]["SE"].iloc[0]
            coef_min_t = individual_treatment_effects[individual_treatment_effects["coef"] == coef_min]["t"].iloc[0]
            coef_min_p = individual_treatment_effects[individual_treatment_effects["coef"] == coef_min]["p"].iloc[0]
            # Auslesen kleinster Koeffizient zzgl. Standardfehler, t-Wert und p-Wert
            coef_min_unit = individual_treatment_effects[individual_treatment_effects["coef"] == coef_min][model_config["unit_col"]].iloc[0]
            # Auslesen Name der Untersuchungsheit mit dem kleinsten Koeffizienten
            coef_max = max(individual_treatment_effects["coef"])
            coef_max_SE = individual_treatment_effects[individual_treatment_effects["coef"] == coef_max]["SE"].iloc[0]
            coef_max_t = individual_treatment_effects[individual_treatment_effects["coef"] == coef_max]["t"].iloc[0]
            coef_max_p = individual_treatment_effects[individual_treatment_effects["coef"] == coef_max]["p"].iloc[0]
            # Auslesen groesster Koeffizient zzgl. Standardfehler, t-Wert und p-Wert
            coef_max_unit = individual_treatment_effects[individual_treatment_effects["coef"] == coef_max][model_config["unit_col"]].iloc[0]
            # Auslesen Name der Untersuchungsheit mit dem kleinsten Koeffizienten
            print ("Min. treatment effect(1):   " + str(round(coef_min, 3)) + " SE=" + str(round(coef_min_SE, 3)) + " t=" + str(round(coef_min_t, 3)) + " p="+ str(round(coef_min_p, 3)))
            print ("Max. treatment effect(2):   " + str(round(coef_max, 3)) + " SE=" + str(round(coef_max_SE, 3)) + " t=" + str(round(coef_max_t, 3)) + " p="+ str(round(coef_max_p, 3)))
            print ("(1) = unit '" + str(coef_min_unit) + "', (2) = unit '" + str(coef_max_unit) + "'")

        if model_config["GTE"]:
            group_treatment_effects = self.data[6][1]
            # Auslesen group_effects[1] = group_treatment_effects = Gruppenspezifische Treatment-Effekte
            print ("Group-specific treatment effects:")
            coef_min = min(group_treatment_effects["coef"])
            coef_min_SE = group_treatment_effects[group_treatment_effects["coef"] == coef_min]["SE"].iloc[0]
            coef_min_t = group_treatment_effects[group_treatment_effects["coef"] == coef_min]["t"].iloc[0]
            coef_min_p = group_treatment_effects[group_treatment_effects["coef"] == coef_min]["p"].iloc[0]
            # Auslesen kleinster Koeffizient zzgl. Standardfehler, t-Wert und p-Wert
            coef_min_unit = group_treatment_effects[group_treatment_effects["coef"] == coef_min][model_config["group_by"]].iloc[0]
            # Auslesen Name der Untersuchungsheit mit dem kleinsten Koeffizienten
            coef_max = max(group_treatment_effects["coef"])
            coef_max_SE = group_treatment_effects[group_treatment_effects["coef"] == coef_max]["SE"].iloc[0]
            coef_max_t = group_treatment_effects[group_treatment_effects["coef"] == coef_max]["t"].iloc[0]
            coef_max_p = group_treatment_effects[group_treatment_effects["coef"] == coef_max]["p"].iloc[0]
            # Auslesen groesster Koeffizient zzgl. Standardfehler, t-Wert und p-Wert
            coef_max_unit = group_treatment_effects[group_treatment_effects["coef"] == coef_max][model_config["group_by"]].iloc[0]
            # Auslesen Name der Untersuchungsheit mit dem kleinsten Koeffizienten
            print ("Min. treatment effect(1):   " + str(round(coef_min, 3)) + " SE=" + str(round(coef_min_SE, 3)) + " t=" + str(round(coef_min_t, 3)) + " p="+ str(round(coef_min_p, 3)))
            print ("Max. treatment effect(2):   " + str(round(coef_max, 3)) + " SE=" + str(round(coef_max_SE, 3)) + " t=" + str(round(coef_max_t, 3)) + " p="+ str(round(coef_max_p, 3)))
            print ("(1) = group '" + str(coef_min_unit) + "', (2) = group '" + str(coef_max_unit) + "'")

        if model_config["after_treatment_period"] is True:
            print ("Av. After Treatment Effect: " + str(round(model_results["AATE"]["AATE"], 3)) + "  SE=" + str(round(model_results["AATE"]["AATE_SE"], 3)) + "  t=" + str(round(model_results["AATE"]["AATE_t"], 3)) + "  p=" + str(round(model_results["AATE"]["AATE_p"], 3)))

        if model_config["FE_unit"] is False and model_config["FE_time"] is False and model_config["GTE"] is False:
            print ("Control group baseline:     " + str(round(model_results["Intercept"]["Intercept"], 3)) + "  SE=" + str(round(model_results["Intercept"]["Intercept_SE"], 3)) + "  t=" + str(round(model_results["Intercept"]["Intercept_t"], 3)) + " p=" + str(round(model_results["Intercept"]["Intercept_p"], 3)))

        if model_config["FE_unit"] is False and model_config["TG_col"] is not None and model_config["GTE"] is False:
            print ("Treatment group deviation:  " + str(round(model_results["TG"]["TG"], 3)) + "  SE=" + str(round(model_results["TG"]["TG_SE"], 3)) + "  t=" + str(round(model_results["TG"]["TG_t"], 3)) + " p=" + str(round(model_results["TG"]["TG_p"], 3)))

        if model_config["FE_time"] is False and model_config["TT_col"] is not None:
            print ("Non-treatment time effect:  " + str(round(model_results["TT"]["TT"], 3)) + "  SE=" + str(round(model_results["TT"]["TT_SE"], 3)) + "  t=" + str(round(model_results["TT"]["TT_t"], 3)) + " p=" + str(round(model_results["TT"]["TT_p"], 3)))


        # Block fixed effects:

        print ("---------------------------------------------------------------")
        print ("Fixed effects")
        if model_config["FE_unit"] is False:
            print ("Observation units:          NO")
        else:
            print ("Observation units:          YES")

        if model_config["FE_time"] is False:
            print ("Time periods:               NO")
        else:
            print ("Time periods:               YES")


        # Block Infos zu Kontrollvariablen (Kontrollbedingungen I):

        print ("---------------------------------------------------------------")
        print ("Control variables")

        if model_config["covariates"] is True:
            print ("Covariates:                 YES")
        else:
            print ("Covariates:                 NO")

        if model_config["ITT"] is True:
            print ("Individual time trends:     YES")
        else:
            print ("Individual time trends:     NO")

        if model_config["GTT"] is True:
            print ("Group-specific time trends: YES")
        else:
            print ("Group-specific time trends: NO")


        # Block Infos zum natuerlichen Experiment (Kontrollbedingungen II):

        print ("---------------------------------------------------------------")
        print ("Experimental conditions")

        if modeldata_issimultaneous:
            print ("Type of adoption:           Simultaneous")
        else:
            print ("Type of adoption:           Staggered")

        if modeldata_isnotreatment[0]:
            print ("No-treatment control group: YES")
        else:
            print ("No-treatment control group: NO")

        print ("Group sizes:                Treatment " + str(treatment_statistics[0][0]) + " (" + str(round(treatment_statistics[0][3]*100, 1)) + " %)")
        print ("                            Control " + str(treatment_statistics[0][1]) + " (" + str(round(treatment_statistics[0][4]*100, 1)) + " %)")
        if modeldata_issimultaneous:
            if model_config["pre_post"]:
                print ("Treatment period:           Pre-post")
            else:
                print ("Treatment period:           " + str(int(treatment_statistics[1])) + " of " + str(int(treatment_statistics[4][0][2])) + " time points")
        else:
            if model_config["pre_post"]:
                print ("Treatment period:           Pre-post")
            else:
                print ("Average treatment period:   " + str(int(treatment_statistics[1])) + " of " + str(int(treatment_statistics[4][0][2])) + " time points")
        

        # Block Infos zu den Daten:
        print ("---------------------------------------------------------------")
        print ("Input data")

        if modeldata_isbalanced is True:
            print ("Balanced panel data:        YES")
        else:
            print ("Balanced panel data:        NO")

        print ("Outcome variable:           " + outcome_col_original + " (Mean=" + str(round(np.mean(model_data[outcome_col_original]), 2)) + " SD=" + str(round(np.std(model_data[outcome_col_original]), 2)) + ")")

        print ("Number of observations:     " + str(len(model_data)))


        # Block zur Outcome-Variable:
        print ("---------------------------------------------------------------")
        print ("R-Squared:                  " + str(round(model_statistics["rsquared"], 3)))
        print ("Adj. R-Squared:             " + str(round(model_statistics["rsquared_adj"], 3)))
        print ("===============================================================")

        if modeldata_isnotreatment[0] == False and modeldata_issimultaneous == True:
            print ("WARNING: All analysis units received the treatment exactly")
            print ("at the same time. There are no control conditions.")

        if model_config["GTE"]:
            print ("NOTE: For a full list of group treatment effects, use")
            print ("did_model.groupef(), did_model.plot_group_treatment_effects().")

        if model_config["ITE"]:
            print ("NOTE: For a full list of individual treatment effects, use")
            print ("did_model.indef(), did_model.plot_individual_treatment_effects().")

        # Ausgabe:

        model_diagnosis = {
            "isnotreatment": modeldata_isnotreatment[0],
            "issimultaneous": modeldata_issimultaneous,
            "isbalanced": modeldata_isbalanced
            }
        # weiteres Dict mit Ergebnissen Modelldiagnosen
        
        return [
            model_results, 
            model_config, 
            model_data, 
            model_statistics,
            model_diagnosis,
            treatment_statistics
            ]
        # Ausgabe als Liste
    

    def predictions(self):

        model_predictions = self.data[3]
        # Auslesen des dictionaries aus self.data[3] (hier: Vorhergesagte Werte)

        return model_predictions


    def effects(self):

        model_results = self.data[0]
        # Auslesen des dictionaries aus self.data[0] (hier: Modellkoeffizienten)
        # (verschachteltes dictionary)

        effects_df = pd.DataFrame (columns = ["effect_name", "coef", "SE", "t", "p", "CI_lower", "CI_upper"])

        if "ATE" in model_results:
            ATE = pd.DataFrame([{
                "effect_name": "ATE",
                "coef": model_results["ATE"]["ATE"],
                "SE": model_results["ATE"]["ATE_SE"],
                "t": model_results["ATE"]["ATE_t"],
                "p": model_results["ATE"]["ATE_p"],
                "CI_lower": model_results["ATE"]["ATE_CI_lower"],
                "CI_upper": model_results["ATE"]["ATE_CI_upper"]
                }])
            effects_df = pd.concat([effects_df, ATE], ignore_index=True)

        if "AATE" in model_results:
            AATE = pd.DataFrame([{
                "effect_name": "AATE",
                "coef": model_results["AATE"]["AATE"],
                "SE": model_results["AATE"]["AATE_SE"],
                "t": model_results["AATE"]["AATE_t"],
                "p": model_results["AATE"]["AATE_p"],
                "CI_lower": model_results["AATE"]["AATE_CI_lower"],
                "CI_upper": model_results["AATE"]["AATE_CI_upper"]
                }])
            effects_df = pd.concat([effects_df, AATE], ignore_index=True)
        
        if "Intercept" in model_results:
            Intercept = pd.DataFrame([{
                "effect_name": "Intercept",
                "coef": model_results["Intercept"]["Intercept"],
                "SE": model_results["Intercept"]["Intercept_SE"],
                "t": model_results["Intercept"]["Intercept_t"],
                "p": model_results["Intercept"]["Intercept_p"],
                "CI_lower": model_results["Intercept"]["Intercept_CI_lower"],
                "CI_upper": model_results["Intercept"]["Intercept_CI_upper"]
                }])
            effects_df = pd.concat([effects_df, Intercept], ignore_index=True)

        if "TG" in model_results:
            TG = pd.DataFrame([{
                "effect_name": "TG",
                "coef": model_results["TG"]["TG"],
                "SE": model_results["TG"]["TG_SE"],
                "t": model_results["TG"]["TG_t"],
                "p": model_results["TG"]["TG_p"],
                "CI_lower": model_results["TG"]["TG_CI_lower"],
                "CI_upper": model_results["TG"]["TG_CI_upper"]
                }])
            effects_df = pd.concat([effects_df, TG], ignore_index=True)

        if "TT" in model_results:
            TT = pd.DataFrame([{
                "effect_name": "TT",
                "coef": model_results["TT"]["TT"],
                "SE": model_results["TT"]["TT_SE"],
                "t": model_results["TT"]["TT_t"],
                "p": model_results["TT"]["TT_p"],
                "CI_lower": model_results["TT"]["TT_CI_lower"],
                "CI_upper": model_results["TT"]["TT_CI_upper"]
                }])
            effects_df = pd.concat([effects_df, TT], ignore_index=True)

        return effects_df


    def fixef(self):

        fixed_effects = self.data[4]
        # Auslesen aus self.data[4]

        return fixed_effects


    def indef(self):

        individual_effects = self.data[5]
        # Auslesen aus self.data[5]

        return individual_effects


    def groupef(self):

        group_effects = self.data[6]
        # Auslesen aus self.data[6]

        return group_effects


    def olsmodel(self):

        ols_model = self.data[8]
        # Auslesen 9. Eintrag (OLS-Modell)

        return ols_model


    def plot_timeline(
        self,
        x_label = "Time",
        y_label = "Analysis units",
        plot_title = "Treatment time",
        plot_symbol = "o",
        treatment_group_only = True
        ):

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] (hier: Konfiggg)
        
        model_data = self.data[2]
        # Auslesen des df aus self.data[2] (hier: Modelldaten)
                
        if treatment_group_only is True:
            model_data = model_data[model_data[model_config["TG_col"]] == 1]

        modeldata_pivot = model_data.pivot_table (
            index = model_config["time_col"],
            columns = model_config["unit_col"],
            values = model_config["treatment_col"]
            )
        # Pivot-Tabelle: Jede Untersuchungseinheit = 1 Spalte, Zeilen = Zeit

        # Erstelle eine neue Figur und Achsen
        fig, ax = plt.subplots(figsize=(12, len(modeldata_pivot.columns) * 0.5))

        modeldata_pivot.index = pd.to_datetime(modeldata_pivot.index)

        # Fuer jede Spalte im df ...
        for i, col in enumerate(modeldata_pivot.columns):
            time_points = modeldata_pivot.index
            # Alle Zeitpunkte im df (muessten bei allen dieselben sein)
            treatment_data = np.zeros(len(time_points))
            # leere Daten
            time_points_treatment = modeldata_pivot.index[modeldata_pivot[col] == 1]
            # Zeitpunkte, an denen der Wert 1 ist (=Treatment period)
            values = [i] * len(time_points_treatment)
            # Generiere Werte fuer Plot fuer die jeweilige df-Spalte
            ax.plot(time_points_treatment, values, plot_symbol, label=col)
            # Zeichne Punkte fuer diese Spalte

        # Achsenbeschriftungen und den Titel:
        ax.set_xlabel(x_label)
        ax.set_yticks(range(len(modeldata_pivot.columns)))
        ax.set_yticklabels(modeldata_pivot.columns)
        ax.set_ylabel(y_label)
        ax.set_title(plot_title)

        # Explizite Formatierung X-Achse:
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        # Datum

        # Diagramm formatieren:
        plt.xticks(rotation=90)
        # X-Achse vertikal
        plt.tight_layout()
        # Mehr Platz fuer Achsenbeschriftungen

        start_date = min(modeldata_pivot.index)
        end_date = max(modeldata_pivot.index)
        ax.set_xlim(start_date, end_date)

        plt.tight_layout()
        plt.xticks(rotation=90)

        plt.show()


    def plot(
        self,
        x_label: str = "Time",
        y_label: str = "Outcome",
        plot_title: str = "Treatment group vs. control group",
        lines_col: list = ["blue", "green", "red", "orange"],
        lines_style: list = ["solid", "solid", "dashed", "dashed"],
        lines_labels: list = ["TG observed", "CG observed", "TG fit", "CG fit"],
        plot_legend: bool = True,
        plot_grid: bool = True,
        plot_observed: bool = False,
        plot_size_auto: bool = True,
        plot_size: list = [12, 6],
        pre_post_ticks: list = ["Pre", "Post"],
        pre_post_barplot = False,
        pre_post_bar_width = 0.5      
        ):

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] (hier: Konfick)

        model_data = self.data[2]
        # Auslesen des df aus self.data[2] (hier: Modelldaten)

        model_predictions = self.data[3]
        # Auslesen des df aus self.data[3] (hier: Vorhergesagte Werte)

        model_data = model_data.reset_index()
        # Index resetten fuer spaeteren concat

        model_predictions = pd.DataFrame(model_predictions)
        # Vorhersagen in df umwandeln ...
        model_predictions = model_predictions.reset_index()
        # ... und auch Index resetten
        model_predictions.rename(columns = {0: "outcome_predicted"}, inplace = True)
        # Spalte umbenennen

        model_data = pd.concat ([model_data, model_predictions], axis = 1)
        # beides zusammenklatschen

        model_data_TG = model_data[model_data["TG"] == 1]
        # nur Interventionsgruppe
        model_data_CG = model_data[model_data["TG"] == 0]
        # nur Kontrollgruppe

        # Aggregation outcome nach Treatment- und Kontrollgruppe und Zeitpunkten:
        model_data_TG_mean = model_data_TG.groupby(model_config["time_col"])[model_config["outcome_col"]].mean()
        model_data_TG_mean = model_data_TG_mean.reset_index()
        # Mittelwert Interventionsgruppe ueber die Zeit
        model_data_CG_mean = model_data_CG.groupby(model_config["time_col"])[model_config["outcome_col"]].mean()
        model_data_CG_mean = model_data_CG_mean.reset_index()
        # Mittelwert Kontrollgruppe ueber die Zeit

        # Aggregation VORHERGESAGTER outcome nach Treatment- und Kontrollgruppe und Zeitpunkten:
        model_data_TG_mean_pred = model_data_TG.groupby(model_config["time_col"])["outcome_predicted"].mean()
        model_data_TG_mean_pred = model_data_TG_mean_pred.reset_index()
        # Mittelwert Interventionsgruppe ueber die Zeit
        model_data_CG_mean_pred = model_data_CG.groupby(model_config["time_col"])["outcome_predicted"].mean()
        model_data_CG_mean_pred = model_data_CG_mean_pred.reset_index()
        # Mittelwert Kontrollgruppe ueber die Zeit

        model_data_TG_CG = pd.concat ([
            model_data_TG_mean.reset_index(),
            # Interventionsgruppe MW beobachtete Werte
            model_data_CG_mean[model_config["outcome_col"]].reset_index(),
            # Kontrollgruppe MW beobachtete Werte
            model_data_TG_mean_pred["outcome_predicted"].reset_index(),
            # Interventionsgruppe MW Modellwerte
            model_data_CG_mean_pred["outcome_predicted"].reset_index()
            # Kontrollgruppe MW Modellwerte
            ],
            axis = 1)
        # alles z'samm

        model_data_TG_CG.columns.values[1] = "t"
        model_data_TG_CG.columns.values[2] = model_config["outcome_col"] + "_observed_TG"
        model_data_TG_CG.columns.values[4] = model_config["outcome_col"] + "_observed_CG"
        model_data_TG_CG.columns.values[6] = model_config["outcome_col"] + "_expected_TG"
        model_data_TG_CG.columns.values[8] = model_config["outcome_col"] + "_expected_CG"
        # Spalten sinnvoll benennen


        if plot_size_auto:
            if model_config["pre_post"]:
                fig, ax = plt.subplots(figsize=(7, 6))
            else:
                fig, ax = plt.subplots(figsize=(12, 6))
        else:
            fig, ax = plt.subplots(figsize=(plot_size[0], plot_size[1]))       
        # Plot initialisieren je nach angegebener Groesse


        model_data_TG_CG["t"] = pd.to_datetime(model_data_TG_CG["t"])

        if not model_config["pre_post"]:
            pre_post_barplot = False


        if pre_post_barplot:
            
            # X-Positionen fuer die Balken (absolut, keine Verschiebung)
            x_pos_t1_TG = 0
            x_pos_t1_CG = x_pos_t1_TG + pre_post_bar_width  
            # Balken nebeneinander
            x_pos_t2_TG = 1.5  
            # Verschiebung zu Zeitpunkt 2
            x_pos_t2_CG = x_pos_t2_TG + pre_post_bar_width  
            # Balken nebeneinander

            plt.bar(
                x = x_pos_t1_TG, 
                height = model_data_TG_CG[model_config["outcome_col"] + "_expected_TG"][0], 
                label = lines_labels[2], 
                color = lines_col[2], 
                width = pre_post_bar_width
                )
            
            plt.bar(
                x = x_pos_t1_CG, 
                height = model_data_TG_CG[model_config["outcome_col"] + "_expected_CG"][0], 
                label = lines_labels[3], 
                color = lines_col[3], 
                width = pre_post_bar_width
                )
            
            plt.bar(
                x = x_pos_t2_TG, 
                height = model_data_TG_CG[model_config["outcome_col"] + "_expected_TG"][1], 
                #label = lines_labels[2], 
                color = lines_col[2], 
                width = pre_post_bar_width
                )
            
            plt.bar(
                x = x_pos_t2_CG, 
                height = model_data_TG_CG[model_config["outcome_col"] + "_expected_CG"][1], 
                #label=lines_labels[3], 
                color=lines_col[3], 
                width = pre_post_bar_width
                )

            # Diagramm zusammenstellen:
            plt.xlabel(x_label)
            # X-Achse Beschriftung
            plt.ylabel(y_label)
            # Y-Achse Beschriftung
            plt.title(plot_title)
            # Titel
            
        else:

            if plot_observed:
                plt.plot(
                    model_data_TG_CG["t"], 
                    model_data_TG_CG[model_config["outcome_col"] + "_observed_TG"], 
                    label = lines_labels[0], 
                    color=lines_col[0], 
                    linestyle=lines_style[0]
                    )
                plt.plot(
                    model_data_TG_CG["t"], 
                    model_data_TG_CG[model_config["outcome_col"] + "_observed_CG"], 
                    label = lines_labels[1], 
                    color=lines_col[1], 
                    linestyle=lines_style[1]
                    )
            
            plt.plot(
                model_data_TG_CG["t"], 
                model_data_TG_CG[model_config["outcome_col"] + "_expected_TG"], 
                label=lines_labels[2], 
                color=lines_col[2], 
                linestyle=lines_style[2]
                )
            plt.plot(
                model_data_TG_CG["t"], 
                model_data_TG_CG[model_config["outcome_col"] + "_expected_CG"], 
                label=lines_labels[3], 
                color=lines_col[3], 
                linestyle=lines_style[3]
                )

            # Diagramm zusammenstellen:
            plt.xlabel(x_label)
            # X-Achse Beschriftung
            plt.ylabel(y_label)
            # Y-Achse Beschriftung
            plt.title(plot_title)
            # Titel

            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            # Explizite Formatierung X-Achse als Datum

        # Diagramm formatieren:
        if model_config["pre_post"]:
            if not pre_post_barplot:
                plt.xticks(
                    model_data_TG_CG["t"].unique(), 
                    labels = [pre_post_ticks[0], pre_post_ticks[1]]
                    )  
                # Achsenbeschriftungen bei Linienplot
            else:
                plt.xticks(
                    [0.25, 1.75], 
                    labels = [pre_post_ticks[0], pre_post_ticks[1]]
                    )  
                # Achsenbeschriftungen bei Barplot
        else:
            plt.xticks(rotation=90)
            # X-Achse vertikal
        
        plt.tight_layout()
        # Mehr Platz fuer Achsenbeschriftungen

        if plot_legend is True:
            plt.legend()

        if plot_grid is True:
            if not model_config["pre_post"]:
                plt.grid(True)
            else:
                plt.grid(axis='y', linestyle='-', alpha=0.7)

        plt.show()

        return model_data_TG_CG
    
    
    def plot_effects(
        self,
        colors = ["blue", "grey"],
        x_label = "Coefficients with confidence intervals",
        plot_title = "DiD effects",
        plot_grid: bool = True,
        sort_by = "name",
        sort_ascending: bool = True,
        plot_size: list = [7, 6],      
        scale_plot: bool = True
        ):
        
        effects = self.effects()
        # Auslesen des Effekte-dfs, erstellt mit Funktion effects()
        print(effects)
        if sort_by == "coef":
            effects = effects.sort_values(
                by = "coef", 
                ascending = not sort_ascending
                )
        else:
            effects = effects.sort_values(
                by = "effect_name", 
                ascending = not sort_ascending
                )

        plt.figure(figsize=(plot_size[0], plot_size[1]))
        
        plt.errorbar(
            x = effects["coef"], 
            y = effects["effect_name"],
            xerr = [effects["coef"] - effects["CI_lower"], effects["CI_upper"] - effects["coef"]], 
                    fmt='o', 
                    color=colors[0], 
                    ecolor=colors[1], 
                    elinewidth=2, 
                    capsize=4, 
                    label="")
        # Punktschaetzer als Punkte, Konfidenzintervalle als Linien

        if scale_plot:
            maxval = effects[["coef", "CI_lower", "CI_upper"]].abs().max().max()
            maxval_plot = maxval*1.1
            plt.xlim(-maxval_plot, maxval_plot)
        # Wenn gewuenscht, wird Plot automatisch skaliert (so dass 0 immer dabei ist)

        plt.xlabel(x_label, fontsize=12)
        plt.title(plot_title, fontsize=14)
        # Achsenbeschriftungen und Titel
        
        if plot_grid:
            plt.grid(True)
        # Wenn gewuenscht: Grid hinzufuegen

        plt.show()
        # Plot zeigen


    def plot_group_treatment_effects (
            self,
            colors = ["blue", "grey"],
            x_label = "Treatment effect",
            y_label = "Groups",
            plot_title = "Group treatment effects",        
            treatment_group_only = False,
            sort_by = "group",
            sort_ascending = True,
            plot_size: list = [9, 6],
            show_central_tendency = False,
            central_tendency = "mean"
            ):

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] (hier: Modellkonfiguration aus create_data)
        if not model_config["GTE"]:
            raise ValueError ("Model does not include group treatment effects. Set GTE=True an define grouping variable using group_by.")
        group_by = model_config["group_by"]
        # Name der Spalte mit den Untersuchungseinheiten im Original
        if group_by is None:
            raise ValueError ("Grouping variable is not defined. Define a grouping variable using group_by.")
        
        # Auslesen und ggf. Nachbearbeitung df mit individuellen Treatment-Effekten:
        group_treatment_effects = self.data[6][1]
        # Auslesen gruppenspezifische Treatment-Effekte aus self.data[6] = group_effects 
        # = Liste mit 2 Eintraegen (1. gruppenspez. Zeittrends, 2. gruppenspez. Effekte)
        if treatment_group_only is True:
            TG_col = model_config["TG_col"]
            # Name der Spalte mit der Zuweisung der Treatment-Gruppe
            model_data = self.data[2]
            # Auslesen des df aus self.data[2] (hier: Modelldaten)
            treatment_group = model_data[model_data[TG_col] == 1].drop_duplicates(subset=[group_by])[group_by]
            # Untersuchungseinheiten, die sich in der Treatment-Gruppe befinden, aus Daten auslesen
            group_treatment_effects = group_treatment_effects[group_treatment_effects[group_by].isin(treatment_group)]
            # GTE-df filtern: nur Treatment-Gruppe
        if sort_by == "coef":
            group_treatment_effects = group_treatment_effects.sort_values(
                by = "coef", 
                ascending = not sort_ascending
                )
        else:
            group_treatment_effects = group_treatment_effects.sort_values(
                by = group_by, 
                ascending = not sort_ascending
                )
        
        # Plot erzeugen
        plt.figure(figsize=(plot_size[0], plot_size[1]))
        # User-Eingabe Groesse
        
        plt.errorbar(
            x = group_treatment_effects["coef"], 
            y = group_treatment_effects[group_by],
            xerr = [group_treatment_effects["coef"] - group_treatment_effects["lower"], group_treatment_effects["upper"] - group_treatment_effects["coef"]], 
                    fmt='o', 
                    color=colors[0], 
                    ecolor=colors[1], 
                    elinewidth=2, 
                    capsize=4, 
                    label="")
        # Punktschaetzer als Punkte, Konfidenzintervalle als Linien

        if show_central_tendency is True:
        # Wenn mittlerer Effekt angezeigt werden soll
            if central_tendency == "median":
                ITE_ct = np.median(group_treatment_effects["coef"])
                # Median (wenn explizit gewuenscht)
            else:
                ITE_ct = np.mean(group_treatment_effects["coef"])
                # ansonsten arithmetisches Mittel
            plt.axvline(x = ITE_ct, color = "black")
            # aequivalent zu abline() in R: vertikale Linie mit gegebener x-Position
        else:
            pass

        # Achsenbeschriftungen
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(plot_title, fontsize=14)
        
        # Grid hinzufuegen
        plt.grid(True)
        
        # Plot anzeigen
        plt.show()


    def plot_individual_treatment_effects (
            self,
            colors = ["blue", "grey"],
            x_label = "Treatment effect",
            y_label = "Analysis units",
            plot_title = "Individual treatment effects",        
            treatment_group_only = False,
            sort_by = "unit",
            sort_ascending = True,
            plot_size: list = [9, 6],
            show_central_tendency = False,
            central_tendency = "mean"
            ):

        model_config = self.data[1]
        # Auslesen des dictionaries aus self.data[1] (hier: Modellkonfiguration aus create_data)
        if not model_config["ITE"]:
            raise ValueError ("Model does not include individuel treatment effects. Set ITE=True for including.")        
        unit_col = model_config["unit_col"]
        # Name der Spalte mit den Untersuchungseinheiten im Original
        
        # Auslesen und ggf. Nachbearbeitung df mit individuellen Treatment-Effekten:
        individual_treatment_effects = self.data[5][1]
        # Auslesen individuelle Treatment-Effekte aus self.data[5]
        if treatment_group_only is True:
            TG_col = model_config["TG_col"]
            # Name der Spalte mit der Zuweisung der Treatment-Gruppe
            model_data = self.data[2]
            # Auslesen des df aus self.data[2] (hier: Modelldaten)
            treatment_group = model_data[model_data[TG_col] == 1].drop_duplicates(subset=[unit_col])[unit_col]
            # Untersuchungseinheiten, die sich in der Treatment-Gruppe befinden, aus Daten auslesen
            individual_treatment_effects = individual_treatment_effects[individual_treatment_effects[unit_col].isin(treatment_group)]
            # ITE-df filtern: nur Treatment-Gruppe
        if sort_by == "coef":
            individual_treatment_effects = individual_treatment_effects.sort_values(
                by = "coef", 
                ascending = not sort_ascending
                )
        else:
            individual_treatment_effects = individual_treatment_effects.sort_values(
                by = unit_col, 
                ascending = not sort_ascending
                )
        
        # Plot erzeugen
        plt.figure(figsize=(plot_size[0], plot_size[1]))
        # User-Eingabe Groesse
        
        plt.errorbar(
            x = individual_treatment_effects["coef"], 
            y = individual_treatment_effects[unit_col],
            xerr = [individual_treatment_effects["coef"] - individual_treatment_effects["lower"], individual_treatment_effects["upper"] - individual_treatment_effects["coef"]], 
                    fmt='o', 
                    color=colors[0], 
                    ecolor=colors[1], 
                    elinewidth=2, 
                    capsize=4, 
                    label="")
        # Punktschaetzer als Punkte, Konfidenzintervalle als Linien

        if show_central_tendency is True:
        # Wenn mittlerer Effekt angezeigt werden soll
            if central_tendency == "median":
                ITE_ct = np.median(individual_treatment_effects["coef"])
                # Median (wenn explizit gewuenscht)
            else:
                ITE_ct = np.mean(individual_treatment_effects["coef"])
                # ansonsten arithmetisches Mittel
            plt.axvline(x = ITE_ct, color = "black")
            # aequivalent zu abline() in R: vertikale Linie mit gegebener x-Position
        else:
            pass

        # Achsenbeschriftungen
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(plot_title, fontsize=14)
        
        # Grid hinzufuegen
        plt.grid(True)
        
        # Plot anzeigen
        plt.show()


def did_analysis(
    data,
    unit_col,
    time_col,
    treatment_col,
    outcome_col,
    TG_col = None,
    TT_col = None,
    after_treatment_period: bool = False,
    after_treatment_col = None,
    pre_post = False,
    log_outcome: bool = False,
    FE_unit: bool = False,
    FE_time: bool = False,
    ITE: bool = False,
    GTE: bool = False,
    ITT: bool = False,
    GTT: bool = False,
    group_by = None,
    covariates = None,
    confint_alpha = 0.05,
    drop_missing: bool = True,
    missing_replace_by_zero: bool = False
    ):

    """
    Definition Funktion "did_analysis()" fuer DiD-Analyse mit einem bestehenden
    Pandas data frame, z.B. wenn Daten schon fertig vorliegen und/oder das Treatment
    nicht bei allen Treatment-Einheiten zur gleichen Zeit startet/endet (staggered adoption)
    Parameter:
        data = Datensatz (pd.DataFrame) mit allen Daten
        unit_col = Spalte mit unique ID der Untersuchungseinheit (i = 1,2,...,I)
        time_col = Spalte mit Zeitpunkten (t = 1,2,...,T)
        treatment_col = Spalte mit Treatment (Dummy: 1 bzw. 0)
        outcome_col = Spalte mit abhaengiger Variable (Y_it mit i = unit und t = Zeitpunkt)
        TG_col = Spalte mit Zuordnung zu Treatment- oder Kontrolgruppe (Dummy: 1 bzw. 0)
            (nicht notwendig bei Modellen mit FE)
        TT_col = Spalte mit Zuordnung zu Treatment-Zeit (Dummy: 1 bzw. 0)
            (nicht notwendig bei Modellen mit FE)
        after_treatment_period = Gibt es eine Nachinterventionsperiode? (True/False)
        after_treatment_col = Spalte mit Nachinterventionsperiode
        FE_unit = Boolean-Parameter (True = mit FE fuer Untersuchungseinheiten)
        FE_time = Boolean-Parameter (True = mit FE fuer Zeitpunkte)
        ITE = Boolean-Parameter (True = mit individuellen Treatment-Effekten)
        GTE = Boolean-Parameter (True = mit gruppenspezifischen Treatment-Effekten)
        ITT = Boolean-Parameter (True = mit individuellem Zeittrend)
        GTT = Boolean-Parameter (True = mit gruppenspezifischen Zeittrends)
        group_by = Bei gruppenspezifischen Effekten: Anhand welcher Spalte aufteilen?      
        covariates = Liste mit etwaigen Kovariaten (Spaltennamen)
        confint_alpha = Alpha fuer Signifikanzpruefung
        drop_missing = Sollen NA-Werte aus df entfernt werden? (True/False)
        missing_replace_by_zero = Sollen NA-Werte aus df auf 0 gesetzt werden? (True/False)
    """

    # Schritt 1) Pruefung von Parametern, die sich logisch ausschliessen:
    
    if ITE is True:
        GTE = False
    if ITT is True:
        GTT = False
    # ENTWEDER Gruppen- ODER individuelle Effekte
    # Wenn faelschlicherweise beides angegeben wurde, sticht Indiviualeffekt


    # Schritt 2) Zusammenstellung der relevanten Spalten aus dem uebergebenen Datensatz:
    
    cols_relevant = [
        unit_col,
        time_col,
        treatment_col,
        outcome_col]
    # Relevante Spalten (diese 4 sind IMMER notwendig)

    if after_treatment_period is True:
        cols_relevant = cols_relevant + [after_treatment_col]

    if TG_col is not None:
    # Wenn eine Spalte fuer Gruppenzuordnung angegeben wurde...
        cols_relevant.append(TG_col)
        # ... dann ist diese Spalte relevant und soll mit extrahiert werden
    else:
        FE_unit = True

        # Identifizierung Treatment- und Kontrollgruppe:
        groups = didtools.is_notreatment(
            data = data,
            unit_col = unit_col,
            treatment_col = treatment_col
            )
        treatment_group = groups[1]
        # und Spalte TG mit dazu:
        data["TG"] = 0
        data.loc[data[unit_col].isin(treatment_group), "TG"] = 1
        # Treatment-Gruppe wird auf 1 gesetzt

        TG_col = "TG"

        cols_relevant = [
        unit_col,
        time_col,
        treatment_col,
        TG_col,
        outcome_col
        ]
        # Spalte soll mit extrahiert werden, daher hier neue Liste cols_relevant


    if TT_col is not None:
    # Wenn eine Spalte fuer Zeitpunkte angegeben wurde...
        cols_relevant.append(TT_col)
        # ... dann ist diese Spalte relevant und soll mit extrahiert werden
    else:
        FE_time = True

    if covariates is not None:
        cols_relevant.extend(covariates)
    # Wenn Kontrollvariablen angegeben werden, wird jedes Element
    # der Liste covariates an die Liste cols_relevant angehaengt (extend, nicht append!)

    data = data[cols_relevant]
    # Datensatz kuerzen --> Nur die relevanten Spalten


    # Schritt 3) Test fuer Datensatz auf fehlende Werte, ggf. Korrektur: 

    modeldata_ismissing = didtools.is_missing(
        data, 
        drop_missing = drop_missing,
        missing_replace_by_zero = missing_replace_by_zero
        )
    # Pruefung ob es fehlende Werte gibt

    if modeldata_ismissing[0] is True:
        print("Variables contain NA values: "+'+'.join(modeldata_ismissing[1]), end = ". ")
        #print(modeldata_ismissing[1])
        # 2. Eintrag [1] sind die Variablen mit NA-Werten

        if drop_missing or missing_replace_by_zero:
            data = modeldata_ismissing[2]
            # 3. Eintrag [2] sind bereinigte Daten (NAs entweder raus oder gleich 0 gesetzt)
                
        if drop_missing:
            print ("Rows with missing values are skipped.")
        elif missing_replace_by_zero:
            print ("Missing values are replaced by 0.")
        else:
            print ("Missing values are not cleaned. Model may crash.")

        
    if log_outcome is True:
        data["log_"+f'{outcome_col}'] = np.log(data[outcome_col])
        outcome_col = "log_"+f'{outcome_col}'


    # Schritt 4) Zusammenstellung Regressionsformel:

    # Basis-Formel:    
    did_formula = f'{outcome_col} ~ {treatment_col}'
    # AV ist immer outcome, treatment_col ist IMMER als UV dabei 
    # (ausser bei Modellen mit individuellen Treatment-Effekten)

    # Dummys fuer Treatment-Gruppe und Zeitpunkte:
    if TG_col is not None and ITE is False and GTE is False:
        did_formula = did_formula + f'+ {TG_col}'
        # Dummy fuer Treatment-Gruppe hinfaellig wenn nicht angegeben oder ITE/GTE gewuenscht
    if TT_col is not None:
        did_formula = did_formula + f'+ {TT_col}'

    # 3 Variablen == Basismodell:
    # did_formula = f'{outcome_col} ~ {TG_col} + {TT_col} + {treatment_col}'


    # Ueberpruefungen muessen stattfinden bevor Formel mit FE gebildet wird:
    
    if ITT is True:
    # Wenn ein individueller Zeittrend (ITT = Individual time trend)
    # ins Modell aufgenommen werden soll...
        FE_unit = True
        # ...dann sind FE fuer Untersuchungseinheiten notwendig...
        FE_time = False
        # ...und FE fuer Zeitpunkte muessen rausfliegen...
        # stattdessen Zeit als numerische Variable rein

    if ITE is True:
    # wenn individuelle Treatment-Effekte (ITE = Individual treatment effects)
    # berechnet werden sollen...
        FE_unit = True
        # ...dann sind FE fuer Untersuchungseinheiten notwendig


    # After-Treatment-Periode:

    if after_treatment_period is True:
    # Wenn es auch eine Nachinterventionsperiode gibt
        did_formula = did_formula + f'+ {after_treatment_col}'
        # Spalte mit Nach-Interventions-Dummy mit in Regressionsformel


    # Feste Effekte:
    
    if FE_unit is True:
    # wenn FE fuer die Untersuchungseinheiten gewuenscht sind (FE_unit == True)
        data[unit_col] = data[unit_col].astype(str)
        # Spalte mit Untersuchungseinheiten als String setzen
        did_formula = did_formula + f'+ {unit_col}'
        # In Regressionsformel zusaetzlich Spalte mit Untersuchungseinheiten dazu
        # dafuer kein Intercept (weil sonst ggf perfekte Kollinearitaet)

    if FE_time is True:
    # wenn FE fuer die Zeitpunkte gewuenscht sind (FE_time == True)
        data[time_col] = data[time_col].astype(str)
        # Spalte mit Zeit als String setzen
        # ==> automatisch Dummy-Variablen fuer jeden Zeitpunkt im Modell
        did_formula = did_formula + f'+ {time_col}'
        # In Regressionsformel zusaetzlich Spalte mit Zeit dazu
        # dafuer kein Intercept (weil sonst ggf perfekte Kollinearitaet)


    # Schritt 5) Berechnung etwaiger neuer UV:

    # Vorbereitung Dummy-Variablen fuer Gruppen (wenn gruppenspez. Zeittrends oder Effekte gewuenscht):
    
    if GTE is True or GTT is True:
    # Wenn GRUPPENspezifische Behandlungseffekte oder Zeittrends gewuenscht werden,
    # braucht man dafuer keine festen Effekte, aber andere Dummy-Variablen (fuer jede Gruppe)
    
        if group_by is None:
            print ("Grouping variable is not defined. Define a grouping variable using group_by.")
        # Wenn keine Gruppierungsvariable fuer Effekte angegeben wird,
        # einfach nichts machen, dann wird, wie im Standardmodell,
        # nur zwischen Treatment- und Kontrollgruppe unterschieden
        else:
            group_dummies = pd.DataFrame(pd.get_dummies(data[group_by].astype(str), dtype = int, prefix = "group"))
            # Dummy-Variablen Gruppe
            group_names = group_dummies.columns
            # Abspeichern Namen der Gruppen fuer spaeter
            group_names = list(map(lambda name: name[6:], group_names))
            # Entfernen der ersten 6 Zeichen (also "group_")
            group_dummies.columns = group_dummies.columns.str.replace(r'[^A-Za-z0-9_]', '', regex=True)
            # Alle Leerzeichen und Sonderzeichen raus
            data = pd.concat([data, group_dummies], axis = 1)
            # Spalten mit Gruppen-Dummies werden angehaengt
            GTE_columns_group = '+'.join(group_dummies.columns)
            # Dummies Einheiten zusammenfuegen fuer Formel
        
    # Vorbereitung Dummy-Variablen fuer Untersuchungseinheiten (wenn individuelle Zeittrends oder Effekte gewuenscht):
    
    if ITT is True or ITE is True:
    # Sowohl fuer individuelle Zeittrends als auch fuer  individuelle Treatment-Effekte muessen Dummies gebildet
    # und den Daten angehaengt werden, ausserdem muessen sie in die Formel rein

        unit_dummies = pd.DataFrame(pd.get_dummies(data[unit_col].astype(str), dtype = int, prefix = "unit"))
        # Dummy-Variablen Untersuchungseinheiten
        unit_names = unit_dummies.columns
        # Abspeichern Namen der Untersuchungseinheiten fuer spaeter
        unit_names = list(map(lambda name: name[5:], unit_names))
        # Entfernen der ersten 5 Zeichen (also "unit_")
        unit_dummies.columns = unit_dummies.columns.str.replace(r'[^A-Za-z0-9_]', '', regex=True)
        # Alle Leerzeichen und Sonderzeichen raus
        data = pd.concat([data, unit_dummies], axis = 1)
        # Spalte mit Unit-ID wird angehaengt
        ITT_columns_unit = '+'.join(unit_dummies.columns)
        # Dummies Einheiten zusammenfuegen fuer Formel

    
    # Bildung Interaktionsvariablen fuer gruppenspezifische Zeittrends (wenn gewuenscht):

    if GTT is True:
    # Wenn gruppenspezifische Zeittrends inkludiert werden sollen...        
        
        if group_by is None:
            print ("Group time trends are desired, but no grouping variable (group_by) was stated. No group time trends are estimated.")
            # Warnhinweis, aber kein Fehler!
        else:
            
            data = didtools.date_counter(
            data,
            time_col,
            new_col="date_counter"
            )
            # Berechnung von Zeitzaehlern mit eigener Funktion date_counter()
            
            group_x_time = pd.DataFrame()
            # Neuer df fuer Gruppe x Zaehler
            for col in group_dummies.columns:
            # Jede Spalte wird durchiteriert
                group_x_time[col] = group_dummies[col] * data["date_counter"]
                # Einheits-Dummies werden mit Zeitzaehler multipliziert
                new_col_name = f"{col}_x_time"
                group_x_time = group_x_time.rename(columns={col: new_col_name})
                # Neue Spaltennamen Gruppe x Zaehler

            data = pd.concat([data, group_x_time], axis = 1)
            # Spalte mit Unit-ID x Zeit wird angehaengt

            GTT_columns_groupxtime = '+'.join(group_x_time.columns)
            # Spalten Einheit x Zeit zusammenfuegen fuer Formel
            did_formula = did_formula + f'+{GTE_columns_group}+{GTT_columns_groupxtime}'
            # Neue DiD-Formel mit Einheits-Dummies und Einheit x Zeit
            did_formula = did_formula.replace(group_by, '').strip()
            # Damit Spaltenname der Units nicht mehr vorkommt
             
    
    # Bildung Interaktionsvariablen fuer individuelle Zeittrends (wenn gewuenscht):

    if ITT is True:
    # Wenn ein individueller Zeittrend (ITT = Individual time trend)
    # ins Modell aufgenommen werden soll...

        data = didtools.date_counter(
            data,
            time_col,
            new_col="date_counter"
            )
        # Berechnung von Zeitzaehlern mit eigener Funktion date_counter()

        unit_x_time = pd.DataFrame()
        # Neuer df fuer Einheit x Zaehler
        for col in unit_dummies.columns:
        # Jede Spalte wird durchiteriert
            unit_x_time[col] = unit_dummies[col] * data["date_counter"]
            # Einheits-Dummies werden mit Zeitzaehler multipliziert
            new_col_name = f"{col}_x_time"
            unit_x_time = unit_x_time.rename(columns={col: new_col_name})
            # Neue Spaltennamen Einheit x Zaehler

        data = pd.concat([data, unit_x_time], axis = 1)
        # Spalte mit Unit-ID x Zeit wird angehaengt

        ITT_columns_unitxtime = '+'.join(unit_x_time.columns)
        # Spalten Einheit x Zeit zusammenfuegen fuer Formel
        did_formula = did_formula + f'+{ITT_columns_unit}+{ITT_columns_unitxtime}'
        # Neue DiD-Formel mit Einheits-Dummies und Einheit x Zeit
        did_formula = did_formula.replace(unit_col, '').strip()
        # Damit Spaltenname der Units nicht mehr vorkommt


    # Bildung Interaktionsvariablen fuer gruppenspezifische Treatment-Effekte (wenn gewuenscht):
    
    if GTE is True:
    # Wenn gruppenspezifische Behandlungseffekte ausgegeben werden sollen...
        if group_by is None:
            pass
        # Wenn keine Gruppierungsvariable fuer Effekte angegeben wird,
        # einfach nichts machen, dann wird, wie im Standardmodell,
        # nur zwischen Treatment- und Kontrollgruppe unterschieden
        else:
            group_x_treatment = pd.DataFrame()
            # Neuer df fuer Gruppe x Treatment
            for col in group_dummies.columns:
            # Jede Spalte wird durchiteriert
                group_x_treatment[col] = group_dummies[col] * data[treatment_col]
                # Gruppen-Dummies werden mit Treatment-Dummy multipliziert
                new_col_name = f"{col}_x_treatment"
                group_x_treatment = group_x_treatment.rename(columns={col: new_col_name})
                # Neue Spaltennamen Gruppe x Treatment

            data = pd.concat([data, group_x_treatment], axis = 1)
            # Spalte mit Gruppe x Treatment wird angehaengt

            GTE_columns_groupxtreatment = '+'.join(group_x_treatment.columns)
            # Spalten Gruppe x Treatment zusammenfuegen fuer Formel
            did_formula = did_formula + f'+{GTE_columns_group}+{GTE_columns_groupxtreatment}'
            # Neue DiD-Formel mit Gruppen-Dummies und Gruppen x Treatment
            did_formula = did_formula.replace(group_by, '').strip()
            # Damit Spaltenname der Gruppen nicht mehr vorkommt

            did_formula = did_formula.replace(f'{treatment_col}+', "")


    # Bildung Interaktionsvariablen fuer individuelle Treatment-Effekte (wenn gewuenscht):

    if ITE is True:
    # Wenn individuelle Behandlungseffekte ausgegeben werden sollen...
        unit_x_treatment = pd.DataFrame()
        # Neuer df fuer Einheit x Treatment
        for col in unit_dummies.columns:
        # Jede Spalte wird durchiteriert
            unit_x_treatment[col] = unit_dummies[col] * data[treatment_col]
            # Einheits-Dummies werden mit Treatment-Dummy multipliziert
            new_col_name = f"{col}_x_treatment"
            unit_x_treatment = unit_x_treatment.rename(columns={col: new_col_name})
            # Neue Spaltennamen Einheit x Treatment

        data = pd.concat([data, unit_x_treatment], axis = 1)
        # Spalte mit Unit-ID x Treatment wird angehaengt

        ITE_columns_unitxtreatment = '+'.join(unit_x_treatment.columns)
        # Spalten Einheit x Treatment zusammenfuegen fuer Formel
        did_formula = did_formula + f'+{ITT_columns_unit}+{ITE_columns_unitxtreatment}'
        # Neue DiD-Formel mit Einheits-Dummies und Einheit x Treatment
        did_formula = did_formula.replace(unit_col, '').strip()
        # Damit Spaltenname der Units nicht mehr vorkommt

        did_formula = did_formula.replace(f'{treatment_col}+', "")


    # Korrektur bei (two-way-)FE-Modell:
    
    if FE_time is True or FE_unit is True:
    # Feste Effekte fuer Untersuchungseinheiten und/oder Zeit?
    # Dann kein Intercept (sonst perfekte Kollinearitaet)
        did_formula = did_formula + f' -1'
        # Ergaenzung mit -1 = Modell ohne Intercept
        

    # Hinzufuegen Kovariaten (wenn gewuenscht):

    if covariates is not None:
    # Etwaige Kontrollvariablen
        covariates_columns = '+'.join(covariates)
        # Spalten Einheit x Treatment zusammenfuegen fuer Formel
        did_formula = did_formula + f'+{covariates_columns}'
        # Neue DiD-Formel mit Kontrollvariablen
        covariates = True
    else:
        covariates = False

    
    # Schritt 6) Zusammenstellung Modellkonfiguration:
    
    model_config = {
        "TG_col": TG_col,
        "TT_col": TT_col,
        "treatment_col": treatment_col,
        "unit_col": unit_col,
        "time_col": time_col,
        "outcome_col": outcome_col,
        "log_outcome": log_outcome,
        "after_treatment_period": after_treatment_period,
        "after_treatment_col": after_treatment_col,
        "pre_post": pre_post,
        "FE_unit": FE_unit,
        "FE_time": FE_time,
        "ITT": ITT,
        "GTT": GTT,
        "ITE": ITE,
        "GTE": GTE,
        "group_by": group_by,
        "covariates": covariates,
        "confint_alpha": confint_alpha,
        "drop_missing": drop_missing,
        "did_formula": did_formula
        }
    # Zusammenstellung Modellkonfiguration als dict


    # Schritt 7) Lineares Regressionsmodell:

    ols_model = ols(did_formula, data = data).fit()
    # Parametrisieren des Regressionsmodells mit oben gebildeter Formel
    # und den (ggf. nachbearbeiteten) User-Daten


    # Koeffizienten, Standardfehler, t-Werte, p-Werte und Konfidenzintervalle aus OLS-Modell extrahieren:

    ols_coefficients = ols_model.params
    # Koeffizienten des Regressionsmodells
    coef_conf_standarderrors = ols_model.bse
    # Zugehoerige Standardfehler    
    coef_conf_t = ols_model.tvalues
    # Zugehoerige t-Werte
    coef_conf_p = ols_model.pvalues
    # zugehoerige p-Werte
    coef_conf_intervals = ols_model.conf_int(alpha = confint_alpha)
    # Konfidenzintervalle der Koeffizieten (mit user-definierter Irrtumswahrscheinlichkeit)


    # Schritt 8) Zusammenstellung Koeffizienten (mit Inferenzstatistik) in dict "model_results":

    if ITE is False and GTE is False:
    # Nur wenn es KEINE individuens- oder gruppenpezifischen Effekte gibt,
    # gibt es einen ATE

        # ATE = Average Treatment Effect = Koeffizient des Interkationsterms
        # (Treatment-Periode x Treatment-Gruppe) bzw. des Treatment-Dummies
        # (Einziger Koeffizient, der in JEDER Modellvariante enthalten ist):
        ATE = ols_coefficients[treatment_col]
        # Regressionskoeffizient
        ATE_SE = round(coef_conf_standarderrors[treatment_col], 3)
        # t-Wert
        ATE_t = round(coef_conf_t[treatment_col], 3)
        # t-Wert
        ATE_p = round(coef_conf_p[treatment_col], 3)
        # p-Wert
        ATE_CI_lower = coef_conf_intervals.loc[treatment_col, 0]
        ATE_CI_upper = coef_conf_intervals.loc[treatment_col, 1]
        # Konfidenzintervalle
        ATE = {
            "ATE": ATE, 
            "ATE_SE": ATE_SE, 
            "ATE_t": ATE_t, 
            "ATE_p": ATE_p, 
            "ATE_CI_lower": ATE_CI_lower,
            "ATE_CI_upper": ATE_CI_upper
            }
        # Zusammenstellung als dictionary

        model_results = {"ATE": ATE}
        # ATE ist immer mit dabei (ausser bei individuellen Treatment-Effekten)
    
    else:
        model_results = {"ATE": None}
        # kein ATE drin


    if GTE is True:
    # Wenn es gruppenspezifischen Effekte gibt...

        if group_by is None:
        # Wenn Gruppierungsvariable vergessen wurde, gibt es nur eine Gruppe,
        # naemlich die Treatment-Gruppe ==> hier ATE berechnen

            print ("Group treatment effects are desired, but no grouping variable (group_by) was stated. Calculating effects for treatment group only.")
            # Warnhinweis, aber kein Fehler!

            # ATE = Average Treatment Effect = Koeffizient des Interkationsterms
            # (Treatment-Periode x Treatment-Gruppe) bzw. des Treatment-Dummies
            # (Einziger Koeffizient, der in JEDER Modellvariante enthalten ist):
            ATE = ols_coefficients[treatment_col]
            # Regressionskoeffizient
            ATE_SE = round(coef_conf_standarderrors[treatment_col], 3)
            # t-Wert
            ATE_t = round(coef_conf_t[treatment_col], 3)
            # t-Wert
            ATE_p = round(coef_conf_p[treatment_col], 3)
            # p-Wert
            ATE_CI_lower = coef_conf_intervals.loc[treatment_col, 0]
            ATE_CI_upper = coef_conf_intervals.loc[treatment_col, 1]
            # Konfidenzintervalle
            ATE = {
                "ATE": ATE, 
                "ATE_SE": ATE_SE, 
                "ATE_t": ATE_t, 
                "ATE_p": ATE_p, 
                "ATE_CI_lower": ATE_CI_lower,
                "ATE_CI_upper": ATE_CI_upper
                }
            # Zusammenstellung als dictionary

            model_results = {"ATE": ATE}
            # ATE ist immer mit dabei (ausser bei individuellen oder gruppenspezifischen Treatment-Effekten)

        else:
            model_results = {"ATE": None}
            # kein ATE drin


    if FE_time is False and FE_unit is False and GTE is False:
    # Modellkoeffizienten fuer Modell ohne feste Effekte (=Standardmodell)

        # TG = Abweichung Durchschnitt Treatment-Gruppe von Kontrollgruppe (Intercept):
        TG = ols_coefficients[TG_col]
        # Regressionskoeffizient
        TG_SE = round(coef_conf_standarderrors[TG_col], 3)
        # t-Wert
        TG_t = round(coef_conf_t[TG_col], 3)
        # t-Wert
        TG_p = round(coef_conf_p[TG_col], 3)
        # p-Wert
        TG_CI_lower = coef_conf_intervals.loc[TG_col, 0]
        TG_CI_upper = coef_conf_intervals.loc[TG_col, 1]
        # Konfidenzintervalle
        TG = {
            "TG": TG, 
            "TG_SE": TG_SE, 
            "TG_t": TG_t, 
            "TG_p": TG_p,
            "TG_CI_lower": TG_CI_lower,
            "TG_CI_upper": TG_CI_upper
            }
        # Zusammenstellung als dictionary

        # TT = Zeiteffekt OHNE Intervention:
        TT = ols_coefficients[TT_col]
        # Regressionskoeffizient
        TT_SE = round(coef_conf_standarderrors[TT_col], 3)
        # t-Wert
        TT_t = round(coef_conf_t[TT_col], 3)
        # t-Wert
        TT_p = round(coef_conf_p[TT_col], 3)
        # p-Wert
        TT_CI_lower = coef_conf_intervals.loc[TT_col, 0]
        TT_CI_upper = coef_conf_intervals.loc[TT_col, 1]
        # Konfidenzintervalle
        TT = {
            "TT": TT, 
            "TT_SE": TT_SE, 
            "TT_t": TT_t, 
            "TT_p": TT_p,
            "TT_CI_lower": TT_CI_lower,
            "TT_CI_upper": TT_CI_upper
            }
        # Zusammenstellung als dictionary

        # Intercept = Baseline Kontrollgruppe vor Intervention
        Intercept = ols_coefficients["Intercept"]
        # Regressionskoeffizient
        Intercept_SE = round(coef_conf_standarderrors["Intercept"], 3)
        # t-Wert
        Intercept_t = round(coef_conf_t["Intercept"], 3)
        # t-Wert
        Intercept_p = round(coef_conf_p["Intercept"], 3)
        # p-Wert
        Intercept_CI_lower = coef_conf_intervals.loc["Intercept", 0]
        Intercept_CI_upper = coef_conf_intervals.loc["Intercept", 1]
        # Konfidenzintervalle
        Intercept = {
            "Intercept": Intercept, 
            "Intercept_SE": Intercept_SE, 
            "Intercept_t": Intercept_t, 
            "Intercept_p": Intercept_p,
            "Intercept_CI_lower": Intercept_CI_lower,
            "Intercept_CI_upper": Intercept_CI_upper
            }
        # Zusammenstellung als dictionary

        model_results["TG"] = TG
        model_results["TT"] = TT
        model_results["Intercept"] = Intercept
        # zum Dict hinzufuegen

    else:
    # Modellkoeffizienten fuer Modell mit FE fuer Einheiten ODER Zeit

        if TG_col is not None and ITE is False and GTE is False:

            # TG = Abweichung Durchschnitt Treatment-Gruppe von Kontrollgruppe (Intercept):
            TG = ols_coefficients[TG_col]
            # Regressionskoeffizient
            TG_SE = round(coef_conf_standarderrors[TG_col], 3)
            # t-Wert
            TG_t = round(coef_conf_t[TG_col], 3)
            # t-Wert
            TG_p = round(coef_conf_p[TG_col], 3)
            # p-Wert
            TG_CI_lower = coef_conf_intervals.loc[TG_col, 0]
            TG_CI_upper = coef_conf_intervals.loc[TG_col, 1]
            # Konfidenzintervalle
            TG = {
                "TG": TG, 
                "TG_SE": TG_SE, 
                "TG_t": TG_t, 
                "TG_p": TG_p,
                "TG_CI_lower": TG_CI_lower,
                "TG_CI_upper": TG_CI_upper
                }
            # Zusammenstellung als dictionary

            model_results["TG"] = TG
            # zum Dict hinzu

        if TT_col is not None:

            # TT = Zeiteffekt OHNE Intervention:
            TT = ols_coefficients[TT_col]
            # Regressionskoeffizient
            TT_SE = round(coef_conf_standarderrors[TT_col], 3)
            # t-Wert
            TT_t = round(coef_conf_t[TT_col], 3)
            # t-Wert
            TT_p = round(coef_conf_p[TT_col], 3)
            # p-Wert
            TT_CI_lower = coef_conf_intervals.loc[TT_col, 0]
            TT_CI_upper = coef_conf_intervals.loc[TT_col, 1]
            # Konfidenzintervalle
            TT = {
                "TT": TT, 
                "TT_SE": TT_SE, 
                "TT_t": TT_t, 
                "TT_p": TT_p,
                "TT_CI_lower": TT_CI_lower,
                "TT_CI_upper": TT_CI_upper
                }
            # Zusammenstellung als dictionary

            model_results["TT"] = TT
            # zum Dict hinzu

    if after_treatment_period is True:
    # Average After Treatment Effect = Koeffizient des Interkationsterms
    # (After-Treatment-Periode x Treatment-Gruppe):
        AATE = ols_coefficients[after_treatment_col]
        # Regressionskoeffizient
        AATE_SE = round(coef_conf_standarderrors[after_treatment_col], 3)
        # t-Wert
        AATE_t = round(coef_conf_t[after_treatment_col], 3)
        # t-Wert
        AATE_p = round(coef_conf_p[after_treatment_col], 3)
        # p-Wert
        AATE_CI_lower = coef_conf_intervals.loc[after_treatment_col, 0]
        AATE_CI_upper = coef_conf_intervals.loc[after_treatment_col, 1]
        # Konfidenzintervalle
        AATE = {
            "AATE": AATE, 
            "AATE_SE": AATE_SE, 
            "AATE_t": AATE_t, 
            "AATE_p": AATE_p,
            "AATE_CI_lower": AATE_CI_lower,
            "AATE_CI_upper": AATE_CI_upper
            }
        # Zusammenstellung als dictionary

        model_results["AATE"] = AATE
        # zum Dict hinzufuegen


    # Schritt 9) Zusammenstellung weitere Modellergebnisse

    model_predictions = ols_model.predict()
    # Vorhergesagte Werte von ols_model


    # Abspeichern Modellstatistiken in dict:

    model_statistics = {
        "rsquared": ols_model.rsquared,
        "rsquared_adj": ols_model.rsquared_adj,
        }


    # Abspeichern feste Effekte (falls im Modell enthalten):

    fixed_effects = [None, None]
    # leere Liste (bleibt so, wenn keine festen Effekte im Modell)

    if FE_unit is True:

        FE_unit_coef = {var: coef for var, coef in ols_coefficients.items() if var.startswith(unit_col)}

        FE_unit_coef_df = pd.DataFrame(list(FE_unit_coef.items()), columns = [unit_col, "coef"])
        FE_unit_coef_df.set_index(unit_col, inplace = True)

        fixed_effects[0] = FE_unit_coef_df

    if FE_time is True:

        FE_time_coef = {var: coef for var, coef in ols_coefficients.items() if var.startswith(time_col)}

        FE_time_coef_df = pd.DataFrame(list(FE_time_coef.items()), columns = [time_col, "coef"])
        FE_time_coef_df.set_index(time_col, inplace = True)

        fixed_effects[1] = FE_time_coef_df


    # Abspeichern individuelle Zeittrends bzw. individuelle Treatment-Effekte:

    individual_effects = [None, None]
    # leere Liste (bleibt so, wenn nichts von Beidem im Modell)

    if ITT is True:
    # Auslesen und Abspeichern Koeffizienten Individuelle Zeittrends
        
        ITT_coef = {var: coef for var, coef in ols_coefficients.items() if var.endswith("_x_time")}
        # Koeffizienten aller Variablen, die auf '_x_time' enden
        ITT_coef_df = pd.DataFrame(ITT_coef.items(), columns = ["unit_x_time", "coef"])
        ITT_coef_df.set_index("unit_x_time", inplace = True)
        # wird in ITT_coef_df geschrieben
        
        ITT_coef_confint = coef_conf_intervals[coef_conf_intervals.index.str.endswith('_x_time')]
        # KI fuer alle Variablen, die auf '_x_time' enden
        ITT_coef_df["lower"] = ITT_coef_confint[0]
        ITT_coef_df["upper"] = ITT_coef_confint[1]
        # wird in ITT_coef_df geschrieben    
        
        ITT_coef_df[unit_col] = unit_names
        
        individual_effects[0] = ITT_coef_df
        # 1. Eintrag der Liste individual_effects

    if ITE is True:
    # Auslesen und Abspeichern Koeffizienten Individuelle Treatment-Effekte
        
        ITE_coef = {var: coef for var, coef in ols_coefficients.items() if var.endswith("_x_treatment")}
        # Koeffizienten aller Variablen, die auf '_x_treatment' enden (hier: Interaktionen Untersuchungseinheit x Treatment)
        ITE_coef_df = pd.DataFrame(ITE_coef.items(), columns = ["unit_x_treatment", "coef"])
        ITE_coef_df.set_index("unit_x_treatment", inplace = True)
        # wird in ITE_coef_df geschrieben
        
        ITE_coef_df["SE"] = {var: SE for var, SE in coef_conf_standarderrors.items() if var.endswith("_x_treatment")}
        # Mit dazu: Zu diesen Koeffizienten zugehoerige Standardfehler
        ITE_coef_df["t"] = {var: tval for var, tval in coef_conf_t.items() if var.endswith("_x_treatment")}
        # Mit dazu: Zu diesen Koeffizienten zugehoerige t-Werte
        ITE_coef_df["p"] = {var: pval for var, pval in coef_conf_p.items() if var.endswith("_x_treatment")}
        # Mit dazu: Zu diesen Koeffizienten zugehoerige p-Werte
            
        ITE_coef_confint = coef_conf_intervals[coef_conf_intervals.index.str.endswith('_x_treatment')]
        # KI fuer alle Variablen, die auf '_x_treatment' enden
        ITE_coef_df["lower"] = ITE_coef_confint[0]
        ITE_coef_df["upper"] = ITE_coef_confint[1]
        # wird in ITE_coef_confint geschrieben    
        
        ITE_coef_df[unit_col] = unit_names

        individual_effects[1] = ITE_coef_df
        # 2. Eintrag der Liste individual_effects


    # Abspeichern gruppensezifische Zeittrends bzw. Treatment-Effekte:

    group_effects = [None, None]
    # leere Liste (bleibt so, wenn nichts von Beidem im Modell)

    if GTT is True:
    # Auslesen und Abspeichern Koeffizienten Gruppenspezifische Zeittrends
        GTT_coef = {var: coef for var, coef in ols_coefficients.items() if var.endswith("_x_time")}
        # Koeffizienten aller Variablen, die auf '_x_time' enden
        GTT_coef_df = pd.DataFrame(GTT_coef.items(), columns = ["group_x_time", "coef"])
        GTT_coef_df.set_index("group_x_time", inplace = True)
        # wird in GTT_coef_df geschrieben
        
        GTT_coef_confint = coef_conf_intervals[coef_conf_intervals.index.str.endswith('_x_time')]
        # KI fuer alle Variablen, die auf '_x_time' enden
        GTT_coef_df["lower"] = GTT_coef_confint[0]
        GTT_coef_df["upper"] = GTT_coef_confint[1]
        # wird in ITT_coef_df geschrieben    
        
        GTT_coef_df[unit_col] = unit_names
        
        group_effects[0] = GTT_coef_df
        # 1. Eintrag der Liste group_effects = gruppenspezifische Zeittrends (wenn vorhanden)

    if GTE is True:
    # Auslesen und Abspeichern Koeffizienten gruppenspezifische Treatment-Effekte
        if group_by is None:
            pass
        else:
            GTE_coef = {var: coef for var, coef in ols_coefficients.items() if var.endswith("_x_treatment")}
            # Koeffizienten aller Variablen, die auf '_x_treatment' enden (hier: Interaktionen Gruppe x Treatment)
            GTE_coef_df = pd.DataFrame(GTE_coef.items(), columns = ["group_x_treatment", "coef"])
            GTE_coef_df.set_index("group_x_treatment", inplace = True)
            # wird in GTE_coef_df geschrieben
            GTE_coef_df["SE"] = {var: SE for var, SE in coef_conf_standarderrors.items() if var.endswith("_x_treatment")}
            # Mit dazu: Zu diesen Koeffizienten zugehoerige Standardfehler
            GTE_coef_df["t"] = {var: tval for var, tval in coef_conf_t.items() if var.endswith("_x_treatment")}
            # Mit dazu: Zu diesen Koeffizienten zugehoerige t-Werte
            GTE_coef_df["p"] = {var: pval for var, pval in coef_conf_p.items() if var.endswith("_x_treatment")}
            # Mit dazu: Zu diesen Koeffizienten zugehoerige p-Werte
            
            GTE_coef_confint = coef_conf_intervals[coef_conf_intervals.index.str.endswith('_x_treatment')]
            # KI fuer alle Variablen, die auf '_x_treatment' enden
            GTE_coef_df["lower"] = GTE_coef_confint[0]
            GTE_coef_df["upper"] = GTE_coef_confint[1]
            # wird in ITE_coef_confint geschrieben    
            
            GTE_coef_df[group_by] = group_names

            group_effects[1] = GTE_coef_df
            # 2 Eintrag der Liste group_effects = gruppenspezifische treatment-Effekte (wenn vorhanden)


    # Schritt 10) Output Ergebnisse:

    # Zusammenstellung Output als Liste und Deklaration als did_model-Objekt:
    did_model_output = did_model(
        model_results,
        model_config,
        data,
        model_predictions,
        fixed_effects,
        individual_effects,
        group_effects,
        model_statistics,
        ols_model
        ) 
    # did_model-Objekt mit 9 Eintraegen:
    # [0] model_results = Modellergebnisse (oben zusammengestellt als dict)
    # [1] model_config = Modellkonfiguration (oben zusammengestellt als dict)
    # [2] data = Datensatz des Nutzers, ggf. erweitert mit log Y (pandas df)
    # [3] model_predictions = Vorhergesagte Werte des Modells (pandas df)
    # [4] fixed_effects = Feste Effekte des Modells (Liste; leer, wenn keine FE)
    # [5] individual_effects = Individuelle Zeittrends bzw. Treatment-Effekte (Liste; leer, wenn keine da)
    # [6] group_effects = Gruppenspezifische Zeittrends bzw. Treatment-Effekte (Liste; leer, wenn keine da)
    # [7] model_statistics = Modellstatistiken u.a. R-Quadrat
    # [8] ols_model = OLS-Modell Objekt

    return did_model_output