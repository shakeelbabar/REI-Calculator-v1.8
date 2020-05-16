from pandas import DataFrame, IndexSlice
from PyQt5.QtCore import QSettings
import matplotlib.pyplot as plt
from numpy import arange

logo_html = ""
property_address = ""
images_html = ""
ana_and_res_table_html = ""
inc_exp_cash_flow_graph_html = ""
ten_year_pro_forma_html = ""

def generate_report(gen_analysis_data, data, plot_data, property_data):
    global logo_html
    global property_address
    global images_html
    global ana_and_res_table_html
    global inc_exp_cash_flow_graph_html
    global ten_year_pro_forma_html
               
    logo_html = "<img alt='SFI white (logo)' src='logo.png' />"
    
    property_address = (
        '<ul class="list-group">'
        f'<li>address: {property_data["address"]}</li>'
        f'<li>city: {property_data["city"]}</li>'
        f'<li>state: {property_data["state"]}</li>'
        f'<li>zip code: {property_data["zipcode"]}</li>'
        f'<li>prior year taxes: {property_data["prior_year_taxes"]}</li>'
        f'<li>landford insurance: {property_data["landford_insurance"]}</li>'
        '</ul>'
    )
    
    # TODO: images
    images = ['fortesting.png', 'fortesting.png']
    images_html = images_to_html(images)
    
    # general analysis and results
    ana_and_res_table_html = analysis_and_results_to_html(gen_analysis_data)
    
    inc_exp_cash_flow_graph_html = graph_to_html(plot_data)
    
    # 10-year Pro-Forma
    ten_year_pro_forma_html = ten_year_pro_forma_to_html(data)    
    
    html = create_report_html()
    
    try:
        with open('report.html', 'w') as f:
            f.write(html)
    except Exception as ex:
        print("generate_report, exception:", ex)
        return None
    
    return 'report.html'
    
def graph_to_html(data):
    fig, ax = plt.subplots()
    
    x = data.columns.values.tolist()
    max_y = 60000
    step = 10000
    #plt.yticks(arange(1300, max_y, step=step))
    ax.plot(x, data.iloc[0, :], label='Total Income')
    ax.plot(x, data.iloc[1, :], label='Total Expenses')
    ax.plot(x, data.iloc[2, :], label='NIAF')    
    #plt.plot(x, y, 'r')  # blue stars    
    legend = ax.legend(loc='best', shadow=False, fontsize='x-large')       
    fig.savefig('plot.png')
    
    return f'<img src="plot.png" />'
    
def images_to_html(images):
    html = ''
    for img in images:
        html += f'<img src="{img}" />'        
    return html

def ten_year_pro_forma_to_html(data):
    settings = QSettings("calculator_settings")
    caption_bgcolor = settings.value('caption_bgcolor')
    special_row_bgcolor = settings.value('special_row_bgcolor')
    
    index_labels = ["Total Income", "Total Expenses", "Fixed Expenses",
                    "Variable Expenses", "NOI", "NOI Growth",
                    "Debt Service", "NIAF", "Property Value",
                    "Cash on Cash Return", "Cum. CoCR", "Total Equity",
                    "Percent of Equity", "ROI", "Total Profit If Sold", "CAGR if Sold"]
    
    df = DataFrame.from_dict(data)    
    df['labels'] = index_labels
    years = range(1, 10)    
    selected_columns = [f'Year_{index}' for index in years]    
    selected_rows = [4,7, 13]
    df = df[['labels'] + selected_columns]
    df.rename(columns={'labels':'---'}, inplace=True)
    
    df_final = df.style.set_properties(**{
                            'background-color': special_row_bgcolor,
                            'color': 'white',
                            }, 
                            subset=IndexSlice[selected_rows, selected_columns]
    )
    
    df_final = df_final.set_properties(**{
                            'background-color': caption_bgcolor,
                            'color': 'black'
                            }, 
                            subset=IndexSlice[:, '---']                            
    ).hide_index()
    
    return df_final.render()
            
def create_report_html():
    html_template = (
        "<html>"
        "<head>"
        "<title>Report</title>"
        "<meta charset='UTF-8'>"
        "<link href='bootstrap-4.4.1-dist/css/bootstrap.min.css' rel='stylesheet'>"
        "</head>"
        "<body>"
        "<div class='container'>"
        f"<div>{logo_html}</div>"
        f"<div>{property_address}</div>"
        "<br>"
        f"{images_html}"
        "<h3>General Analysis and Results</h3>"
        f"<div>{ana_and_res_table_html}</div>"
        "<br>"
        f"<div>{inc_exp_cash_flow_graph_html}</div>"
        "<br>"
        f"<div>{ten_year_pro_forma_html}</div>"
        "</div>"
        "</body>"
        "</html>"
    )
    return html_template

def analysis_and_results_to_html(values):
    df = DataFrame(values, columns=['a', 'b', 'c'])       
    df['titles1'] = ['Cash to Close', 'Monthly Expenses', 'NOI', 'Cap Rate']
    df['titles2'] = ['Purchase Price', 'Monthly Cash Flow', 'NIAF', '1% Rule']
    df['titles3'] = ['Monthly Income', '50% Rule', 'Cash on Cash', 'Gross Rent Mult.']
    
    # re-order columns
    ordered_columns = ['titles1', 'a', 'titles2', 'b', 'titles3', 'c']
    df = df[ordered_columns]
    
    # hide columns and index
    return df.to_html(header=None, index=False)


def set_dataframe_style():
    """Set style for dataframe in charge of storing all final calculations"""
    df.style.set_properties(
        **{"background-color": "green", "color": "white", "border-color": "white"},
        subset=IndexSlice[1, ["id", "count", "type"]]
    )
