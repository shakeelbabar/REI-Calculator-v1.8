from pandas import DataFrame, IndexSlice

def set_dataframe_style():
    """Set style for dataframe in charge of storing all final calculations"""
    df.style.set_properties(
        **{"background-color": "green", "color": "white", "border-color": "white"},
        subset=IndexSlice[1, ["id", "count", "type"]]
    )
