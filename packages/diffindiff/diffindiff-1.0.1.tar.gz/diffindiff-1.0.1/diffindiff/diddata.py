#-------------------------------------------------------------------------------
# Name:        diddata (diffindiff)
# Purpose:     Creating data for Difference-in-Differences Analysis
# Author:      Thomas Wieland (geowieland@googlemail.com)
# Version:     1.0.1
# Last update: 29.01.2025 18:35
# Copyright (c) 2025 Thomas Wieland
#-------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from diffindiff import didanalysis


class did_groups:
    def __init__(
        self, 
        groups_data_df, 
        groups_config_dict
        ):
    # Das "did_groups"-Objekt ist eigentlich eine Liste mit zwei Eintraegen:
    # 1.) Pandas data frame mit unit_UID und Zuordnung zur T/K-Gruppe (groups_data_df)
    # 2.) Dictionary mit den wichtigsten Informationen (groups_config_dict)
        self.data = [groups_data_df, groups_config_dict]

    def get_df (self):
        return self.data[0]
        # Auslesen 1. Eintrag (df)

    def get_dict (self):
        return self.data[1]
        # Auslesen 2. Eintrag (dict)

    def summary(self):
    # Funktion fuer Summary von Objekten der Klasse "did_groups"
    # Noetig hierfur ist nur das 2. Objekt (dictionary), also self.dict,
    # weil hier die Gruppengroessen drinstehen

        groups_config = self.data[1]

        print ("DiD Analysis Treatment and Control Group")
        print ("Units:                   " + str(groups_config['full_sample']) + " (" + str(round(groups_config['full_sample']/groups_config['full_sample']*100,2)) + " %)")
        print ("Treatment Group:         " + str(groups_config['treatment_group']) + " (" + str(round(groups_config['treatment_group']/groups_config['full_sample']*100,2)) + " %)")
        print ("Control Group:           " + str(groups_config["control_group"]) + " (" + str(round(groups_config['control_group']/groups_config['full_sample']*100,2)) + " %)")
        # self_dict ist ein dictionary, aus dem die einzelnen Eintraege
        # ausgelesen werden. Dafuer werden noch %-Werte berechnet    


def create_groups(
    treatment_group,
    control_group
    ):

    treatment_group_unique = treatment_group.unique()
    # Untersuchungseinheiten (einzelne Werte) Behandungsgruppe
    control_group_unique = control_group.unique()
    # Untersuchungseinheiten (einzelne Werte) Kontrollgruppe
    # falls jemand es verpeilt bei der Erstellung der Gruppen

    treatment_group_N = treatment_group.nunique()
    # Anzahl Untersuchungseinheiten in der Behandlungsgruppe
    control_group_N = control_group.nunique()
    # Anzahl Untersuchungseinheiten in der Kontrollgruppe

    TG_dummies = [1] * treatment_group_N
    CG_dummies = [0] * control_group_N
    # Dummies werden fuer die Laenge der Gruppen unit x time wiederholt
    # 1 = Treatmentgruppe, 2= Kontrollgruppe

    TG_data = {
        "unit_UID": treatment_group_unique, 
        "TG": TG_dummies
        }
    CG_data = {
        "unit_UID": control_group_unique, 
        "TG": CG_dummies
        }
    # Definition als Dictionary

    groups_data = pd.concat ([pd.DataFrame(TG_data), pd.DataFrame(CG_data)], axis = 0)
    # Konvertierung in df mit pd.DataFrame und merge (kartesisches Produkt)

    # Zusammenstellung Konfigurationsdaten (wird ans Ergebnis angehaengt):
    groups_config = {
        "treatment_group": treatment_group_N, 
        "control_group": control_group_N, 
        "full_sample": treatment_group_N+control_group_N
        }
    # Definition als Dictionary

    groups = did_groups(groups_data, groups_config)
    # Zusammenfuegen als Liste "groups"
    # Eintrag 1: Liste Untersuchungseinheiten mit Zuordnung 1/0
    # Eintrag 2: Konfigurationsdaten (Gruppengroessen)

    return groups


