from openpyxl import Workbook, load_workbook
import sys
import os
import openmatrix as omx
import numpy
import pandas
import re
import parameters as param


def read_scen (scenario, time_period):
    """Read travel cost and demand data for scenario from files"""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(script_dir, "..", "..")
    path = os.path.join(project_dir, "Matrices", scenario)
    files = dict.fromkeys(["demand", "time", "cost", "dist"])
    for mtx_type in files:
        file_name = mtx_type + '_' + time_period + ".omx"
        file_path = os.path.join(path, file_name)
        files[mtx_type] = omx.open_file(file_path)
    matrices = {}
    for transport_class in param.transport_classes:
        matrices[transport_class] = {}
        for mtx_type in files:
            if mtx_type != "demand":
                mtx_label = transport_class.split('_')[0]
                if mtx_label == "transit" or mtx_label == "bike":
                    ass_class = mtx_label
                elif transport_class in ("truck", "trailer_truck", "van"):
                    # TODO Calculate and output impendance matrices for
                    # these modes in end assignment
                    ass_class = "car_work"
                else:
                    ass_class = transport_class
            else:
                ass_class = transport_class
            if mtx_label == "bike" and mtx_type == "cost":
                matrices[transport_class][mtx_type] = 0
            else:
                matrices[transport_class][mtx_type] = numpy.array(files[mtx_type][ass_class])
    for mtx_type in files:
        files[mtx_type].close()
    print "Files read"
    return matrices    

def calc_revenue (ve0, ve1):
    """Calculate difference in producer revenue between scenarios ve1 and ve0"""
    revenue = 0
    demand_change = ve1["demand"] - ve0["demand"]
    cost_change = ve1["cost"] - ve0["cost"]
    revenue += (ve1["cost"] * demand_change)[demand_change >= 0].sum()
    revenue += (cost_change * ve0["demand"])[demand_change >= 0].sum()
    revenue += (ve0["cost"] * demand_change)[demand_change < 0].sum()
    revenue += (cost_change * ve1["demand"])[demand_change < 0].sum()
    return revenue

def calc_cost_gains (ve0, ve1):
    """Calculate difference in consumer surplus between scenarios ve1 and ve0"""
    gains = {"existing": 0, "additional": 0}
    gain = ve1["cost"] - ve0["cost"]
    demand_change = ve1["demand"] - ve0["demand"]
    gains["existing"] += (ve0["demand"] * gain)[demand_change >= 0].sum()
    gains["additional"] += 0.5 * (demand_change * gain)[demand_change >= 0].sum()
    gains["existing"] += (ve1["demand"] * gain)[demand_change < 0].sum()
    gains["additional"] -= 0.5 * (demand_change * gain)[demand_change < 0].sum()
    return gains

def calc_gains (ve0, ve1):
    """Calculate time, distance and cost gains"""
    gains = {}
    gains["time"] = calc_cost_gains(
        {
            "cost": ve0["time"],
            "demand": ve0["demand"],
        },
        {
            "cost": ve1["time"],
            "demand": ve1["demand"],
        },
    )
    gains["dist"] = calc_cost_gains(
        {
            "cost": ve0["dist"],
            "demand": ve0["demand"],
        },
        {
            "cost": ve1["dist"],
            "demand": ve1["demand"],
        },
    )
    gains["cost"] = calc_cost_gains(ve0, ve1)
    return gains

def mileages (scenario):
    """Read scenario data from files"""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(script_dir, "..", "..")
    data_dir = os.path.join(project_dir, "Results", scenario)
    data_dir = os.path.abspath(data_dir)
    filename = os.path.join(data_dir, "vehicle_kms.txt")
    data = pandas.read_csv(filename, delim_whitespace=True)
    filename = os.path.join(data_dir, "transit_kms.txt")
    transit_data = pandas.read_csv(filename, delim_whitespace=True)
    miles = {
        "car": data["car"],
        "truck": data["truck"],
        "van": data["van"],
        "trailer_truck": data["trailer_truck"],
        "transit": {
            "time": {
                "bus": transit_data["time"]["bde"], 
                "trunk": transit_data["time"]["g"],
                "metro": transit_data["time"]["m"],
                "train": transit_data["time"]["rj"],
                "tram": transit_data["time"]["tp"],
            },
            "dist": {
                "bus": transit_data["km"]["bde"], 
                "trunk": transit_data["km"]["g"],
                "metro": transit_data["km"]["m"],
                "train": transit_data["km"]["rj"],
                "tram": transit_data["km"]["tp"],
            },
        },
    }
    return miles

