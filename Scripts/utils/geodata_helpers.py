from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from assignment.emme_bindings.mock_project import Network
    from assignment.emme_bindings.mock_project import Scenario
import pandas as pd
import geopandas as gpd
from shapely import LineString, Point

def get_links(network: 'Network', scen: 'Scenario') -> gpd.GeoDataFrame:
    """
    Extracts link data from a network and scenario and returns it as a GeoDataFrame.

    Args:
        network (Network): The network object containing link data.
        scen (Scenario): The scenario object containing attributes and ID.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing link data with the following columns:
            - 'scenario': The scenario ID.
            - 'id': The link ID.
            - 'geom': The geometry of the link as a LineString.
            - 'inode': The ID of the starting node of the link.
            - 'jnode': The ID of the ending node of the link.
            - Additional columns for each attribute in the scenario's "LINK" attributes.
    """
    attributes = scen.attributes("LINK")
    obj = network.links()
    values = [dict(zip(
        ['scenario', 'id', 'geom', 'inode', 'jnode'] + attributes,
        [int(scen.id), o.id, LineString(o.shape), o.i_node.id, o.j_node.id] + [o[a] for a in attributes]))
            for o in obj]
    return gpd.GeoDataFrame(values, geometry='geom').set_crs('epsg:3879')

def get_nodes(network: 'Network', scen: 'Scenario') -> gpd.GeoDataFrame:
    """
    Extracts node data from a network and scenario, and returns it as a GeoDataFrame.

    Args:
        network (Network): The network object containing node information.
        scen (Scenario): The scenario object containing attributes and scenario ID.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing node data with the following columns:
            - 'scenario': The scenario ID.
            - 'id': The node ID.
            - 'geom': The geometry of the node as a Point.
            - Additional columns for each attribute in the scenario's "NODE" attributes.
    """
    attributes = scen.attributes("NODE")
    obj = network.nodes()
    values = [dict(zip(
        ['scenario', 'id', 'geom'] + attributes,
        [int(scen.id), o.id, Point(o.x, o.y)] + [o[a] for a in attributes]))
            for o in obj]
    return gpd.GeoDataFrame(values, geometry='geom').set_crs('epsg:3879')

def get_transit_lines(network: 'Network', scen: 'Scenario') -> pd.DataFrame:
    """
    Retrieve transit line data from a given network and scenario.

    This function extracts transit line information from the provided network
    and scenario, including attributes such as scenario ID, transit line ID,
    mode, vehicle, and any additional attributes defined for transit lines
    in the scenario.

    Args:
        network (Network): The network object containing transit line data.
        scen (Scenario): The scenario object containing attributes and context.

    Returns:
        pd.DataFrame: A DataFrame containing transit line data with the following columns:
            - 'scenario': The ID of the scenario.
            - 'id': The ID of the transit line.
            - 'mode': The mode of the transit line.
            - 'vehicle': The vehicle type of the transit line.
            - Additional columns for each attribute defined in the scenario for transit lines.
    """
    attributes = scen.attributes("TRANSIT_LINE")
    obj = network.transit_lines()
    values = [dict(zip(
        ['scenario', 'id', 'mode', 'vehicle'] + attributes,
        [int(scen.id), o.id, o.mode.id, o.vehicle.id] + [o[a] for a in attributes]))
            for o in obj]
    return pd.DataFrame(values)

def get_transit_segments(network: 'Network', scen: 'Scenario') -> pd.DataFrame:
    """
    Extracts transit segment data from a given network and scenario and returns it as a pandas DataFrame.

    Args:
        network (Network): The transit network object containing transit lines and segments.
        scen (Scenario): The scenario object containing attributes and scenario-specific data.

    Returns:
        pd.DataFrame: A DataFrame containing transit segment data with the following columns:
            - 'scenario': The ID of the scenario.
            - 'id': The ID of the transit segment.
            - 'line_id': The ID of the transit line to which the segment belongs.
            - 'link_id': The ID of the link associated with the segment.
            - Additional columns for each attribute defined in the scenario's "TRANSIT_SEGMENT" attributes.
    """
    attributes = scen.attributes("TRANSIT_SEGMENT")
    tls = network.transit_lines()
    values = [dict(zip(
        ['scenario', 'id', 'line_id', 'link_id'] + attributes,
        [int(scen.id), ts.id, tl.id, ts.link.id] + [ts[a] for a in attributes]))
        for tl in tls for ts in tl.segments()]
    return pd.DataFrame(values)
