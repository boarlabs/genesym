
from datetime import datetime, timedelta
import pytz
import pytest
from typing import List
from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.demand_response_charge import DemandResponseCharge
from src.try_two.parameters.intervals import Interval
from src.try_two.parameters.tariff_charges import DemandResponseChargeParameters



def test_demand_response_only():
    model = Solver(client=Client(target="localhost:50051"))
    intervals: List[Interval] = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    demand_import_charge_params = DemandResponseChargeParameters.create_demand_response_charges(
        intervals, 2.2, (intervals[0].interval_end - timedelta(hours=1)).time(), intervals[0].interval_end.time()
    )
   
    assert demand_import_charge_params.P_in_max == [0]
    assert demand_import_charge_params.P_in_min == [0]
    assert demand_import_charge_params.P_out_max == [None]
    assert demand_import_charge_params.P_out_min == [0]

    demand_import_charge_params.P_in_max = [20]
    demand_import_charge_params.P_in_min  = [0]
    demand_import_charge_params.P_out_max = [10]
    demand_import_charge_params.P_out_min = [2]

    energy_import_model = DemandResponseCharge(
        model, demand_import_charge_params
    )

    ortool_model = model._request.model

    vars = ortool_model.variable

    var_pout = vars[0]
    assert var_pout.upper_bound == 10
    assert var_pout.lower_bound == 2
    assert var_pout.objective_coefficient == -2.2
    var_pin = vars[1]
    assert var_pin.upper_bound == 20
    assert var_pin.lower_bound == 0

    var_pin.objective_coefficient = 0.000001
    model.solve_model(OptSense.minimize, {})

    ort_response = model._model_response
    assert ort_response.variable_value == [10,0]
    assert ort_response.objective_value == pytest.approx(-10*2.2)

    ck=1
if __name__ == "__main__":
    test_demand_response_only()