class did_treatment:
    def __init__(self, treatment_data_df, treatment_config_dict):
    # Das "did_treatment"-Objekt ist eigentlich eine Liste mit zwei Eintraegen:
    # 1. = [0] Pandas data frame mit Intervention und Dummys (treatment_data_df)
    # 2. = [1] Dictionary mit den wichtigsten Informationen, z.B. Zeitraum (treatment_config_dict)
        self.data = [treatment_data_df, treatment_config_dict]

    def get_df (self):
        return self.data[0]

    def get_dict (self):
        return self.data[1]
        # Auslesen 2. Eintrag (dict)

    def add_treatment(self):
        pass
        #hier funktion fuer 2., 3., x.tes Treatment rein

    def summary(self):
    # Funktion fuer Summary von Objekten der Klasse "did_treatment"
    # Noetig hierfur ist nur das 2. Objekt (dictionary), also self.dict,
    # weil hier die Gruppengroessen drinstehen

        treatment_config = self.data[1]

        print ("DiD Analysis Treatment Configuration")

        # Darstellung abhaengig davon ob es pre_post ist oder nicht
        # und ob es eine Nach-Interventionsperiode gibt:
        if treatment_config["pre_post"] is True:
            print ("Study period (pre-post): " + str(treatment_config["treatment_period_start"]) + " vs. " + str(treatment_config["treatment_period_end"]))
        else:
            print ("Study period:            " + str(treatment_config["study_period_start"]) + " - " + str(treatment_config["study_period_end"]) + (" (") + str(treatment_config["study_period"]) + " " + treatment_config["frequency"] + ")")
            print ("Treatment Period:        " + str(treatment_config["treatment_period_start"]) + " - " + str(treatment_config["treatment_period_end"])+ (" (") + str(treatment_config["treatment_period"]) + " " + treatment_config["frequency"] + ")")
        # self_dict ist ein dictionary, aus dem die einzelnen Eintraege
        # ausgelesen werden. Dafuer werden noch %-Werte berechnet

        if treatment_config["after_treatment_period"] is True:
            print ("After treatment period:  " + str(treatment_config["treatment_period_end"]) + " - " + str(treatment_config["study_period_end"]) + " (" + str(treatment_config["after_treatment_period_N"]) + " " + treatment_config["frequency"] + ")")


