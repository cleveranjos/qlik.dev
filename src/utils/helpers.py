"""
Utility functions for handling Qlik API responses and data manipulation.

This module provides helper functions for working with Qlik Cloud API responses,
including functions for:
- Table formatting and display
- Nested data structure navigation
- API pagination handling
- URL manipulation
- Data transformation and flattening

Typical usage example:
    >>> from utils.helpers import print_table, iterate_over_next
    >>> results = []
    >>> for page in iterate_over_next(client, '/users', ['id', 'name']):
    ...     results.extend(page)
    >>> print_table(results)
"""

from urllib.parse import urlparse
from tabulate import tabulate
from json import loads, JSONDecodeError
from typing import List, Dict, Optional, Any, Iterator, Union
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
    print(tabulate(data, headers="keys", tablefmt="simple", showindex=True))


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


def iterate_over_next(
    q: Qlik,
    initial_path: str,
    columns: Optional[List[str]] = None
) -> Iterator[Optional[List[Dict[str, Any]]]]:
    """
    Iterate through paginated API responses, transforming and yielding data from each page.

    This function handles Qlik Cloud's pagination mechanism by following the 'next' links
    in the API response. It automatically transforms the response data using the plainify
    function to flatten nested structures and extract specified columns.

    Args:
        q: Qlik API client instance used for making REST calls.
        initial_path: The initial API endpoint path to fetch data from.
            Should not include the '/v1' prefix as it's handled automatically.
        columns: Optional list of columns to include in the output.
            If None, all available columns are included.
            Supports dot notation for nested fields (e.g., 'user.profile.name').

    Yields:
        List[Dict[str, Any]]: Transformed data from each page, with specified columns.
        None: If there's an error in fetching or processing the data.

    Example:
        >>> # Fetch all users but only include id and name
        >>> results = []
        >>> for page in iterate_over_next(client, '/users', ['id', 'name']):
        ...     if page:
        ...         results.extend(page)
        ...     else:
        ...         print("Error fetching page")

    Note:
        The function automatically handles the pagination logic by following
        the 'next' links in the API response. It will stop when there are
        no more pages or if an error occurs.
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
            if isinstance(data, list):
                yield plainify(data, columns)

            next_link = data.get('links', {}).get('next', {}).get('href', '')
            path = return_relative_url(next_link) if next_link else None

        except (JSONDecodeError, Exception) as e:
            yield None
            break


def plainify(
    data: List[Dict[str, Any]],
    columns: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Transform a list of dictionaries by extracting specified columns and flattening nested structures.

    This function is particularly useful for processing Qlik API responses where you want to:
    1. Extract specific fields from complex nested structures
    2. Flatten nested objects into dot-notation fields
    3. Filter out unnecessary data
    4. Create a consistent table structure

    Args:
        data: List of dictionaries to transform. Each dictionary represents a row
            of data that may contain nested structures.
        columns: Optional list of column keys to include in the output.
            If None, all keys from the first row are used.
            Supports dot notation for accessing nested fields (e.g., 'user.profile.name').

    Returns:
        List[Dict[str, Any]]: Transformed list of dictionaries where:
            - Only specified columns are included
            - Nested structures are flattened using dot notation
            - Missing values are replaced with None

    Example:
        >>> # Complex nested data
        >>> data = [{
        ...     'user': {'profile': {'name': 'John', 'age': 25}},
        ...     'status': 'active'
        ... }]
        >>> # Extract specific fields using dot notation
        >>> plainify(data, ['user.profile.name', 'status'])
        [{'user.profile.name': 'John', 'status': 'active'}]

    Note:
        The function preserves the order of columns as specified in the columns parameter.
        If a column path doesn't exist in a row, the value will be None.
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
