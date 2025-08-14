from typing import List
import argparse
from datetime import time

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.input_parser import InputData
from src.try_two.output_writer import OutputData
from src.try_two.parameters.intervals import Interval
from src.try_two.load import Load
from src.try_two.solar import Solar
from src.try_two.battery import Battery
from src.try_two.itc_site import ITCSite
from src.try_two.energy_import_charge import EnergyImportCharge
from src.try_two.energy_export_charge import EnergyExportCharge
from src.try_two.demand_import_charge import DemandImportCharge
from src.try_two.demand_response_charge import DemandResponseCharge
from src.try_two.parameters.tariff_charges import(
    EnergyImportChargeParameters,
    EnergyExportChargeParameters,
    DemandChargeParameters,
    DemandResponseChargeParameters,
)
from src.try_two.parameters.site import SiteParameters
from src.try_two.parameters.solar import SolarParameters
from src.try_two.parameters.battery import BatteryParameters
from src.try_two.parameters.load import LoadParameters

INPUT_DATA_PATH = "data/input_data.csv"
OUTPUT_DATA_PATH = "output/output_data_approach2.csv"




def run_optimization(
    price_energy_import: float=0.1,
    price_energy_export: float=0.03,
    price_peak_demand: float=9.0,
    price_demand_response: float=10.0,
):
    
    inputs: List[InputData] = InputData.read_csv_file(INPUT_DATA_PATH)
    
    intervals: List[Interval] = Interval.create_intervals_from_input(
        time_stamps=[input_data.time_stamp for input_data in inputs]
    )
    
    load_params: LoadParameters = LoadParameters.read_load_data(
        intervals=intervals,
        load_vals=[input_data.load for input_data in inputs],
    )
    solar_params: SolarParameters = SolarParameters.read_solar_data(
        intervals=intervals,
        solar_vals=[input_data.solar for input_data in inputs],
    )
    battery_params: BatteryParameters = BatteryParameters.load_constant_battery_data(
        intervals=intervals,
        initial_energy=0.0,
        energy_capacity=53.0,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
        min_soc=0.0,
        nominal_power=25.0,
    )
    site_params: SiteParameters = SiteParameters.create_constant_limit_site(
        intervals=intervals,
        P_in_limit=1000.0,   # PCC limits We don't need this in this particular example, a large number so that it does not bind
        P_out_limit=1000.0,
    )
    energy_import_charge_params: EnergyImportChargeParameters = EnergyImportChargeParameters.create_energy_import_charges(
        intervals=intervals,
        import_charge_rate=price_energy_import,
    )
    
    energy_export_charge_params: EnergyExportChargeParameters = EnergyExportChargeParameters.create_energy_export_charges(
        intervals=intervals,
        export_charge_rate=price_energy_export,
    )
    
    demand_charge_params: DemandChargeParameters = DemandChargeParameters.create_demand_charges(
        intervals=intervals,
        demand_charge_rate=price_peak_demand,
        demand_charge_period_start=time(hour=17, minute=0),
        demand_charge_period_end=time(hour=21, minute=0),
    )
    
    demand_response_charge_params: DemandResponseChargeParameters = DemandResponseChargeParameters.create_demand_response_charges(
        intervals=intervals,
        demand_response_charge_rate=price_demand_response,
        demand_response_period_start=time(hour=19, minute=0),
        demand_response_period_end=time(hour=20, minute=0),
    )
    
    
    model = Solver(client=Client(target="localhost:50051"))
    
    asset1: Load = Load(
        model=model,
        asset_params=load_params,
    )
    asset2: Solar = Solar(
        model=model,
        asset_params=solar_params,
    )
    asset3: Battery = Battery(
        model=model,
        asset_params=battery_params,
    )
    
    service1: EnergyImportCharge = EnergyImportCharge(
        model=model,
        service_params=energy_import_charge_params,
    )
    service2: EnergyExportCharge = EnergyExportCharge(
        model=model,
        service_params=energy_export_charge_params,
    )
    service3: DemandImportCharge = DemandImportCharge(
        model=model,
        service_params=demand_charge_params,
    )
    service4: DemandResponseCharge = DemandResponseCharge(
        model=model,
        service_params=demand_response_charge_params,
    )
    
    asset_group1: ITCSite = ITCSite(
        model=model,
        assets=[asset1, asset2, asset3],
        services=[service1, service2, service3, service4],
        asset_group_params=site_params,
    )
    
    
    model.solve_model(sense=OptSense.minimize, options={'solver': 'CBC'})
    
    print(model.get_objective_value())
    
    battery_ac_powers: List[float] = asset3.get_battery_ac_power_vars()
    site_ac_powers: List[float] = asset_group1.get_site_ac_power_vars()
    
    
    outputs: List[OutputData] = [
        OutputData(
            time=interval.interval_end - interval.interval_duration,
            battery_ac_power=battery_ac_powers[interval.index],
            ppc_meter_ac_power=site_ac_powers[interval.index],
        ) for interval in intervals
    ]
    
    OutputData.write_to_csv(OUTPUT_DATA_PATH, outputs)
    
    # var_vals = model.get_all_var_values()
    # dual_vars = model.get_dual_var_values()
    # print(dual_vars)
    # list = model.get_binding_constraints()
    
    
    return
    
    
    
    
                

def main():
    
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument(
        "-ip", "--import_price", type=float, default=0.1, help="price for imported energy per kwh"
    )
    cmd_parser.add_argument(
        "-ep",
        "--export_price",
        type=float,
        default=0.03, # having this default does not seem right, but I did not wish to make the parameter Optional
        help="price for exported energy per kwh",
    )
    cmd_parser.add_argument(
        "-pd",
        "--demand_price",
        type=float,
        default=9.0,
        help="price for peak demand  per kw",
    )
    cmd_parser.add_argument(
        "-dr",
        "--demand_response",
        type=float,
        default=10.0, 
        help="price for demand response per kwh",
    )
    args = cmd_parser.parse_args()
    
    
    run_optimization(
        args.import_price,
        args.export_price,
        args.peak_demand,
        args.demand_response,
    )



if __name__ == "__main__":
    main()