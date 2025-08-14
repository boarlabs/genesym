from datetime import datetime
import pytz

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.load import Load
from src.try_two.parameters.load import LoadParameters
from src.try_two.parameters.intervals import Interval
def test_setup_model_with_asset_only():

    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    load_params: LoadParameters = LoadParameters.read_load_data(
        intervals=intervals,
        load_vals=[44],
    )
    load = Load(model, load_params)


    ortool_model = model._request.model

    variable_pout = ortool_model.variable[0]
    assert variable_pout.upper_bound ==0
    assert variable_pout.lower_bound ==0

    var_pin = ortool_model.variable[1]
    assert  var_pin.lower_bound == 0
    assert var_pin.upper_bound ==44

    constrs = ortool_model.constraint

    p_in_constr = constrs[0]
    assert p_in_constr.var_index == [1]
    assert p_in_constr.coefficient == [1]
    assert p_in_constr.lower_bound == 44
    assert p_in_constr.upper_bound == 44
    assert p_in_constr.name == "load_uncontrollable_load_P_in_t0_power_balance"

    model.solve_model(OptSense.maximize, {})

    ort_response = model._model_response
    assert ort_response.variable_value == [0,44]
    





if __name__ == "__main__":
    test_setup_model_with_asset_only()