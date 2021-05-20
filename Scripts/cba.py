from openpyxl import load_workbook
import os
import numpy
import pandas
from argparse import ArgumentError, ArgumentParser

import parameters.assignment as param
from datahandling.matrixdata import MatrixData


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TRANSLATIONS = {
    "car_work": "ha_tyo",
    "car_leisure": "ha_muu",
    "transit_work": "jl_tyo",
    "transit_leisure": "jl_muu",
    "bike_work": "pp_tyo",
    "bike_leisure": "pp_muu",
    "truck": "ka",
    "trailer_truck": "yhd",
    "van": "pa",
}

COLUMNS = {
    "aht": 'B',
    "pt": 'C',
    "iht": 'D',
}

COLUMNS2 = {
    "aht": 'F',
    "pt": 'G',
    "iht": 'H',
}

ROWS = {
    1: {
        "time": ("9", "10"),
        "dist": ("22", "23"),
        "cost": ("37", "38"),
    },
    2: {
        "time": ("14", "15"),
        "dist": ("27", "28"),
        "cost": ("42", "43"),
    },
}

TRANSIT_ROWS = {
    1: "43",
    2: "46",
}

CAR_ROWS = {
    1: "8",
    2: "13",
}

def run_cost_benefit_analysis(scenario_0, scenario_1, year, workbook):
    """Runs CBA and writes the results to excel file.

    Parameters
    ----------
    scenario_0 : str
        Name of do-nothing scenario, for which 
        forecast results are available in Results folder
    scenario_1 : str
        Name of project scenario, for which 
        forecast results are available in Results folder
    year : int
        The evaluation year (1 or 2)
    results_directory : str
        Path to where "scenario_name/Matrices" result folder exists
    workbook : openpyxl.WorkBook
        The excel workbook where to save results
    """
    wb = workbook
    mile_diff = read_miles(scenario_1) - read_miles(scenario_0)
    transit_mile_diff = (read_transit_miles(scenario_1)
                         - read_transit_miles(scenario_0))
    if year == 1:
        write_results_1(wb, mile_diff, transit_mile_diff)
    elif year == 2:
        write_results_2(wb, mile_diff, transit_mile_diff)
    else:
        raise ArgumentError("Evaluation year must be either 1 or 2")

    for tp in ["aht", "pt", "iht"]:
        ve1_data = MatrixData(os.path.join(scenario_1, "Matrices"))
        ve0_data = MatrixData(os.path.join(scenario_0, "Matrices"))
        revenues_transit = 0
        revenues_car = 0
        for transport_class in param.transport_classes:
            with ve1_data.open("demand", tp) as mtx:
                ve1_demand = mtx[transport_class]
            with ve0_data.open("demand", tp) as mtx:
                ve0_demand = mtx[transport_class]
            for mtx_type in ["time", "cost", "dist"]:
                ve1_cost = read_costs(
                    ve1_data, tp, transport_class, mtx_type)
                ve0_cost = read_costs(
                    ve0_data, tp, transport_class, mtx_type)
                gains_existing, gains_additional = calc_gains(
                    ve0_demand, ve1_demand, ve0_cost, ve1_cost)
                ws = wb[TRANSLATIONS[transport_class]]
                ws[COLUMNS[tp]+ROWS[year][mtx_type][0]] = gains_existing
                ws[COLUMNS[tp]+ROWS[year][mtx_type][1]] = gains_additional
                if mtx_type == "cost":
                    revenue = calc_revenue(
                        ve0_demand, ve1_demand, ve0_cost, ve1_cost)
                    if transport_class in param.transit_classes:
                        revenues_transit += revenue
                    if transport_class in param.assignment_modes:
                        revenues_car += revenue
        ws = wb["Tuottajahyodyt"]
        ws[COLUMNS[tp]+TRANSIT_ROWS[year]] = revenues_transit
        ws = wb["Julkistaloudelliset"]
        ws[COLUMNS2[tp]+CAR_ROWS[year]] = revenues_car
        print ("Gains and revenues " + tp + " calculated")


