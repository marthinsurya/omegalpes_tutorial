"""
    ** Case Study Tutorial 4 - Storage & Shiftable consumption

"""

import os
import pandas as pd

from pulp import LpStatus
from omegalpes.energy.energy_nodes import EnergyNode
from omegalpes.energy.units.consumption_units import FixedConsumptionUnit, \
    VariableConsumptionUnit, ShiftableConsumptionUnit
from omegalpes.energy.units.production_units import VariableProductionUnit, \
    FixedProductionUnit, SeveralProductionUnit, SeveralImaginaryProductionUnit
from omegalpes.general.optimisation.model import OptimisationModel
from omegalpes.general.utils.plots import plot_quantity, plt, \
    plot_node_energetic_flows,plot_quantity_bar,sum_quantities_in_quantity
from omegalpes.general.time import TimeUnit
from omegalpes.energy.energy_types import elec,thermal
from omegalpes.energy.units.conversion_units import \
    ElectricalToThermalConversionUnit
from omegalpes.energy.units.storage_units import StorageUnit

def main(work_path,consumption_profile, pv_profile,wm_profile,dhw_profile):

##step 1 create time period
    time = TimeUnit(periods=24*1, dt=1)

##step 2 create empty model
    model = OptimisationModel(time=time,
                          name='tutorial_4')

##step 3 create fixed consumption unit
    house_cons_file = [p for p in map(float, consumption_profile)]


    house_consumption = \
    FixedConsumptionUnit(time, 'johns_consumption_minus_washing_machine',
                         p=house_cons_file,
                         energy_type=elec)

    dhw_load = dhw_profile['kwh'].tolist()

    dhw = FixedConsumptionUnit(time, name="domestic_hot_water", p=dhw_load,
                               energy_type=thermal)

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


##step 6 Create conversion unit & Storage Unit
    water_heater = ElectricalToThermalConversionUnit(
        time, name="water_heater", elec_to_therm_ratio=0.9)

    water_tank = StorageUnit(time, name="water_tank", self_disch_t=0.05,
                             soc_min=0.2, energy_type=thermal,
                         ef_is_e0=True, capacity=6000)

##step 7 define objective
    grid_import.minimize_production()

##step 8 Create the energy nodes
    elec_node = EnergyNode(time, name="elec_node",
                       energy_type=elec)


    elec_node.connect_units(pv_production, house_consumption, grid_import, grid_export, wm_consumption,
                        water_heater.elec_consumption_unit)


    heat_node = EnergyNode(time, name="heat_node",
                       energy_type=thermal)

    heat_node.connect_units(dhw, water_tank, water_heater.thermal_production_unit)

##step 9 Add the energy nodes to the optimization model
    model.add_nodes(elec_node, heat_node)

##step 10 Launch the optimization

    model.writeLP(work_path + r'\optim_models\tutorial_4.lp')
    model.solve_and_update()

##step 11 plot result
    plot_node_energetic_flows(elec_node)
    plot_node_energetic_flows(heat_node)


    return model, time, pv_production, house_consumption, grid_export, grid_import, elec_node, wm_consumption, dhw

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
    CONSUMPTION_PROFILE = open("data/simulation purpose marthin/pv lv0/house con 24.csv", "r")
    PV_profile = open("data/simulation purpose marthin/pv lv0/pv prod 24.csv", "r")
    WASHING_MACHINE_PROFILE = open("data/simulation purpose marthin/pv lv0/washer 24.csv", "r")
    DOMESTIC_HOT_WATER = pd.read_csv("./data/simulation purpose marthin/pv lv0/DHW 24.csv", sep=';')

    # *** RUN MAIN ***
    MODEL, TIME, PV_PRODUCTION, HOUSE_CONSUMPTION, GRID_EXPORT, GRID_IMPORT, NODE, WASHING_MACHINE_CONSUMPTION, DOMESTIC_HOT_WATER \
        = main(work_path=WORK_PATH, consumption_profile=CONSUMPTION_PROFILE, pv_profile=PV_profile,wm_profile=WASHING_MACHINE_PROFILE,dhw_profile=DOMESTIC_HOT_WATER)

    TOTAL_CONSUMPTION = sum_quantities_in_quantity(quantities_list=[HOUSE_CONSUMPTION.p, WASHING_MACHINE_CONSUMPTION.p])

    # Show results
    print_results()