def mile_gains (miles0, miles1):
    """Calculate mile gains"""
    miles = miles1 - miles0
    return miles

def pt_miles (miles0, miles1):
    """Calculate public transport mile gains"""
    miles = {}
    miles["bus"] = miles1["bus"] - miles0["bus"]
    miles["trunk"] = miles1["trunk"] - miles0["trunk"]
    miles["metro"] = miles1["metro"] - miles0["metro"]
    miles["train"] = miles1["train"] - miles0["train"]
    miles["tram"] = miles1["tram"] - miles0["tram"]
    return miles

def write_results_1 (wb, miles, revenues, gains):
    """Write results for year 1"""
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
    ws = wb.get_sheet_by_name("Kayttajahyodyt")
    ws["J9"] = gains["car"]["aht"]["time"]["existing"]
    ws["J10"] = gains["car"]["aht"]["time"]["additional"]
    ws["K9"] = gains["car"]["pt"]["time"]["existing"]
    ws["K10"] = gains["car"]["pt"]["time"]["additional"]
    ws["L9"] = gains["car"]["iht"]["time"]["existing"]
    ws["L10"] = gains["car"]["iht"]["time"]["additional"]
    ws["J22"] = gains["car"]["aht"]["dist"]["existing"]
    ws["J23"] = gains["car"]["aht"]["dist"]["additional"]
    ws["K22"] = gains["car"]["pt"]["dist"]["existing"]
    ws["K23"] = gains["car"]["pt"]["dist"]["additional"]
    ws["L22"] = gains["car"]["iht"]["dist"]["existing"]
    ws["L23"] = gains["car"]["iht"]["dist"]["additional"]
    ws["J37"] = gains["car"]["aht"]["cost"]["existing"]
    ws["J38"] = gains["car"]["aht"]["cost"]["additional"]
    ws["K37"] = gains["car"]["pt"]["cost"]["existing"]
    ws["K38"] = gains["car"]["pt"]["cost"]["additional"]
    ws["L37"] = gains["car"]["iht"]["cost"]["existing"]
    ws["L38"] = gains["car"]["iht"]["cost"]["additional"]
    ws["P9"] = gains["truck"]["aht"]["time"]["existing"]
    ws["P10"] = gains["truck"]["aht"]["time"]["additional"]
    ws["Q9"] = gains["truck"]["pt"]["time"]["existing"]
    ws["Q10"] = gains["truck"]["pt"]["time"]["additional"]
    ws["R9"] = gains["truck"]["iht"]["time"]["existing"]
    ws["R10"] = gains["truck"]["iht"]["time"]["additional"]
    ws["P22"] = gains["truck"]["aht"]["dist"]["existing"]
    ws["P23"] = gains["truck"]["aht"]["dist"]["additional"]
    ws["Q22"] = gains["truck"]["pt"]["dist"]["existing"]
    ws["Q23"] = gains["truck"]["pt"]["dist"]["additional"]
    ws["R22"] = gains["truck"]["iht"]["dist"]["existing"]
    ws["R23"] = gains["truck"]["iht"]["dist"]["additional"]
    ws["P37"] = gains["truck"]["aht"]["cost"]["existing"]
    ws["P38"] = gains["truck"]["aht"]["cost"]["additional"]
    ws["Q37"] = gains["truck"]["pt"]["cost"]["existing"]
    ws["Q38"] = gains["truck"]["pt"]["cost"]["additional"]
    ws["R37"] = gains["truck"]["iht"]["cost"]["existing"]
    ws["R38"] = gains["truck"]["iht"]["cost"]["additional"]
    ws["V9"] = gains["transit"]["aht"]["time"]["existing"]
    ws["V10"] = gains["transit"]["aht"]["time"]["additional"]
    ws["W9"] = gains["transit"]["pt"]["time"]["existing"]
    ws["W10"] = gains["transit"]["pt"]["time"]["additional"]
    ws["X9"] = gains["transit"]["iht"]["time"]["existing"]
    ws["X10"] = gains["transit"]["iht"]["time"]["additional"]
    ws["V37"] = gains["transit"]["aht"]["cost"]["existing"]
    ws["V38"] = gains["transit"]["aht"]["cost"]["additional"]
    ws["W37"] = gains["transit"]["pt"]["cost"]["existing"]
    ws["W38"] = gains["transit"]["pt"]["cost"]["additional"]
    ws["X37"] = gains["transit"]["iht"]["cost"]["existing"]
    ws["X38"] = gains["transit"]["iht"]["cost"]["additional"]
    ws = wb.get_sheet_by_name("Tuottajahyodyt")
    ws["S8"] = miles["transit"]["dist"]["bus"]
    ws["S9"] = miles["transit"]["dist"]["trunk"]
    ws["S10"] = miles["transit"]["dist"]["tram"]
    ws["S11"] = miles["transit"]["dist"]["metro"]
    ws["S12"] = miles["transit"]["dist"]["train"]
    ws["T8"] = miles["transit"]["time"]["bus"]
    ws["T9"] = miles["transit"]["time"]["trunk"]
    ws["T10"] = miles["transit"]["time"]["tram"]
    ws["T11"] = miles["transit"]["time"]["metro"]
    ws["T12"] = miles["transit"]["time"]["train"]
    ws["B43"] = revenues["transit"]["aht"]
    ws["C43"] = revenues["transit"]["pt"]
    ws["D43"] = revenues["transit"]["iht"]
    ws = wb.get_sheet_by_name("Julkistaloudelliset")
    ws["F8"] = revenues["car"]["aht"]
    ws["G8"] = revenues["car"]["pt"]
    ws["H8"] = revenues["car"]["iht"]

