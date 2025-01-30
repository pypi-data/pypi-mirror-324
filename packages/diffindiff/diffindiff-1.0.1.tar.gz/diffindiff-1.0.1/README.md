# diffindiff: Difference-in-Differences (DiD) Analysis Python Library

This Python library is designed for performing Difference-in-Differences (DiD) analyses in a convenient way. It allows users to construct datasets, define treatment and control groups, and set treatment periods. DiD model analyses may be conducted with both datasets created by built-in functions and ready-to-use external datasets. Both simultaneous and staggered adoption are supported. The library allows for various extensions, such as two-way fixed effects models, group- or individual-specific effects, and post-treatment periods. Additionally, it includes functions for visualizing results, such as plotting DiD coefficients with confidence intervals and illustrating the temporal evolution of staggered treatments.

## Author

This library was developed by Thomas Wieland (geowieland@googlemail.com).


## Features

- **Data Setup**: Define custom treatment and control groups as well as treatment periods; Save ready-to-fit DiD objects.
- **DiD analysis**: Perfom standard DiD analysis  
**Model Extensions**: e.g.
  - Staggered adoption
  - Two-way fixed effects models
  - Group-specific or individual-specific effects
  - Group-specific or individual specific time trends
  - Covariates
  - After-treatment period
- **Visualization**: e.g.
  - Plot observed and expected time course of treatment and control group 
  - Plot DiD coefficients with confidence intervals
  - Visualize the temporal evolution of staggered treatments
- **Data diagnosis**: e.g.
  - Test for control conditions
  - Test for type of adoption
  - Test whether the panel dataset is balanced 

## Examples

```python
curfew_DE=pd.read_csv("data/curfew_DE.csv", sep=";", decimal=",")

curfew_data=create_data(
    outcome_data=curfew_DE,
    unit_id_col="county",
    time_col="infection_date",
    outcome_col="infections_cum_per100000",
    treatment_group= 
        curfew_DE.loc[curfew_DE["Bundesland"].isin([9,10,14])]["county"],
    control_group= 
        curfew_DE.loc[~curfew_DE["Bundesland"].isin([9,10,14])]["county"],
    study_period=["2020-03-01", "2020-05-15"],
    treatment_period=["2020-03-21", "2020-05-05"],
    freq="D"
    )
# Creating DiD dataset by defining groups and
# treatment time at once

curfew_data.summary()
# Summary of created treatment data

curfew_model = curfew_data.analysis()
# Model analysis of created data

curfew_model.summary()
# Model summary

curfew_model.plot(
    y_label="Cumulative infections per 100,000",
    plot_title="Curfew effectiveness - Groups over time",
    plot_observed=True
    )
# Plot observed vs. predicted (means) separated by group (treatment and control)

curfew_model.plot_effects(
    x_label="Coefficients with 95% CI",
    plot_title="Curfew effectiveness - DiD effects"
    )
# plot effects

See the /tests directory for usage examples of most of the included functions.

## Installation

To install the package, use `pip`:

```bash
pip install diffindiff