from datetime import datetime
import pytz

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.parameters.intervals import Interval
from src.try_two.parameters.solar import SolarParameters
from src.try_two.solar import Solar

def test_simple_solar():

    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    solar_params = SolarParameters.read_solar_data(intervals, [32])

    solar = Solar(model, solar_params)


    ortool_model = model._request.model
    vars = ortool_model.variable
    variable_pout = vars[0]
    assert variable_pout.upper_bound ==32
    assert variable_pout.lower_bound ==0

    var_pin = ortool_model.variable[1]
    assert  var_pin.lower_bound == 0
    assert var_pin.upper_bound ==0

    constrs = ortool_model.constraint

    p_out_constr = constrs[0]
    assert p_out_constr.var_index == [0]
    assert p_out_constr.coefficient == [1]
    assert p_out_constr.lower_bound == 32
    assert p_out_constr.upper_bound == 32
    # assert p_out_constr.name == "load_uncontrollable_load_P_in_t0_power_balance"

    model.solve_model(OptSense.maximize, {})

    ort_response = model._model_response
    assert ort_response.variable_value == [32,0]
    




if __name__ == "__main__":
    test_simple_solar()