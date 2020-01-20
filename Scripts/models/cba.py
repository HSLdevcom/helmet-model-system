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
    for ass_class in param.transport_classes:
        matrices[ass_class] = {}
        for mtx_type in files:
            matrices[ass_class][mtx_type] = numpy.array(files[mtx_type][ass_class])
    for mtx_type in files:
        files[mtx_type].close()
    print "Files read"
    return matrices    

def calc_revenue (ve0, ve1):
    """Calculate difference in producer revenue between scenarios ve1 and ve0"""
    revenue = 0
    demand_change = ve1['demand'] - ve0['demand']
    cost_change = ve1['cost'] - ve0['cost']
    revenue += (ve1['cost'] * demand_change)[demand_change >= 0].sum()
    revenue += (cost_change * ve0['demand'])[demand_change >= 0].sum()
    revenue += (ve0['cost'] * demand_change)[demand_change < 0].sum()
    revenue += (cost_change * ve1['demand'])[demand_change < 0].sum()
    return revenue

def calc_cost_gains (ve0, ve1):
    """Calculate difference in consumer surplus between scenarios ve1 and ve0"""
    gains = {'existing': 0, 'additional': 0}
    gain = ve1['cost'] - ve0['cost']
    demand_change = ve1['demand'] - ve0['demand']
    gains['existing'] += (ve0['demand'] * gain)[demand_change >= 0].sum()
    gains['additional'] += 0.5 * (demand_change * gain)[demand_change >= 0].sum()
    gains['existing'] += (ve1['demand'] * gain)[demand_change < 0].sum()
    gains['additional'] -= 0.5 * (demand_change * gain)[demand_change < 0].sum()
    return gains

def calc_gains (ve0, ve1):
    """Calculate time, distance and cost gains"""
    gains = {}
    gains['time'] = calc_cost_gains(
        {
            'cost': ve0['time'],
            'demand': ve0['demand'],
        },
        {
            'cost': ve1['time'],
            'demand': ve1['demand'],
        },
    )
    gains['dist'] = calc_cost_gains(
        {
            'cost': ve0['dist'],
            'demand': ve0['demand'],
        },
        {
            'cost': ve1['dist'],
            'demand': ve1['demand'],
        },
    )
    gains['cost'] = calc_cost_gains(ve0, ve1)
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
        'ha': data["car"],
        'ka': data["truck"],
        'pa': data["van"],
        'yhd': data["trailer_truck"],
        'jl': {
            "hr": {
                'bus': transit_data["time"]["bde"], 
                'trunk': transit_data["time"]["g"],
                'metro': transit_data["time"]["m"],
                'train': transit_data["time"]["rj"],
                'tram': transit_data["time"]["tp"],
            },
            "km": {
                'bus': transit_data["km"]["bde"], 
                'trunk': transit_data["km"]["g"],
                'metro': transit_data["km"]["m"],
                'train': transit_data["km"]["rj"],
                'tram': transit_data["km"]["tp"],
            },
        },
    }
    return miles

def mile_gains (miles0, miles1):
    """Calculate mile gains"""
    miles = {}
    miles['vdf1'] = miles1[1] - miles0[1]
    miles['vdf2'] = miles1[2] - miles0[2]
    miles['vdf3'] = miles1[3] - miles0[3]
    miles['vdf4'] = miles1[4] - miles0[4]
    miles['vdf5'] = miles1[5] - miles0[5]
    return miles

def pt_miles (miles0, miles1):
    """Calculate public transport mile gains"""
    miles = {}
    miles['bus'] = miles1['bus'] - miles0['bus']
    miles['trunk'] = miles1['trunk'] - miles0['trunk']
    miles['metro'] = miles1['metro'] - miles0['metro']
    miles['train'] = miles1['train'] - miles0['train']
    miles['tram'] = miles1['tram'] - miles0['tram']
    return miles