def write_results_2 (wb, miles, revenues, gains):
    """Write results for year 2"""
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
    ws["J14"] = gains["car"]["aht"]["time"]["existing"]
    ws["J15"] = gains["car"]["aht"]["time"]["additional"]
    ws["K14"] = gains["car"]["pt"]["time"]["existing"]
    ws["K15"] = gains["car"]["pt"]["time"]["additional"]
    ws["L14"] = gains["car"]["iht"]["time"]["existing"]
    ws["L15"] = gains["car"]["iht"]["time"]["additional"]
    ws["J27"] = gains["car"]["aht"]["dist"]["existing"]
    ws["J28"] = gains["car"]["aht"]["dist"]["additional"]
    ws["K27"] = gains["car"]["pt"]["dist"]["existing"]
    ws["K28"] = gains["car"]["pt"]["dist"]["additional"]
    ws["L27"] = gains["car"]["iht"]["dist"]["existing"]
    ws["L28"] = gains["car"]["iht"]["dist"]["additional"]
    ws["J42"] = gains["car"]["aht"]["cost"]["existing"]
    ws["J43"] = gains["car"]["aht"]["cost"]["additional"]
    ws["K42"] = gains["car"]["pt"]["cost"]["existing"]
    ws["K43"] = gains["car"]["pt"]["cost"]["additional"]
    ws["L42"] = gains["car"]["iht"]["cost"]["existing"]
    ws["L43"] = gains["car"]["iht"]["cost"]["additional"]
    ws["P14"] = gains["truck"]["aht"]["time"]["existing"]
    ws["P15"] = gains["truck"]["aht"]["time"]["additional"]
    ws["Q14"] = gains["truck"]["pt"]["time"]["existing"]
    ws["Q15"] = gains["truck"]["pt"]["time"]["additional"]
    ws["R14"] = gains["truck"]["iht"]["time"]["existing"]
    ws["R15"] = gains["truck"]["iht"]["time"]["additional"]
    ws["P27"] = gains["truck"]["aht"]["dist"]["existing"]
    ws["P28"] = gains["truck"]["aht"]["dist"]["additional"]
    ws["Q27"] = gains["truck"]["pt"]["dist"]["existing"]
    ws["Q28"] = gains["truck"]["pt"]["dist"]["additional"]
    ws["R27"] = gains["truck"]["iht"]["dist"]["existing"]
    ws["R28"] = gains["truck"]["iht"]["dist"]["additional"]
    ws["P42"] = gains["truck"]["aht"]["cost"]["existing"]
    ws["P43"] = gains["truck"]["aht"]["cost"]["additional"]
    ws["Q42"] = gains["truck"]["pt"]["cost"]["existing"]
    ws["Q43"] = gains["truck"]["pt"]["cost"]["additional"]
    ws["R42"] = gains["truck"]["iht"]["cost"]["existing"]
    ws["R43"] = gains["truck"]["iht"]["cost"]["additional"]
    ws["V14"] = gains["transit"]["aht"]["time"]["existing"]
    ws["V15"] = gains["transit"]["aht"]["time"]["additional"]
    ws["W14"] = gains["transit"]["pt"]["time"]["existing"]
    ws["W15"] = gains["transit"]["pt"]["time"]["additional"]
    ws["X14"] = gains["transit"]["iht"]["time"]["existing"]
    ws["X15"] = gains["transit"]["iht"]["time"]["additional"]
    ws["V42"] = gains["transit"]["aht"]["cost"]["existing"]
    ws["V43"] = gains["transit"]["aht"]["cost"]["additional"]
    ws["W42"] = gains["transit"]["pt"]["cost"]["existing"]
    ws["W43"] = gains["transit"]["pt"]["cost"]["additional"]
    ws["X42"] = gains["transit"]["iht"]["cost"]["existing"]
    ws["X43"] = gains["transit"]["iht"]["cost"]["additional"]
    ws = wb.get_sheet_by_name("Tuottajahyodyt")
    ws["S16"] = miles["transit"]["dist"]["bus"]
    ws["S17"] = miles["transit"]["dist"]["trunk"]
    ws["S18"] = miles["transit"]["dist"]["tram"]
    ws["S19"] = miles["transit"]["dist"]["metro"]
    ws["S20"] = miles["transit"]["dist"]["train"]
    ws["T16"] = miles["transit"]["time"]["bus"]
    ws["T17"] = miles["transit"]["time"]["trunk"]
    ws["T18"] = miles["transit"]["time"]["tram"]
    ws["T19"] = miles["transit"]["time"]["metro"]
    ws["T20"] = miles["transit"]["time"]["train"]
    ws["B46"] = revenues["transit"]["aht"]
    ws["C46"] = revenues["transit"]["pt"]
    ws["D46"] = revenues["transit"]["iht"]
    ws = wb.get_sheet_by_name("Julkistaloudelliset")
    ws["F13"] = revenues["car"]["aht"]
    ws["G13"] = revenues["car"]["pt"]
    ws["H13"] = revenues["car"]["iht"]

