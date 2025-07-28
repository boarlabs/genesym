import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class InputData:
    time_stamp: datetime
    load: float
    solar: float
    

    @staticmethod
    def read_csv_file(file_path: str) -> List["InputData"]:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            data = [
                InputData(
                    time_stamp=datetime.strptime(row[0], '%m/%d/%y %H:%M'),
                    load=float(row[1]),
                    solar=float(row[2]),                    
                ) for row in csv_reader
            ]
        return data
    


# if __name__ == "__main__":
#     data = InputData.read_csv_file('input_data.csv')
#     print(data[0].time_stamp)

