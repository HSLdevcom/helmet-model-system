from openpyxl import load_workbook
import os
import openmatrix as omx
import numpy
import pandas
import parameters.assignment as param
from argparse import ArgumentParser

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class CBA:
    def __init__(self, scenario_0, scenario_1):
        """Cost-benefit analysis class.

        Parameters
        ----------
        emme_scenarios : list
            Usually same as road network scenarios in Emme-project
        scenario_0 : str
            Name of do-nothing scenario, for which 
            forecast results are available in Results folder
        scenario_1 : str
            Name of project scenario, for which 
            forecast results are available in Results folder
        """
        self.emme_scenarios = ["aht", "pt", "iht"]
        self.scenario_1 = scenario_1 
        self.scenario_0 = scenario_0 

    def run_cost_benefit_analysis(self, results_directory):
        """Runs CBA and writes the results to excel file.

        Parameters
        ----------
        results_directory : str
            Path to where "scenario_name/Matrices" result folder exists
        """
        # read miles
        self.miles = self.read_miles(
            results_directory, self.scenario_1) - self.read_miles(results_directory, self.scenario_0)
        self.transit_miles = self.read_transit_miles(
            results_directory, self.scenario_1) - self.read_transit_miles(results_directory, self.scenario_0)
        # open omx-data
        ve1 = self.read_scenarios(os.path.join(results_directory, self.scenario_1, "Matrices"))
        ve0 = self.read_scenarios(os.path.join(results_directory, self.scenario_0, "Matrices"))
        # calculate revenues for 24h
        self.revenues = {}
        self.revenues["transit"] = self.calc_revenue(param.transit_classes, ve0, ve1)
        self.revenues["car"] = self.calc_revenue(param.assignment_modes, ve0, ve1)
        # gains 24h for all transport classes
        self.gains = dict.fromkeys(param.transport_classes)
        for transport_class in param.transport_classes:
            self.gains[transport_class] = self.calc_gains(ve0, ve1, transport_class)
            print "Gains " + transport_class + " calculated"

    def read_scenarios(self, path):
        files = dict.fromkeys(["demand", "time", "cost", "dist"])
        matrices = dict.fromkeys(param.transport_classes)
        for transport_class in param.transport_classes:
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
                matrices[transport_class][mtx_type] = dict.fromkeys(self.emme_scenarios)
                for tp in self.emme_scenarios:
                    if mtx_label == "bike" and mtx_type == "cost":
                        matrices[transport_class][mtx_type][tp] = 0
                    else:
                        matrices[transport_class][mtx_type][tp] = self.read_scenario(path, mtx_type, ass_class, tp)
        return matrices 

    def read_scenario(self, path, mtx_type, ass_class, tp):
        """Read travel cost and demand data for scenario from files"""
        file_name = mtx_type + '_' + tp + ".omx"
        file_path = os.path.join(path, file_name)
        file_data = omx.open_file(file_path)
        matrix_data = numpy.array(file_data[ass_class])
        file_data.close()
        if mtx_type == "cost":
            if ass_class == "transit_work":
                trips_per_month = numpy.full_like(matrix_data, 60)
                # Surrounding area has a lower number of trips per month
                trips_per_month[901:, :] = 44
                trips_per_month = 0.5 * (trips_per_month+trips_per_month.T)
                matrix_data = matrix_data / trips_per_month
            if ass_class == "transit_leisure":
                matrix_data = matrix_data / 30       
        return matrix_data
        
    def calc_revenue(self, ass_classes, ve0, ve1):
        """Calculate difference in producer revenue between scenarios ve1 and ve0"""
        revenue = 0
        for tp in self.emme_scenarios:
            for ass_class in ass_classes:
                demand_change = (
                    ve1[ass_class]["demand"][tp] - ve0[ass_class]["demand"][tp]) * param.volume_factors[ass_class][tp]
                cost_change = ve1[ass_class]["cost"][tp] - ve0[ass_class]["cost"][tp]
                revenue += (ve1[ass_class]["cost"][tp] * demand_change)[demand_change >= 0].sum() 
                revenue += (cost_change * ve0[ass_class]["demand"][tp])[demand_change >= 0].sum()
                revenue += (ve0[ass_class]["cost"][tp] * demand_change)[demand_change < 0].sum()
                revenue += (cost_change * ve1[ass_class]["demand"][tp])[demand_change < 0].sum()
        return revenue


    def calc_cost_gains(self, ve0, ve1, tp_coeffs):
        """Calculate difference in consumer surplus between scenarios ve1_tp_tp and ve0_tp"""
        gains = {"existing": 0, "additional": 0}
        for tp in self.emme_scenarios:
            tp_coeff = tp_coeffs[tp]
            demand_change = (ve1["demand"][tp] - ve0["demand"][tp]) * tp_coeff
            gain = ve1["cost"][tp] - ve0["cost"][tp]
            gains["existing"] += (ve0["demand"][tp] * tp_coeff * gain)[demand_change >= 0].sum()
            gains["additional"] += 0.5 * (demand_change * gain)[demand_change >= 0].sum()
            gains["existing"] += (ve1["demand"][tp] * tp_coeff * gain)[demand_change < 0].sum()
            gains["additional"] -= 0.5 * (demand_change * gain)[demand_change < 0].sum() 
        return gains


    def calc_gains(self, ve0, ve1, transport_class):
        """Calculate time, distance and cost gains"""
        gain_types = ["cost", "time", "dist"]
        gains = dict.fromkeys(gain_types)
        for gain_type in gain_types:
            gains[gain_type] = self.calc_cost_gains(
                {
                    "cost": ve0[transport_class][gain_type],
                    "demand": ve0[transport_class]["demand"],
                },
                {
                    "cost": ve1[transport_class][gain_type],
                    "demand": ve1[transport_class]["demand"],
                },
                param.volume_factors[transport_class]
            )
        return gains


    def read_miles(self, results_directory, scenario_name):
        """Read scenario data from files"""
        file_path = os.path.join(results_directory, scenario_name, "vehicle_kms.txt")
        return pandas.read_csv(file_path, delim_whitespace=True)


    def read_transit_miles(self, results_directory, scenario_name):
        """Read scenario data from files"""
        file_path = os.path.join(results_directory, scenario_name, "transit_kms.txt")
        return pandas.read_csv(file_path, delim_whitespace=True)


    def write_results_1(self, wb):
        """Write results for year 1"""
        ws = wb.get_sheet_by_name("ha_tyo")
        self.write_gains_1(ws, "car_work")
        ws = wb.get_sheet_by_name("ha_muu")
        self.write_gains_1(ws, "car_leisure")
        ws = wb.get_sheet_by_name("jl_tyo")
        self.write_gains_1(ws, "transit_work")
        ws = wb.get_sheet_by_name("jl_muu")
        self.write_gains_1(ws, "transit_leisure")
        ws = wb.get_sheet_by_name("pp_tyo")
        self.write_gains_1(ws, "bike_work")
        ws = wb.get_sheet_by_name("pp_muu")
        self.write_gains_1(ws, "bike_leisure")
        ws = wb.get_sheet_by_name("ka")
        self.write_gains_1(ws, "truck")
        ws = wb.get_sheet_by_name("yhd")
        self.write_gains_1(ws, "trailer_truck")
        ws = wb.get_sheet_by_name("pa")
        self.write_gains_1(ws, "van")
        ws = wb.get_sheet_by_name("Ulkoisvaikutukset")
        ws["I19"] = self.miles["car"][1]
        ws["J19"] = self.miles["car"][2]
        ws["K19"] = self.miles["car"][3]
        ws["L19"] = self.miles["car"][4]
        ws["M19"] = self.miles["car"][5]
        ws["I20"] = self.miles["van"][1]
        ws["J20"] = self.miles["van"][2]
        ws["K20"] = self.miles["van"][3]
        ws["L20"] = self.miles["van"][4]
        ws["M20"] = self.miles["van"][5]
        ws["I21"] = self.miles["truck"][1]
        ws["J21"] = self.miles["truck"][2]
        ws["K21"] = self.miles["truck"][3]
        ws["L21"] = self.miles["truck"][4]
        ws["M21"] = self.miles["truck"][5]
        ws["I22"] = self.miles["trailer_truck"][1]
        ws["J22"] = self.miles["trailer_truck"][2]
        ws["K22"] = self.miles["trailer_truck"][3]
        ws["L22"] = self.miles["trailer_truck"][4]
        ws["M22"] = self.miles["trailer_truck"][5]
        ws = wb.get_sheet_by_name("Tuottajahyodyt")
        ws["S8"] = self.transit_miles["dist"]["bus"]
        ws["S9"] = self.transit_miles["dist"]["trunk"]
        ws["S10"] = self.transit_miles["dist"]["tram"]
        ws["S11"] = self.transit_miles["dist"]["metro"]
        ws["S12"] = self.transit_miles["dist"]["train"]
        ws["T8"] = self.transit_miles["time"]["bus"]
        ws["T9"] = self.transit_miles["time"]["trunk"]
        ws["T10"] = self.transit_miles["time"]["tram"]
        ws["T11"] = self.transit_miles["time"]["metro"]
        ws["T12"] = self.transit_miles["time"]["train"]
        ws["E43"] = self.revenues["transit"]
        ws = wb.get_sheet_by_name("Julkistaloudelliset")
        ws["I8"] = self.revenues["car"]

    def write_gains_1(self, ws, ass_class):
        ws["E9"] = self.gains[ass_class]["time"]["existing"]
        ws["E10"] = self.gains[ass_class]["time"]["additional"]
        ws["E22"] = self.gains[ass_class]["dist"]["existing"]
        ws["E23"] = self.gains[ass_class]["dist"]["additional"]
        ws["E37"] = self.gains[ass_class]["cost"]["existing"]
        ws["E38"] = self.gains[ass_class]["cost"]["additional"]

    def write_results_2(self, wb):
        """Write results for year 2"""
        ws = wb.get_sheet_by_name("ha_tyo")
        self.write_gains_2(ws, "car_work")
        ws = wb.get_sheet_by_name("ha_muu")
        self.write_gains_2(ws, "car_leisure")
        ws = wb.get_sheet_by_name("jl_tyo")
        self.write_gains_2(ws, "transit_work")
        ws = wb.get_sheet_by_name("jl_muu")
        self.write_gains_2(ws, "transit_leisure")
        ws = wb.get_sheet_by_name("pp_tyo")
        self.write_gains_2(ws, "bike_work")
        ws = wb.get_sheet_by_name("pp_muu")
        self.write_gains_2(ws, "bike_leisure")
        ws = wb.get_sheet_by_name("ka")
        self.write_gains_2(ws, "truck")
        ws = wb.get_sheet_by_name("yhd")
        self.write_gains_2(ws, "trailer_truck")
        ws = wb.get_sheet_by_name("pa")
        self.write_gains_2(ws, "van")
        ws = wb.get_sheet_by_name("Ulkoisvaikutukset")
        ws["I32"] = self.miles["car"][1]
        ws["J32"] = self.miles["car"][2]
        ws["K32"] = self.miles["car"][3]
        ws["L32"] = self.miles["car"][4]
        ws["M32"] = self.miles["car"][5]
        ws["I33"] = self.miles["van"][1]
        ws["J33"] = self.miles["van"][2]
        ws["K33"] = self.miles["van"][3]
        ws["L33"] = self.miles["van"][4]
        ws["M33"] = self.miles["van"][5]
        ws["I34"] = self.miles["truck"][1]
        ws["J34"] = self.miles["truck"][2]
        ws["K34"] = self.miles["truck"][3]
        ws["L34"] = self.miles["truck"][4]
        ws["M34"] = self.miles["truck"][5]
        ws["I35"] = self.miles["trailer_truck"][1]
        ws["J35"] = self.miles["trailer_truck"][2]
        ws["K35"] = self.miles["trailer_truck"][3]
        ws["L35"] = self.miles["trailer_truck"][4]
        ws["M35"] = self.miles["trailer_truck"][5]
        ws = wb.get_sheet_by_name("Kayttajahyodyt")
        ws = wb.get_sheet_by_name("Tuottajahyodyt")
        ws["S16"] = self.transit_miles["dist"]["bus"]
        ws["S17"] = self.transit_miles["dist"]["trunk"]
        ws["S18"] = self.transit_miles["dist"]["tram"]
        ws["S19"] = self.transit_miles["dist"]["metro"]
        ws["S20"] = self.transit_miles["dist"]["train"]
        ws["T16"] = self.transit_miles["time"]["bus"]
        ws["T17"] = self.transit_miles["time"]["trunk"]
        ws["T18"] = self.transit_miles["time"]["tram"]
        ws["T19"] = self.transit_miles["time"]["metro"]
        ws["T20"] = self.transit_miles["time"]["train"]
        ws["E46"] = self.revenues["transit"]
        ws = wb.get_sheet_by_name("Julkistaloudelliset")
        ws["I13"] = self.revenues["car"]


    def write_gains_2(self, ws, ass_class):
        ws["E14"] = self.gains[ass_class]["time"]["existing"]
        ws["E15"] = self.gains[ass_class]["time"]["additional"]
        ws["E27"] = self.gains[ass_class]["dist"]["existing"]
        ws["E28"] = self.gains[ass_class]["dist"]["additional"]
        ws["E42"] = self.gains[ass_class]["cost"]["existing"]
        ws["E43"] = self.gains[ass_class]["cost"]["additional"]


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
    cba1 = CBA(args.baseline_scenario, args.projected_scenario)
    cba1.run_cost_benefit_analysis(args.results_path)
    cba1.write_results_1(wb)
    if args.baseline_scenario_2 is not None and args.baseline_scenario_2 != "undefined":
        cba2 = CBA(args.baseline_scenario_2, args.projected_scenario_2)
        cba2.run_cost_benefit_analysis(args.results_path)
        cba2.write_results_2(wb)
    results_filename =  "cba_{}_{}.xlsx".format(
        os.path.basename(args.projected_scenario),
        os.path.basename(args.baseline_scenario))
    wb.save(os.path.join(args.results_path, results_filename))
    print "CBA results saved to file: {}".format(results_filename)
