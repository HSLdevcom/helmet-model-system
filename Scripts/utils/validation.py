from __future__ import annotations
from pathlib import Path
from typing import Dict, List, NamedTuple

import pandas as pd
from typing import Callable, Optional, Union

class ValidationAggregator(NamedTuple):
    name: str
    aggregation: Callable[[pd.DataFrame], float]
    filter: Optional[str] = None
    group_by: Optional[Union[str, List[str]]] = None

class ValidationGroup:
    items: pd.DataFrame
    aggregations: List[ValidationAggregator]
    
    def __init__(self):
        """
        Initializes the Validation class.
        """
        self.items = pd.DataFrame()
        self.aggregations = []
    
    def add_item(self, observation: float, expected: float, weight: float=1.0, **metadata):
        """
        Adds an item to the collection with the given observation, expected value, weight, and additional metadata.

        Args:
            observation (float): The observed value.
            expected (float): The expected value.
            weight (float, optional): The weight of the observation. Defaults to 1.0.
            **metadata: Additional metadata to be included with the item.

        Returns:
            None
        """
        item = pd.DataFrame([{
            "observation": observation,
            "expected": expected,
            "weight": weight,
            **metadata
        }])
        self.items = pd.concat([self.items, item], ignore_index=True)
 
    def _run_aggregation(self, aggregator: ValidationAggregator) -> Dict[str, float]:
        filtered_items = self.items.query(aggregator.filter) if aggregator.filter is not None else self.items
        results: Dict[str, float] = {}
        if aggregator.group_by:
            grouped = filtered_items.groupby(aggregator.group_by)
            for grp_name, grp in grouped:
                if isinstance(aggregator.group_by, list):
                    grp_name_str = '_'.join(map(str, grp_name))
                else:
                    grp_name_str = str(grp_name)
                results[f"{aggregator.name}_{grp_name_str}"] = aggregator.aggregation(grp)
        else:
            results = {aggregator.name: aggregator.aggregation(filtered_items)}
        return results

    def add_aggregation(self,
                        name: str,
                        aggregation: Callable[[pd.DataFrame], float],
                        filter: Optional[str]=None,
                        group_by: Optional[Union[str, List[str]]]=None) -> None:
        """
        Adds an aggregation function to the list of aggregations.

        Args:
            name (str): The name of the aggregation.
            aggregation (Callable[[pd.DataFrame], float]): A function that takes a pandas DataFrame and returns a float.
            filter (Optional[str]): An optional filter to apply before aggregation. Defaults to None.
            group_by (Optional[Union[str, List[str]]]): An optional column or list of columns to group by before aggregation. Defaults to None.

        Returns:
            None
        """
        self.aggregations.append(ValidationAggregator(name, aggregation, filter, group_by))

    def run_all_aggregations(self) -> Dict[str, float]:
        """
        Executes all aggregation functions stored in the `aggregations` attribute and combines their results.

        Returns:
            Dict[str, float]: A dictionary containing the combined results of all aggregation functions.
        """
        all_results = {}
        for aggregator in self.aggregations:
            results = self._run_aggregation(aggregator)
            all_results.update(results)
        return all_results

class Validation:
    groups: Dict[str, ValidationGroup]
    
    def __init__(self):
        """
        Initializes a new instance of the class.
        """
        self.groups = {}
    
    def create_group(self, name: str):
        """
        Create or retrieve a validation group by name.

        If a group with the given name already exists, it returns the existing group.
        Otherwise, it creates a new ValidationGroup, stores it in the groups dictionary,
        and returns the new group.

        Args:
            name (str): The name of the validation group.

        Returns:
            ValidationGroup: The existing or newly created validation group.
        """
        if name in self.groups:
            return self.groups[name]
        group = ValidationGroup()
        self.groups[name] = group
        return group

    def run_all_aggregations(self) -> Dict[str, Dict[str, float]]:
        """
        Executes the run_all_aggregations method for each group in self.groups and 
        collects the results in a dictionary.

        Returns:
            Dict[str, float]: A dictionary where the keys are group names and the 
                values are the results of the run_all_aggregations method for each group.
        """
        all_results = {}
        for group_name, group in self.groups.items():
            all_results[group_name] = group.run_all_aggregations()
        return all_results

    def run_all_aggregations_to_html(self, file_path: Path):
        """
        Runs all aggregations and writes the results to an HTML file.
        This method executes all aggregation functions, collects their results,
        and formats them into an HTML document. The HTML document includes a 
        title, a header, and a table for each validation group, displaying 
        metrics and their corresponding values.

        Args:
            file_path (Path): The file path where the HTML document will be saved.

        Returns:
            None
        """
        all_results = self.run_all_aggregations()
        html_content = "<html><head><title>Validation Results</title></head><body>"
        html_content += "<h1>Validation Results</h1>"
        for group_name, results in all_results.items():
            html_content += f"<h2>Validation group: {group_name}</h2><table border='0'><tr><th>Metric</th><th>Value</th></tr>"
            for metric_name, value in results.items():
                html_content += f"<tr><td>{metric_name}</td><td>{value}</td></tr>"
            html_content += "</table>"
        html_content += "</body></html>"
        
        with open(file_path, 'w') as file:
            file.write(html_content)

# Predefined aggregation functions
def mse(df: pd.DataFrame) -> float:
    return ((df["observation"] - df["expected"]) ** 2 * df['weight']).mean()
def mae(df: pd.DataFrame) -> float:
    return ((df["observation"] - df["expected"]) * df['weight']).abs().mean()
def max_error(df: pd.DataFrame) -> float:
    return ((df["observation"] - df["expected"]) * df['weight']).abs().max()
def mean_error(df: pd.DataFrame) -> float:
    return ((df["observation"] - df["expected"]) * df['weight']).mean()

# # Usage example
# test_valid = Validation()

# # Create a group
# group = test_valid.create_group("test")

# # Add sample items to the group
# group.add_item(1, 1,   test1='a'  , te=1)
# group.add_item(2, 2.5, test1='a'  , te=2)
# group.add_item(3, 4,   test1='b')
# group.add_item(4, 6,   test1='c'  , te=2)
# group.add_item(5, 7,   test1='b'  , te=1)

# # Add aggregations to the group
# group.add_aggregation("max_error", max_error)
# group.add_aggregation("mse_error", mse, filter='observation>=3', group_by='test1')
# group.add_aggregation('mae', mae)
# group.add_aggregation('max', max_error, group_by='te')

# # Run all aggregations and print the results
# test_valid.run_all_aggregations_to_html('test.html')