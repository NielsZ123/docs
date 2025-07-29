#!/usr/bin/env python3
"""
Kordiam Excel Importer
A script that reads data from an Excel file and creates elements in Kordiam via its API.
"""

import pandas as pd
import requests
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import sys
import argparse
from datetime import datetime


@dataclass
class KordiamConfig:
    """Configuration for Kordiam API connection."""
    base_url: str
    api_key: str
    headers: Dict[str, str]
    timeout: int = 30


class KordiamAPIClient:
    """Client for interacting with Kordiam API."""
    
    def __init__(self, config: KordiamConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)
        
    def create_element(self, element_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an element in Kordiam.
        
        Args:
            element_data: Dictionary containing element data
            
        Returns:
            Response from the API
        """
        try:
            # This endpoint will need to be updated based on actual Kordiam API documentation
            url = f"{self.config.base_url}/elements"
            
            response = self.session.post(
                url,
                json=element_data,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            logging.info(f"Successfully created element: {response.json().get('id', 'Unknown ID')}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create element: {e}")
            raise
    
    def get_element(self, element_id: str) -> Dict[str, Any]:
        """
        Get an element from Kordiam by ID.
        
        Args:
            element_id: ID of the element to retrieve
            
        Returns:
            Element data
        """
        try:
            url = f"{self.config.base_url}/elements/{element_id}"
            
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get element {element_id}: {e}")
            raise
    
    def update_element(self, element_id: str, element_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an element in Kordiam.
        
        Args:
            element_id: ID of the element to update
            element_data: Updated element data
            
        Returns:
            Response from the API
        """
        try:
            url = f"{self.config.base_url}/elements/{element_id}"
            
            response = self.session.put(
                url,
                json=element_data,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            logging.info(f"Successfully updated element: {element_id}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to update element {element_id}: {e}")
            raise


class ExcelProcessor:
    """Processes Excel files and transforms data for Kordiam API."""
    
    def __init__(self, excel_file: str, sheet_name: Optional[str] = None):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        
    def read_excel_data(self) -> pd.DataFrame:
        """
        Read data from Excel file.
        
        Returns:
            DataFrame containing the Excel data
        """
        try:
            if self.sheet_name:
                df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
            else:
                df = pd.read_excel(self.excel_file)
            
            logging.info(f"Successfully read {len(df)} rows from Excel file")
            return df
            
        except Exception as e:
            logging.error(f"Failed to read Excel file {self.excel_file}: {e}")
            raise
    
    def transform_row_to_element(self, row: pd.Series, column_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Transform a DataFrame row to Kordiam element format.
        
        Args:
            row: Pandas Series representing a row
            column_mapping: Mapping from Excel columns to Kordiam fields
            
        Returns:
            Dictionary formatted for Kordiam API
        """
        element_data = {}
        
        for excel_col, kordiam_field in column_mapping.items():
            if excel_col in row.index and pd.notna(row[excel_col]):
                value = row[excel_col]
                
                # Handle different data types
                if isinstance(value, pd.Timestamp):
                    value = value.isoformat()
                elif isinstance(value, (int, float)) and pd.isna(value):
                    continue
                
                element_data[kordiam_field] = value
        
        return element_data


class KordiamImporter:
    """Main importer class that orchestrates the Excel to Kordiam import process."""
    
    def __init__(self, config: KordiamConfig):
        self.client = KordiamAPIClient(config)
        self.results = {
            'success': 0,
            'errors': 0,
            'details': []
        }
    
    def import_from_excel(self, 
                         excel_file: str, 
                         column_mapping: Dict[str, str],
                         sheet_name: Optional[str] = None,
                         dry_run: bool = False) -> Dict[str, Any]:
        """
        Import data from Excel file to Kordiam.
        
        Args:
            excel_file: Path to Excel file
            column_mapping: Mapping from Excel columns to Kordiam fields
            sheet_name: Specific sheet to read (optional)
            dry_run: If True, don't actually create elements
            
        Returns:
            Import results summary
        """
        processor = ExcelProcessor(excel_file, sheet_name)
        df = processor.read_excel_data()
        
        logging.info(f"Starting import of {len(df)} rows (dry_run={dry_run})")
        
        for index, row in df.iterrows():
            try:
                element_data = processor.transform_row_to_element(row, column_mapping)
                
                if not element_data:
                    logging.warning(f"Row {index + 1}: No valid data found, skipping")
                    continue
                
                if dry_run:
                    logging.info(f"Row {index + 1}: Would create element with data: {element_data}")
                    self.results['success'] += 1
                else:
                    response = self.client.create_element(element_data)
                    self.results['success'] += 1
                    self.results['details'].append({
                        'row': index + 1,
                        'status': 'success',
                        'element_id': response.get('id'),
                        'data': element_data
                    })
                
            except Exception as e:
                self.results['errors'] += 1
                error_detail = {
                    'row': index + 1,
                    'status': 'error',
                    'error': str(e),
                    'data': element_data if 'element_data' in locals() else None
                }
                self.results['details'].append(error_detail)
                logging.error(f"Row {index + 1}: {e}")
        
        return self.results


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'kordiam_import_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_config(config_file: str) -> KordiamConfig:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return KordiamConfig(
            base_url=config_data['base_url'],
            api_key=config_data['api_key'],
            headers=config_data.get('headers', {
                'Authorization': f"Bearer {config_data['api_key']}",
                'Content-Type': 'application/json'
            }),
            timeout=config_data.get('timeout', 30)
        )
    except Exception as e:
        logging.error(f"Failed to load config file {config_file}: {e}")
        raise


def main():
    """Main function to run the importer."""
    parser = argparse.ArgumentParser(description='Import Excel data to Kordiam')
    parser.add_argument('excel_file', help='Path to Excel file')
    parser.add_argument('--config', default='config.json', help='Path to config file')
    parser.add_argument('--mapping', default='column_mapping.json', help='Path to column mapping file')
    parser.add_argument('--sheet', help='Excel sheet name (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Test run without creating elements')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Load column mapping
        with open(args.mapping, 'r') as f:
            column_mapping = json.load(f)
        
        # Create importer and run
        importer = KordiamImporter(config)
        results = importer.import_from_excel(
            args.excel_file,
            column_mapping,
            args.sheet,
            args.dry_run
        )
        
        # Print results
        print(f"\nImport completed:")
        print(f"Success: {results['success']}")
        print(f"Errors: {results['errors']}")
        
        if results['errors'] > 0:
            print("\nErrors occurred. Check the log file for details.")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Import failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()