def create_treatment (
    study_period,
    treatment_period,
    freq = "D",
    pre_post: bool = False,
    after_treatment_period: bool = False
    ):

    if pre_post:

        after_treatment_period = False
        # nur 2 Zeitpunkte, keine Nach-Treatment-Periode

        # Zusammenstellung Daten gesamter Untersuchungszeitraum:
        study_period_range = [study_period[0], study_period[1]]
        # Datumsreihe gesamter Untersuchungszeitraum

        study_period_N = 2
        # Anzahl Zeitpunkte des gesamten Untersuchungszeitraums
        # bei pre vs. post = 2

        study_period_counter = [1, 2]
        # Zaehler Zeitpunkte (z.B. Tage)

        # Zusammenstellung Daten Interventionszeitraum:
        treatment_period_range = [treatment_period[0], treatment_period[1]]
        # Datumsreihe Interventionszeitraum

        treatment_period_N = 1
        # Anzahl Zeitpunkte des Interventionszeitraums (siehe unten)
        # bei Pre-Post gibt es nur zwei Zeitpunkte (vorher vs. nachher) und
        # dementsprechend genau einen Interventionszeitraum (nachher)

        TT_dummies = [0,1]
        # nur 2 Eintraege: pre (0) und post (1)

        study_period_range = pd.DataFrame (treatment_period_range, columns=["t"])
        # bei pre_post ist study_period_range = treatment_period_range
        # (davor und danach, jeweils 1 Zeitpunkt)
        # direkt Umwandlung in Pandas data frame
        study_period_range["t_counter"] = pd.DataFrame(study_period_counter)
        # Zeitpunkte noch dazu

        TT_data = {
            "t": treatment_period_range, 
            "TT": TT_dummies
            }
        
        # Erst Definition als Dictionary
        TT_data = pd.DataFrame(TT_data)
        # Umwandlung in Pandas data frame
        
        treatment_period_range = pd.DataFrame(study_period_range)

        treatment_data = treatment_period_range.merge(TT_data, how = "left")
        # left join, so dass nur noch 1x Datum und der TT-Dummy uebrig bleiben

    else:

        # Zusammenstellung Daten gesamter Untersuchungszeitraum:
        study_period_range = pd.date_range(
            start = study_period[0], 
            end = study_period[1], 
            freq = freq
            )
        # Datumsreihe gesamter Untersuchungszeitraum

        study_period_N = len(study_period_range)
        # Anzahl Zeitpunkte des gesamten Untersuchungszeitraums

        study_period_counter = np.arange (1, study_period_N+1, 1)
        # Zaehler Zeitpunkte (z.B. Tage)

        # Zusammenstellung Daten Interventionszeitraum:
        treatment_period_range = pd.date_range(
            start = treatment_period[0], 
            end = treatment_period[1]
            )
        # Datumsreihe Interventionszeitraum

        treatment_period_N = len(treatment_period_range)
        # Anzahl Zeitpunkte des gesamten Untersuchungszeitraums

        TT_dummies = [1] * treatment_period_N
        # Dummy-Variablen Interventionszeitraum

        study_period_range = {"t": study_period_range}
        # erst Umwandlung in Dictionary, ...
        study_period_range = pd.DataFrame (study_period_range)
        # ... dann Umwandlung in Pandas data frame
        study_period_range["t_counter"] = pd.DataFrame(study_period_counter)

        TT_data = {
            "t": treatment_period_range, 
            "TT": TT_dummies
            }
        # Erst Definition als Dictionary
        TT_data = pd.DataFrame(TT_data)
        # Umwandlung in Pandas data frame
    
        treatment_data = study_period_range.merge(TT_data, how = "left")
        # left join, so dass nur noch 1x Datum und der TT-Dummy uebrig bleiben


    treatment_data["TT"] = treatment_data["TT"].fillna(0)
    # Alle Zellen in Spalte TT, die NaN sind, werden durch 0 ersetzt
    # (alle die in der study period vorkommen, aber nicht in der treatment period)


    if after_treatment_period is True:
    # Wenn auch Nach-Interventionsperiode gewuenscht ist
        
        # Tag 1 nach Ende der Intervention:
        treatment_period_last = datetime.strptime(treatment_period[1], "%Y-%m-%d")
        # String in ein datetime-Objekt umwandeln
        after_treatment_period_day1 = treatment_period_last + timedelta(days=1)
        # Einen Tag hinzufuegen
        
        after_treatment_period_range = pd.date_range(start = after_treatment_period_day1, end = study_period[1])
        # Datumsreihe Nach-Interventionszeitraum
        after_treatment_period_N = len(after_treatment_period_range)
        # Anzahl Zeitpunkte des Nach-Treatment-Zeitraums

        ATT_dummies = [1] * after_treatment_period_N
        # Dummy-Variablen Interventionszeitraum

        ATT_data = {"t": after_treatment_period_range, "ATT": ATT_dummies}
        # Erst Definition als Dictionary
        ATT_data = pd.DataFrame(ATT_data)
        # Umwandlung in Pandas data frame

        # Zusammenfuegen von beidem:
        after_treatment_data = study_period_range.merge(ATT_data, how = "left")
        # left join, so dass nur noch 1x Datum und der TT-Dummy uebrig bleiben

        after_treatment_data['ATT'] = after_treatment_data['ATT'].fillna(0)
        # Alle Zellen in Spalte TT, die NaN sind, werden durch 0 ersetzt
        # (alle die in der study period vorkommen, aber nicht in der treatment period)

        after_treatment_data = after_treatment_data.drop(columns=["t", "t_counter"])
        # ueberfluessige Spalten raus ...

        treatment_data = pd.concat([treatment_data, after_treatment_data], axis=1)
        # ... und an treatment_data Spalten mit ATT anhaengen

    else:
        after_treatment_period_N = 0
        # wird in dict treatment_config mit ausgegeben


    # Zusammenstellung Konfigurationsdaten (wird ans Ergebnis angehaengt):
    treatment_config = {
        "study_period_start": study_period[0],
        "study_period_end": study_period[1],
        "study_period": study_period_N,
        "treatment_period_start": treatment_period[0],
        "treatment_period_end": treatment_period[1],
        "treatment_period": treatment_period_N,
        "frequency": freq,
        "pre_post": pre_post,
        "after_treatment_period": after_treatment_period,
        "after_treatment_period_N": after_treatment_period_N
        }
    # Definition als Dictionary

    treatment = did_treatment(treatment_data, treatment_config)

    return treatment


