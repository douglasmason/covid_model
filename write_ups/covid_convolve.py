from sub_units.bayes_model_implementations.convolution_model import \
    ConvolutionModel  # want to make an instance of this class for each state / set of params
from sub_units.utils import run_everything as run_everything_imported  # for plotting the report across all states
import scrap_code.load_data as load_data  # only want to load this once, so import as singleton pattern
import datetime
#####
# Set up model
#####

n_bootstraps = 100
n_likelihood_samples = 100000
opt_force_plot = False
opt_force_calc = False
override_run_states = None
# ['Kansas', 'New York', 'Alaska', 'South Dakota', 'Wyoming', 'Arkansas', 'Arizona', 'Virginia']  #['New York', 'total'] #['North Carolina', 'Michigan', 'Georgia']
# ['total', 'Virginia', 'Arkansas', 'Connecticut', 'Alaska', 'South Dakota', 'Hawaii', 'Vermont', 'Wyoming'] # None
override_max_date_str = None

####
# Make whisker plots
####
def run_everything():
    if override_max_date_str is None:
        hyperparameter_max_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        hyperparameter_max_date_str = override_max_date_str

    state_models_filename = f'state_models_smoothed_convolution_{n_bootstraps}_bootstraps_{n_likelihood_samples}_likelihood_samples_{hyperparameter_max_date_str.replace("-", "_")}_max_date.joblib'
    state_report_filename = f'state_report_smoothed_convolution_{n_bootstraps}_bootstraps_{n_likelihood_samples}_likelihood_samples_{hyperparameter_max_date_str.replace("-", "_")}_max_date.joblib'

    # fixing parameters I don't want to train for saves a lot of computer power
    static_params = {'contagious_to_positive_width': 7,
                     'contagious_to_deceased_width': 7,
                     'contagious_to_positive_mult': 0.1}
    logarithmic_params = ['I_0',
                          'contagious_to_deceased_mult',
                          'sigma_positive',
                          'sigma_deceased']
    sorted_init_condit_names = ['I_0']
    sorted_param_names = ['alpha_1',
                          'alpha_2',
                          'contagious_to_positive_delay',
                          'contagious_to_deceased_delay',
                          'contagious_to_deceased_mult',
                          'sigma_positive',
                          'sigma_deceased'
                          ]
    plot_param_names = ['alpha_1',
                        'alpha_2',
                        'contagious_to_positive_delay',
                        'positive_to_deceased_delay',
                        'positive_to_deceased_mult']

    def get_positive_to_deceased_delay(x, map_name_to_sorted_ind=None):
        return x[map_name_to_sorted_ind['contagious_to_deceased_delay']] - x[
            map_name_to_sorted_ind['contagious_to_positive_delay']]

    def get_positive_to_deceased_mult(x, map_name_to_sorted_ind=None):
        return x[map_name_to_sorted_ind['contagious_to_deceased_mult']] / 0.1

    extra_params = {
        'positive_to_deceased_delay': get_positive_to_deceased_delay,
        'positive_to_deceased_mult': get_positive_to_deceased_mult
    }

    curve_fit_bounds = {'I_0': (1e-12, 100.0),  # starting infections
                        'alpha_1': (-1, 2),
                        'alpha_2': (-1, 2),
                        'sigma_positive': (0, 100),
                        'sigma_deceased': (0, 100),
                        'contagious_to_positive_delay': (-14, 21),
                        # 'contagious_to_positive_width': (0, 14),
                        'contagious_to_deceased_delay': (-14, 42),
                        # 'contagious_to_deceased_width': (0, 14),
                        'contagious_to_deceased_mult': (1e-12, 1),
                        }

    test_params = {'I_0': 2e-3,  # starting infections
                   'alpha_1': 0.23,
                   'alpha_2': 0.01,
                   'sigma_positive': 0.01,
                   'sigma_deceased': 0.2,
                   'contagious_to_positive_delay': 9,
                   # 'contagious_to_positive_width': 7,
                   'contagious_to_deceased_delay': 15,
                   # 'contagious_to_deceased_width': 7,
                   'contagious_to_deceased_mult': 0.01,
                   }

    # uniform priors with bounds:
    priors = curve_fit_bounds

    # cycle over most populous states first
    population_ranked_state_names = sorted(load_data.map_state_to_current_case_cnt.keys(),
                                           key=lambda x: -load_data.map_state_to_current_case_cnt[x])
    run_states = population_ranked_state_names
    if override_run_states is not None:
        run_states = override_run_states

    return run_everything_imported(run_states,
                                   ConvolutionModel,
                                   max_date_str,
                                   load_data,
                                   state_models_filename=state_models_filename,
                                   state_report_filename=state_report_filename,
                                   n_bootstraps=n_bootstraps,
                                   n_likelihood_samples=n_likelihood_samples,
                                   load_data_obj=load_data,
                                   sorted_param_names=sorted_param_names,
                                   sorted_init_condit_names=sorted_init_condit_names,
                                   curve_fit_bounds=curve_fit_bounds,
                                   priors=priors,
                                   test_params=test_params,
                                   static_params=static_params,
                                   opt_force_calc=opt_force_calc,
                                   opt_force_plot=opt_force_plot,
                                   logarithmic_params=logarithmic_params,
                                   extra_params=extra_params,
                                   plot_param_names=plot_param_names,
                                   )


if __name__ == '__main__':
    run_everything()
