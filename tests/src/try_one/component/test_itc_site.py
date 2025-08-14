from datetime import datetime
import pytz
import pytest 

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.load import Load
from src.try_two.parameters.load import LoadParameters
from src.try_two.parameters.intervals import Interval

from src.try_two.parameters.tariff_charges import EnergyImportChargeParameters
from src.try_two.energy_import_charge import EnergyImportCharge
from src.try_two.parameters.site import SiteParameters
from src.try_two.itc_site import ITCSite
from src.try_two.solar import Solar
from src.try_two.battery import Battery
from src.try_two.parameters.solar import SolarParameters
from src.try_two.parameters.battery import BatteryParameters


def test_model_basic_site(site_limit: float):
    site_limit = 60
    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    load_params: LoadParameters = LoadParameters.read_load_data(
        intervals=intervals,
        load_vals=[44],
    )
    load = Load(model, load_params)

    solar_params = SolarParameters.read_solar_data(
        intervals, [32]
    )
    solar = Solar(model, solar_params)

    battery_params = BatteryParameters.load_constant_battery_data(
        intervals=intervals,
        initial_energy=10.0,
        energy_capacity=30.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
        min_soc=0.0,
        nominal_power=25.0,
    )
  
    battery = Battery(model, battery_params)

    energy_import_params = EnergyImportChargeParameters.create_energy_import_charges(
        intervals, 1.5
    )

    energy_import_model = EnergyImportCharge(
        model, energy_import_params
    )

    site_params = SiteParameters.create_constant_limit_site(
        intervals, site_limit, 10.0
    )

    site = ITCSite(model, [load,solar,battery], [energy_import_model], site_params)

    ortool_model = model._request.model

    vars = ortool_model.variable

    var_battery_pout = vars[4]
    var_battery_pin = vars[5]
    var_battery_pin.objective_coefficient = - 4
    var_site_pout = vars[10]
    var_site_pin = vars[11]
    var_site_commit = vars[12]

    assert var_site_pout.lower_bound == 0 
    assert var_site_pout.upper_bound == 10
    assert var_site_pin.lower_bound == 0
    assert var_site_pin.upper_bound == site_limit
    assert var_site_commit.upper_bound == 1
    assert var_site_pin.name == "asset_group_constant_limit_site_P_in_t0"

    constrs = ortool_model.constraint

    constr_assetgroup_asset_bind1 = constrs[7]
    assert constr_assetgroup_asset_bind1.name == "asset_group_constant_limit_site_P_net_t0_asset_bind"
    assert constr_assetgroup_asset_bind1.var_index == [10,11,0,2,4,1,3,5]
    assert constr_assetgroup_asset_bind1.coefficient == [1,-1, -1, -1,-1,1,1,1]
    assert constr_assetgroup_asset_bind1.upper_bound == 0

    constr_assetgroup_commit = constrs[8]
    assert constr_assetgroup_commit.name == "asset_group_constant_limit_site_P_out_complementarity_t0"
    assert constr_assetgroup_commit.var_index == [10,12]
    assert constr_assetgroup_commit.upper_bound == 0
    assert constr_assetgroup_commit.coefficient == [1.0 , -10.0]

    constr_assetgroup_commit2 = constrs[9]

    assert constr_assetgroup_commit2.name == "asset_group_constant_limit_site_P_in_complementarity_t0"
    assert constr_assetgroup_commit2.var_index == [11, 12]
    assert constr_assetgroup_commit2.coefficient == [1, site_limit]
    assert constr_assetgroup_commit2.upper_bound == site_limit

    model.solve_model(OptSense.minimize, {'solver': 'CBC'})

    ort_response = model._model_response
    var_vals = ort_response.variable_value
    assert var_vals[6] == pytest.approx(30)
    assert var_vals[9] == pytest.approx(44 - 32 + 21.0526)
    ck=1

      
if __name__ == "__main__":
    test_model_basic_site(50)