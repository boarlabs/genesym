import pandas as pd
from pathlib import Path

def read_model_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)





def main():
    

    current_file = Path(__file__).resolve()
    root_path = current_file.parent.parent.parent
    df_cvx = read_model_data(root_path / "src/optimization/data/output_data.csv")
    df_new = read_model_data(root_path / "src/try_one/data/output_data.csv")

    df_delta = df_new.copy()
    df_delta["battery_delta"] = df_new['AC Battery Power (kW)'] - df_cvx['AC Battery Power (kW)']

    ck=1






if __name__ == "__main__":
    main()