#!/usr/bin/env python3
"""
Kordiam Excel Importer
A script that reads data from an Excel file and creates elements in Kordiam via its API.
"""

import pandas as pd
import requests
import json
import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import sys
import argparse
from datetime import datetime, timedelta


@dataclass
class KordiamConfig:
    """Configuration for Kordiam API connection."""
    base_url: str
    client_id: str
    client_secret: str
    token_endpoint: str = "/api/token"
    timeout: int = 30


class KordiamAPIClient:
    """Client for interacting with Kordiam API with OAuth2 authentication."""
    
    def __init__(self, config: KordiamConfig):
        self.config = config
        self.session = requests.Session()
        self.access_token = None
        self.token_expires_at = None
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _get_access_token(self) -> str:
        """
        Get OAuth2 access token using client credentials flow.
        
        Returns:
            Access token string
        """
        # Check if we have a valid token
        if (self.access_token and self.token_expires_at and 
            datetime.now() < self.token_expires_at):
            return self.access_token
        
        try:
            token_url = f"{self.config.base_url}{self.config.token_endpoint}"
            
            # Prepare OAuth2 client credentials request
            token_data = {
                'grant_type': 'client_credentials',
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret
            }
            
            # Use form data for token request
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(
                token_url,
                data=token_data,
                headers=headers,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            token_response = response.json()
            self.access_token = token_response['access_token']
            
            # Calculate token expiration (with 5 minute buffer)
            expires_in = token_response.get('expires_in', 3600)  # Default 1 hour
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            logging.info("Successfully obtained OAuth2 access token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to obtain access token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Token response status: {e.response.status_code}")
                logging.error(f"Token response body: {e.response.text}")
            raise
        except KeyError as e:
            logging.error(f"Invalid token response format: {e}")
            raise
    
    def _make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an authenticated request to the Kordiam API.
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            url: API endpoint URL
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        # Get valid access token
        access_token = self._get_access_token()
        
        # Add authorization header
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {access_token}'
        kwargs['headers'] = headers
        
        # Make the request
        response = self.session.request(method, url, timeout=self.config.timeout, **kwargs)
        return response
        
    def create_element(self, element_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an element in Kordiam using the actual API endpoint.
        
        Args:
            element_data: Dictionary containing element data in Kordiam format
            
        Returns:
            Response from the API
        """
        try:
            # Use the actual Kordiam API endpoint
            url = f"{self.config.base_url}/api/v1_0_1/elements/"
            
            response = self._make_authenticated_request(
                'POST',
                url,
                json=element_data
            )
            response.raise_for_status()
            
            logging.info(f"Successfully created element: {response.json().get('id', 'Unknown ID')}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create element: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status: {e.response.status_code}")
                logging.error(f"Response body: {e.response.text}")
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
            url = f"{self.config.base_url}/api/v1_0_1/elements/{element_id}/"
            
            response = self._make_authenticated_request('GET', url)
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
            url = f"{self.config.base_url}/api/v1_0_1/elements/{element_id}/"
            
            response = self._make_authenticated_request(
                'PUT',
                url,
                json=element_data
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
    
    def transform_row_to_element(self, row: pd.Series, mapping_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a DataFrame row to Kordiam element format.
        
        Args:
            row: Pandas Series representing a row
            mapping_config: Complete mapping configuration including element fields and sub-structures
            
        Returns:
            Dictionary formatted for Kordiam API
        """
        element_data = {}
        
        # Basic element fields
        basic_fields = mapping_config.get('element_fields', {})
        for excel_col, kordiam_field in basic_fields.items():
            if excel_col in row.index and pd.notna(row[excel_col]):
                value = row[excel_col]
                
                # Handle different data types
                if isinstance(value, pd.Timestamp):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(value, (int, float)) and pd.isna(value):
                    continue
                
                element_data[kordiam_field] = value
        
        # Handle tasks if configured
        task_config = mapping_config.get('tasks', {})
        if task_config and any(col in row.index and pd.notna(row[col]) for col in task_config.keys()):
            task = {}
            
            for excel_col, task_field in task_config.items():
                if excel_col in row.index and pd.notna(row[excel_col]):
                    value = row[excel_col]
                    
                    # Handle special task fields
                    if task_field == 'deadline' and isinstance(value, pd.Timestamp):
                        task['deadline'] = {
                            'date': value.strftime('%Y-%m-%d'),
                            'time': value.strftime('%H:%M') if not pd.isna(value) else None
                        }
                    elif task_field in ['status', 'format', 'user'] and isinstance(value, (int, float)):
                        task[task_field] = int(value)
                    elif task_field == 'confirmationStatus':
                        # Default to "Not requested" (-2) if not specified
                        task[task_field] = int(value) if pd.notna(value) else -2
                    else:
                        task[task_field] = value
            
            # Ensure required task fields have defaults
            if 'confirmationStatus' not in task:
                task['confirmationStatus'] = -2  # Not requested
            
            if task:  # Only add if we have task data
                element_data['tasks'] = [task]
        
        # Handle publications if configured
        publication_config = mapping_config.get('publications', {})
        if publication_config and any(col in row.index and pd.notna(row[col]) for col in publication_config.keys()):
            publication = {}
            
            for excel_col, pub_field in publication_config.items():
                if excel_col in row.index and pd.notna(row[excel_col]):
                    value = row[excel_col]
                    
                    # Handle special publication fields
                    if pub_field == 'single' and isinstance(value, pd.Timestamp):
                        publication['single'] = {
                            'start': {
                                'date': value.strftime('%Y-%m-%d'),
                                'time': value.strftime('%H:%M') if not pd.isna(value) else None
                            }
                        }
                    elif pub_field in ['status', 'platform', 'category', 'type'] and isinstance(value, (int, float)):
                        publication[pub_field] = int(value)
                    elif pub_field == 'assignments':
                        # Handle assignments as boolean array
                        if isinstance(value, str):
                            # Convert string like "true,false" to [true, false]
                            assignments = [s.strip().lower() == 'true' for s in value.split(',')]
                            publication[pub_field] = assignments
                        else:
                            publication[pub_field] = [True]  # Default
                    else:
                        publication[pub_field] = value
            
            # Set default assignments if not provided
            if 'assignments' not in publication and 'tasks' in element_data:
                publication['assignments'] = [True] * len(element_data['tasks'])
            
            if publication:  # Only add if we have publication data
                element_data['publications'] = [publication]
        
        # Handle groups if configured
        groups_config = mapping_config.get('groups', {})
        if groups_config:
            for excel_col, group_field in groups_config.items():
                if excel_col in row.index and pd.notna(row[excel_col]):
                    value = row[excel_col]
                    if isinstance(value, (int, float)):
                        element_data['groups'] = [{'id': int(value)}]
                    elif isinstance(value, str):
                        # Handle comma-separated group IDs
                        group_ids = [{'id': int(g.strip())} for g in value.split(',') if g.strip().isdigit()]
                        if group_ids:
                            element_data['groups'] = group_ids
        
        # Handle location if configured
        location_config = mapping_config.get('location', {})
        if location_config and any(col in row.index and pd.notna(row[col]) for col in location_config.keys()):
            location = {}
            
            for excel_col, loc_field in location_config.items():
                if excel_col in row.index and pd.notna(row[excel_col]):
                    location[loc_field] = str(row[excel_col])
            
            if location:
                element_data['location'] = location
        
        # Handle event if configured
        event_config = mapping_config.get('event', {})
        if event_config and any(col in row.index and pd.notna(row[col]) for col in event_config.keys()):
            event = {}
            
            for excel_col, event_field in event_config.items():
                if excel_col in row.index and pd.notna(row[excel_col]):
                    value = row[excel_col]
                    
                    if event_field in ['fromDate', 'toDate'] and isinstance(value, pd.Timestamp):
                        event[event_field] = value.strftime('%Y-%m-%d')
                    elif event_field in ['fromTime', 'toTime'] and isinstance(value, pd.Timestamp):
                        event[event_field] = value.strftime('%H:%M')
                    else:
                        event[event_field] = str(value)
            
            if event:
                element_data['event'] = event
        
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
                         mapping_config: Dict[str, Any],
                         sheet_name: Optional[str] = None,
                         dry_run: bool = False) -> Dict[str, Any]:
        """
        Import data from Excel file to Kordiam.
        
        Args:
            excel_file: Path to Excel file
            mapping_config: Complete mapping configuration
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
                element_data = processor.transform_row_to_element(row, mapping_config)
                
                if not element_data:
                    logging.warning(f"Row {index + 1}: No valid data found, skipping")
                    continue
                
                # Validate that element has required components
                has_publication = 'publications' in element_data and element_data['publications']
                has_task = 'tasks' in element_data and element_data['tasks']
                has_group = 'groups' in element_data and element_data['groups']
                
                if not (has_publication or has_task or has_group):
                    logging.warning(f"Row {index + 1}: Element must contain at least one of: publication, task, or group. Skipping.")
                    continue
                
                if dry_run:
                    logging.info(f"Row {index + 1}: Would create element with data: {json.dumps(element_data, indent=2)}")
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


def load_config_with_args(args) -> KordiamConfig:
    """Load configuration with command line argument support."""
    try:
        # First priority: Command line arguments
        if args.client_id and args.client_secret:
            logging.info("Using OAuth2 credentials from command line arguments")
            return KordiamConfig(
                base_url=args.base_url,
                client_id=args.client_id,
                client_secret=args.client_secret,
                token_endpoint='/api/token',
                timeout=30
            )
        
        # Second priority: Environment variables
        client_id = os.getenv('KORDIAM_CLIENT_ID')
        client_secret = os.getenv('KORDIAM_CLIENT_SECRET')
        
        if client_id and client_secret:
            logging.info("Using OAuth2 credentials from environment variables")
            return KordiamConfig(
                base_url=os.getenv('KORDIAM_BASE_URL', args.base_url),
                client_id=client_id,
                client_secret=client_secret,
                token_endpoint=os.getenv('KORDIAM_TOKEN_ENDPOINT', '/api/token'),
                timeout=int(os.getenv('KORDIAM_TIMEOUT', '30'))
            )
        
        # Third priority: Config file
        return load_config(args.config)
        
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        logging.error("\nTo provide OAuth2 credentials, use one of these methods:")
        logging.error("1. Command line: --client-id YOUR_ID --client-secret YOUR_SECRET")
        logging.error("2. Environment variables: export KORDIAM_CLIENT_ID=your_id KORDIAM_CLIENT_SECRET=your_secret")
        logging.error("3. Config file: Update config.json with your credentials")
        raise

def load_config(config_file: str) -> KordiamConfig:
    """Load configuration from JSON file or environment variables."""
    try:
        # Try to load from environment variables first (more secure)
        client_id = os.getenv('KORDIAM_CLIENT_ID')
        client_secret = os.getenv('KORDIAM_CLIENT_SECRET')
        base_url = os.getenv('KORDIAM_BASE_URL', 'https://kordiam.app')
        
        if client_id and client_secret:
            logging.info("Using OAuth2 credentials from environment variables")
            return KordiamConfig(
                base_url=base_url,
                client_id=client_id,
                client_secret=client_secret,
                token_endpoint=os.getenv('KORDIAM_TOKEN_ENDPOINT', '/api/token'),
                timeout=int(os.getenv('KORDIAM_TIMEOUT', '30'))
            )
        
        # Fall back to config file if environment variables not set
        if os.path.exists(config_file):
            logging.info(f"Loading configuration from {config_file}")
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            return KordiamConfig(
                base_url=config_data['base_url'],
                client_id=config_data['client_id'],
                client_secret=config_data['client_secret'],
                token_endpoint=config_data.get('token_endpoint', '/api/token'),
                timeout=config_data.get('timeout', 30)
            )
        else:
            raise FileNotFoundError(f"Config file {config_file} not found and no environment variables set")
            
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        logging.error("\nTo provide credentials, either:")
        logging.error("1. Set environment variables: KORDIAM_CLIENT_ID and KORDIAM_CLIENT_SECRET")
        logging.error("2. Create config.json with your credentials")
        logging.error("3. Use --client-id and --client-secret command line options")
        raise


def main():
    """Main function to run the importer."""
    parser = argparse.ArgumentParser(description='Import Excel data to Kordiam')
    parser.add_argument('excel_file', help='Path to Excel file')
    parser.add_argument('--config', default='config.json', help='Path to config file')
    parser.add_argument('--mapping', default='kordiam_mapping.json', help='Path to Kordiam mapping file')
    parser.add_argument('--sheet', help='Excel sheet name (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Test run without creating elements')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    
    # OAuth2 credential options
    parser.add_argument('--client-id', help='Kordiam OAuth2 client ID')
    parser.add_argument('--client-secret', help='Kordiam OAuth2 client secret')
    parser.add_argument('--base-url', default='https://kordiam.app', help='Kordiam base URL')
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    try:
        # Load configuration with command line override support
        config = load_config_with_args(args)
        
        # Load mapping configuration
        with open(args.mapping, 'r') as f:
            mapping_config = json.load(f)
        
        # Create importer and run
        importer = KordiamImporter(config)
        results = importer.import_from_excel(
            args.excel_file,
            mapping_config,
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