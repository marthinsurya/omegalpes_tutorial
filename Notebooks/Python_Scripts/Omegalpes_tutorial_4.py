"""
    ** Case Study Tutorial 4 - Cost comparison

"""

import os

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
from omegalpes.energy.energy_types import elec
from omegalpes.energy.units.storage_units import StorageUnit

def main(work_path,consumption_profile, pv_profile,op_cost_a,op_cost_b,export_cost):

##step 1 create time period
    time = TimeUnit(periods=24*1, dt=1)

##step 2 create empty model
    model = OptimisationModel(time=time,
                          name='tutorial_3')

##step 3 create fixed consumption unit
    house_cons_file = [p for p in map(float, consumption_profile)]

    house_consumption = \
        FixedConsumptionUnit(time, 'johns_consumption',
                         p=house_cons_file,
                         energy_type=elec)

##step 4 Create fixed production units = PV production
    pv_production_daily = [p for p in map(float, pv_profile)]


    pv_production = FixedProductionUnit(
        time, name='pv_production', p=pv_production_daily ,
        energy_type=elec)

##step 5 Create variable units


    grid_production_a = VariableProductionUnit(time=time,
                                          name='grid_production_A',
                                          energy_type=elec,
                                          operating_cost=op_cost_a)


    grid_production_b = VariableProductionUnit(time=time,
                                           name='grid_production_B',
                                           energy_type=elec,
                                           operating_cost=op_cost_b)


    grid_export = VariableConsumptionUnit(time, 'grid_export',
                                      energy_type=elec,
                                      p_min=0,operating_cost=export_cost)

##step 6 create storage unit
    storage = StorageUnit(time, name='storage', pc_max=1,
                          pd_max=1, soc_min=0.1,
                          soc_max=0.9, self_disch=0.01, ef_is_e0=True)


##step 7 define objective
    grid_production_a.minimize_operating_cost()
    grid_production_b.minimize_operating_cost()

##step 8 Create the energy nodes
    elec_node = EnergyNode(time, name="electrical_node",
                       energy_type=elec)

    elec_node.connect_units(pv_production, house_consumption, grid_production_a, grid_production_b, grid_export, storage)

##step 9 Add the energy nodes to the optimization model
    model.add_nodes(elec_node)

##step 10 Launch the optimization

    model.writeLP(work_path + r'\optim_models\tutorial_3.lp')
    model.solve_and_update()

##step 11 plot result
    plot_node_energetic_flows(elec_node)


    return model, time, pv_production, house_consumption, grid_export, grid_production_a,grid_production_b,elec_node, storage




# PROCESSING RESULT

##function to show results
def print_results():

    if LpStatus[MODEL.status] == 'Optimal':
        print("\n - - - - - OPTIMISATION RESULTS - - - - - ")
        print('House consumption = {0} kWh'.format(
            sum(HOUSE_CONSUMPTION.p.get_value())))
        print('PV production = {0} kWh'.format(
            sum(PV_PRODUCTION.p.get_value())))
        print('Energy surplus = {0} kWh'.format(
            sum(GRID_EXPORT.p.get_value())))
        print("The optimal storage capacity is {0} kWh".format(
            STORAGE.capacity.get_value()))
        print('Grid A production = {0} kWh'.format(
            GRID_PRODUCTION_A.e_tot.get_value()))
        print('Grid B production = {0} kWh'.format(
            GRID_PRODUCTION_B.e_tot.get_value()))
        print('Total Grid Import = {0} kWh'.format(
            sum(TOTAL_IMPORT.get_value())))

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
    CONSUMPTION_PROFILE = open("data/simulation purpose marthin/pv lv0/house tot con 24 kwh.csv", "r")
    PV_profile = open("data/simulation purpose marthin/pv lv0/pv prod 24 kwh.csv", "r")

    # Hourly operating costs for the first production unit
    OP_COST_A = [41.1, 41.295, 43.125, 51.96, 58.275,
                 62.955, 58.08, 57.705, 59.94, 52.8,
                 53.865,
                 46.545, 41.4, 39, 36.87,
                 36.6, 39.15, 43.71, 45.195, 47.04,
                 44.28, 39.975, 34.815, 28.38]

    # Hourly operating costs for the second production unit
    OP_COST_B = [58.82, 58.23, 51.95, 47.27, 45.49,
                 44.5, 44.5, 44.72, 44.22, 42.06,
                 45.7,
                 47.91, 49.57, 48.69, 46.91,
                46.51, 46.52, 51.59, 59.07, 62.1,
                 56.26, 55, 56.02, 52]

    EXPORT_COST = [50, 50, 50, 50, 50,
                           50, 50, 50, 50, 50,
                           50,
                           80, 80, 20, 30,
                           50, 50, 50, 50, 50,
                           50, 50, 50, 50]

    # *** RUN MAIN ***
    MODEL, TIME, PV_PRODUCTION, HOUSE_CONSUMPTION, GRID_EXPORT, GRID_PRODUCTION_A, GRID_PRODUCTION_B, NODE, STORAGE \
        = main(work_path=WORK_PATH, consumption_profile=CONSUMPTION_PROFILE, pv_profile=PV_profile,op_cost_a=OP_COST_A,op_cost_b=OP_COST_B,export_cost=EXPORT_COST)

    TOTAL_IMPORT = sum_quantities_in_quantity(quantities_list=[GRID_PRODUCTION_A.p, GRID_PRODUCTION_B.p])

    # Show results
    print_results()





