import numpy as np
import pandas as pd
import streamlit as st

# Name the app
st.title('Predicting the health outcome of HRH expansion in 2025-2034 in Malawi')

# Markdown
st.markdown(
    """
This predictor is built on an HRH expansion study that is published elsewhere XXX.

Each HRH expansion strategy is determined by inputs of five percentage numbers for each of Clinical, DCSA, 
Nursing and Midwifery, Pharmacy and Other cadres that sum up to 100%. Each number means the proportion of 
a limited additional budget that is allocated to each cadre for expansion each year.

The health outcomes are measured by percent DALYs averted and DALYs averted of each input strategy against no expansion 
scenario.

The prediction can be done in 5 settings:\\
    (1) main analysis - \\
        annual budget growth rate = 4.2%, perfect consumable availability, default health system function\\
    (2) sensitivity analysis with more budget -\\
        annual budget growth rate = 5.8%, perfect consumable availability, default health system function\\
    (3) sensitivity analysis with less budget -\\
        annual budget growth rate = 2.6%, perfect consumable availability, default health system function\\
    (4) sensitivity analysis with default consumable availability - \\
        annual budget growth rate = 4.2%, default consumable availability, default health system function\\
    (5) sensitivity analysis with maximal health system function - \\
        annual budget growth rate = 4.2%%, perfect consumable availability, maximal health system function
        
In each setting, we interpret an HRH expansion strategy as "good" if the percentage DALYs averted is no less than 
the estimated health outcome of a strategy that implement the current (as of 2024) cost proportions for each cadre. 
These thresholds are (1) 6%, (2) 8%, (3) 3%, (4) 4%, (5) 5%. 
See XXX for more information on the thresholds for "good" strategies.
    """
)

# Take inputs
p_clinical = st.number_input(label='Enter the proportion for Clinical cadre (in %)',
                             min_value=0.0, max_value=100.0, value=20.0, step=1.0)
p_dcsa = st.number_input(label='Enter the proportion for DCSA cadre (in %)',
                         min_value=0.0, max_value=100.0, value=20.0, step=1.0)
p_nursing = st.number_input(label='Enter the proportion for Nursing and Midwifery cadre (in %)',
                            min_value=0.0, max_value=100.0, value=20.0, step=1.0)
p_pharmacy = st.number_input(label='Enter the proportion for Pharmacy cadre (in %)',
                             min_value=0.0, max_value=100.0, value=20.0, step=1.0)
p_other = st.number_input(label='Enter the proportion for Other cadre (in %)',
                          min_value=0.0, max_value=100.0, value=20.0, step=1.0)
p = [p_clinical/100, p_dcsa/100, p_nursing/100, p_pharmacy/100, p_other/100]

# Check inputs if summing up to 1 and re-take the inputs
if abs(sum(p) - 1) > 0:
    st.error('The 5 input proportions do not sum up to 100%. Please re-input.')

# Choose the prediction setting
setting = st.radio('Select the setting for the prediction: ',
                   ('Main analysis',
                    'Sensitivity analysis with more budget',
                    'Sensitivity analysis with less budget',
                    'Sensitivity analysis with default consumable availability',
                    'Sensitivity analysis with maximal health system function',
                    )
                   )


# Define functions to transform inputs to average increase rates
def increase_rate(R=0.042, input=p):
    # the current cost fractions for each cadre, in order of Clinical, DCSA, Nursing and Midwifery, Pharmacy, Other
    f = [0.2178, 0.2349, 0.4514, 0.0269, 0.0690]
    # calculate the increase rate x
    x = [0, 0, 0, 0, 0]
    for i in range(5):
        x[i] = (1 + input[i] * ((1+R) ** 10 - 1) / f[i]) ** (1/10) - 1
    return x


