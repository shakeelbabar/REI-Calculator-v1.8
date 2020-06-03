from pandas import DataFrame, IndexSlice
from PyQt5.QtCore import QSettings
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numpy import arange

logo_html = ""
property_address = ""
images_html = ""
ana_and_res_table_html = ""
inc_exp_cash_flow_graph_html = ""
ten_year_pro_forma_html = ""

def generate_report(gen_analysis_data, data, data_30_years, plot_data, property_data, tab1data, tab2data, property_images):
    global logo_html
    global property_address
    global images_html
    global ana_and_res_table_html
    global inc_exp_cash_flow_graph_html
    global ten_year_pro_forma_html
    global Full_Proforma_Section
    global Table_One_Section
    global Table_Two_Section
               
    logo_html = "<img alt='SFI white (logo)' src='logo.png' />"

    print("Setting Propery Data")
    property_address = (
        "<div class='card'>"
            "<h3 class='card-header bg-dark text-white'>Property Information</h3>"
            "<div class='card-body'>"
                "<dl class='row'>"
                    f'<dt class="col-6">Address:</dt><dd>{property_data["address"]}</dd>'
                    f'<dt class="col-6">City:</dt><dd>{property_data["city"]}</dd>'
                    f'<dt class="col-6">State:</dt><dd>{property_data["state"]}</dd>'
                    f'<dt class="col-6">Zip Code:</dt><dd>{property_data["zipcode"]}</dd>'
                    f'<dt class="col-6">Prior Year Taxes:</dt><dd>{"${:,.0f}".format(property_data["prior_year_taxes"])}</dd>'
                    f'<dt class="col-6">Landford Insurance:</dt><dd>{"${:,.0f}".format(property_data["landford_insurance"])}</dd>'
                "</dl>"
            "</div>"
        "</div>"
    )
    
    # TODO: images
    images = ['fortesting.png', 'fortesting.png']
    images_html = images_to_html(images)


    # general analysis and results
    ana_and_res_table_html = analysis_and_results_to_html(gen_analysis_data)
    print("after table 1")
    inc_exp_cash_flow_graph_html = graph_to_html(plot_data)
    print("after graph")
    # 10-year Pro-Forma
    ten_year_pro_forma_html = ten_year_pro_forma_to_html(data)
    print("after ten year table")

    if not data_30_years == None:
        thirty_year_pro_forma = thirty_year_pro_forma_to_html(data_30_years)
        Full_Proforma_Section = f'<div class="col-sm"><h3>30 Years ProForma </h3>{thirty_year_pro_forma}</div>'
    else:
        Full_Proforma_Section = ""
    print("after 30 years table")

    if not tab1data == None:
        Table_One_Section = f'<div class="col-sm"><h3>30 Amortization Table 24 Months </h3>{amortization_table1_to_html(tab1data)}</div>'
    else:
        Table_One_Section = ""
    print("amortization table 1")

    if not tab2data == None:
        Table_Two_Section = f'<div class="col-sm"><h3>30 Amortization Table 28 Years </h3>{amortization_table2_to_html(tab2data)}</div>'
    else:
        Table_Two_Section = ""
    print("amortization table 2")

    html = create_report_html()
    print("after creating html")

    import PyQt5
    options = PyQt5.QtWidgets.QFileDialog.Options()
    options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = PyQt5.QtWidgets.QFileDialog.getSaveFileName(None, "Generate Report", "",
                                                              "HTML (*.html)", options=options)
    if fileName:
        if not str(fileName).__contains__(".html"):
            fileName += ".html"
        try:
            with open(fileName, 'w') as f:
                f.write(html)
        except Exception as ex:
            print("generate_report, exception:", ex)
            return None
    return fileName
    
def graph_to_html(data):
    fig, ax = plt.subplots()

    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)
    plt.xticks(rotation=-90)

    x = data.columns.values.tolist()
    max_y = 60000
    step = 10000
    #plt.yticks(arange(1300, max_y, step=step))
    ax.plot(x, data.iloc[0, :], label='Total Income')
    ax.plot(x, data.iloc[1, :], label='Total Expenses')
    ax.plot(x, data.iloc[2, :], label='NIAF')    
    #plt.plot(x, y, 'r')  # blue stars    
    legend = ax.legend(loc='best', shadow=False, fontsize='x-large')

    fig.savefig('plot.png', dpi=400, bbox_inches="tight")
    
    return f'<img src="plot.png" style="width: 650px; height: 450px;"/>'
    
def images_to_html(images):
    html = ''
    for img in images:
        html += f'<img src="{img}" />'
    return html

