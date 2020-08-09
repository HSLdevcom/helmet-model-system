def main_program(self, scen_id, folder, version):
    
        ebank = _m.Modeller().emmebank
        desktop = _m.Modeller().desktop
        data_explorer = desktop.data_explorer()
        
        scen_list = [19, 20, 21, 22, 23]

        # bike network
		
		scen_id = scen_list[0]
        try:
            scen_xx = ebank.scenario(scen_id)
            data_explorer.replace_primary_scenario(scen_xx)
        except Exception, error:
            display('Could not change ', scen_id, ' to primary scenario')
            
        initiallze_network(self, scen_id, bike=True)
        read_network(self, scen_id, folder, version, bike=True)
        bike_functions(self, scen_id)
        
        # road and rail networks
        
        scen_id = scen_list[2]
        initiallze_network(self, scen_id, bike=False)
        read_network(self, scen_id, folder, version, bike=False)
        bus_stops(self, scen_id)
        
        delete_scenario(self, scen_list[1], scen_list[2])
        copy_scenario(self, scen_list[2], scen_list[1])
        delete_scenario(self, scen_list[3], scen_list[2])
        copy_scenario(self, scen_list[2], scen_list[3])
        delete_scenario(self, scen_list[4], scen_list[2])
        copy_scenario(self, scen_list[2], scen_list[4])]
        
        period_list = ['aht', 'pt', 'iht']
        attr_list_line = [@hwaht, @hwpt, @hwiht]
        attr_list_link = [@hinah, @hinpt, @hinih]
                
        for k in range(3):
            modify_function_parameters(self, scen_list[k+2], period_list[k])
            copy_attribute(self, scen_list[k+2], 'line', attr_list_line[k], 'hdwy')
            copy_attribute(self, scen_list[k+2], 'link', attr_list_link[k], '@hinta')
            check_network(self, scen_list[k+2])   # method still missing
   