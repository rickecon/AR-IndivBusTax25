# Import packages
import pandas as pd
import numpy as np
import os
import json

from policyengine_us.model_api import *
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from policyengine_core.periods import instant
import ccc


# Define the 12 filer types
situation_sgl_low = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "0"},
            "employment_income": {"2025": "13000"},
            "medical_out_of_pocket_expenses": {"2025": "200"},
        },
    },
    "families": {
        "your family": {
            "members": [
                "you",
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
            ],
            "broadband_cost": {"2025": "400"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "5000"},
            "phone_cost": {"2025": "500"},
            "spm_unit_id": {"2025": "0"},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_sgl_mid = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "2000"},
            "employment_income": {"2025": "40000"},
            "medical_out_of_pocket_expenses": {"2025": "1000"},
        },
    },
    "families": {
        "your family": {
            "members": [
                "you",
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
            ],
            "broadband_cost": {"2025": "700"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "15000"},
            "phone_cost": {"2025": "1200"},
            "spm_unit_id": {"2025": "0"},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_sgl_high = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "8000"},
            "employment_income": {"2025": "90000"},
            "medical_out_of_pocket_expenses": {"2025": "2000"},
        },
    },
    "families": {
        "your family": {
            "members": [
                "you",
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
            ],
            "broadband_cost": {"2025": "1200"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "30000"},
            "phone_cost": {"2025": "2000"},
            "spm_unit_id": {"2025": "0"},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_hoh_low = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "0"},
            "employment_income": {"2025": "20000"},
            "medical_out_of_pocket_expenses": {"2025": "500"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "500"},
            "childcare_expenses": {"2025": "1000"},
            "housing_cost": {"2025": "9000"},
            "phone_cost": {"2025": "600"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_hoh_mid = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "2000"},
            "employment_income": {"2025": "60000"},
            "medical_out_of_pocket_expenses": {"2025": "2000"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "800"},
            "childcare_expenses": {"2025": "2000"},
            "housing_cost": {"2025": "20000"},
            "phone_cost": {"2025": "1000"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_hoh_high = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "15000"},
            "employment_income": {"2025": "150000"},
            "medical_out_of_pocket_expenses": {"2025": "3000"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "1200"},
            "childcare_expenses": {"2025": "3000"},
            "housing_cost": {"2025": "36000"},
            "phone_cost": {"2025": "1800"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_0_low = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "0"},
            "employment_income": {"2025": "12000"},
            "medical_out_of_pocket_expenses": {"2025": "400"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "10000"},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "broadband_cost": {"2025": "500"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "6000"},
            "phone_cost": {"2025": "800"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_0_mid = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "2000"},
            "employment_income": {"2025": "35000"},
            "medical_out_of_pocket_expenses": {"2025": "1800"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "25000"},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "broadband_cost": {"2025": "900"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "18000"},
            "phone_cost": {"2025": "1200"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_0_high = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "16000"},
            "employment_income": {"2025": "90000"},
            "medical_out_of_pocket_expenses": {"2025": "3000"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "70000"},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "broadband_cost": {"2025": "1200"},
            "childcare_expenses": {"2025": "0"},
            "housing_cost": {"2025": "36000"},
            "phone_cost": {"2025": "2000"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_2_low = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "0"},
            "employment_income": {"2025": "25000"},
            "medical_out_of_pocket_expenses": {"2025": "600"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "0"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "500"},
            "childcare_expenses": {"2025": "1000"},
            "housing_cost": {"2025": "10000"},
            "phone_cost": {"2025": "800"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_2_mid = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "2500"},
            "employment_income": {"2025": "40000"},
            "medical_out_of_pocket_expenses": {"2025": "2500"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "30000"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "900"},
            "childcare_expenses": {"2025": "2200"},
            "housing_cost": {"2025": "22000"},
            "phone_cost": {"2025": "1500"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

situation_mar_2_high = {
    "people": {
        "you": {
            "age": {"2025": "38"},
            "charitable_cash_donations": {"2025": "20000"},
            "employment_income": {"2025": "100000"},
            "medical_out_of_pocket_expenses": {"2025": "3500"},
        },
        "your partner": {
            "age": {"2025": "35"},
            "employment_income": {"2025": "100000"},
        },
        "your first dependent": {
            "age": {"2025": "10"},
            "is_tax_unit_dependent": {"2025": True},
        },
        "your second dependent": {
            "age": {"2025": "6"},
            "is_tax_unit_dependent": {"2025": True},
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": ["you", "your partner"],
            "marital_unit_id": {"2025": 0}
        },
        "your first dependent's marital unit": {
            "members": ["your first dependent"],
            "marital_unit_id": {"2025": 2}
        },
        "your second dependent's marital unit": {
            "members": ["your second dependent"],
            "marital_unit_id": {"2025": 3}
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "broadband_cost": {"2025": "1200"},
            "childcare_expenses": {"2025": "3000"},
            "housing_cost": {"2025": "36000"},
            "phone_cost": {"2025": "1800"},
            "spm_unit_id": {"2025": 0},
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {"2025": "AR"}
        }
    }
}

# Run baseline and reform simulations for the 3.4% flat tax
# Create baseline (no change) parameters
def modify_parameters_b(parameters):
    """
    Baseline reform is to not modify the parameters.
    """
    pass
    return parameters


# Create  baseline (no change) reform
class reform_b(Reform):
    def apply(self):
        self.modify_parameters(modify_parameters_b)


# Define the parameters that change in the reform
def modify_parameters_1(parameters):
    # Set flat 3.4% rate for all brackts on income < $92.3
    parameters.gov.states.ar.tax.income.rates.rates[0].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    parameters.gov.states.ar.tax.income.rates.rates[1].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    parameters.gov.states.ar.tax.income.rates.rates[2].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    parameters.gov.states.ar.tax.income.rates.rates[3].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    parameters.gov.states.ar.tax.income.rates.rates[4].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    # Set flat 3.4% rate for all brackts on income > $92.3
    parameters.gov.states.ar.tax.income.rates.high_income_rates[0].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    parameters.gov.states.ar.tax.income.rates.high_income_rates[1].rate.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=0.034
    )
    # Increase the standard deduction for each filer type
    parameters.gov.states.ar.tax.income.deductions.standard.JOINT.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=6_680
    )
    parameters.gov.states.ar.tax.income.deductions.standard.SURVIVING_SPOUSE.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=6_680
    )
    parameters.gov.states.ar.tax.income.deductions.standard.HEAD_OF_HOUSEHOLD.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=6_680
    )
    parameters.gov.states.ar.tax.income.deductions.standard.SINGLE.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=6_680
    )
    parameters.gov.states.ar.tax.income.deductions.standard.SEPARATE.update(
        start=instant("2025-01-01"), stop=instant("2030-12-31"), value=6_680
    )

    return parameters


