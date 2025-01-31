import pandas as pd
import typer


def aj_count(keyword: str , asorde : bool, wotby: str ):
    
    df = pd.read_csv("data/AJ.csv")
    df['name']=df['name'].astype(str).str.strip()
    fdf = df[df['name'].str.contains(keyword,case=False,na=False)]
    sdf = fdf.sort_values(by=wotby, ascending=asorde).reset_index(drop=True)
    return sdf

def print_aj_count(keyword: str, asorde : bool, wotby:str ):

    sdf = aj_count(keyword, asorde, wotby)
    print(sdf.to_string(index=False))

def entry_point():
    typer.run(print_aj_count)
