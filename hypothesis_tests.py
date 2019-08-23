"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
import math
import functions_kyle as f
import statistics
from statsmodels.stats.power import TTestIndPower
power_analysis = TTestIndPower()

def create_sample_dists(cleaned_data, y_var=None, categories=[]):
    htest_dfs = []
    if y_var == "percentage_nonvoting":
        if categories == ["republican", "democratic"]:
            htest_dfs = f.collect_sample_means_party(cleaned_data)
        elif categories == ["senate", "house"]:
            htest_dfs = f.collect_sample_means_chamber(cleaned_data)
        elif categories == ["senate republican", "senate democratic"]:
            data_list = f.collect_sample_means_chamber_party(cleaned_data)
            rep_senate = data_list[0]
            dem_senate = data_list[1]
            htest_dfs.append(rep_senate)
            htest_dfs.append(dem_senate)
        elif categories == ["house republican", "house democratic"]:
            data_list = f.collect_sample_means_chamber_party(cleaned_data)
            rep_house = data_list[2]
            dem_house = data_list[3]
            htest_dfs.append(rep_house)
            htest_dfs.append(dem_house)
    return htest_dfs

def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(cleaned_data, alpha = None):

    # Check to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')
    
    
    print('The purpose of this test is to determine whether the percentages of Republicans and'
          '\n Democrats that abstain from voting in congressional bills is equal.'
          '\n')
    
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["republican", "democratic"])

    # Determine P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples,dem_samples, equal_var = False))
    p_val = ttest[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=500, alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()} the null hypothesis.'
          f'\n Due to these results, we {assertion} state that there is a difference between the percentage'
          f'\n of Republicans and Democrats that abstain from voting when present.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_two(cleaned_data, alpha = None):
    # Check to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')
    
    
    print('The purpose of this test is to determine whether the percentages of Republicans and'
          '\nDemocrats that abstain from voting in congressional bills within the Senate is equal.'
          '\n')
    
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["senate republican", "senate democratic"])

    # Determine P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples,dem_samples, equal_var = False))
    p_val = ttest[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=500, alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()} the null hypothesis.'
          f'\n Due to these results, we {assertion} state that there is a difference between the percentage'
          f'\n of Republicans and Democrats in the Senate that abstain from voting when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_three(cleaned_data, alpha = None):
    # Check to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')
    
    
    print('The purpose of this test is to determine whether the percentages of Republicans and'
          '\n Democrats that abstain from voting in congressional bills within the House of'
          '\n Representatives is equal.'
          '\n')
    
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["house republican", "house democratic"])

    # Determine P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples,dem_samples, equal_var = False))
    p_val = ttest[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=500, alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()} the null hypothesis.'
          f'\n Due to these results, we {assertion} state that there is a difference between the percentage'
          f'\n of Republicans and Democrats in the House of Representatives that abstain from voting when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_four(cleaned_data, alpha = None):
    
    # Check to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')
    
    
    print('The purpose of this test is to determine whether the percentages of congresspeople in'
          '\n both the Senate and the House of Representatives that abstain from voting in' 
          '\n congressional bills is equal.')
    
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["senate", "house"])

    # Determine P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples,dem_samples, equal_var = False))
    p_val = ttest[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=500, alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()} the null hypothesis.'
          f'\n Due to these results, we {assertion} state that there is a difference between the percentage'
          f'\n of members from the Senate and House of Representatives that abstain from voting when present.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status