def ten_year_pro_forma_to_html(data):
    settings = QSettings("calculator_settings")
    caption_bgcolor = settings.value('caption_bgcolor')
    special_row_bgcolor = settings.value('special_row_bgcolor')

    print("caption color: ", caption_bgcolor)
    print("row Color: ",special_row_bgcolor)

    index_labels = ["Total Income",
                    "Total Expenses",
                    "Fixed Expenses",
                    "Variable Expenses",
                    "NOI",
                    "NOI Growth",
                    "Debt Service",
                    "NIAF",
                    "Property Value",
                    "Cash on Cash Return",
                    "Cum. CoCR",
                    "Total Equity",
                    "Percent of Equity",
                    "ROI",
                    "Total Profit If Sold",
                    "CAGR if Sold"
                    ]

    df = DataFrame.from_dict(data)
    df['labels'] = index_labels
    years = range(1, 11)
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
                            'color': 'white'
                            },
                            subset=IndexSlice[:, '---']
    ).hide_index()
    df_final.set_table_attributes('class="table table-striped table-sm"')
    return df_final.render()


def thirty_year_pro_forma_to_html(data):
    settings = QSettings("calculator_settings")
    caption_bgcolor = settings.value('caption_bgcolor')
    special_row_bgcolor = settings.value('special_row_bgcolor')
    index_labels = ["Total Income",
                    "Total Expenses",
                    "Fixed Expenses",
                    "Variable Expenses",
                    "NOI",
                    "NOI Growth",
                    "Debt Service",
                    "NIAF",
                    "Property Value",
                    "Cash on Cash Return",
                    "Cum. CoCR",
                    "Total Equity",
                    "Percent of Equity",
                    "ROI",
                    "Total Profit If Sold",
                    "CAGR if Sold"
                    ]
    df = DataFrame.from_dict(data)
    df['labels'] = index_labels
    years = range(1, 31)
    selected_columns = [f'Year_{index}' for index in years]
    selected_rows = [4, 7, 13]
    df = df[['labels'] + selected_columns]
    df.rename(columns={'labels': '---'}, inplace=True)
    df_final = df.style.set_properties(**{
        'background-color': special_row_bgcolor,
        'color': 'white',
    },
    subset=IndexSlice[selected_rows, selected_columns]
    )

    df_final = df_final.set_properties(**{
        'background-color': caption_bgcolor,
        'color': 'white'
    },
    subset=IndexSlice[:, '---']).hide_index()

    df_final.set_table_attributes('class="table table-striped table-sm"')
    return df_final.render()


def amortization_table1_to_html(data):
    print("in table 1")
    settings = QSettings("calculator_settings")
    caption_bgcolor = settings.value('caption_bgcolor')
    special_row_bgcolor = settings.value('special_row_bgcolor')

    # Starting Principle, Interest Paid, Principle Paid
    # Total Interest Paid, Total Principle Paid, Loan Balance
    index_labels = ["Starting Principle",
                    "Interest Paid",
                    "Principle Paid",
                    "Total Interest Paid",
                    "Total Principle Paid",
                    "Loan Balance"
                    ]
    print("create dataframe")
    df = DataFrame.from_dict(data)
    df['labels'] = index_labels
    months = range(1, 25)
    print("setting month heading")
    selected_columns = [f'Month_{index}' for index in months]
    print("after columns settings")
    selected_rows = [1,2,5]
    df = df[['labels'] + selected_columns]
    df.rename(columns={'labels':'---'}, inplace=True)
    # print("setup labels")
    df_final = df.style.set_properties(**{
                            'background-color': special_row_bgcolor,
                            'color': 'white',
                            },
                            subset=IndexSlice[selected_rows, selected_columns]
    )
    df_final = df_final.set_properties(**{
                            'background-color': caption_bgcolor,
                            'color': 'white'
                            },
                            subset=IndexSlice[:, '---']
    ).hide_index()
    df_final.set_table_attributes('class="table table-striped table-sm"')
    return df_final.render()


def amortization_table2_to_html(data):
    print("in table 2")
    settings = QSettings("calculator_settings")
    caption_bgcolor = settings.value('caption_bgcolor')
    special_row_bgcolor = settings.value('special_row_bgcolor')

    # Starting Principle, Interest Paid, Principle Paid
    # Total Interest Paid, Total Principle Paid, Loan Balance
    index_labels = [
                    "Starting Principle",
                    "Interest Paid",
                    "Principle Paid",
                    "Total Interest Paid",
                    "Total Principle Paid",
                    "Loan Balance"
                    ]
    print("creating dataframe")
    df = DataFrame.from_dict(data)
    df['labels'] = index_labels
    years = range(3, 31)
    print("setting columns")
    selected_columns = [f'Year_{index}' for index in years]
    print("setup columns")
    selected_rows = [0,3,5]
    df = df[['labels'] + selected_columns]
    df.rename(columns={'labels':'---'}, inplace=True)
    print("set properties")
    df_final = df.style.set_properties(**{
                            'background-color': special_row_bgcolor,
                            'color': 'white',
                            },
                            subset=IndexSlice[selected_rows,selected_columns]
    )

    df_final = df_final.set_properties(**{
                            'background-color': caption_bgcolor,
                            'color': 'white'
                            },
                            subset=IndexSlice[:, '---']
    ).hide_index()
    df_final.set_table_attributes('class="table table-striped table-sm"')
    return df_final.render()


