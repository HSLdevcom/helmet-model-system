from utils.config import Config
from utils.log import Log
from emme_bindings.emme_project import EmmeProject
from datahandling.matrixdata import MatrixData
import results.assignment_analysis as assign_analysis
import results.matrix_operations as mtx_operations
import parameters
import pandas as pd
import numpy as np
from Tkinter import *
from tkFileDialog import *
import os

class Results:
    def __init__(self, config):
        """
        Helps end users with typical analysis cases.
        Uses Helmet-scenario specific emmebank and matrices.
        """
        # Emme-project
        emme_project_path = config.EMME_PROJECT_PATH
        try: 
            self.emme_project = EmmeProject(emme_project_path)
            self.emme_project.logger.info("Emme-project {}".format(emme_project_path))
        except: 
            self.emme_project.logger.error('Could not open Emme-project.')
        # Helmet-scenario name
        scenario_name = config.SCENARIO_NAME
        self.emme_project.logger.info("Helmet-scenario: {}".format(scenario_name))
        # Helmet-scenario matrices
        self.result_path = os.path.join(config.RESULTS_PATH, config.SCENARIO_NAME)
        self.matrices_path = os.path.join(self.result_path, "Matrices")
        try:
            self.resultmatrices = MatrixData(self.matrices_path)
            self.ass_classes = self.resultmatrices.list_matrices("demand", "aht")
            self.emme_project.logger.info("Matrices {}".format(self.result_path))
        except: 
            self.emme_project.logger.error('Could not open matrix files from {}.'.format(self.matrices_path))
        # Emme-scenario instances
        self.first_scenario_id = config.FIRST_SCENARIO_ID
        self.bike_scenario = self.first_scenario_id
        self.day_scenario = self.first_scenario_id+1
        self.emme_scenarios = {
            "aht": self.first_scenario_id+2,
            "pt": self.first_scenario_id+3,
            "iht": self.first_scenario_id+4,
        }
        emme_scenario = self.emme_project.modeller.emmebank.scenario(self.first_scenario_id + 2)
        self.zone_numbers = emme_scenario.zone_numbers
    
    def delete_emmebank_matrices(self):
        while True:
            try:
                lower_limit = int(input("Lower limit (id):"))
                upper_limit = int(input("Lower limit (id):"))
                mtxtype = str(raw_input("Matrix type (mo, md, mf, ms):"))
                break
            except ValueError:
                print("Value should be a whole number.")
        mtx_operations.del_emmebank_matrices(self.emme_project, mtxtype, lower_limit, upper_limit)

    def run_end_assignment(self):
        """ 
        Perform end assignment for current Helmet-scenario.
        """
        assign_analysis.end_assignment(self.emme_project, self.resultmatrices, self.first_scenario_id)

    def traffic_count(self):
        """ 
        Traffic counts comparisons
        """
        root = Tk()
        count_datapath = askopenfilename(
            filetypes=[('txt', '*.txt')],
            title='Choose txt-file containing the count data:',
            initialdir='%s/helmet/system-results' % (os.path.expanduser('~'))
            )
        root.withdraw()  
        try:  
            scen_id = int(input("Scenario id for the count data:"))
        except ValueError:
                print("Value should be a whole number.")
        attr = raw_input("Count data variable name (c_count, t_count, b_count):")
        assign_analysis.import_count_data(self.emme_project, scen_id, count_datapath, attr)
        self.emme_project.logger.info("Succesfully loaded count data from {} to scenario {}".format(count_datapath, scen_id))

    def sum_omx_24h(self):
        """
        Sum matrices to 24h with volume factors.
        Write to omx-files.
        """
        mtx_operations.mtx_to_24h(self.resultmatrices, self.zone_numbers, self.emme_scenarios)
        self.emme_project.logger.info("Saved 24h demand matrices to: {}".format(self.matrices_path))

    def aggregate_mtx(self):
        """ 
        Sum results with input data. Input data must 
        include columns "sij2019", "aggregation", "share" delimited
        by whitespace.
        """
        mtxtype = raw_input('Choose matrix type (demand, transit, transfers):')
        tp = raw_input('Choose time period (aht, iht, pt, day):')
        submatrices = self.resultmatrices.list_matrices(mtxtype, tp)
        root = Tk()
        agg_datapath = askopenfilename(
            filetypes=[('txt', '*.txt')],
            title='Choose txt-file containing the aggregation:',
            initialdir='%s/helmet/system-results' % (os.path.expanduser('~'))
            )
        root.withdraw()
        nr_zones = len(self.zone_numbers)
        try:
            aggregation_data = pd.read_csv(
                agg_datapath, delim_whitespace=True, squeeze=False, 
                keep_default_na=False, na_values="", comment='#', header="infer"
                )
            self.emme_project.logger.debug("Succesfully loaded agg data from {}".format(agg_datapath))
            mtxs = {}
            for submtx in submatrices:
                mtxs[submtx] = np.zeros((nr_zones, nr_zones))
            with self.resultmatrices.open(mtxtype, tp) as mtx:
                for name in submatrices:
                    mtxs[name] = mtx[name]
                    self.emme_project.logger.debug("Succesfully loaded matrix {}".format(name))          
        except:
            self.emme_project.logger.error('Tables could not be read') 
        colname = aggregation_data.columns[1]
        fname = "{}_{}_{}".format(colname, mtxtype, tp)
        mtx_operations.aggregate_matrix(aggregation_data, mtxs, self.result_path, self.zone_numbers, fname)
        self.emme_project.logger.info("Saved {} aggregated data".format(fname))

    def transit_modes_omx(self):
        emme_modes = ['b','g','m','p,t','w', 'r']
        no_mtx = len(emme_modes) * len(self.emme_scenarios.keys())
        self.emme_project.logger.info("Reads {} matrices to Emme-project".format(no_mtx)) 
        while True:
            try:
                mtx_id = int(input("Matrix id save results:"))
                break
            except ValueError:
                self.emme_project.logger.error("Value should be a whole number.")
        mtxdict = {}
        for tp in self.emme_scenarios:
            for emme_name in emme_modes:
                name = emme_name.replace(',', '')
                mtxdict[name] = {
                    'id':'mf' + str(mtx_id), 
                    'emme_mode':emme_name, 
                    'scenario':tp}
                mtx_id = mtx_id + 1
            mtx_operations.transit_mode_matrices(
                self.emme_project,
                self.emme_scenarios, 
                mtxdict)
            for name in mtxdict:
                mtxdict[name] = {'demand': mtx_operations.get_emme_matrix(self.emme_project, mtxdict[name]['id'])}
            mtx_operations.emme_matrices_to_omx(self.zone_numbers, self.resultmatrices, "transit", tp, mtxdict)

    def transfers_omx(self):
        select_limits = ['2,2','3,999']
        no_mtx = len(select_limits) * len(self.emme_scenarios.keys())
        self.emme_project.logger.info("Reads {} matrices to Emme-project".format(no_mtx))
        while True:
            try:
                mtx_id = int(input("Matrix id save results:"))
                break
            except ValueError:
                self.emme_project.logger.error("Value should be a whole number.")
        mtxdict = {}
        for tp in self.emme_scenarios:
            for limit in select_limits:
                name = 'transfers_' + limit.replace(',', '_')
                select_lower = int(limit.split(',')[0])
                select_upper = int(limit.split(',')[1])
                mtxdict[name] = {
                    'id':'mf' + str(mtx_id), 
                    'select_lower':select_lower, 
                    'select_upper':select_upper, 
                    'scenario':tp}
                mtx_id = mtx_id + 1
            mtx_operations.transfer_matrices(
                self.emme_project,
                self.emme_scenarios, 
                mtxdict)
            for name in mtxdict:
                mtxdict[name] = {'demand': mtx_operations.get_emme_matrix(self.emme_project, mtxdict[name]['id'])}
            mtx_operations.emme_matrices_to_omx(self.zone_numbers, self.resultmatrices, "transfers", tp, mtxdict)

