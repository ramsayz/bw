from pathlib import Path

bw_dir = Path.cwd() / "bridgewater"

def get_bw_file(pattern):
    pattern = pattern.lower()

    for f in bw_dir.glob("*.xls*"):
        if pattern in f.name.lower():
            print("Matched file:", f.name)
            return f

    raise ValueError(f"Bridgewater file not found: {pattern}")

nav_file_jpny  = get_bw_file("jpny isda aum")
nav_file_chase = get_bw_file("chase isda aum")

mtd_file = get_bw_file("client returns")



nav_jpny  = extract_nav(nav_file_jpny)
nav_chase = extract_nav(nav_file_chase)

import pandas as pd

nav_all = pd.concat([nav_jpny, nav_chase], ignore_index=True)

# if same ID appears in both → sum NAV
nav_all = nav_all.groupby("ID", as_index=False)["NAV"].sum()

print("NAV combined rows:", len(nav_all))

mtd_df = extract_mtd(mtd_file)

final_df = nav_all.merge(mtd_df, on="ID", how="left")