def create_report_html():
    html_template = (
        "<html>"
        "<head>"
        "<title>Report</title>"
        "<meta charset='UTF-8'>"
        "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>"
        "<link rel='stylesheet' href='./bootstrap-4.4.1-dist/css/bootstrap.min.css'>"
        "<script src='./bootstrap-4.4.1-dist/js/bootstrap.min.js'></script>"
        '''
        <script>
            var slideIndex = 1;
            showSlides(slideIndex);

            function plusSlides(n) {
            showSlides(slideIndex += n);
            }

            function currentSlide(n) {
            showSlides(slideIndex = n);
            }

            function showSlides(n) {
            var i;
            var slides = document.getElementsByClassName("carousel-item");
            var dots = document.getElementsByClassName("carousel-indicators");
            if (n > slides.length) {slideIndex = 1}    
            if (n < 1) {slideIndex = slides.length}
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";  
            }
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace(" active", "");
            }
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
            }
        </script>
        
        <style rel='stylesheet'>
        .row-content{
            margin: 0px auto;
            padding: 20px 0px 20px 0px;
            min-height: auto;
            }
        .jumbotron{
            padding: 20px 30px 20px 30px; 
            margin: 0px auto;
            background: #39974A;
        }
        #title{
            left: 0px; 
            position: absolute; 
            bottom: 0px;
        }
        thead{
            background-color: black;
            color: white;
            padding: 8px;
            text-align: center;
        }
        .carousel-item{
            margin-top: 50px;
            margin-bottom: 50px;
        }
        .carousel-item img{
            width: 850px;
            height: 400px;
        }
        </style>'''
        "</head>"
        "<body>"
        '''        
        <div class='jumbotron'>
            <div class='container'>
                <div class='row'>
                    <div class='col-12 col-md-3 align-self-center text-center'>
                        <img class='border border-dark rounded' alt='SFI white (logo)' src='logo.png' />
                    </div>
                    <div class='col-12 col-md-9'>
                        <span id='title'>
                            <h1 class='mb-0 text-white'>Steiner Foresti Investment</h1>
                        </span>
                    </div>
                </div>
            </div>
        </div>'''
        
        '''<div class='container'>
            <div class="row row-content">'''
                f'<div class="col-sm">{property_address}</div>'
        '''</div>
    
        <div class="row row-content">
            <div class="col-sm " style="text-align: center;">
                <div class="carousel slide" id="mycarousel" data-ride="carousel">
                    <div class="carousel-inner bg-dark rounded" role="listbox">
                        <div class="carousel-item active">
                            <img src="70% Rule Chart.png" alt="70% Chart" class="rounded">
                        </div>
                        <div class="carousel-item">
                            <img src="1% Goal Chart (horizontal).png" alt="1% Chart" class="rounded">
                        </div>
                        <div class="carousel-item">
                            <img src="Half Income.png" alt="1% Chart" class="rounded">
                        </div>
                        <div class="carousel-item">
                            <img src="Monthly Expense.png" alt="Monthly Expense" class="rounded">
                        </div>
                        <div class="carousel-item">
                            <img src="Monthly Income.png" alt="Monthly Income" class="rounded">
                        </div>
                    </div>
                    <ol class="carousel-indicators">
                        <li onclick="currentSlide(1)"></li>
                        <li onclick="currentSlide(2)"></li>
                        <li onclick="currentSlide(3)"></li>
                        <li onclick="currentSlide(4)"></li>
                        <li onclick="currentSlide(5)"></li>
                    </ol>
                    <a class="carousel-control-prev" onclick="plusSlides(-1)">
                        &#10094;<span class="carousel-control-prev-icon"></span>
                    </a>
                    <a class="carousel-control-next" onclick="plusSlides(1)">
                        &#10095;<span class="carousel-control-next-icon"></span>
                    </a>
                </div>
            </div>
        </div>
   
        <div class="row row-content">'''
            f'<div class="col-sm"><h4 class="mb-0 bg-dark text-white border border-dark rounded-top" style="padding: 15px;">General Analysis and Results</h4>{ana_and_res_table_html}</div>'
        '''</div>
    
        <div class="row row-content">'''
            f'<div class="col-sm"><h3>Plot Analysis</h3>{inc_exp_cash_flow_graph_html}</div>'
        '''</div>
    
        <div class="row row-content">'''
            f'<div class="col-sm"><h3>10 Years ProForma</h3>{ten_year_pro_forma_html}</div>'
        '''</div>

        <div class="row row-content">'''
            f'{Full_Proforma_Section}'
        '''</div>

        <div class="row row-content">'''
            f'{Table_One_Section}'
        '''</div>

        <div class="row row-content">'''
            f'{Table_Two_Section}'
        '''</div>

        "</body>"
        "</html>"
        '''
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
    return df.to_html(header=None, index=False, classes="table table-striped")


def set_dataframe_style():
    """Set style for dataframe in charge of storing all final calculations"""
    df.style.set_properties(
        **{"background-color": "green", "color": "white", "border-color": "white"},
        subset=IndexSlice[1, ["id", "count", "type"]]
    )
