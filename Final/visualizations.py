"""This is the visualization module"""

import matplotlib.pyplot as plt
import seaborn as sns
import functions as f

# Set specific parameters for the visualizations
LARGE = 22
MED = 16
SMALL = 12
PARAMS = {'axes.titlesize': LARGE,
          'legend.fontsize': MED,
          'figure.figsize': (16, 10),
          'axes.labelsize': MED,
          'xtick.labelsize': MED,
          'ytick.labelsize': MED,
          'figure.titlesize': LARGE}
plt.rcParams.update(PARAMS)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def overlapping_density(input_vars):
    """Creates overlapping density graph"""
    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    # Starter code for figuring out which package to use
    for variable in input_vars:
        sns.kdeplot(variable[1], shade=True, color=variable[2],
                    label=variable[0], figure=fig)
    return fig


def visualization_one(cleaned_data, input_vars=None,
                      output_image_name="hypothesis_one"):
    """Creates visualization for hypothesis one"""

    comparison_groups = f.sample_of_means_percent_yay(cleaned_data)
    rep_samples = ["Republican", comparison_groups[0], "r"]
    dem_samples = ["Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel('Percentage Voting "Yay"')
    plt.ylabel("Probability Density")
    plt.title('Comparison of Parties Voting "Yay" by Percentage')
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_two(cleaned_data, input_vars=None,
                      output_image_name="hypothesis_two"):
    """Creates visualization for hypothesis two"""

    cleaned_data = cleaned_data.loc[cleaned_data.chamber == 'house']
    comparison_groups = f.sample_of_means_percent_yay(cleaned_data)
    rep_samples = ["Republican", comparison_groups[0], "r"]
    dem_samples = ["Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel('Percentage Voting "Yay"')
    plt.ylabel("Probability Density")
    plt.title('Comparison of Parties Voting "Yay" by Percentage in House')
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_three(cleaned_data, input_vars=None,
                        output_image_name="hypothesis_three"):
    """Creates visualization for hypothesis three"""

    cleaned_data = cleaned_data.loc[cleaned_data.chamber == 'senate']
    comparison_groups = f.sample_of_means_percent_yay(cleaned_data)
    rep_samples = ["Republican", comparison_groups[0], "r"]
    dem_samples = ["Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel('Percentage Voting "Yay"')
    plt.ylabel("Probability Density")
    plt.title('Comparison of Parties Voting "Yay" by Percentage in Senate')
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_four(cleaned_data, input_vars=None,
                       output_image_name="hypothesis_four"):
    """Creates visualization for hypothesis four"""
    ###
    comparison_groups = f.collect_sample_means_party(cleaned_data)
    rep_samples = ["Republican", comparison_groups[0], "r"]
    dem_samples = ["Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel("Percentage Abstaining from Vote")
    plt.ylabel("Probability Density")
    plt.title("Comparison of Nonvoting Parties by Percentage")
    plt.legend()

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_five(cleaned_data, input_vars=None,
                       output_image_name="hypothesis_five"):
    """Creates visualization for hypothesis five"""
    ###
    comparison_groups = f.collect_sample_means_chamber(cleaned_data)
    sen_samples = ["Senate", comparison_groups[0], "r"]
    house_samples = ["House", comparison_groups[1], "b"]
    input_vars = [sen_samples, house_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel("Percentage Abstaining from Vote")
    plt.ylabel("Probability Density")
    plt.title("Comparison of Nonvoting Chambers by Percentage")
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_six(cleaned_data, input_vars=None,
                      output_image_name="hypothesis_six"):
    """Creates visualization for hypothesis six"""

    cleaned_data = cleaned_data.loc[cleaned_data.chamber == 'senate']
    comparison_groups = f.collect_sample_means_party(cleaned_data)
    rep_samples = ["Senate Republican", comparison_groups[0], "r"]
    dem_samples = ["Senate Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel("Percentage Abstaining from Vote")
    plt.ylabel("Probability Density")
    plt.title("Comparison of Nonvoting Senate Parties by Percentage")
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)


def visualization_seven(cleaned_data, input_vars=None,
                        output_image_name="hypothesis_seven"):
    """Creates visualization for hypothesis seven"""

    cleaned_data = cleaned_data.loc[cleaned_data.chamber == 'house']
    comparison_groups = f.collect_sample_means_party(cleaned_data)
    rep_samples = ["House Republican", comparison_groups[0], "r"]
    dem_samples = ["House Democratic", comparison_groups[1], "b"]
    input_vars = [rep_samples, dem_samples]
    overlapping_density(input_vars)
    ###

    # Starter code for labeling the image
    plt.xlabel("Percentage Abstaining from Vote")
    plt.ylabel("Probability Density")
    plt.title("Comparison of Nonvoting House Parties by Percentage")
    plt.legend()

    plt.savefig(f'img/{output_image_name}.png', transparent=True)