class did_data:
# Definition Klasse "did_data"
    def __init__(
        self,
        did_modeldata,
        did_groups,
        did_treatment,
        outcome_col_original,
        unit_time_col_original,
        covariates
        ):
    # Das "did_data"-Objekt ist eigentlich eine Liste mit drei Eintraegen:
    # [0] did_modeldata = Pandas data frame mit Modelldaten
    # [1] did_groups = did_groups-Objekt (Definition Treatment- und Kontrollgruppe)
    # [2] did_treatment = did_treatments-Objekt (Definition Treatment-Zeit)
    # [3] outcome_col_original = Urspruenglicher Name der AV
    # [4] unit_time_col_original = Liste mit Originalnamen der U-Einheiten und der Zeit
    # [5] covariates = Liste mit etwaigen Kontrollvariablen

        self.data = [
            did_modeldata, 
            did_groups, 
            did_treatment, 
            outcome_col_original,
            unit_time_col_original,
            covariates
            ]


    def get_did_modeldata_df (self):
        return pd.DataFrame(self.data[0])
        # Auslesen 1. Eintrag (Modelldaten) (df)

    def get_did_groups_dict (self):
        return self.data[1]
        # Auslesen 2. Eintrag (Gruppendaten) (dict)

    def get_did_treatment_dict (self):
        return self.data[2]
        # Auslesen 3. Eintrag (Treatment-Daten) (dict)

    def get_unit_time_cols (self):
        return self.data[4]
        # Auslesen 5. Eintrag (unit_time_col_original = Liste mit Originalnamen der U-Einheiten und der Zeit)

    def get_covariates (self):
        return self.data[5]
        # Auslesen 6. Eintrag (covariates = Liste mit etwaigen Kontrollvariablen)


    def add_covariates(
        self, 
        additional_df,
        variables,
        unit_col = None,
        time_col = None
        ):
    # Funktion, um Datensatz mit Untersuchungseinheiten noch Kontrollvariablen
    # hinzuzufuegen. Noetig hierfuer ist nur das erste Objekt, also self.df,
    # wo die Untersuchungseinheiten und ihre Zuordnung zur Treatment-
    # bzw. Kontrollgruppe drinstehen
        
        if unit_col is None and time_col is None:
            raise ValueError("unit_col and/or time_col must be stated")
        
        did_modeldata = self.data[0]
        # Auslesen des df aus self.data[0] (hier: Modelldaten)
        
        if unit_col is not None and time_col is not None:
        # wenn BEIDES angebeben wurde, wird angenommen, dass Verknuepfung
        # ueber Untersuchungseinheiten UND Zeit vorgenommen werden soll
            if "unit_time" not in additional_df.columns:
                additional_df["unit_time"] = additional_df[unit_col]+"_"+additional_df[time_col]
            if variables is None:
            # Wenn keine Variablen angegeben werden, wird das gesamte df
            # mit did_modeldata verknuepft
                did_modeldata = pd.merge(
                    did_modeldata, 
                    additional_df, 
                    on = "unit_time", 
                    how = "inner"
                    )
            else:
                additional_df_cols = ["unit_time"] + [col for col in additional_df.columns if col in variables]
                # nur ausgewaehlte Variablen als Liste [variables] zzgl. "unit_time"
                did_modeldata = pd.merge(
                    did_modeldata, 
                    additional_df[additional_df_cols], 
                    on = "unit_time", 
                    how = "inner"
                    )

        if unit_col is not None:
            if variables is None:
            # Wenn keine Variablen angegeben werden, wird das gesamte df
            # mit did_modeldata verknuepft
                did_modeldata = pd.merge(
                    did_modeldata, 
                    additional_df, 
                    left_on = "unit_UID", #did_unit_time_cols[0],
                    right_on = unit_col,
                    how = "inner"
                    )
            else:
                additional_df_cols = [unit_col] + [col for col in additional_df.columns if col in variables]
                # nur ausgewaehlte Variablen als Liste [variables] zzgl. unit_col
                did_modeldata = pd.merge(
                    did_modeldata, 
                    additional_df[additional_df_cols], 
                    left_on = "unit_UID", #did_unit_time_cols[0],
                    right_on = unit_col,
                    how = "inner"
                    ) 

        if time_col is not None:
            additional_df_cols = [unit_col] + [col for col in additional_df.columns if col in variables]
                # nur ausgewaehlte Variablen als Liste [variables] zzgl. unit_col
            did_modeldata = pd.merge(
                did_modeldata, 
                additional_df[additional_df_cols], 
                left_on = "unit_UID", #did_unit_time_cols[0],
                right_on = "t",
                how = "inner"
                )  
        
        self.data[0] = did_modeldata
        # Update in did_data-Objekt: did_modeldata mit neuen Spalten/Variablen
        self.data[5] = variables
        # Update in did_data-Objekt: covariates

        return self
        # did_data-Objekt wird in aktualisierter Form wieder ausgegeben


    def summary(self):

        did_modeldata = self.data[0]
        # Auslesen des df aus self.data[0] (hier: Modelldaten)
        
        groups_config = self.data[1].get_dict()
        # Auslesen des dictionaries aus self.data[1] (hier: Gruppendaten)

        treatment_config = self.data[2].get_dict()
        # Auslesen des dictionaries aus self.data[2] (hier: Treatmentdaten)

        outcome_col_original = self.data[3]
        # Auslesen Spaltennamen der Outcome-Variable (Y)


        print ("Difference-in-Differences Analysis")
        print ("---------------------------------------------------------------")
        print ("Treatment and Control Group")
        print ("Units:                   " + str(groups_config["full_sample"]) + " (" + str(round(groups_config["full_sample"]/groups_config["full_sample"]*100,2)) + " %)")
        print ("Treatment Group:         " + str(groups_config["treatment_group"]) + " (" + str(round(groups_config["treatment_group"]/groups_config["full_sample"]*100,2)) + " %)")
        print ("Control Group:           " + str(groups_config["control_group"]) + " (" + str(round(groups_config["control_group"]/groups_config["full_sample"]*100,2)) + " %)")
        print ("---------------------------------------------------------------")
        print ("Time Periods")

        if treatment_config["pre_post"] is True:
            print ("Study period (pre-post): " + str(treatment_config["treatment_period_start"]) + " vs. " + str(treatment_config["treatment_period_end"]))
        else:
            print ("Study period:            " + str(treatment_config["study_period_start"]) + " - " + str(treatment_config["study_period_end"]) + (" (") + str(treatment_config["study_period"]) + " " + treatment_config["frequency"] + ")")
            print ("Treatment Period:        " + str(treatment_config["treatment_period_start"]) + " - " + str(treatment_config["treatment_period_end"])+ (" (") + str(treatment_config["treatment_period"]) + " " + treatment_config["frequency"] + ")")

        print ("---------------------------------------------------------------")
        print ("Outcome '" + outcome_col_original + "'")
        print ("Mean:                    " + str(round(np.mean(did_modeldata[outcome_col_original]), 2)))
        print ("Standard deviation:      " + str(round(np.std(did_modeldata[outcome_col_original]), 2)))


    def analysis(
        self, 
        log_outcome: bool = False, 
        FE_unit: bool = False, 
        FE_time: bool = False, 
        ITE: bool = False,
        GTE: bool = False,
        ITT: bool = False,
        GTT: bool = False,
        group_by = None,
        confint_alpha = 0.05,
        drop_missing: bool = True,
        missing_replace_by_zero: bool = False
        ):

        """
        Funktion zur Auswertung des DiD-Objektes mit Funktion did_analysis()
        hier werden nur die Funktionsargumente angegeben, die sich auf etwas beziehen,
        dass in der Modellanalyse geklaert werden muss (fixed effects, logs, ITE)
        Der Rest wird schon ueber die Datenzusammenstellung geklaert (z.B. Treatment)
        """

        did_pd = self.data[0]
        # Auslesen Modelldaten

        treatment_config = self.data[2].get_dict()
        # Auslesen des dictionaries aus self.data[2] (hier: Treatmentdaten)

        outcome_col_original = self.data[3]
        # Auslesen "outcome_col_original" (4. Eintrag in der Liste)
        # = Variablenname von Y im Datensatz

        covariates = self.data[5]
        # Auslesen 6. Eintrag (covariates = Liste mit etwaigen Kontrollvariablen)

        did_results = didanalysis.did_analysis(
            data = did_pd,
            TG_col = "TG",
            TT_col = "TT",
            treatment_col = "TGxTT",
            unit_col = "unit_UID",
            time_col = "t",
            outcome_col = outcome_col_original,
            after_treatment_period = treatment_config["after_treatment_period"],
            after_treatment_col = "TGxATT",
            pre_post = treatment_config["pre_post"],
            log_outcome = log_outcome,
            FE_unit = FE_unit,
            FE_time = FE_time,
            ITE = ITE,
            GTE = GTE,
            ITT = ITT,
            GTT = GTT,
            group_by = group_by,
            covariates = covariates,
            confint_alpha = confint_alpha,
            drop_missing = drop_missing,
            missing_replace_by_zero = missing_replace_by_zero
            )
        # Auswertung mit did_analysis()

        return did_results


