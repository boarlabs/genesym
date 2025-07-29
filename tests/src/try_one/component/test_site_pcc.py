from datetime import datetime
import pytz
import pytest 

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_one.load import Load
from src.try_one.parameters.load import LoadParameters
from src.try_one.parameters.intervals import Interval

from src.try_one.parameters.tariff_charges import EnergyImportChargeParameters
from src.try_one.energy_import_charge import EnergyImportCharge
from src.try_one.parameters.site import SiteParameters
from src.try_one.site_pcc import SitePCC

@pytest.mark.parameterize('site_limit', [30, 44, 45])
def test_model_basic_site(site_limit: float):

    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    load_params: LoadParameters = LoadParameters.read_load_data(
        intervals=intervals,
        load_vals=[44],
    )
    load = Load(model, load_params)

    energy_import_params = EnergyImportChargeParameters.create_energy_import_charges(
        intervals, 1.5
    )

    energy_import_model = EnergyImportCharge(
        model, energy_import_params
    )

    site_params = SiteParameters.create_constant_limit_site(
        intervals, site_limit, 10.0
    )

    site = SitePCC(model, [load], [energy_import_model], site_params)

    ortool_model = model._request.model

    vars = ortool_model.variable
    
    var_site_pout = vars[4]
    var_site_pin = vars[5]
    var_site_commit = vars[6]

    assert var_site_pout.lower_bound == 0 
    assert var_site_pout.upper_bound == 10
    assert var_site_pin.lower_bound == 0
    assert var_site_pin.upper_bound == site_limit
    assert var_site_commit.upper_bound == 1
    assert var_site_pin.name == "asset_group_constant_limit_site_P_in_t0"

    constrs = ortool_model.constraint

    constr_assetgroup_asset_bind1 = constrs[2]
    assert constr_assetgroup_asset_bind1.name == "asset_group_constant_limit_site_P_net_t0_asset_bind"
    assert constr_assetgroup_asset_bind1.var_index == [4,5,0,1]
    assert constr_assetgroup_asset_bind1.coefficient == [1,-1, -1, 1]
    assert constr_assetgroup_asset_bind1.upper_bound == 0

    constr_assetgroup_commit = constrs[3]
    assert constr_assetgroup_commit.name == "asset_group_constant_limit_site_P_out_complementarity_t0"
    assert constr_assetgroup_commit.var_index == [4,6]
    assert constr_assetgroup_commit.upper_bound == 0
    assert constr_assetgroup_commit.coefficient == [1.0 , -10.0]

    constr_assetgroup_commit2 = constrs[4]

    assert constr_assetgroup_commit2.name == "asset_group_constant_limit_site_P_in_complementarity_t0"
    assert constr_assetgroup_commit2.var_index == [5, 6]
    assert constr_assetgroup_commit2.coefficient == [1, site_limit]
    assert constr_assetgroup_commit2.upper_bound == site_limit

    model.solve_model(OptSense.minimize, {'solver': 'CBC'})

    ort_response = model._model_response
    if site_limit < 44:
        assert ort_response.status == 2
    else:
        variable_vals = ort_response.variable_value
        assert ort_response.objective_value == pytest.approx(44*1.5)
        assert variable_vals[0] == pytest.approx(0)
        assert variable_vals[1] == pytest.approx(44)
        assert variable_vals[2] == pytest.approx(0)
        assert variable_vals[3] == pytest.approx(44)
        assert variable_vals[4] == pytest.approx(0)
        assert variable_vals[5]  == pytest.approx(44)
    ck=1

      
if __name__ == "__main__":
    test_model_basic_site(50)