class reform_1(Reform):
    def apply(self):
        self.modify_parameters(modify_parameters_1)


def calculate_base_reform(sim_name, base_reform, reform, situation):
    print("Simulating baseline scenario for:", sim_name)
    simulation_b = Simulation(reform=base_reform, situation=situation)
    simulation_b.trace = True
    income_before_tax = sum(simulation_b.calculate("employment_income", 2024))
    income_after_tax_b = simulation_b.calculate("household_net_income", 2024)[0]
    ar_net_tax_liability_b = simulation_b.calculate("ar_income_tax", 2024)[0]
    print("Simulating reform scenario for:", sim_name)
    simulation_r = Simulation(reform=reform, situation=situation)
    simulation_r.trace = True
    income_after_tax_r = simulation_r.calculate("household_net_income", 2024)[0]
    ar_net_tax_liability_r = simulation_r.calculate("ar_income_tax", 2024)[0]
    ar_net_tax_liab_dol_chg = ar_net_tax_liability_r - ar_net_tax_liability_b
    ar_net_tax_liab_pct_chg = (ar_net_tax_liab_dol_chg /
                               np.absolute(ar_net_tax_liability_b))
    print("")
    return (
        income_before_tax, income_after_tax_b, ar_net_tax_liability_b,
        income_after_tax_r, ar_net_tax_liability_r, ar_net_tax_liab_dol_chg,
        ar_net_tax_liab_pct_chg
    )

simulations = [
    ('Single, no kids, low income', situation_sgl_low),
    ('Single, no kids, middle income', situation_sgl_mid),
    ('Single, no kids, high income', situation_sgl_high),
    ('Married filing jointly, no kids, low income', situation_mar_0_low),
    ('Married filing jointly, no kids, middle income', situation_mar_0_mid),
    ('Married filing jointly, no kids, high income', situation_mar_0_high),
    ('Head of household, 2 kids, low income', situation_hoh_low),
    ('Head of household, 2 kids, middle income', situation_hoh_mid),
    ('Head of household, 2 kids, high income', situation_hoh_high),
    ('Married, 2 kids, low income', situation_mar_2_low),
    ('Married, 2 kids, middle income', situation_mar_2_mid),
    ('Married, 2 kids, high income', situation_mar_2_high),
]

results = []

# Loop through each simulation
for sim_name, situation in simulations:
    # Calculate before_tax_income, after_tax_income, and sc_net_tax_liability
    (
        income_before_tax, income_after_tax_b, ar_net_tax_liability_b,
        income_after_tax_r, ar_net_tax_liability_r, ar_net_tax_liab_dol_chg,
        ar_net_tax_liab_pct_chg
    ) = calculate_base_reform(sim_name, reform_b, reform_1, situation)

    # Append the results as a dictionary where key is the column name and value
    # is the simulation output
    results.append({
        "Situation": sim_name,
        "Before tax income": income_before_tax,
        "Baseline after tax income": income_after_tax_b,
        "Baseline Arkansas net tax liability": ar_net_tax_liability_b,
        "Reform after tax income": income_after_tax_r,
        "Reform Arkansas net tax liability": ar_net_tax_liability_r,
        "Arkansas net tax liability change, dollars": ar_net_tax_liab_dol_chg,
        "Arkansas net tax liability change, percent": ar_net_tax_liab_pct_chg
    })

# Convert the results to a DataFrame
df = pd.DataFrame(results)

# Check the DataFrame
df