def merge_data(
    outcome_data,
    unit_id_col,
    time_col,
    outcome_col,
    did_groups,
    did_treatment 
    ):

    # Schritt 1) Auslesen relevante Daten:

    groups_data_df = did_groups.get_df()
    groups_dict = did_groups.get_dict()
    # Auslesen Daten aus did_groups-Objekt

    treatment_data_df = did_treatment.get_df()
    treatment_dict = did_treatment.get_dict()
    # Auslesen Daten aus did_treatment-Objekt

    # Schritt 2) Zusammenstellung Gruppen- und Interventionsdaten:
   
    did_modeldata = groups_data_df.merge(treatment_data_df, how = "cross")
    # verknuepfen als kartesisches Produkt M x N


    # Schritt 3) Neue Variablen erstellen:

    did_modeldata["TGxTT"] = did_modeldata["TG"] * did_modeldata["TT"]
    # Interaktionsterm erstellen

    if treatment_dict["after_treatment_period"] is True:
        did_modeldata["TGxATT"] = did_modeldata["TG"] * did_modeldata["ATT"]
        # Zusaetzlichen Interaktionsterm fuer Nach-Interventionsperiode erstellen

    did_modeldata["unit_time"] = did_modeldata["unit_UID"].astype(str) + "_" + did_modeldata["t"].astype(str)
    # neue Spalte mit UID der Untersuchungseinheit und Zeit-Zaehler
    # damit beides zusammengesetzt werden, muss beides im str-Format verarbeitet werden

    
    # Schritt 4) Outcome-Daten anhaengen:

    outcome_data["unit_time"] = outcome_data[unit_id_col].astype(str) + "_" + outcome_data[time_col].astype(str)
    # neue Spalte mit UID der Untersuchungseinheit und Zeit-Zaehler
    outcome_data_short = outcome_data[["unit_time", outcome_col]]
    # df nur mit "unit_time" und der abhaengigen Variable
    did_modeldata = did_modeldata.merge(outcome_data_short, on="unit_time", how="left")
    # Verknuepfung ueber Spalte "unit_time"


    # Schritt 5) Alles in ein did_data-Objekt schreiben und ausgeben:

    outcome_col_original = outcome_col
    # Name der Outcome-Spale
    unit_time_col_original = [unit_id_col, time_col]
    # Liste mit den Namen der unit_col und time_col

    did_data_all = did_data(
        did_modeldata, 
        did_groups, 
        did_treatment, 
        outcome_col_original,
        unit_time_col_original,
        None
        )
    # 5 Eintraege:
    # [0] did_modeldata = Modelldaten
    # [1] groups = Gruppendaten
    # [2] treatment = Treatment-Daten
    # [3] outcome_col_original = Original-Variablenname von Y
    # [4] unit_time_col = Liste mit Originalnamen der U-Einheiten und der Zeit
    # [5] Platzhalter fuer etwaige Kontrollvariables (covariates)

    return did_data_all
    # ...und ausgeben


