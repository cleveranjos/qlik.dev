"""
Utility functions for handling Qlik API responses and data manipulation.
This module provides helper functions for working with nested data structures,
table formatting, and API pagination.
"""

from urllib.parse import urlparse
from tabulate import tabulate
from json import loads, JSONDecodeError
from typing import List, Dict, Optional, Any,  Iterator
from qlik_sdk import Qlik 

def print_table(data: Dict[str, Any]) -> None:
    """
    Print a dictionary as a formatted table using tabulate.
    
    Args:
        data: Dictionary containing the data to be displayed in table format.
            Each key becomes a column header, and the values form the rows.
    
    Example:
        >>> data = {'Name': ['John', 'Jane'], 'Age': [25, 30]}
        >>> print_table(data)
    """
    print(tabulate(data, headers="keys", showindex=True))


def get_nested_value(obj: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Safely retrieves a value from a nested object using a dot-separated key path.
    
    Args:
        obj: The dictionary to search through.
        key_path: A string of keys separated by dots (e.g., 'user.profile.name').
        default: The value to return if the path is not found.
    
    Returns:
        The value at the specified path if it exists, otherwise the default value.
    
    Example:
        >>> data = {'user': {'profile': {'name': 'John'}}}
        >>> get_nested_value(data, 'user.profile.name')
        'John'
        >>> get_nested_value(data, 'user.settings', 'not found')
        'not found'
    """
    keys = key_path.split('.')
    current_value = obj
    for key in keys:
        if isinstance(current_value, dict) and key in current_value:
            current_value = current_value[key]
        else:
            return default  # Path not found
    return current_value


def return_relative_url(url: str) -> str:
    """
    Extract the relative path after '/v1/' from a URL.
    
    Args:
        url: The full URL string containing '/v1/' path segment.
    
    Returns:
        The portion of the URL path after '/v1/', or empty string if not found.
    
    Example:
        >>> return_relative_url('https://customer.us.qlikcloud.com/api/v1/resources')
        'resources'
    """
    (_, _, path) = url.partition('/v1')
    return path


def iterate_over_next(q: Qlik, initial_path: str, columns: Optional[List[str]] = None) -> Iterator[Optional[List[Dict[str, Any]]]]:
    """
    Iterate through paginated API responses, transforming and yielding data from each page.
    
    Args:
        q: Qlik API client instance used for making REST calls.
        initial_path: The initial API endpoint path to fetch data from.
        columns: Optional list of columns to include in the output. It dumps all columns if None.
    
    Yields:
        Transformed data from each page, or None if there's an error.
        The data is transformed using the plainify function if it contains a 'data' field.
    
    Example:
        >>> for page in iterate_over_next(client, '/api/items', ['id', 'name']):
        ...     if page:
        ...         process_items(page)
    """
    path = initial_path
    while path:
        try:
            response = q.rest(path=path)
            content = response.text
            if not isinstance(content, str):
                yield None
                break
                
            data = loads(content)
            if isinstance(data, dict) and 'data' in data:
                yield plainify(data['data'], columns)
            
            next_link = data.get('links', {}).get('next', {}).get('href','')
            path = return_relative_url(next_link) if next_link else None
            
        except (JSONDecodeError, Exception) as e:
            yield None
            break


def plainify(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Transform a list of dictionaries by extracting specified columns and flattening nested structures.
    
    Args:
        data: List of dictionaries to transform.
        columns: Optional list of column keys to include in the output.
            If None, all keys from the first row are used.
    
    Returns:
        List of transformed dictionaries containing only the specified columns.
        Nested values are accessed using dot notation in the column names.
    
    Example:
        >>> data = [{'user': {'name': 'John'}, 'age': 25}]
        >>> plainify(data, ['user.name', 'age'])
        [{'user.name': 'John', 'age': 25}]
    """
    if not data:
        return []
        
    if columns is None:
        columns = list(data[0].keys())
        
    return [
        {col: get_nested_value(row, col) if '.' in col else row.get(col) 
         for col in columns}
        for row in data
    ]
