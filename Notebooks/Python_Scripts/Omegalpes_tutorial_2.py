"""
    ** Case Study Tutorial 2 - Storage & Shiftable consumption

"""

import os

from pulp import LpStatus
from omegalpes.energy.energy_nodes import EnergyNode
from omegalpes.energy.units.consumption_units import FixedConsumptionUnit, \
    VariableConsumptionUnit, ShiftableConsumptionUnit
from omegalpes.energy.units.production_units import VariableProductionUnit, \
    FixedProductionUnit
from omegalpes.general.optimisation.model import OptimisationModel
from omegalpes.general.utils.plots import plot_quantity, plt, \
    plot_node_energetic_flows,plot_quantity_bar,sum_quantities_in_quantity
from omegalpes.general.time import TimeUnit
from omegalpes.energy.energy_types import elec
from omegalpes.energy.units.storage_units import StorageUnit

def main(work_path,consumption_profile, pv_profile,wm_profile):

##step 1 create time period
    time = TimeUnit(periods=24*1, dt=1)

##step 2 create empty model
    model = OptimisationModel(time=time,
                          name='tutorial_2')

##step 3 create fixed consumption unit
    house_cons_file = [p for p in map(float, consumption_profile)]


    house_consumption = \
    FixedConsumptionUnit(time, 'johns_consumption_minus_washing_machine',
                         p=house_cons_file,
                         energy_type=elec)



##step 4 Create fixed production units = PV production
    pv_production_daily = [p for p in map(float, pv_profile)]


    pv_production = FixedProductionUnit(
        time, name='pv_production', p=pv_production_daily ,
        energy_type=elec)

##step 5 Create variable units
    grid_import = VariableProductionUnit(time, 'grid_import',
                                             energy_type=elec,
                                             p_min=0)

    grid_export = VariableConsumptionUnit(time, 'grid_export',
                                               energy_type=elec,
                                               p_min=0)

    wm_cons_file = [p for p in map(float, wm_profile)]

    wm_consumption = ShiftableConsumptionUnit(time, 'washing_machine_consumption', power_values=wm_cons_file,
                                          energy_type=elec)
##step 6 create storage unit
    storage = StorageUnit(time, name='storage', pc_max=1,
                          pd_max=1, soc_min=0.1,
                          soc_max=0.9, self_disch=0.01, ef_is_e0=True)

##step 7 define objective
    grid_import.minimize_production()

##step 8 Create the energy nodes
    elec_node = EnergyNode(time, name="elec_node",
                       energy_type=elec)

    elec_node.connect_units(pv_production,house_consumption,grid_import, grid_export,storage,wm_consumption)


##step 9 Add the energy nodes to the optimization model
    model.add_nodes(elec_node)

##step 10 Launch the optimization

    model.writeLP(work_path + r'\optim_models\tutorial_2.lp')
    model.solve_and_update()


##step 11 plot result
    plot_node_energetic_flows(elec_node)

    # #plot house consumption and pv production
    # fig4 = plt.figure(4)
    # ax4 = plt.axes()
    # wm_consumption_fix = FixedProductionUnit(time, 'washing_machine_consumption', p=wm_cons_file,
    #                                       energy_type=elec)
    # plot_quantity(time, house_consumption.p, fig4, ax4, label='John consumption w/o washing machine', title='John consumption profile',color='g')
    # plot_quantity(time, wm_consumption_fix.p, fig4, ax4, label='Washing machine consumption', title='John consumption profile',color='r')
    # plt.xlabel('Time (hours)')
    # plt.ylabel('Hourly mean power (kW)')
    # ax4.legend()

    return model, time, pv_production, house_consumption, grid_export, grid_import, elec_node, wm_consumption, storage


# PROCESSING RESULT

##function to show results
def print_results():

    if LpStatus[MODEL.status] == 'Optimal':
        print("\n - - - - - OPTIMISATION RESULTS - - - - - ")
        print('House consumption = {0} kWh'.format(
            sum(TOTAL_CONSUMPTION.get_value())))
        print('PV production = {0} kWh'.format(
            sum(PV_PRODUCTION.p.get_value())))
        print('Grid import = {0} kWh'.format(
            sum(GRID_IMPORT.p.get_value())))
        print('Energy surplus = {0} kWh'.format(
            sum(GRID_EXPORT.p.get_value())))
        print("The optimal storage capacity is {0} kWh".format(
            STORAGE.capacity.get_value()))

        plt.show()

    elif LpStatus[MODEL.status] == 'Infeasible':
        print("Sorry, the optimisation problem has no feasible solution !")

    elif LpStatus[MODEL.status] == 'Unbounded':
        print("The cost function of the optimisation problem is unbounded !")

    elif LpStatus[MODEL.status] == 'Undefined':
        print("Sorry, a feasible solution has not been found (but may exist). "
              "PuLP does not manage to interpret the solver's output, "
              "the infeasibility of the MILP problem may have been "
              "detected during presolve.")

    else:
        print("Sorry, the optimisation problem has not been solved.")

if __name__ == "__main__":
    # OPTIMIZATION PARAMETERS #
    WORK_PATH = os.getcwd()
    CONSUMPTION_PROFILE = open("data/simulation purpose marthin/pv lv0/house con 24 kwh wo wm.csv", "r")
    PV_profile = open("data/simulation purpose marthin/pv lv0/pv prod 24 kwh.csv", "r")
    WASHING_MACHINE_PROFILE = open("data/simulation purpose marthin/pv lv0/washer 24 kwh.csv", "r")



    # *** RUN MAIN ***
    MODEL, TIME, PV_PRODUCTION, HOUSE_CONSUMPTION, GRID_EXPORT, GRID_IMPORT, NODE, WASHING_MACHINE_CONSUMPTION, STORAGE \
        = main(work_path=WORK_PATH, consumption_profile=CONSUMPTION_PROFILE, pv_profile=PV_profile,wm_profile=WASHING_MACHINE_PROFILE)

    TOTAL_CONSUMPTION = sum_quantities_in_quantity(quantities_list=[HOUSE_CONSUMPTION.p, WASHING_MACHINE_CONSUMPTION.p])

    # Show results
    print_results()