# Define functions to calculate the health outcome
def main_analysis(input=p):
    # the linear predicting model
    const = -0.0699
    coefs = [1.0046, 0.4170, 1.0309, 0.2691, 0.1965]
    # get increase rates
    rate = increase_rate(R=0.042, input=input)
    # calculate the health outcome
    percent_dalys_averted = sum([coefs[i] * rate[i] for i in range(5)]) + const  # percent DALYs averted
    dalys_averted = percent_dalys_averted * 94.22  # DALYs averted in millions
    return percent_dalys_averted, dalys_averted


def more_budget(input=p):
    # the linear predicting model
    const = -0.0694
    coefs = [0.7980, 0.3189, 0.7588, 0.2332, 0.1568]
    # get increase rates
    rate = increase_rate(R=0.058, input=input)
    # calculate the health outcome
    percent_dalys_averted = sum([coefs[i] * rate[i] for i in range(5)]) + const  # percent DALYs averted
    dalys_averted = percent_dalys_averted * 93.90  # DALYs averted in millions
    return percent_dalys_averted, dalys_averted


def less_budget(input=p):
    # the linear predicting model
    const = -0.0850
    coefs = [1.3943, 0.7054, 1.6656, 0.3415, 0.2941]
    # get increase rates
    rate = increase_rate(R=0.026, input=input)
    # calculate the health outcome
    percent_dalys_averted = sum([coefs[i] * rate[i] for i in range(5)]) + const  # percent DALYs averted
    dalys_averted = percent_dalys_averted * 94.31  # DALYs averted in millions
    return percent_dalys_averted, dalys_averted


def default_cons(input=p):
    # the linear predicting model
    const = -0.0529
    coefs = [0.6820, 0.2670, 0.7319, 0.1569, 0.1205]
    # get increase rates
    rate = increase_rate(R=0.042, input=input)
    # calculate the health outcome
    percent_dalys_averted = sum([coefs[i] * rate[i] for i in range(5)]) + const  # percent DALYs averted
    dalys_averted = percent_dalys_averted * 112.18  # DALYs averted in millions
    return percent_dalys_averted, dalys_averted


def max_hs_func(input=p):
    # the linear predicting model
    const = -0.0963
    coefs = [1.1703, 0.3473, 1.5802, 0.1734, 0.1676]
    # get increase rates
    rate = increase_rate(R=0.042, input=input)
    # calculate the health outcome
    percent_dalys_averted = sum([coefs[i] * rate[i] for i in range(5)]) + const  # percent DALYs averted
    dalys_averted = percent_dalys_averted * 128.05  # DALYs averted in millions
    return percent_dalys_averted, dalys_averted


# calculate the outcomes
if setting == 'Main analysis':
    outcomes = main_analysis(input=p)
elif setting == 'Sensitivity analysis with more budget':
    outcomes = more_budget(input=p)
elif setting == 'Sensitivity analysis with less budget':
    outcomes = less_budget(input=p)
elif setting == 'Sensitivity analysis with default consumable availability':
    outcomes = default_cons(input=p)
elif setting == 'Sensitivity analysis with maximal health system function':
    outcomes = max_hs_func(input=p)

# Check the predicting button and print outcomes
if st.button('Predict the health outcome'):

    # print the health outcome
    st.markdown(f"The percent dalys averted is **{round(outcomes[0], 4) * 100}%** in the 10 year period of 2025-2034, "
                f"equating to **{round(outcomes[1], 2)} million DALYs averted** as compared with no expansion scenario.")

    # give the interpretation of the strategy
    if (
            ((setting == 'Main analysis') and (outcomes[0] >= 0.06)) or
            ((setting == 'Sensitivity analysis with more budget') and (outcomes[0] >= 0.08)) or
            ((setting == 'Sensitivity analysis with less budget') and (outcomes[0] >= 0.03)) or
            ((setting == 'Sensitivity analysis with default consumable availability') and (outcomes[0] >= 0.04)) or
            ((setting == 'Sensitivity analysis with maximal health system function') and (outcomes[0] >= 0.05))
       ):
        st.success("This is a good strategy as interpreted.")
    else:
        st.warning("There should be better strategies as interpreted.")
