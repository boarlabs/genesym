from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass
import csv



output_name_map: Dict[str, str] = dict(
    time="Time",
    battery_ac_power="AC Battery Power (kW)",
    ppc_meter_ac_power="Grid Meter (kW)",
)




    
    
@dataclass
class OutputData:
    time: datetime
    battery_ac_power: float
    ppc_meter_ac_power: float
    
    
    @staticmethod
    def write_to_csv(file_path: str, outputs: List["OutputData"]):
        
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([output_name_map[k] for k in output_name_map.keys()])
            for d in outputs:
                writer.writerow([d.time, d.battery_ac_power, d.ppc_meter_ac_power])
    
    
    
    
    
    