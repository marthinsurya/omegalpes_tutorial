"""
    ** Case Study Tutorial 1 - Energy Balance

"""

#Import required packages

import os

from pulp import LpStatus
from omegalpes.energy.energy_nodes import EnergyNode
from omegalpes.energy.units.consumption_units import FixedConsumptionUnit, \
    VariableConsumptionUnit
from omegalpes.energy.units.production_units import VariableProductionUnit, \
    FixedProductionUnit
from omegalpes.general.optimisation.model import OptimisationModel
from omegalpes.general.utils.plots import plot_quantity, plt, \
    plot_node_energetic_flows
from omegalpes.general.time import TimeUnit
from omegalpes.energy.energy_types import elec

# MAIN FUNCTION

def main(work_path,consumption_profile, pv_profile):

##step 1 create time period
    time = TimeUnit(periods=24*1, dt=1)

##step 2 create empty model
    model = OptimisationModel(time=time,
                          name='tutorial_1')

##step 3 create consumption unit
    house_cons_file = [p for p in map(float, consumption_profile)]

    house_consumption = \
        FixedConsumptionUnit(time, 'johns_consumption',
                         p=house_cons_file,
                         energy_type=elec)

##step 4 Create the production units = PV panels and the grid imports and exports
    pv_production_daily = [p for p in map(float, pv_profile)]


    pv_production = FixedProductionUnit(
        time, name='pv_production', p=pv_production_daily ,
        energy_type=elec)

    grid_import = VariableProductionUnit(time, 'grid_import',
                                             energy_type=elec,
                                             p_min=0)

    grid_export = VariableConsumptionUnit(time, 'grid_export',
                                               energy_type=elec,
                                               p_min=0)

##step 5 define objective
    grid_import.minimize_production()

##step 6 Create the energy nodes
    elec_node = EnergyNode(time, name="electrical_node",
                       energy_type=elec)

    elec_node.connect_units(grid_import, grid_export, pv_production,house_consumption)

##step 7 Add the energy nodes to the optimization model
    model.add_nodes(elec_node)

##step 8 Launch the optimization

    model.writeLP(work_path + r'\optim_models\tutorial_1.lp')
    model.solve_and_update()

##step 9 processing result
    plot_node_energetic_flows(elec_node)


    return model, time, pv_production, house_consumption, grid_export, grid_import, elec_node

# PROCESSING RESULT

##function to show results
def print_results():

    if LpStatus[MODEL.status] == 'Optimal':
        print("\n - - - - - OPTIMISATION RESULTS - - - - - ")
        print('House consumption = {0} kWh'.format(
            sum(HOUSE_CONSUMPTION.p.get_value())))
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
    CONSUMPTION_PROFILE = open("data/simulation purpose marthin/pv lv0/house con 24 kwh.csv", "r")
    PV_profile = open("data/simulation purpose marthin/pv lv0/pv prod 24 kwh.csv", "r")

    # *** RUN MAIN ***
    MODEL, TIME, PV_PRODUCTION, HOUSE_CONSUMPTION, GRID_EXPORT, GRID_IMPORT, NODE \
        = main(work_path=WORK_PATH, consumption_profile=CONSUMPTION_PROFILE, pv_profile=PV_profile)

    # Show results
    print_results()