def read_costs(matrixdata, time_period, transport_class, mtx_type):
    mtx_label = transport_class.split('_')[0]
    ass_class = mtx_label if mtx_label == "bike" else transport_class
    if mtx_label == "bike" and mtx_type == "cost":
        matrix = 0
    else:
        with matrixdata.open(mtx_type, time_period) as mtx:
            matrix = mtx[ass_class]
    if transport_class == "transit_work" and mtx_type == "cost":
        trips_per_month = numpy.full_like(matrix, 60)
        # Surrounding area has a lower number of trips per month
        trips_per_month[901:, :] = 44
        trips_per_month = 0.5 * (trips_per_month+trips_per_month.T)
        matrix /= trips_per_month
    elif transport_class == "transit_leisure":
        matrix /= 30
    return matrix


def calc_revenue(ve0_demand, ve1_demand, ve0_cost, ve1_cost):
    """Calculate difference in producer revenue between scenarios ve1 and ve0"""
    demand_change = ve1_demand - ve0_demand
    cost_change = ve1_cost - ve0_cost
    revenue = ((ve1_cost*demand_change)[demand_change >= 0].sum()
               + (cost_change*ve0_demand)[demand_change >= 0].sum()
               + (ve0_cost*demand_change)[demand_change < 0].sum()
               + (cost_change*ve1_demand)[demand_change < 0].sum())
    return revenue


def calc_gains(ve0_demand, ve1_demand, ve0_cost, ve1_cost):
    """Calculate difference in consumer surplus between scenarios ve1 and ve0"""
    gain = ve1_cost - ve0_cost
    demand_change = ve1_demand - ve0_demand
    gains_existing = ((ve0_demand*gain)[demand_change >= 0].sum()
                      + (ve1_demand*gain)[demand_change < 0].sum())
    gains_additional = (0.5*(demand_change*gain)[demand_change >= 0].sum()
                        - 0.5*(demand_change*gain)[demand_change < 0].sum())
    return gains_existing, gains_additional


def read_miles(scenario_path):
    """Read vehicle km data from file."""
    file_path = os.path.join(scenario_path, "vehicle_kms_vdfs.txt")
    return pandas.read_csv(file_path, delim_whitespace=True)


def read_transit_miles(scenario_path):
    """Read transit vehicle travel time and dist data from file."""
    file_path = os.path.join(scenario_path, "transit_kms.txt")
    return pandas.read_csv(file_path, delim_whitespace=True)


def write_results_1(wb, miles, transit_miles):
    """Write results for year 1"""
    ws = wb["Ulkoisvaikutukset"]
    ws["I19"] = miles["car_work"][1] + miles["car_leisure"][1]
    ws["J19"] = miles["car_work"][2] + miles["car_leisure"][2]
    ws["K19"] = miles["car_work"][3] + miles["car_leisure"][3]
    ws["L19"] = miles["car_work"][4] + miles["car_leisure"][4]
    ws["M19"] = miles["car_work"][5] + miles["car_leisure"][5]
    ws["I20"] = miles["van"][1]
    ws["J20"] = miles["van"][2]
    ws["K20"] = miles["van"][3]
    ws["L20"] = miles["van"][4]
    ws["M20"] = miles["van"][5]
    ws["I21"] = miles["truck"][1]
    ws["J21"] = miles["truck"][2]
    ws["K21"] = miles["truck"][3]
    ws["L21"] = miles["truck"][4]
    ws["M21"] = miles["truck"][5]
    ws["I22"] = miles["trailer_truck"][1]
    ws["J22"] = miles["trailer_truck"][2]
    ws["K22"] = miles["trailer_truck"][3]
    ws["L22"] = miles["trailer_truck"][4]
    ws["M22"] = miles["trailer_truck"][5]
    ws = wb["Tuottajahyodyt"]
    ws["S8"] = transit_miles["dist"]["bus"]
    ws["S9"] = transit_miles["dist"]["trunk"]
    ws["S10"] = transit_miles["dist"]["tram"]
    ws["S11"] = transit_miles["dist"]["metro"]
    ws["S12"] = transit_miles["dist"]["train"]
    ws["T8"] = transit_miles["time"]["bus"]
    ws["T9"] = transit_miles["time"]["trunk"]
    ws["T10"] = transit_miles["time"]["tram"]
    ws["T11"] = transit_miles["time"]["metro"]
    ws["T12"] = transit_miles["time"]["train"]


