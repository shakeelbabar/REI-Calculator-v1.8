from pandas import DataFrame, IndexSlice

ana_and_res_table = ""
inc_exp_cash_flow_graph = ""

def create_html():
    html_template = f"""
    <html>
    <body>
    <img alt='logo' src='' />
    <h1>"Property Address" Report</h1>
    ...pictures...
    {ana_and_res_table}
    <br>
    {inc_exp_cash_flow_graph}
    </body>
    </html>
    """

def general_analysis_and_results(values):
    df = DataFrame(values, columns=['a', 'b', 'c'])   
    
    df['titles1'] = ['Cash to Close', 'Monthly Expenses', 'NOI', 'Cap Rate']
    df['titles2'] = ['Purchase Price', 'Monthly Cash Flow', 'NIAF', '1% Rule']
    df['titles3'] = ['Monthly Income', '50% Rule', 'Cash on Cash', 'Gross Rent Mult.']
    
    # re-order columns
    df = df[['titles1', 'a', 'titles2', 'b', 'titles3', 'c']]


def set_dataframe_style():
    """Set style for dataframe in charge of storing all final calculations"""
    df.style.set_properties(
        **{"background-color": "green", "color": "white", "border-color": "white"},
        subset=IndexSlice[1, ["id", "count", "type"]]
    )
