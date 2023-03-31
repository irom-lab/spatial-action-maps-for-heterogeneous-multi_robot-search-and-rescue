from itertools import product
from pathlib import Path
import utils

robot_config_list = [[{'rescue_robot': 1}, {'exploring_robot': 1}], [{'rescue_robot': 1}, {'uav_robot': 1}], [{'rescue_robot': 1}], [{'rescue_robot': 2}]]
environment_list = ['large_rooms', 'large_empty']
cubes_list = [1]
map_combination_list = ['all', 'all_but_sim', 'all_but_sptrrm', 'all_but_vfm', 'all_but_sim_sptrrm_vfm', 'all_but_clm', 'all_but_sptcm', 'all_but_clm_sptcm']
config_params_list = list(product(robot_config_list, environment_list, cubes_list, map_combination_list))

def generate_experiments(template_path, output_dir):
    i = 0

    # Ensure output dir exists
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Read template config
    cfg = utils.load_config(Path(template_path))

    for config_params in config_params_list:

        # Generate experiment name
        robot_config_name = ''
        for robot_type in config_params[0]:
            for key, value in robot_type.items():
                robot_config_name += key[:key.find('robot')] + str(value) + '_'
        experiment_name = '{}-{}-cubes_{}-{}'.format(robot_config_name[:-1], config_params[1], config_params[2], config_params[3])
        print(experiment_name, i)
        i += 1

        # Apply modifications

        cfg.experiment_name = experiment_name

        cfg.robot_config = config_params[0]
        cfg.discount_factors = [0.35] * len(config_params[0])

        cfg.env_name = config_params[1]

        cfg.num_cubes = config_params[2]
        
        cfg.use_intention_map = config_params[3].find('sim') == -1
        cfg.use_shortest_path_to_rescue_robot_map = config_params[3].find('sptrrm') == -1
        cfg.use_visit_frequency_map = config_params[3].find('vfm') == -1
        cfg.visit_frequncy_map_scale = 0.25
        cfg.use_cube_location_map = config_params[3].find('clm') == -1
        cfg.cube_location_map_scale = 0.25
        cfg.use_shortest_path_to_cube_map = config_params[3].find('sptcm') == -1
        cfg.num_input_channels = 3 + int(cfg.use_intention_map) + int(cfg.use_shortest_path_to_rescue_robot_map) + int(cfg.use_visit_frequency_map) + int(cfg.use_cube_location_map) + int(cfg.use_shortest_path_to_cube_map)

        # Save new config
        utils.save_config(output_dir / '{}.yml'.format(experiment_name), cfg)

generate_experiments('config/experiments/daphne_final/daphne_template.yml', 'config/experiments/daphne_final')