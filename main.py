from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox
import sys
from collections import defaultdict
from REI_calc_main_design import Ui_MainWindow
from settings_window import Ui_SettingsDialog
import REI_Calculations
import data_output


class SettingsWindow(QDialog):
    caption_bgcolor = "#ffbf00"
    special_row_bgcolor = "#359aa5"

    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.set_default_colors()

    def set_default_colors(self):
        settings = QtCore.QSettings("calculator_settings")
        if not settings.value("caption_bgcolor"):
            print("Setting default colors")
            settings.setValue("caption_bgcolor", self.caption_bgcolor)
            settings.setValue("special_row_bgcolor", self.caption_bgcolor)

        # set default colors
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", self.caption_bgcolor
        )
        self.ui.caption_bgcolor_button.setStyleSheet(color_name)
        self.ui.caption_bgcolor_button.setText("")
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", self.special_row_bgcolor
        )
        self.ui.special_row_bgcolor_button.setStyleSheet(color_name)
        self.ui.special_row_bgcolor_button.setText("")

        self.init_controls()

    def init_controls(self):
        self.ui.caption_bgcolor_button.clicked.connect(self.set_caption_bgcolor)
        self.ui.special_row_bgcolor_button.clicked.connect(self.set_special_row_bgcolor)
        self.settings = QtCore.QSettings("calculator_settings")
        self.ui.save_button.clicked.connect(self.save_settings)

    def set_caption_bgcolor(self):
        col = QColorDialog.getColor()
        self.caption_bgcolor = col.name()
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", col.name()
        )

        if col.isValid():
            self.ui.caption_bgcolor_button.setStyleSheet(color_name)

    def set_special_row_bgcolor(self):
        col = QColorDialog.getColor()
        self.special_row_bgcolor = col.name()
        color_name = "QPushButton { background-color: color_name }".replace(
            "color_name", col.name()
        )

        if col.isValid():
            self.ui.special_row_bgcolor_button.setStyleSheet(color_name)

    def save_settings(self):
        self.settings.setValue("caption_bgcolor", self.caption_bgcolor)
        self.settings.setValue("special_row_bgcolor", self.special_row_bgcolor)
        self.close()