def write_results_2(wb, miles, transit_miles):
    """Write results for year 2"""
    ws = wb["Ulkoisvaikutukset"]
    ws["I32"] = miles["car_work"][1] + miles["car_leisure"][1]
    ws["J32"] = miles["car_work"][2] + miles["car_leisure"][2]
    ws["K32"] = miles["car_work"][3] + miles["car_leisure"][3]
    ws["L32"] = miles["car_work"][4] + miles["car_leisure"][4]
    ws["M32"] = miles["car_work"][5] + miles["car_leisure"][5]
    ws["I33"] = miles["van"][1]
    ws["J33"] = miles["van"][2]
    ws["K33"] = miles["van"][3]
    ws["L33"] = miles["van"][4]
    ws["M33"] = miles["van"][5]
    ws["I34"] = miles["truck"][1]
    ws["J34"] = miles["truck"][2]
    ws["K34"] = miles["truck"][3]
    ws["L34"] = miles["truck"][4]
    ws["M34"] = miles["truck"][5]
    ws["I35"] = miles["trailer_truck"][1]
    ws["J35"] = miles["trailer_truck"][2]
    ws["K35"] = miles["trailer_truck"][3]
    ws["L35"] = miles["trailer_truck"][4]
    ws["M35"] = miles["trailer_truck"][5]
    ws = wb["Tuottajahyodyt"]
    ws["S16"] = transit_miles["dist"]["bus"]
    ws["S17"] = transit_miles["dist"]["trunk"]
    ws["S18"] = transit_miles["dist"]["tram"]
    ws["S19"] = transit_miles["dist"]["metro"]
    ws["S20"] = transit_miles["dist"]["train"]
    ws["T16"] = transit_miles["time"]["bus"]
    ws["T17"] = transit_miles["time"]["trunk"]
    ws["T18"] = transit_miles["time"]["tram"]
    ws["T19"] = transit_miles["time"]["metro"]
    ws["T20"] = transit_miles["time"]["train"]


if __name__ == "__main__":
    parser = ArgumentParser(epilog="Calculates the Cost-Benefit Analysis between Results of two HELMET-Scenarios, "
                                   "and writes the outcome in CBA_kehikko.xlsx -file (in same folder).")
    parser.add_argument(
        "baseline_scenario", type=str, help="A 'do-nothing' baseline scenario")
    parser.add_argument(
        "projected_scenario", type=str,
        help="A projected scenario, compared to the baseline scenario")
    parser.add_argument(
        "baseline_scenario_2", nargs='?', type=str,
        help="A 'do-nothing' baseline scenario for second forecast year (optional)")
    parser.add_argument(
        "projected_scenario_2", nargs='?', type=str,
        help="A projected scenario, compared to the baseline scenario for second forecast year (optional)")
    parser.add_argument(
        "--results-path", dest="results_path", type=str, required=True,
        help="Path to Results directory.")
    args = parser.parse_args()
    wb = load_workbook(os.path.join(SCRIPT_DIR, "CBA_kehikko.xlsx"))
    run_cost_benefit_analysis(
        args.baseline_scenario, args.projected_scenario, 1, wb)
    if args.baseline_scenario_2 is not None and args.baseline_scenario_2 != "undefined":
        run_cost_benefit_analysis(
            args.baseline_scenario_2, args.projected_scenario_2, 2, wb)
    results_filename =  "cba_{}_{}.xlsx".format(
        os.path.basename(args.projected_scenario),
        os.path.basename(args.baseline_scenario))
    wb.save(os.path.join(args.results_path, results_filename))
    print ("CBA results saved to file: {}".format(results_filename))