def write_results_1 (wb, miles, revenues, gains):
    """Write results for year 1"""
    ws = wb.get_sheet_by_name('Ulkoisvaikutukset')
    ws['I19'] = miles['ha']['vdf1']
    ws['J19'] = miles['ha']['vdf2']
    ws['K19'] = miles['ha']['vdf3']
    ws['L19'] = miles['ha']['vdf4']
    ws['M19'] = miles['ha']['vdf5']
    ws['I20'] = miles['pa']['vdf1']
    ws['J20'] = miles['pa']['vdf2']
    ws['K20'] = miles['pa']['vdf3']
    ws['L20'] = miles['pa']['vdf4']
    ws['M20'] = miles['pa']['vdf5']
    ws['I21'] = miles['ka']['vdf1']
    ws['J21'] = miles['ka']['vdf2']
    ws['K21'] = miles['ka']['vdf3']
    ws['L21'] = miles['ka']['vdf4']
    ws['M21'] = miles['ka']['vdf5']
    ws['I22'] = miles['yhd']['vdf1']
    ws['J22'] = miles['yhd']['vdf2']
    ws['K22'] = miles['yhd']['vdf3']
    ws['L22'] = miles['yhd']['vdf4']
    ws['M22'] = miles['yhd']['vdf5']
    ws = wb.get_sheet_by_name('Kayttajahyodyt')
    ws['J9'] = gains['ha_aht']['time']['existing']
    ws['J10'] = gains['ha_aht']['time']['additional']
    ws['K9'] = gains['ha_pai']['time']['existing']
    ws['K10'] = gains['ha_pai']['time']['additional']
    ws['L9'] = gains['ha_iht']['time']['existing']
    ws['L10'] = gains['ha_iht']['time']['additional']
    ws['J22'] = gains['ha_aht']['dist']['existing']
    ws['J23'] = gains['ha_aht']['dist']['additional']
    ws['K22'] = gains['ha_pai']['dist']['existing']
    ws['K23'] = gains['ha_pai']['dist']['additional']
    ws['L22'] = gains['ha_iht']['dist']['existing']
    ws['L23'] = gains['ha_iht']['dist']['additional']
    ws['J37'] = gains['ha_aht']['cost']['existing']
    ws['J38'] = gains['ha_aht']['cost']['additional']
    ws['K37'] = gains['ha_pai']['cost']['existing']
    ws['K38'] = gains['ha_pai']['cost']['additional']
    ws['L37'] = gains['ha_iht']['cost']['existing']
    ws['L38'] = gains['ha_iht']['cost']['additional']
    ws['P9'] = gains['ka_aht']['time']['existing']
    ws['P10'] = gains['ka_aht']['time']['additional']
    ws['Q9'] = gains['ka_pai']['time']['existing']
    ws['Q10'] = gains['ka_pai']['time']['additional']
    ws['R9'] = gains['ka_iht']['time']['existing']
    ws['R10'] = gains['ka_iht']['time']['additional']
    ws['P22'] = gains['ka_aht']['dist']['existing']
    ws['P23'] = gains['ka_aht']['dist']['additional']
    ws['Q22'] = gains['ka_pai']['dist']['existing']
    ws['Q23'] = gains['ka_pai']['dist']['additional']
    ws['R22'] = gains['ka_iht']['dist']['existing']
    ws['R23'] = gains['ka_iht']['dist']['additional']
    ws['P37'] = gains['ka_aht']['cost']['existing']
    ws['P38'] = gains['ka_aht']['cost']['additional']
    ws['Q37'] = gains['ka_pai']['cost']['existing']
    ws['Q38'] = gains['ka_pai']['cost']['additional']
    ws['R37'] = gains['ka_iht']['cost']['existing']
    ws['R38'] = gains['ka_iht']['cost']['additional']
    ws['V9'] = gains['jl_aht']['time']['existing']
    ws['V10'] = gains['jl_aht']['time']['additional']
    ws['W9'] = gains['jl_pai']['time']['existing']
    ws['W10'] = gains['jl_pai']['time']['additional']
    ws['X9'] = gains['jl_iht']['time']['existing']
    ws['X10'] = gains['jl_iht']['time']['additional']
    ws['V37'] = gains['jl_aht']['cost']['existing']
    ws['V38'] = gains['jl_aht']['cost']['additional']
    ws['W37'] = gains['jl_pai']['cost']['existing']
    ws['W38'] = gains['jl_pai']['cost']['additional']
    ws['X37'] = gains['jl_iht']['cost']['existing']
    ws['X38'] = gains['jl_iht']['cost']['additional']
    ws = wb.get_sheet_by_name('Tuottajahyodyt')
    ws['S8'] = miles['pt_km']['bus']
    ws['S9'] = miles['pt_km']['trunk']
    ws['S10'] = miles['pt_km']['tram']
    ws['S11'] = miles['pt_km']['metro']
    ws['S12'] = miles['pt_km']['train']
    ws['T8'] = miles['pt_hr']['bus']
    ws['T9'] = miles['pt_hr']['trunk']
    ws['T10'] = miles['pt_hr']['tram']
    ws['T11'] = miles['pt_hr']['metro']
    ws['T12'] = miles['pt_hr']['train']
    ws['B43'] = revenues['jl_aht']
    ws['C43'] = revenues['jl_pai']
    ws['D43'] = revenues['jl_iht']
    ws = wb.get_sheet_by_name('Julkistaloudelliset')
    ws['F8'] = revenues['ha_aht']
    ws['G8'] = revenues['ha_pai']
    ws['H8'] = revenues['ha_iht']