class CalculatorWindow(QtWidgets.QMainWindow):  
    
    data = None
    
    # purchase information
    arv = 0
    loan_amount_auto = 0
    int_rate = 0
    downpayment = 0
    purchase_price = 0
    rehab_budget = 0
    closing_costs = 0
    finance_rehab_logical = 0
    emergency_fund = 0
    term_years = 0
    
    # fixed expenses
    electric = 0
    WandS = 0
    PMI = 0
    garbage = 0
    HOA = 0
    insurance = 0
    taxes = 0
    other = 0
    
    # variable expenses
    repair_and_maintenance = 0
    vacancy = 0
    rep_and_main = 0
    cap_ex = 0
    other_income = 0
    management = 0

    # income
    total_income_monthly = 0
    tot_monthly_income = 0
    ave_rent = 0
    rental_income_monthly = 0
    
    # assumptions 
    exp_appreciation = 0
    rent_appreciation = 0
    selling_costs = 0
    prop_appreciation = 0
    
    
    def __init__(self):
        super(CalculatorWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_signals()
        self.init_validators()
        
        self.data = defaultdict(list)

    def init_signals(self):
        self.ui.Generate_Report.clicked.connect(self.generate_report)
        self.ui.actionSettings.triggered.connect(self.settings_window)
                
        # auto fields
        self.ui.r_and_m_input.editingFinished.connect(
            self.repair_and_maintenance_changed
        )
        self.ui.cap_ex_input.editingFinished.connect(self.cap_ex_changed)
        self.ui.ave_rent_input.editingFinished.connect(self.ave_rent_changed)
        self.ui.other_income_month_input.editingFinished.connect(
            self.other_income_month_changed
        )

    def init_validators(self):
        # purchase information tab
        self.ui.asking_price_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.purchase_price_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.rehab_budget_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.arv_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.closing_costs_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.emerg_fund_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        # income tab
        self.ui.ave_rent_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.other_income_month_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        # expenses tab
        self.ui.electric_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.w_and_s_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.hoa_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.other_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.r_and_m_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.cap_ex_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.vacancy_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.manag_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        # assumptions tab
        self.ui.rent_appreciation_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.exp_appreciation_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.prop_appreciation_input.setValidator(QDoubleValidator(999999999, -999999999, 8))
        self.ui.selling_costs_input.setValidator(QDoubleValidator(999999999, -999999999, 8))

    def settings_window(self):
        settings_dialog = SettingsWindow(self)
        settings_dialog.show()

    def other_income_month_changed(self):
        try:
            self.other_income = float(
                self.ui.other_income_month_input.text()
                .strip()
                .replace("%", "")
                .replace(",", ".")
            )
        except Exception as ex:
            print(ex)
            self.show_message("Wrong value for other income month", msg_type="warning")

    def ave_rent_changed(self):
        try:
            self.ave_rent = float(
                self.ui.ave_rent_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            print(ex)
            self.show_message(
                "Wrong value for average rent per unit", msg_type="warning"
            )

    def repair_and_maintenance_changed(self):
        try:
            self.rep_and_main = float(
                self.ui.r_and_m_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            print(ex)
            self.show_message(
                "Wrong value for repair and maintenance", msg_type="warning"
            )

    def cap_ex_changed(self):
        try:
            self.cap_ex = float(
                self.ui.cap_ex_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            print(ex)
            self.show_message("Wrong value for cap. ex", msg_type="warning")

    def generate_report(self):
        print("Running calculations...")
        self.run_calculations()

    def show_message(self, message, details=None, msg_type="info"):
        msg = QMessageBox()
        if msg_type == "warning":
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)

        msg.setText(message)
        msg.setWindowTitle("Message")
        if details:
            msg.setInformativeText(details)
            msg.setDetailedText(details)

        msg.exec_()

    def run_calculations(self):
        ## Initially we just need to calculate the 12 key figures.
        ## Will then build a loop for the Pro forma statement.

        # Begin by calculating the monthly payment of the loan
        payment = REI_Calculations.loan_payment(self.rate, self.term, self.present_value)

        # Each item that is to be showcased will have a number before it.
        # only 8 are being calculated here.  There are an additional 4
        #   - Purchase Price (taken from GUI input)
        #   - Monthly Income (taken from GUI input)
        #   - Monthly Expense ( sum(fixed_monthly, var_monthly) )
        # The desired order for the 12 are to be as follows:
        #
        # cash_2_close  Purch. Price   Monthly Income
        # Monthly Exp.  Monthly CF     50% Rule
        # NOI           NIAF           CoCR
        # Cap Rate      1% Rule        Gross Rent Mult.

        # Calculate the fixed and variable expenses
        fixed_monthly, fixed_yearly = REI_Calculations.fixed_expenses_monthly(
            self.electric, self.WandS, self.PMI, 
            self.garbage, self.HOA, self.insurance, 
            self.taxes, self.other
        )

        var_monthly, var_yearly = REI_Calculations.variable_expenses_monthly(
            self.total_income_monthly, self.vacancy, self.rep_and_main, 
            self.cap_ex, self.management
        )

        # 1 Calculate NOI
        NOI = REI_Calculations.NOI_yearly(
            self.total_income_monthly * 12, fixed_yearly, var_yearly
        )

        # 2,3 Calculate Monthly and yearly NIAF or monthly cash flows
        cf_monthly = REI_Calculations.cash_flow_monthly(
            self.total_income_monthly, payment, fixed_monthly, var_monthly
        )
        NIAF = REI_Calculations.NIAF_yearly(NOI, payment)

        # 4 Calculate the cash to close
        cash_2_close = REI_Calculations.cash_to_close(
            self.downpayment,
            self.closing_costs,
            self.emergency_fund,
            self.rehab_budget,
            self.finance_rehab_logical,
        )

        # 5 Calculate Cash on Cash Return (CoCR)
        CoCR = REI_Calculations.cash_on_cash_return(NIAF, cash_2_close)

        # 6 Calculate the cap rate
        capRate = REI_Calculations.cap_rate(NOI, self.purchase_price, self.closing_costs)

        # 7 Calculate Gross Rent Multiplier
        GRM = REI_Calculations.gross_rent_mult(
            self.purchase_price, self.rehab_budget, self.total_income_monthly
        )

        # 8,9 Calculate the 1 and 50 percent rules
        one_perc = REI_Calculations.one_perc_rule(
            self.purchase_price, self.rehab_budget, self.total_income_monthly
        )
        fifty_perc = REI_Calculations.fifty_perc_rule(
            fixed_monthly, var_monthly, self.total_income_monthly
        )
        
        self.general_analysis_and_results = [
            [cash_2_close, self.purchase_price, self.tot_monthly_income], 
            [var_monthly, cf_monthly, 0], 
            [NIAF, NIAF, CoCR],
            [capRate, 0, GRM]
        ]
            
        ## Will need to store this data now as some of it may be overwritten
        # during the pro forma construction

        ## Now we begin the loop for ten years.  I will define a var here
        # because in the future I may make this adjustable for the number
        # of years to do the pro forma for

        ## Pro forma begins
        # Set initial values
        cum_NIAF = 0
        cum_CoCR = 0
        length_yrs = range(1, 10)

        for year_index in length_yrs:
            # Everything will be on a yearly scale and we may calculate some
            # variables two time for this first year
            
            # Calculate total annual income for each year
            tot_income_annual = REI_Calculations.future_value(
                self.rent_appreciation, year_index - 1, 0, self.tot_monthly_income
            )

            # Calculate total fixed expenses for each year
            fixed_yearly = REI_Calculations.future_value(
                self.exp_appreciation, year_index - 1, 0, fixed_monthly * 12
            )

            # Calculate total variable expenses for each year
            var_yearly = tot_income_annual * sum(
                self.repair_and_maintenance, self.cap_ex, self.vacancy, self.management
            )

            # Calculate Total Expenses
            tot_expense_yearly = sum(fixed_yearly, var_yearly)

            # Calculate NOI
            NOI = REI_Calculations.NOI_yearly(
                tot_income_annual, fixed_yearly, var_yearly
            )

            # Calculate Debt service
            if self.term < year_index:
                payment = 0
            payment_annual = payment * 12

            # Calculate NIAF
            NIAF = REI_Calculations.NIAF_yearly(NOI, payment)

            # Calculate Property Value
            prop_value = REI_Calculations.future_value(
                self.prop_appreciation, year_index - 1, 0, self.arv
            )

            # Calculate Cash on Cash Return
            CoCR = REI_Calculations.cash_on_cash_return(NIAF, cash_2_close)

            # Calculate cumulative CoCR
            cum_CoCR = cum_CoCR + CoCR

            # Calculate cumulative NIAF
            cum_NIAF = cum_NIAF + NIAF

            # Calculate future loan balance
            loan_balance = REI_Calculations.future_value(
                self.int_rate / 12, year_index * 12, payment, self.loan_amount_auto
            )
            # Calculate total equity owned by investor
            tot_equity = REI_Calculations.future_equity(prop_value, loan_balance)

            # Calculate percent of equity owned by the investor
            equity_perc = tot_equity / prop_value

            # Calculate ROI
            ROI = REI_Calculations.return_on_investment(
                tot_equity, cum_NIAF, cash_2_close
            )

            # Calculate profit if sold
            total_profit_sold = REI_Calculations.tot_profit_sold(
                prop_value, self.selling_costs, self.loan_balance, cash_2_close, cum_NIAF
            )

            # Calculate the compounded annual growth rate (CAGR) if sold
            CAGR = REI_Calculations.compound_annual_growth_rate(
                total_profit_sold, year_index, cash_2_close
            )
            
            self.data[f'Year_{year_index}'] = [
                tot_income_annual, tot_expense_yearly, fixed_yearly,
                var_yearly, NOI, 0,
                0, NIAF, prop_value,
                CoCR ,cum_CoCR, tot_equity,
                equity_perc, ROI, total_profit_sold,
                CAGR
            ]



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = CalculatorWindow()
    application.show()
    sys.exit(app.exec())
