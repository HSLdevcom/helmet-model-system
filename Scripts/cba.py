from openpyxl import load_workbook
import os
import openmatrix as omx
import numpy
import pandas
import parameters.assignment as param
from argparse import ArgumentParser

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def run_cost_benefit_analysis(scenario_0, scenario_1, year, results_directory, workbook):
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
    mile_diff = read_miles(results_directory, scenario_1) - read_miles(results_directory, scenario_0)
    transit_mile_diff = read_transit_miles(results_directory, scenario_1) - read_transit_miles(results_directory, scenario_0)
    emme_scenarios = ["aht", "pt", "iht"]
    ve1 = read_scenarios(os.path.join(results_directory, scenario_1, "Matrices"), emme_scenarios)
    ve0 = read_scenarios(os.path.join(results_directory, scenario_0, "Matrices"), emme_scenarios)
    # calculated revenues for 24h
    revenues = {}
    revenues["transit"] = calc_revenue(param.transit_classes, emme_scenarios, ve0, ve1)
    revenues["car"] = calc_revenue(param.assignment_modes, emme_scenarios, ve0, ve1)
    # gains 24h for all transport classes
    gains = dict.fromkeys(param.transport_classes)
    for transport_class in gains:
        gains[transport_class] = calc_gains(ve0, ve1, transport_class, emme_scenarios)
        print "Gains " + transport_class + " calculated"
    if year == 1:
        write_results_1(wb, mile_diff, transit_mile_diff, revenues, gains)
    elif year == 2:
        write_results_2(wb, mile_diff, transit_mile_diff, revenues, gains)
    else:
        print "Evaluation year must be either 1 or 2"

def read_scenarios(path, emme_scenarios):
    files = dict.fromkeys(["demand", "time", "cost", "dist"])
    matrices = dict.fromkeys(param.transport_classes)
    for transport_class in matrices:
        matrices[transport_class] = dict.fromkeys(files)
        for mtx_type in files:
            # set ass_class
            if mtx_type != "demand":
                mtx_label = transport_class.split('_')[0]
                if mtx_label == "bike":
                    ass_class = mtx_label
                else:
                    ass_class = transport_class
            else:
                ass_class = transport_class
            matrices[transport_class][mtx_type] = {}
            for tp in emme_scenarios:
                if mtx_label == "bike" and mtx_type == "cost":
                    matrices[transport_class][mtx_type][tp] = 0
                else:
                    matrices[transport_class][mtx_type][tp] = read_scenario(path, mtx_type, ass_class, tp)
    return matrices 

def read_scenario(path, mtx_type, ass_class, tp):
    """Read travel cost and demand data for scenario from files"""
    file_name = mtx_type + '_' + tp + ".omx"
    file_path = os.path.join(path, file_name)
    file_data = omx.open_file(file_path)
    matrix_data = numpy.array(file_data[ass_class])
    if mtx_type == "cost":
        if ass_class == "transit_work":
            trips_per_month = numpy.full_like(matrix_data, 60)
            # Surrounding area has a lower number of trips per month
            trips_per_month[901:, :] = 44
            trips_per_month = 0.5 * (trips_per_month+trips_per_month.T)
            matrix_data = matrix_data / trips_per_month
            if ass_class == "transit_leisure":
                 matrix_data = matrix_data / 30       
    file_data.close()
    print "Files read"
    return matrix_data
       
def calc_revenue(ass_classes, emme_scenarios, ve0, ve1):
    """Calculate difference in producer revenue between scenarios ve1 and ve0"""
    revenue = 0
    for ass_class in ass_classes:
        for tp in emme_scenarios:
            demand_change = ve1[ass_class]["demand"][tp] - ve0[ass_class]["demand"][tp]
            cost_change = ve1[ass_class]["cost"][tp] - ve0[ass_class]["cost"][tp]
            tp_coeff = param.volume_factors[ass_class][tp]
            revenue += ((ve1[ass_class]["cost"][tp] * demand_change)[demand_change >= 0].sum() * tp_coeff)
            revenue += ((cost_change * ve0[ass_class]["demand"][tp])[demand_change >= 0].sum() * tp_coeff)
            revenue += ((ve0[ass_class]["cost"][tp] * demand_change)[demand_change < 0].sum() * tp_coeff)
            revenue += ((cost_change * ve1[ass_class]["demand"][tp])[demand_change < 0].sum() * tp_coeff)
    return revenue


def calc_cost_gains(ve0, ve1, emme_scenarios, tp_coeffs):
    """Calculate difference in consumer surplus between scenarios ve1_tp_tp and ve0_tp"""
    for tp in emme_scenarios:
        tp_coeff = tp_coeffs[tp]
        gains = {"existing": 0, "additional": 0}
        demand_change = ve1["demand"][tp] - ve0["demand"][tp]
        gain = ve1["cost"][tp] - ve0["cost"][tp]
        gains["existing"] += ((ve0["demand"][tp] * gain)[demand_change >= 0].sum() * tp_coeff)
        gains["additional"] += (0.5 * (demand_change * gain)[demand_change >= 0].sum() * tp_coeff)
        gains["existing"] += ((ve1["demand"][tp] * gain)[demand_change < 0].sum() * tp_coeff)
        gains["additional"] -= (0.5 * (demand_change * gain)[demand_change < 0].sum() * tp_coeff)
    return gains


