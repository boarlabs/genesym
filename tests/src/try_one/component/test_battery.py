


from datetime import datetime
import pytz
import pytest

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.parameters.intervals import Interval
from src.try_two.parameters.battery import BatteryParameters
from src.try_two.battery import Battery

def test_simple_battery():

    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    battery_params = BatteryParameters.load_constant_battery_data(
        intervals=intervals,
        initial_energy=10.0,
        energy_capacity=53.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
        min_soc=0.0,
        nominal_power=25.0,
    )
  
    solar = Battery(model, battery_params)


    ortool_model = model._request.model
    vars = ortool_model.variable
    variable_pout = vars[0]
    assert variable_pout.upper_bound == 25
    assert variable_pout.lower_bound == 0
    variable_pout.objective_coefficient = 1.5

    var_pin = ortool_model.variable[1]
    assert  var_pin.lower_bound == 0
    assert var_pin.upper_bound == 25
    var_soc = ortool_model.variable[2]
    assert var_soc.lower_bound == 0
    assert var_soc.upper_bound == 53
    constrs = ortool_model.constraint

    p_in_compl = constrs[2]
    assert p_in_compl.name == "battery_basic_battery_P_in_complementarity_t0"
    assert p_in_compl.upper_bound == 25
    assert p_in_compl.var_index == [1,3]
    assert p_in_compl.coefficient == [1,25]
    
    model.solve_model(OptSense.maximize, {'solver': 'CBC'})

    ort_response = model._model_response
    assert ort_response.variable_value == pytest.approx([9.5,0,0,1])
    ck=1





if __name__ == "__main__":
    test_simple_battery()