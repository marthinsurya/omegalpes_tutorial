import os

from pulp import LpStatus
from omegalpes.actor.operator_actors.consumer_producer_actors import \
    Prosumer, Supplier
from omegalpes.energy.energy_nodes import EnergyNode
from omegalpes.energy.units.consumption_units import FixedConsumptionUnit, \
    VariableConsumptionUnit
from omegalpes.energy.units.production_units import VariableProductionUnit, \
    FixedProductionUnit, SeveralProductionUnit, SeveralImaginaryProductionUnit
from omegalpes.general.optimisation.model import OptimisationModel
from omegalpes.general.utils.plots import plot_quantity, plt, \
    plot_node_energetic_flows
from omegalpes.general.time import TimeUnit
from omegalpes.energy.energy_types import elec

def main():

#step 2 create time period
    time = TimeUnit(periods=24*1, dt=1)

#step 1 create empty model
    model = OptimisationModel(time=time,
                          name='tutorial')

#step 3 create consumption unit
    CONSUMPTION_PROFILE = open("data/Building_consumption_day.txt", "r")

    building_cons_file = [p for p in map(float, CONSUMPTION_PROFILE)]

    building_consumption = \
        FixedConsumptionUnit(time, 'building_consumption',
                         p=building_cons_file,
                         energy_type=elec)

#step 4 Create the production units = PV panels and the grid imports and exports
    pv_production_file = open("data/pv_production_hourly2.csv",
                            "r")
    pv_production_daily = [p for p in map(float, pv_production_file)]


    pv_production = FixedProductionUnit(
        time, name='pv_production', p=pv_production_daily ,
        energy_type=elec)

    grid_import = VariableProductionUnit(time, 'grid_import',
                                             energy_type=elec,
                                             p_min=0)

    grid_export = VariableConsumptionUnit(time, 'grid_export',
                                               energy_type=elec,
                                               p_min=0)

#step 5 define objective
    grid_import.minimize_production()

#step 6 Create the energy nodes
    elec_node = EnergyNode(time, name="elec_node",
                       energy_type=elec)

    elec_node.connect_units(grid_import, grid_export, pv_production,building_consumption)

#step 7 Add the energy nodes to the optimization model
    model.add_nodes(elec_node)

#step 8 Launch the optimization

    model.writeLP(WORK_PATH + r'\optim_models\om_tut1.lp')
    model.solve_and_update()

#step 9 plot result
    plot_node_energetic_flows(elec_node)
    #plt.show()


    #if LpStatus[model.status] == 'Optimal':
     #   print("\n - - - - - OPTIMIZATION RESULTS - - - - - ")
      #  print('Building consumption = {0} kWh.'.format(sum(
       #    building_consumption.p.get_value())))
        #print('Pv production = {0} kWh.'.format(sum(
         #   pv_production.p.get_value())))
        #print('grid_export = {0} kWh'.format(
        #    grid_export.p.get_value()))
        #print('grid_import = {0} kWh'.format(
        #   grid_import.p.get_value()))
        #print('grid_import = {0} kWh'.format(sum(
        #    grid_import.p.get_value())))

        #plt.plot(building_consumption.p.get_value())
        #legend1 += ['grid import']

        #plt.legend(legend1)

    plt.show()

   # elif LpStatus[MODEL.status] == 'Infeasible':
    #    print("Sorry, the optimisation problem has no feasible solution !")

#    elif LpStatus[MODEL.status] == 'Unbounded':
 #       print("The cost function of the optimisation problem is unbounded !")

  #  elif LpStatus[MODEL.status] == 'Undefined':
   #     print("Sorry, a feasible solution has not been found (but may exist). "
    #          "PuLP does not manage to interpret the solver's output, "
     #         "the infeasibility of the MILP problem may have been "
      #        "detected during presolve")

    #else:
    #    print("Sorry, the optimisation problem has not been solved.")

    return model, time, building_consumption, grid_export, grid_import

if __name__ == "__main__":
    WORK_PATH = os.getcwd()

    # *** RUN MAIN ***
    MODEL, TIME, BUILDING_CONSUMPTION, GRID_EXPORT, GRID_IMPORT \
    = main()
    #main()