def calc_gains(ve0, ve1, transport_class, emme_scenarios):
    """Calculate time, distance and cost gains"""
    gains = dict.fromkeys(param.transport_classes)
    for gain_type in ["cost", "time", "dist"]:
        class_gains = calc_cost_gains(
            {
                "cost": ve0[transport_class][gain_type],
                "demand": ve0[transport_class]["demand"],
            },
            {
                "cost": ve1[transport_class][gain_type],
                "demand": ve1[transport_class]["demand"],
            },
            emme_scenarios,
            param.volume_factors[transport_class]
        )
        gains[gain_type] = class_gains
    return gains


def read_miles(results_directory, scenario_name):
    """Read scenario data from files"""
    file_path = os.path.join(results_directory, scenario_name, "vehicle_kms.txt")
    return pandas.read_csv(file_path, delim_whitespace=True)


def read_transit_miles(results_directory, scenario_name):
    """Read scenario data from files"""
    file_path = os.path.join(results_directory, scenario_name, "transit_kms.txt")
    return pandas.read_csv(file_path, delim_whitespace=True)


def write_results_1(wb, miles, transit_miles, revenues, gains):
    """Write results for year 1"""
    ws = wb.get_sheet_by_name("ha_tyo")
    write_gains_1(ws, gains["car_work"])
    ws = wb.get_sheet_by_name("ha_muu")
    write_gains_1(ws, gains["car_leisure"])
    ws = wb.get_sheet_by_name("jl_tyo")
    write_gains_1(ws, gains["transit_work"])
    ws = wb.get_sheet_by_name("jl_muu")
    write_gains_1(ws, gains["transit_leisure"])
    ws = wb.get_sheet_by_name("pp_tyo")
    write_gains_1(ws, gains["bike_work"])
    ws = wb.get_sheet_by_name("pp_muu")
    write_gains_1(ws, gains["bike_leisure"])
    ws = wb.get_sheet_by_name("ka")
    write_gains_1(ws, gains["truck"])
    ws = wb.get_sheet_by_name("yhd")
    write_gains_1(ws, gains["trailer_truck"])
    ws = wb.get_sheet_by_name("pa")
    write_gains_1(ws, gains["van"])
    ws = wb.get_sheet_by_name("Ulkoisvaikutukset")
    ws["I19"] = miles["car"][1]
    ws["J19"] = miles["car"][2]
    ws["K19"] = miles["car"][3]
    ws["L19"] = miles["car"][4]
    ws["M19"] = miles["car"][5]
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
    ws = wb.get_sheet_by_name("Tuottajahyodyt")
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
    ws["E43"] = revenues["transit"]
    ws = wb.get_sheet_by_name("Julkistaloudelliset")
    ws["I8"] = revenues["car"]

def write_gains_1(ws, gains):
    ws["E9"] = gains["time"]["existing"]
    ws["E10"] = gains["time"]["additional"]
    ws["E22"] = gains["dist"]["existing"]
    ws["E23"] = gains["dist"]["additional"]
    ws["E37"] = gains["cost"]["existing"]
    ws["E38"] = gains["cost"]["additional"]

def write_results_2(wb, miles, transit_miles, revenues, gains):
    """Write results for year 2"""
    ws = wb.get_sheet_by_name("ha_tyo")
    write_gains_2(ws, gains["car_work"])
    ws = wb.get_sheet_by_name("ha_muu")
    write_gains_2(ws, gains["car_leisure"])
    ws = wb.get_sheet_by_name("jl_tyo")
    write_gains_2(ws, gains["transit_work"])
    ws = wb.get_sheet_by_name("jl_muu")
    write_gains_2(ws, gains["transit_leisure"])
    ws = wb.get_sheet_by_name("pp_tyo")
    write_gains_2(ws, gains["bike_work"])
    ws = wb.get_sheet_by_name("pp_muu")
    write_gains_2(ws, gains["bike_leisure"])
    ws = wb.get_sheet_by_name("ka")
    write_gains_2(ws, gains["truck"])
    ws = wb.get_sheet_by_name("yhd")
    write_gains_2(ws, gains["trailer_truck"])
    ws = wb.get_sheet_by_name("pa")
    write_gains_2(ws, gains["van"])
    ws = wb.get_sheet_by_name("Ulkoisvaikutukset")
    ws["I32"] = miles["car"][1]
    ws["J32"] = miles["car"][2]
    ws["K32"] = miles["car"][3]
    ws["L32"] = miles["car"][4]
    ws["M32"] = miles["car"][5]
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
    ws = wb.get_sheet_by_name("Kayttajahyodyt")
    ws = wb.get_sheet_by_name("Tuottajahyodyt")
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
    ws["E46"] = revenues["transit"]
    ws = wb.get_sheet_by_name("Julkistaloudelliset")
    ws["I13"] = revenues["car"]


def write_gains_2(ws, gains):
    ws["E14"] = gains["time"]["existing"]
    ws["E15"] = gains["time"]["additional"]
    ws["E27"] = gains["dist"]["existing"]
    ws["E28"] = gains["dist"]["additional"]
    ws["E42"] = gains["cost"]["existing"]
    ws["E43"] = gains["cost"]["additional"]


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
        args.baseline_scenario, args.projected_scenario, 1, args.results_path, wb)
    if args.baseline_scenario_2 is not None and args.baseline_scenario_2 != "undefined":
        run_cost_benefit_analysis(
            args.baseline_scenario_2, args.projected_scenario_2, 2, args.results_path, wb)
    results_filename =  "cba_{}_{}.xlsx".format(
        os.path.basename(args.projected_scenario),
        os.path.basename(args.baseline_scenario))
    wb.save(os.path.join(args.results_path, results_filename))
    print "CBA results saved to file: {}".format(results_filename)
