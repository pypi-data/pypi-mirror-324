import yaml
import os
import logging

def save_to_yaml(selected_actives, selected_contaminants, nonselected_actives, nonselected_contaminants, random_seed, output_file):
    """Save the results to a YAML file with full absolute paths and random seed information."""
    logging.info(f"Saving results to {output_file}")
    data = {
        'selected_actives': selected_actives,
        'selected_contaminants': selected_contaminants,
        'nonselected_actives': nonselected_actives,
        'nonselected_contaminants': nonselected_contaminants,
        'random_seed': random_seed,  # Include the seed for reproducibility
    }
    
    try:
        with open(output_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        logging.info(f"Results successfully saved to {output_file}")
    except Exception as e:
        logging.error(f"Error while saving YAML: {e}")
        raise

def load_from_yaml(yaml_file):
    """Load the data from a YAML file and return it as Python lists."""
    if not os.path.exists(yaml_file):
        logging.error(f"YAML file not found: {yaml_file}")
        raise FileNotFoundError(f"YAML file not found: {yaml_file}")
    
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        required_keys = [
            'selected_actives',
            'selected_contaminants',
            'nonselected_actives',
            'nonselected_contaminants'
        ]
        
        for key in required_keys:
            if key not in data:
                logging.error(f"Missing expected key: {key}")
                raise ValueError(f"Missing expected key: {key}")
            if not isinstance(data[key], list):
                logging.error(f"Expected list for {key}, got {type(data[key])}")
                raise ValueError(f"Expected list for {key}, got {type(data[key])}")
        
        selected_actives = data.get('selected_actives', [])
        selected_contaminants = data.get('selected_contaminants', [])
        nonselected_actives = data.get('nonselected_actives', [])
        nonselected_contaminants = data.get('nonselected_contaminants', [])
        
        logging.info("YAML file loaded successfully.")
        return selected_actives, selected_contaminants, nonselected_actives, nonselected_contaminants
    
    except yaml.YAMLError as e:
        logging.error(f"Error reading YAML file: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading the YAML: {e}")
        raise