def write_results_2 (wb, miles, revenues, gains):
    """Write results for year 2"""
    ws = wb.get_sheet_by_name('Ulkoisvaikutukset')
    ws['I32'] = miles['ha']['vdf1']
    ws['J32'] = miles['ha']['vdf2']
    ws['K32'] = miles['ha']['vdf3']
    ws['L32'] = miles['ha']['vdf4']
    ws['M32'] = miles['ha']['vdf5']
    ws['I33'] = miles['pa']['vdf1']
    ws['J33'] = miles['pa']['vdf2']
    ws['K33'] = miles['pa']['vdf3']
    ws['L33'] = miles['pa']['vdf4']
    ws['M33'] = miles['pa']['vdf5']
    ws['I34'] = miles['ka']['vdf1']
    ws['J34'] = miles['ka']['vdf2']
    ws['K34'] = miles['ka']['vdf3']
    ws['L34'] = miles['ka']['vdf4']
    ws['M34'] = miles['ka']['vdf5']
    ws['I35'] = miles['yhd']['vdf1']
    ws['J35'] = miles['yhd']['vdf2']
    ws['K35'] = miles['yhd']['vdf3']
    ws['L35'] = miles['yhd']['vdf4']
    ws['M35'] = miles['yhd']['vdf5']
    ws = wb.get_sheet_by_name('Kayttajahyodyt')
    ws['J14'] = gains['ha_aht']['time']['existing']
    ws['J15'] = gains['ha_aht']['time']['additional']
    ws['K14'] = gains['ha_pai']['time']['existing']
    ws['K15'] = gains['ha_pai']['time']['additional']
    ws['L14'] = gains['ha_iht']['time']['existing']
    ws['L15'] = gains['ha_iht']['time']['additional']
    ws['J27'] = gains['ha_aht']['dist']['existing']
    ws['J28'] = gains['ha_aht']['dist']['additional']
    ws['K27'] = gains['ha_pai']['dist']['existing']
    ws['K28'] = gains['ha_pai']['dist']['additional']
    ws['L27'] = gains['ha_iht']['dist']['existing']
    ws['L28'] = gains['ha_iht']['dist']['additional']
    ws['J42'] = gains['ha_aht']['cost']['existing']
    ws['J43'] = gains['ha_aht']['cost']['additional']
    ws['K42'] = gains['ha_pai']['cost']['existing']
    ws['K43'] = gains['ha_pai']['cost']['additional']
    ws['L42'] = gains['ha_iht']['cost']['existing']
    ws['L43'] = gains['ha_iht']['cost']['additional']
    ws['P14'] = gains['ka_aht']['time']['existing']
    ws['P15'] = gains['ka_aht']['time']['additional']
    ws['Q14'] = gains['ka_pai']['time']['existing']
    ws['Q15'] = gains['ka_pai']['time']['additional']
    ws['R14'] = gains['ka_iht']['time']['existing']
    ws['R15'] = gains['ka_iht']['time']['additional']
    ws['P27'] = gains['ka_aht']['dist']['existing']
    ws['P28'] = gains['ka_aht']['dist']['additional']
    ws['Q27'] = gains['ka_pai']['dist']['existing']
    ws['Q28'] = gains['ka_pai']['dist']['additional']
    ws['R27'] = gains['ka_iht']['dist']['existing']
    ws['R28'] = gains['ka_iht']['dist']['additional']
    ws['P42'] = gains['ka_aht']['cost']['existing']
    ws['P43'] = gains['ka_aht']['cost']['additional']
    ws['Q42'] = gains['ka_pai']['cost']['existing']
    ws['Q43'] = gains['ka_pai']['cost']['additional']
    ws['R42'] = gains['ka_iht']['cost']['existing']
    ws['R43'] = gains['ka_iht']['cost']['additional']
    ws['V14'] = gains['jl_aht']['time']['existing']
    ws['V15'] = gains['jl_aht']['time']['additional']
    ws['W14'] = gains['jl_pai']['time']['existing']
    ws['W15'] = gains['jl_pai']['time']['additional']
    ws['X14'] = gains['jl_iht']['time']['existing']
    ws['X15'] = gains['jl_iht']['time']['additional']
    ws['V42'] = gains['jl_aht']['cost']['existing']
    ws['V43'] = gains['jl_aht']['cost']['additional']
    ws['W42'] = gains['jl_pai']['cost']['existing']
    ws['W43'] = gains['jl_pai']['cost']['additional']
    ws['X42'] = gains['jl_iht']['cost']['existing']
    ws['X43'] = gains['jl_iht']['cost']['additional']
    ws = wb.get_sheet_by_name('Tuottajahyodyt')
    ws['S16'] = miles['pt_km']['bus']
    ws['S17'] = miles['pt_km']['trunk']
    ws['S18'] = miles['pt_km']['tram']
    ws['S19'] = miles['pt_km']['metro']
    ws['S20'] = miles['pt_km']['train']
    ws['T16'] = miles['pt_hr']['bus']
    ws['T17'] = miles['pt_hr']['trunk']
    ws['T18'] = miles['pt_hr']['tram']
    ws['T19'] = miles['pt_hr']['metro']
    ws['T20'] = miles['pt_hr']['train']
    ws['B46'] = revenues['jl_aht']
    ws['C46'] = revenues['jl_pai']
    ws['D46'] = revenues['jl_iht']
    ws = wb.get_sheet_by_name('Julkistaloudelliset')
    ws['F13'] = revenues['ha_aht']
    ws['G13'] = revenues['ha_pai']
    ws['H13'] = revenues['ha_iht']