def main():
    # define Helmet-scenario with user input
    root = Tk()
    config_datapath = askopenfilename(
        filetypes=[('json', '*.json')],
        title='Select json-file for scenario parameters:',
        initialdir=os.path.expanduser('~')
        )
    root.withdraw()  
    config = Config().read_from_file(config_datapath)
    # init logger
    logger = Log.get_instance().initialize(config)
    # start Emme and load matrices
    results = Results(config)
    while True:
        print "1. Clear Emme-project matrices"
        print "2. Assign bike, traffic and transit for current Helmet-project"
        print "3. Read external count data"
        print "4. Get transit modes to omx-files"
        print "5. Get transfer transit trips to omx-files"
        print "6. Expand demand matrices to 24h (save to omx)"
        print "7. Aggregate omx-matrix results"
        print "99. Quit"
        try:
            opt_chosen = int(raw_input("Choose:"))
            if opt_chosen == 99:  
                break
            elif opt_chosen == 1: 
                results.delete_emmebank_matrices()
            elif opt_chosen == 2: 
                results.run_end_assignment()
            elif opt_chosen == 3: 
                results.traffic_count()
            elif opt_chosen == 4: 
                results.transit_modes_omx()
            elif opt_chosen == 5: 
                results.transfers_omx()
            elif opt_chosen == 6: 
                results.sum_omx_24h()
            elif opt_chosen == 7: 
                results.aggregate_mtx()
            else:
                print "Error: Invalid choice. Please select between 1-7."
        except ValueError:
            print("Error: Value should be a whole number.") 
            pass
        
if __name__ == "__main__":
    main()