def create_data(
    outcome_data,
    unit_id_col,
    time_col,
    outcome_col,
    treatment_group,
    control_group,
    study_period,
    treatment_period,
    freq = "D",
    pre_post = False,
    after_treatment_period = False
    ):

    # Schritt 1) Erstellen von Gruppen- und Interventionsdaten

    groups = create_groups (treatment_group, control_group)
    # Gruppendaten aufbauen mit Funktion groups()
    treatment = create_treatment (
        study_period = study_period, 
        treatment_period = treatment_period, 
        freq = freq, 
        pre_post = pre_post, 
        after_treatment_period = after_treatment_period
        )
    # Treatment-Daten aufbauen mit Funktion treatment()

    groups_data_df = groups.get_df()
    treatment_data_df = treatment.get_df()
    # data frames auslesen

    
    # Schritt 2) Zusammenstellung Gruppen- und Interventionsdaten

    did_modeldata = groups_data_df.merge(treatment_data_df, how = "cross")
    # verknuepfen als kartesisches Produkt M x N


    # Schritt 3) Neue Variablen erstellen:

    did_modeldata["TGxTT"] = did_modeldata["TG"] * did_modeldata["TT"]
    # Interaktionsterm erstellen

    if after_treatment_period is True:
        did_modeldata["TGxATT"] = did_modeldata["TG"] * did_modeldata["ATT"]
        # Zusaetzlichen Interaktionsterm fuer Nach-Interventionsperiode erstellen

    did_modeldata["unit_time"] = did_modeldata["unit_UID"].astype(str) + "_" + did_modeldata["t"].astype(str)
    # neue Spalte mit UID der Untersuchungseinheit und Zeit-Zaehler
    # damit beides zusammengesetzt werden, muss beides im str-Format verarbeitet werden

    
    # Schritt 4) Outcome-Daten anhaengen:

    outcome_data["unit_time"] = outcome_data[unit_id_col].astype(str) + "_" + outcome_data[time_col].astype(str)
    # neue Spalte mit UID der Untersuchungseinheit und Zeit-Zaehler
    outcome_data_short = outcome_data[["unit_time", outcome_col]]
    # df nur mit "unit_time" und der abhaengigen Variable
    did_modeldata = did_modeldata.merge(outcome_data_short, on="unit_time", how="left")
    # Verknuepfung ueber Spalte "unit_time"


    # Schritt 5) Alles in ein did_data-Objekt schreiben und ausgeben:

    outcome_col_original = outcome_col
    # Name der Outcome-Spale
    unit_time_col_original = [unit_id_col, time_col]
    # Liste mit den Namen der unit_col und time_col

    did_data_all = did_data(
        did_modeldata, 
        groups, 
        treatment, 
        outcome_col_original,
        unit_time_col_original,
        None
        )
    # 5 Eintraege:
    # [0] did_modeldata = Modelldaten
    # [1] groups = Gruppendaten
    # [2] treatment = Treatment-Daten
    # [3] outcome_col_original = Original-Variablenname von Y
    # [4] unit_time_col = Liste mit Originalnamen der U-Einheiten und der Zeit
    # [5] Platzhalter fuer etwaige Kontrollvariables (covariates)

    return did_data_all
    # ...und ausgeben