def main (args):
    miles1 = mileages(args[2])
    miles0 = mileages(args[1])
    miles = {}
    miles["car"] = mile_gains(miles0["car"], miles1["car"])
    miles["truck"] = mile_gains(miles0["truck"], miles1["truck"])
    miles["van"] = mile_gains(miles0["van"], miles1["van"])
    miles["trailer_truck"] = mile_gains(miles0["trailer_truck"], miles1["trailer_truck"])
    miles["transit"] = {}
    miles["transit"]["dist"] = pt_miles(miles0["transit"]["dist"], miles1["transit"]["dist"])
    miles["transit"]["time"] = pt_miles(miles0["transit"]["time"], miles1["transit"]["time"])
    revenues = {
        "car": {},
        "transit": {},
    }
    gains = {
        "car": {}, 
        "transit": {}, 
        "truck": {},
    }
    for tp in ["aht", "pt", "iht"]:
        ve1 = read_scen(args[2], tp)
        ve0 = read_scen(args[1], tp)
        revenues["transit"][tp] = calc_revenue(ve0["transit_work"], ve1["transit_work"])
        revenues["car"][tp] = calc_revenue(ve0["car_work"], ve1["car_work"])
        print "Revenues aht calculated"
        gains["car"][tp] = calc_gains(ve0["car_work"], ve1["car_work"])
        gains["truck"][tp] = calc_gains(ve0["truck"], ve1["truck"])
        gains["transit"][tp] = calc_gains(ve0["transit_work"], ve1["transit_work"])
        print "Gains " + tp + " calculated"
    wb = load_workbook(args[3])
    year = int(args[4])
    if year == 1:
        write_results_1(wb, miles, revenues, gains)
    elif year == 2:
        write_results_2(wb, miles, revenues, gains)
    else:
        print "ENNUSTEVUOSI must be either 1 or 2"
    wb.save("cba_" + args[2] + ".xlsx")


# main(sys.argv)
main([0, "2030_test", "2030_test", "CBA_kehikko.xlsx", 1])
