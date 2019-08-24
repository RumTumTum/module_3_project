"""Imports Hypothesis Tests"""
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import functions_kyle as f
POWER_ANALYSIS = TTestIndPower()


def create_sample_dists(cleaned_data, y_var=None, categories=None):
    """Creates samples based on imput"""
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
    """Compares p-value to alpha"""
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(cleaned_data, alpha=None):
    """Runs first hypothesis test"""
    # Checks to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')

    print('The purpose of this test is to determine whether the percentages'
          'of Republicans and\n Democrats that abstain from voting in '
          'congressional bills is equal.\n')

    # Gets data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["republican",
                                                        "democratic"])

    # Determines P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples, dem_samples, equal_var=False))
    p_val = ttest[1]

    # Returns statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = POWER_ANALYSIS.solve_power(effect_size=coh_d, nobs1=500,
                                           alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we'
          f'{status.lower()} the null hypothesis.\n Due to these results,'
          f'we {assertion} state that there is a difference between the'
          f'percentage\n of Republicans and Democrats that abstain from'
          f'voting when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} "
              f"and power of {power}.")
    else:
        print(".")

    return status


def hypothesis_test_two(cleaned_data, alpha=None):
    """Runs second hypothesis test"""
    # Check to verify alpha
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')

    print('The purpose of this test is to determine whether the percentages of'
          f'congresspeople in\n both the Senate and the House of '
          f'Representatives that abstain from voting in\n congressional '
          f'bills is equal.')

    # Gets data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["senate", "house"])

    # Determines P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples, dem_samples, equal_var=False))
    p_val = ttest[1]

    # Returns statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = POWER_ANALYSIS.solve_power(effect_size=coh_d, nobs1=500,
                                           alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we '
          f'{status.lower()} the null hypothesis.\n Due to these results, '
          f'we {assertion} state that there is a difference between the '
          f'percentage\n of members from the Senate and House of '
          f'Representatives that abstain from voting when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)}"
              f"and power of {power}.")
    else:
        print(".")

    return status


def hypothesis_test_three(cleaned_data, alpha=None):
    """Runs third hypothesis test"""
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')

    print('The purpose of this test is to determine whether the percentages '
          'of Republicans and\n Democrats that abstain from voting in '
          'congressional bills within the Senate is equal.\n')

    # Gets data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["senate republican",
                                                        "senate democratic"])

    # Determines P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples, dem_samples, equal_var=False))
    p_val = ttest[1]

    # Returns statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = POWER_ANALYSIS.solve_power(effect_size=coh_d, nobs1=500,
                                           alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} '
          f'we {status.lower()} the null hypothesis.\n Due to these '
          f'results, we {assertion} state that there is a difference '
          f'between the percentage\n of Republicans and Democrats in '
          f'the Senate that abstain from voting when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and "
              f"power of {power}.")
    else:
        print(".")

    return status


def hypothesis_test_four(cleaned_data, alpha=None):
    """Runs fourth hypothesis test"""
    if alpha < 0 or alpha > 1:
        return print('Alpha must be between 0 and 1.')

    print('The purpose of this test is to determine whether the percentages '
          f'of Republicans and\n Democrats that abstain from voting in '
          f'congressional bills within the House of\n Representatives is '
          f'equal.\n')

    # Gets data for tests
    comparison_groups = create_sample_dists(cleaned_data,
                                            y_var="percentage_nonvoting",
                                            categories=["house republican",
                                                        "house democratic"])

    # Determines P value
    rep_samples = comparison_groups[0]
    dem_samples = comparison_groups[1]
    ttest = list(stats.ttest_ind(rep_samples, dem_samples, equal_var=False))
    p_val = ttest[1]

    # Returns statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = f.cohen_d(rep_samples, dem_samples)
        power = POWER_ANALYSIS.solve_power(effect_size=coh_d, nobs1=500,
                                           alpha=alpha)

    print(f'Based on the p value of {p_val} and our alpha of {alpha} '
          f'we {status.lower()} the null hypothesis.\n Due to these '
          f'results, we {assertion} state that there is a difference '
          f'between the percentage\n of Republicans and Democrats in '
          f'the House of Representatives that abstain from voting '
          f'when present')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and "
              f"power of {power}.")
    else:
        print(".")

    return status
