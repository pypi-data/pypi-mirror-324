import os
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any

import pandas as pd
import joblib

def load_data(data_path: Optional[str]) -> Optional[Union[pd.DataFrame, Dict[str, Any]]]:
    """Load data from specified path. Supports CSV and JSON formats.
    
    Args:
        data_path: Path to the data file. If None, returns None.
        
    Returns:
        DataFrame for CSV files, dict for JSON files, or None if path is None
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file format is not supported
    """
    if data_path is None:
        return None
        
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")
        
    if data_path.endswith('.csv'):
        return pd.read_csv(data_path)
    elif data_path.endswith('.json'):
        with open(data_path, 'r') as f:
            return json.load(f)
    else:
        return data_path

def load_model(model_path: str) -> Any:
    """Load a saved model from a file.
    
    Args:
        model_path: Path to the model directory containing model.joblib
        
    Returns:
        Loaded model object
        
    Raises:
        FileNotFoundError: If model files are not found
        ValueError: If model files are corrupted
    """
    model_dir = Path(model_path)
    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {model_path}")
        
    model_file = model_dir / "model.joblib"
    
    if not model_file.exists():
        raise FileNotFoundError(f"Model files missing in: {model_path}")
        
    try:
        return joblib.load(model_file)
    except Exception as e:
        raise ValueError(f"Error loading model file: {str(e)}")
