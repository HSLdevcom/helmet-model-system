from __future__ import annotations
from pathlib import Path
from typing import Dict, List, NamedTuple

import pandas as pd
from typing import Callable, Optional, Union
import random
import pickle
import gzip

class ValidationAggregator(NamedTuple):
    name: str
    aggregation: Callable[[pd.DataFrame], float]
    filter: Optional[str] = None
    group_by: Optional[Union[str, List[str]]] = None

class ValidationGroup:
    _items: pd.DataFrame
    _aggregations: List[ValidationAggregator]
    _error_terms: Dict[str, Callable[[pd.DataFrame], pd.Series]]
    _errors_ok: bool
    _visualizations: Dict[str, Callable[[pd.DataFrame], str]]
    
    def __init__(self):
        """
        Initializes the Validation class.
        """
        self._items = pd.DataFrame()
        self._aggregations = []
        self._error_terms = {}
        self._visualizations = {}
        self._errors_ok = False
    
    def __getstate__(self):
        """
        Prepares the state for pickling by excluding error terms and aggregations.
        """
        state = self.__dict__.copy()
        state['_aggregations'] = []
        state['_error_terms'] = {}
        state['_visualizations'] = {}
        # Remove columns corresponding to error terms from the items DataFrame
        state['_items'] = state['_items'].drop(columns=self._error_terms.keys(), errors='ignore')
        return state

    def __setstate__(self, state):
        """
        Restores the state from the unpickled data.
        """
        self.__dict__.update(state)
        self._aggregations = []
        self._error_terms = {}
        self._visualizations = {}
    
    def add_item(self, id: str, prediction: float, expected: float, weight: float=1.0, **metadata):
        """
        Adds an item to the collection with the given prediction, 
        expected value, weight, and additional metadata.

        Args:
            id (str): The identifier of the item.
            prediction (float): The predicted value.
            expected (float): The expected value.
            weight (float, optional): The weight of the prediction. Defaults to 1.0.
            **metadata: Additional metadata to be included with the item.

        Returns:
            None
        """
        self._errors_ok = False
        item = pd.DataFrame([{
            "id": id,
            "prediction": prediction,
            "expected": expected,
            "weight": weight,
            **metadata
        }])
        self._items = pd.concat([self._items, item], ignore_index=True)
 
    def add_error_terms(self, error_funcs: Dict[str, Callable[[pd.DataFrame], pd.Series]]) -> None:
        """
        Adds error functions to the validation group.

        Args:
            error_funcs (Dict[str, Callable[[pd.DataFrame], pd.Series]]): 
                A dictionary where the keys are error term names and the values are 
                functions that take a pandas DataFrame and return a pandas Series 
                representing the error term.

        Returns:
            None
        """
        self._errors_ok = False
        self._error_terms.update(error_funcs)
    
    def _update_errors(self) -> None:
        if self._items.empty or self._errors_ok:
            return
        for name, error_func in self._error_terms.items():
            self._items[name] = error_func(self._items)
        self._errors_ok = True
    
    def get_items(self) -> pd.DataFrame:
        """
        Retrieves the items DataFrame after updating error terms.

        Returns:
            pd.DataFrame: The DataFrame containing the items.
        """
        self._update_errors()
        return self._items
 
    def _run_aggregation(self, aggregator: ValidationAggregator) -> Dict[str, float]:
        if self._items.empty:
            return {}
        self._update_errors()
        filtered_items = self._items.query(aggregator.filter) if aggregator.filter is not None else self._items
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
            aggregation (Callable[[pd.DataFrame], float]): A function that takes a pandas
                DataFrame and returns a float.
            filter (Optional[str]): An optional filter to apply before aggregation. Defaults to None.
            group_by (Optional[Union[str, List[str]]]): An optional column or list of columns to 
                group by before aggregation. Defaults to None.

        Returns:
            None
        """
        self._aggregations.append(ValidationAggregator(name, aggregation, filter, group_by))

    def get_aggregations(self) -> Dict[str, float]:
        """
        Executes all aggregation functions stored in the `aggregations`
        attribute and combines their results.

        Returns:
            Dict[str, float]: A dictionary containing the combined results of all aggregation functions.
        """
        self._update_errors()
        all_results = {}
        for aggregator in self._aggregations:
            results = self._run_aggregation(aggregator)
            all_results.update(results)
        return all_results
    
    def add_visualization(self, name: str, visualization: Callable[[pd.DataFrame], str]) -> None:
        """
        Adds a visualization function to the list of visualizations.

        Args:
            name (str): The name of the visualization.
            visualization (Callable[[pd.DataFrame], str]): A function that takes a pandas
                DataFrame and returns a html string.

        Returns:
            None
        """
        self._visualizations[name] = visualization

    def run_visualizations(self) -> Dict[str, str]:
        """
        Executes all visualization functions stored in the `visualizations`
        attribute and combines their results.

        Returns:
            Dict[str, str]: A dictionary containing the combined results of all visualization functions.
        """
        self._update_errors()
        return {k: v(self._items) for k, v in self._visualizations.items()}

class Validation:
    groups: Dict[str, ValidationGroup]
    
    def __init__(self):
        """
        Initializes a new instance of the class.
        """
        self.groups = {}
    
    def create_group(self, name: str, add_default_error_terms: bool = True) -> ValidationGroup:
        """
        Create or retrieve a validation group by name.

        If a group with the given name already exists, it returns the existing group.
        Otherwise, it creates a new ValidationGroup, stores it in the groups dictionary,
        and returns the new group.

        Args:
            name (str): The name of the validation group.
            add_default_error_terms (bool, optional): Whether to add default error terms to the
                group. Defaults to True.

        Returns:
            ValidationGroup: The existing or newly created validation group.
        """
        if name in self.groups:
            return self.groups[name]
        group = ValidationGroup()
        self.groups[name] = group
        if add_default_error_terms:
            group.add_error_terms(default_error_terms)
        return group
    
    def save_to_file(self, file_path: Path) -> None:
        """
        Saves the content of the Validation object to a file.

        Args:
            file_path (Path): The file path where the content should be saved.

        Returns:
            None
        """
        with gzip.open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, file_path: Path) -> Validation:
        """
        Loads the content of a Validation object from a file.

        Args:
            file_path (Path): The file path from where the content should be loaded.

        Returns:
            Validation: The loaded Validation object.
        """
        with gzip.open(file_path, 'rb') as file:
            return pickle.load(file)

    def to_html(self, file_path: Path = None) -> str:
        """
        Generates an HTML representation of validation items and optionally writes it to a file.
        The generated HTML includes collapsible sections for each group of validation items,
        with a table displaying the predictions, expected values, weights, and any additional columns.

        Args:
            file_path (Path, optional): The file path where the HTML content should be written. 
                                        If not provided, the HTML content is not written to a file.

        Returns:
            str: The generated HTML content as a string.
        """
        html_content = ""
        for group_name, group in self.groups.items():
            items = group.get_items()
            html_content += f"""
            <h2>{group_name}</h2>
            <button class="collapsible">Items</button>
            <div class="content">
                <table>
                    <thead>
                        <tr>
                            {''.join(f'<th class="sortable" onclick="sortTable(this, {i})">{col}</th>' for i, col in enumerate(items.columns))}
                        </tr>
                    </thead>
                    <tbody>
            """
            for _, row in items.iterrows():
                html_content += "<tr>"
                html_content += ''.join(f"<td>{row[col]}</td>" for col in items.columns)
                html_content += "</tr>"
            html_content += "</tbody></table></div>"

            visualizations = group.run_visualizations()
            if visualizations:
                html_content += """
                <button class="collapsible">Visualizations</button>
                <div class="content" style="display: block;">
                """
                for viz_name, viz_content in visualizations.items():
                    html_content += f"<h3>{viz_name}</h3><div>{viz_content}</div>"
                html_content += " </div>"

            aggregation_results = group.get_aggregations()
            html_content += """
            <button class="collapsible">Aggregation Results</button>
            <div class="content" style="display: block;">
                <table>
                    <tr><th>Metric</th><th>Value</th></tr>
            """
            for metric_name, value in aggregation_results.items():
                html_content += f"<tr><td>{metric_name}</td><td>{value}</td></tr>"
            html_content += "</table></div>"

        template_path = Path(__file__).parent / "validation_template.html"
        with open(template_path, 'r', encoding='utf8') as template_file:
            template_content = template_file.read()
        html_content = template_content.replace("{{content}}", html_content)

        if file_path:
            with open(file_path, 'w', encoding='utf8') as file:
                file.write(html_content)
        return html_content

# Predefined error terms
def basic_error(df: pd.DataFrame) -> pd.Series:
    return df["prediction"] - df["expected"]
def absolute_error(df: pd.DataFrame) -> pd.Series:
    return (df["prediction"] - df["expected"]).abs()
def relative_error(df: pd.DataFrame) -> pd.Series:
    return (df["prediction"] - df["expected"]) / df["expected"]
def squared_error(df: pd.DataFrame) -> pd.Series:
    return (df["prediction"] - df["expected"]) ** 2

default_error_terms = {
    "basic_error": basic_error,
    "absolute_error": absolute_error,
    "relative_error": relative_error,
    "squared_error": squared_error
}

# Predefined aggregation functions
def mse(df: pd.DataFrame) -> float:
    return ((df["prediction"] - df["expected"]) ** 2 * df['weight']).mean()
def mae(df: pd.DataFrame) -> float:
    return ((df["prediction"] - df["expected"]) * df['weight']).abs().mean()
def max_error(df: pd.DataFrame) -> float:
    return ((df["prediction"] - df["expected"]) * df['weight']).abs().max()
def mean_error(df: pd.DataFrame) -> float:
    return ((df["prediction"] - df["expected"]) * df['weight']).mean()
def relative_error(df: pd.DataFrame) -> float:
    return ((df["prediction"] - df["expected"]) / df["expected"] * df['weight']).mean()

def mean(source: str):
    return lambda df: df[source].mean()
def sum(source: str):
    return lambda df: df[source].sum()
def count(source: str):
    return lambda df: df[source].count()
def weighted_mean(source: str, weight: str = 'weight'):
    return lambda df: (df[source] * df[weight]).sum() / df[weight].sum()

# Visualizations
def scatter_plot(x: str = 'expected',
                 y: str = 'prediction',
                 color: str = None,
                 colormap: str = 'viridis',
                 show_diagonal: bool = True,
                 discrete_colors: bool = False) -> Callable[[pd.DataFrame], str]:
    def _scatter_plot(df: pd.DataFrame) -> str:
        try:
            import plotly.express as px
            import plotly.graph_objects as go
        except ImportError:
            return "Plotly is not installed. Please install it using 'pip install plotly'"
        
        if color is not None and discrete_colors:
            # Use color_discrete_map='identity' for categorical colors
            fig = px.scatter(df, x=x, y=y, color=color, 
                            color_discrete_sequence=px.colors.qualitative.Plotly)
        else:
            # Original behavior for continuous colors
            fig = px.scatter(df, x=x, y=y, color=color, 
                            color_continuous_scale=colormap)
            
        if show_diagonal:
            min_val = min(df[x].min(), df[y].min())
            max_val = max(df[x].max(), df[y].max())
            fig.add_trace(go.Scatter(x=[min_val, max_val],
                                     y=[min_val, max_val],
                                     mode='lines',
                                     line=dict(color='red', dash='dash'),
                                     showlegend=False))
        
        return fig.to_html()
    return _scatter_plot

def bar_plot(x: str = 'id', y: Union[str, List[str]] = None) -> Callable[[pd.DataFrame], str]:
    if y is None:
        y = ['prediction', 'expected']
    if isinstance(y, str):
        y = [y]

    def _bar_plot(df: pd.DataFrame) -> str:
        try:
            import plotly.graph_objects as go
        except ImportError:
            return "Plotly is not installed. Please install it using 'pip install plotly'"
        
        fig = go.Figure()
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']
        
        for i, y_col in enumerate(y):
            fig.add_trace(go.Bar(name=y_col, x=df[x], y=df[y_col], marker_color=colors[i % len(colors)]))
        
        fig.update_layout(barmode='group', xaxis_title=x, yaxis_title='Value')
        return fig.to_html()
    
    return _bar_plot

# # Usage example
# test_valid = Validation()

# # Create a group without default error terms
# group = test_valid.create_group("test", add_default_error_terms=False)

# # Add sample predictions to the group
# # use arbitrary "example1" and "example2" columns for grouping
# group.add_item('s1', 1, 1,   example1='a'  , example2=1)
# group.add_item('s2', 2, 2.5, example1='a'  , example2=2)
# group.add_item('s3', 3, 4,   example1='b')
# group.add_item('s4', 4, 6,   example1='c'  , example2=2)
# group.add_item('s5', 5, 7,   example1='b'  , example2=1)

# # Add error terms
# group.add_error_terms({'squared_error': squared_error})

# # Add aggregations to the group
# # Mean absolute error for all items
# group.add_aggregation('mae', mae)
# # Maximum error for all items, grouped by test_val
# group.add_aggregation('max', max_error, group_by='example2')

# # mean squared error for predictions >= 3, grouped by test1
# group.add_aggregation("mse_error", mse, filter='prediction>=3', group_by='example1')
# # Same as above but using a precalculated error term
# group.add_aggregation('mse_error2', mean('squared_error'), filter='prediction>=3', group_by='example1')

# group2 = test_valid.create_group("test2")
# # Add larget dataset of random points
# for i in range(1, 1000):
#     group2.add_item(f'point{i}', i**1.02 + random.random()*200-150, i, even='even' if i % 2 == 0 else 'odd')
# group2.add_aggregation('mse', mean('squared_error'), group_by='even')

# group.add_visualization('test bar plot', bar_plot(y=['prediction', 'expected', 'squared_error']))
# group2.add_visualization('test scatter plot', scatter_plot(color='absolute_error'))

# # Run all aggregations and print the results
# test_valid.to_html('test_validation.html')
# # Save the validation object to a file
# test_valid.save_to_file('test_validation.pklz')
# # Load the validation object from a file
# loaded_valid = Validation.load_from_file('test_validation.pklz')
# loaded_valid.to_html('test_validation_loaded.html')
# # Open the generated HTML file in the default web browser
# import webbrowser
# webbrowser.open('test_validation.html')