def main (args):
    miles1 = mileages(args[2])
    miles0 = mileages(args[1])
    miles = {}
    miles['ha'] = mile_gains(miles0['ha'], miles1['ha'])
    miles['ka'] = mile_gains(miles0['ka'], miles1['ka'])
    miles['pa'] = mile_gains(miles0['pa'], miles1['pa'])
    miles['yhd'] = mile_gains(miles0['yhd'], miles1['yhd'])
    miles['pt_km'] = pt_miles(miles0['jl']['km'], miles1['jl']['km'])
    miles['pt_hr'] = pt_miles(miles0['jl']['hr'], miles1['jl']['hr'])
    revenues = {}
    gains = {}
    for tp in ["aht"]:
        ve1 = read_scen(args[2], tp)
        ve0 = read_scen(args[1], tp)
        revenues["jl_" + tp] = calc_revenue(ve0["transit"], ve1["transit"])
        revenues["ha_" + tp] = calc_revenue(ve0["car"], ve1["car"])
        print "Revenues aht calculated"
        gains["ha_" + tp] = calc_gains(ve0["car"], ve1["car"])
        gains["ka_" + tp] = calc_gains(ve0["truck"], ve1["truck"])
        gains["jl_" + tp] = calc_gains(ve0["transit"], ve1["transit"])
        print "Gains " + tp + " calculated"
    wb = load_workbook(args[3])
    year = int(args[4])
    if year == 1:
        write_results_1(wb, miles, revenues, gains)
    elif year == 2:
        write_results_2(wb, miles, revenues, gains)
    else:
        print "ENNUSTEVUOSI must be either 1 or 2"
    wb.save('cba_' + args[2] + '.xlsx')


main(sys.argv)
main([0, "test", "test"])
