from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import * #QDoubleValidator,
from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox
import sys
import re
from collections import defaultdict
from random import randint
from pandas import DataFrame

from gui2 import Ui_MainWindow
from settings_window import Ui_SettingsDialog
import REI_Calculations
import data_output

class SettingsWindow(QDialog):
    caption_bgcolor = "#39974A"
    special_row_bgcolor = "#973986"

    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.set_default_colors()

    def set_default_colors(self):
        settings = QtCore.QSettings("calculator_settings")
        if not settings.value("caption_bgcolor"):
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
    
    # data for html table
    data = None
    # data without format (decimal separator, percent, dollar,...)
    tmp_data = None
    
    general_analysis_and_results = None
    
    # property info
    address = ''
    city = ''
    state = ''
    zip_code = 0
    prior_year_taxes = 0
    landford_insurance = 0
    property_images = []
    
    # purchase information
    asking_price = 0
    term = 0
    present_value = 0
    arv = 0
    loan_amount_auto = 0
    int_rate = 4.5 / 100
    downpayment = 20 / 100
    downpayment_dollar = 0
    purchase_price = 0
    rehab_budget = 0
    closing_costs = 0
    finance_rehab_logical = 'Yes'
    emergency_fund = 0
    term_years = 0
    
    # fixed expenses
    total_fixed_expense = 0
    electric = 0
    WandS = 0
    PMI = 0
    garbage = 0
    HOA = 0
    insurance = 0
    taxes = 0
    other_fixed_expense = 0
    
    # variable expenses
    total_variable_expense = 0
    vacancy = 0
    vacancy_dollar = 0
    rep_and_main = 0
    rep_and_main_dollar = 0
    cap_ex = 0
    cap_ex_dollar = 0
    other_variable_expense = 0
    management = 0
    management_dollar = 0

    # income
    total_income_monthly = 0
    tot_rent_income = 0
    ave_rent = 0
    rental_income_monthly = 0
    num_units = 0
    other_income = 0
    
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
        self.init_fake_values() # TODO: remove
        
        # init data structures
        self.data = defaultdict(list)        
        self.tmp_data = defaultdict(list)        
        
        self.auto_calculations()
        self.update_total_exp_auto()
        
    def auto_calculations(self):
        self.calculate_loan_amount()
        
    def init_fake_values(self):
        """ TODO: delete after testing"""

        self.ui.address_input.setText("123 SFI Dr.")
        self.ui.city_input.setText("Anytown")
        self.ui.zip_input.setText(str(12340))
        self.ui.taxes_input.setText(str(500))
        self.ui.annual_insurance_input.setText(str(230))
        self.property_images = []

        self.ui.asking_price_input.setText(str(0))
        self.ui.purchase_price_input.setText(str(200000))
        self.ui.arv_input.setText(str(325000))
        self.ui.purchase_price_input.setText(str(200000))
        self.ui.rehab_budget_input.setText(str(50000))
        self.ui.closing_costs_input.setText(str(3500))
        self.ui.emerg_fund_input.setText(str(5000))

        # fixed expenses

        # variable expenses

        # income
        self.ui.other_income_month_input.setText(str(1300))
        self.ui.ave_rent_input.setText(str(1200))

        # assumptions
        self.ui.rent_appreciation_input.setText(str(20 / 100))
        self.ui.exp_appreciation_input.setText(str(30 / 100))
        self.ui.prop_appreciation_input.setText(str(40 / 100))
        self.ui.selling_costs_input.setText(str(50 / 100))
        
    def validate_values(self):
        try:
            # property info
            self.address = self.ui.address_input.text()
            self.city = self.ui.city_input.text()
            self.state = self.ui.state_input.currentText()            
            self.zip_code = int(self.ui.zip_input.text())
            self.prior_year_taxes = float(self.formatted_currency_to_float(
                self.ui.taxes_input.text()
            ))
            self.landford_insurance = float(self.formatted_currency_to_float(
                self.ui.annual_insurance_input.text()
            ))
            
            self.int_rate = self.ui.int_rate_input_2.value()

            # purchase information tab inputs
            self.asking_price = float(self.formatted_currency_to_float(
                self.ui.asking_price_input.text()
            ))
            self.purchase_price = float(self.formatted_currency_to_float(
                self.ui.purchase_price_input.text()
            ))
            self.finance_rehab_logical = self.formatted_currency_to_float(
                self.ui.fin_rehab_logical.currentText()
            )
            self.rehab_budget = float(self.formatted_currency_to_float(
                self.ui.rehab_budget_input.text()
            ))
            self.arv = float(self.formatted_currency_to_float(
                self.ui.arv_input.text()
            ))
            self.closing_costs = float(self.formatted_currency_to_float(
                self.ui.closing_costs_input.text()
            ))
            self.emergency_fund = float(self.formatted_currency_to_float(
                self.ui.emerg_fund_input.text()
            ))
            self.downpayment = float(self.percent_to_float(
                self.ui.downpayment_percentage_input_2.value() / 100
            ))
            self.downpayment_dollar = float(self.formatted_currency_to_float(
                self.ui.dp_dollar_auto_2.text()
            ))
            self.loan_amount = float(self.formatted_currency_to_float(
                self.ui.loan_amount_auto_2.text()
            ))
            self.term = self.ui.term_input_2.value()
            self.int_rate = self.formatted_currency_to_float(
                self.ui.int_rate_input_2.text()
            )
            self.int_rate = float(self.int_rate) / 100
            
            # income tab inputs
            self.num_units = float(self.ui.num_units_input.value())
            self.ave_rent = float(self.formatted_currency_to_float(
                self.ui.ave_rent_input.text()
            ))
            self.tot_rent_income = float(self.formatted_currency_to_float(
                self.ui.tot_rent_month_auto.text()
            ))
            self.other_income = float(self.formatted_currency_to_float(
                self.ui.other_income_month_input.text()
            ))
            self.total_income_monthly = float(self.formatted_currency_to_float(
                self.ui.tot_income_month_auto.text()
            ))
            
            # expenses tab inputs
            self.total_fixed_expense = float(self.formatted_currency_to_float(
                self.ui.tot_fixed_exp_auto.text()
            ))
            self.electric = float(self.formatted_currency_to_float(
                self.ui.electric_input.text()
            ))
            self.WandS = float(self.formatted_currency_to_float(
                self.ui.w_and_s_input.text()
            ))
            self.PMI = float(self.formatted_currency_to_float(
                self.ui.pmi_input.text()
            ))
            self.garbage = float(self.formatted_currency_to_float(
                self.ui.garbage_input.text()
            ))
            self.HOA = float(self.formatted_currency_to_float(
                self.ui.hoa_input.text()
            ))
            self.taxes = float(self.formatted_currency_to_float(
                self.ui.monthly_taxes_auto.text()
            ))
            self.insurance = float(self.formatted_currency_to_float(
                self.ui.insurance_auto.text()
            ))
            self.other_fixed_expense = float(self.formatted_currency_to_float(
                self.ui.other_input.text()
            ))
            self.total_variable_expense = float(self.formatted_currency_to_float(
                self.ui.tot_var_exp_auto.text()
            ))
            self.rep_and_main = float(self.percent_to_float(
                self.ui.r_and_m_input.text()
            )) / 100
            self.rep_and_main_dollar = float(self.formatted_currency_to_float(
                self.ui.r_and_m_auto.text()
            ))
            self.cap_ex = float(self.percent_to_float(
                self.ui.cap_ex_input.text()
            )) / 100
            self.cap_ex_dollar = float(self.formatted_currency_to_float(
                self.ui.cap_ex_auto.text()
            ))
            self.vacancy = float(self.percent_to_float(
                self.ui.vacancy_input.text()
            )) / 100
            self.vacancy_dollar = float(self.formatted_currency_to_float(
                self.ui.vacancy_auto.text()
            ))
            self.management = float(self.percent_to_float(
                self.ui.manag_input.text()
            )) / 100
            self.management_dollar = float(self.formatted_currency_to_float(
                self.ui.manag_auto.text()
            ))
            
            # Assumptions tab inputs
            self.rent_appreciation = float(
                self.percent_to_float(self.ui.rent_appreciation_input.text())
            ) / 100
            self.exp_appreciation = float(
                self.percent_to_float(self.ui.exp_appreciation_input.text())
            ) / 100
            self.prop_appreciation = float(
                self.percent_to_float(self.ui.prop_appreciation_input.text())
            ) / 100
            self.selling_costs = float(
                self.percent_to_float(self.ui.selling_costs_input.text())
            ) / 100
            
        except Exception as ex:
            _, _, tb = sys.exc_info()
            self.show_message(message='Validate values', 
                              details=f'Line: {tb.tb_lineno},\n {str(ex)}', 
                              msg_type='warning')
            return False
        
        return True


    def NewFile(self):
        check = QMessageBox.question(self, "Confirm", "Are you sure to reset the Values?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if(check == QMessageBox.Yes):
            # DEFINE PROPERTY VALUES
            self.ui.address_input.setText("")
            self.ui.city_input.setText("")
            self.ui.state_input.setCurrentText("")
            self.ui.zip_input.setText("")
            self.ui.taxes_input.setText("")
            self.ui.annual_insurance_input.setText("")

            # DEFINE PURCHASE VALUES
            self.ui.asking_price_input.setText("")
            self.ui.purchase_price_input.setText("")
            self.ui.fin_rehab_logical.setCurrentText("")
            self.ui.rehab_budget_input.setText("")
            self.ui.arv_input.setText("")
            self.ui.closing_costs_input.setText("")
            self.ui.emerg_fund_input.setText("")
            self.ui.downpayment_percentage_input_2.setValue(0) # check the value  * 100
            self.ui.term_input_2.setValue(0)
            self.ui.int_rate_input_2.setValue(0)   #check for values * 100

            # DEFINE INCOME VALUES
            self.ui.num_units_input.setValue(0)
            self.ui.ave_rent_input.setText("")
            self.ui.other_income_month_input.setText("")

            # DEFINE EXPENSES VALUES
            self.ui.tot_fixed_exp_auto.setText("")
            self.ui.tot_var_exp_auto.setText("")
            self.ui.electric_input.setText("")
            self.ui.w_and_s_input.setText("")
            self.ui.pmi_input.setText("")
            self.ui.garbage_input.setText("")
            self.ui.hoa_input.setText("")
            self.ui.r_and_m_input.setText("")
            self.ui.cap_ex_input.setText("")
            self.ui.vacancy_input.setText("")
            self.ui.manag_input.setText("")
            self.ui.insurance_auto.setText("")


            # ASSUMPTIONS TAB INPUTS
            self.ui.rent_appreciation_input.setText("")
            self.ui.exp_appreciation_input.setText("")
            self.ui.prop_appreciation_input.setText("")
            self.ui.selling_costs_input.setText("")


    def loadFile(self):
        import PyQt5
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, "Open file", "",
                                                                  "All files (*.*)", options=options)
        values = []
        if fileName:
            file = open(fileName)
            lines = file.readlines()
            for line in lines:
                if line.__contains__(':'):
                    parts = line.split(':')
                    values.append(parts[1].strip())

        # DEFINE PROPERTY VALUES
        self.ui.address_input.setText(values[0])
        self.ui.city_input.setText(values[1])
        self.ui.state_input.setCurrentText(values[2])
        self.ui.zip_input.setText(values[3])
        self.ui.taxes_input.setText(values[4])
        self.ui.annual_insurance_input.setText(values[5])

        # DEFINE PURCHASE VALUES
        self.ui.asking_price_input.setText(values[6])
        self.ui.purchase_price_input.setText(values[7])
        self.ui.fin_rehab_logical.setCurrentText(values[8])
        self.ui.rehab_budget_input.setText(values[9])
        self.ui.arv_input.setText(values[10])
        self.ui.closing_costs_input.setText(values[11])
        self.ui.emerg_fund_input.setText(values[12])
        self.ui.downpayment_percentage_input_2.setValue(int(values[13])) # check the value  * 100
        self.ui.term_input_2.setValue(int(values[14]))
        self.ui.int_rate_input_2.setValue(float(values[15]))   #check for values * 100

        # DEFINE INCOME VALUES
        self.ui.num_units_input.setValue(int(float(values[16])))
        self.ui.ave_rent_input.setText(values[17])
        self.ui.other_income_month_input.setText(values[18])

        # DEFINE EXPENSES VALUES
        self.ui.electric_input.setText(values[19])
        self.ui.w_and_s_input.setText(values[20])
        self.ui.pmi_input.setText(values[21])
        self.ui.garbage_input.setText(values[22])
        self.ui.hoa_input.setText(values[23])
        self.ui.r_and_m_input.setText(values[24])
        self.ui.cap_ex_input.setText(values[25])
        self.ui.vacancy_input.setText(values[26])
        self.ui.manag_input.setText(values[27])


        # ASSUMPTIONS TAB INPUTS
        self.ui.rent_appreciation_input.setText(values[28])
        self.ui.exp_appreciation_input.setText(values[29])
        self.ui.prop_appreciation_input.setText(values[30])
        self.ui.selling_costs_input.setText(values[31])


    def saveFile(self):
        import PyQt5
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = PyQt5.QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "",
                                                                  "All files (*.*)", options=options)
        if fileName:
            if not str(fileName).__contains__(".txt"):
                fileName += ".txt"
            try:
                # property info
                self.address = self.ui.address_input.text()
                self.city = self.ui.city_input.text()
                self.state = self.ui.state_input.currentText()
                self.zip_code = int(self.ui.zip_input.text())
                self.prior_year_taxes = float(self.formatted_currency_to_float(
                    self.ui.taxes_input.text()
                ))
                self.landford_insurance = float(self.formatted_currency_to_float(
                    self.ui.annual_insurance_input.text()
                ))
                self.int_rate = self.ui.int_rate_input_2.value()

                # purchase information tab inputs
                self.asking_price = float(self.formatted_currency_to_float(
                    self.ui.asking_price_input.text()
                ))
                self.purchase_price = float(self.formatted_currency_to_float(
                    self.ui.purchase_price_input.text()
                ))
                self.finance_rehab_logical = self.formatted_currency_to_float(
                    self.ui.fin_rehab_logical.currentText()
                )
                self.rehab_budget = float(self.formatted_currency_to_float(
                    self.ui.rehab_budget_input.text()
                ))
                self.arv = float(self.formatted_currency_to_float(
                    self.ui.arv_input.text()
                ))
                self.closing_costs = float(self.formatted_currency_to_float(
                    self.ui.closing_costs_input.text()
                ))
                self.emergency_fund = float(self.formatted_currency_to_float(
                    self.ui.emerg_fund_input.text()
                ))
                self.downpayment = int(self.percent_to_float(
                    self.ui.downpayment_percentage_input_2.value()
                ))
                # REMOVE DOWNPAYMENT ($)
                # self.downpayment_dollar = float(self.formatted_currency_to_float(
                #     self.ui.dp_dollar_auto_2.text()
                # ))
                # REMOVE LOAN AMOUNT
                # self.loan_amount = float(self.formatted_currency_to_float(
                #     self.ui.loan_amount_auto_2.text()
                # ))
                self.term = self.ui.term_input_2.value()
                self.int_rate = self.formatted_currency_to_float(
                    self.ui.int_rate_input_2.text()
                )
                self.int_rate = float(self.int_rate)

                # income tab inputs
                self.num_units = float(self.ui.num_units_input.value())
                self.ave_rent = float(self.formatted_currency_to_float(
                    self.ui.ave_rent_input.text()
                ))
                # REMOVE TOTAL RENT INCOME
                # self.tot_rent_income = float(self.formatted_currency_to_float(
                #     self.ui.tot_rent_month_auto.text()
                # ))
                self.other_income = float(self.formatted_currency_to_float(
                    self.ui.other_income_month_input.text()
                ))
                # REMOVE TOTAL MONTHLY INCOME
                # self.total_income_monthly = float(self.formatted_currency_to_float(
                #     self.ui.tot_income_month_auto.text()
                # ))

                # EXPENSES TAB INPUTS
                # REMOVE TOTAL FIXED EXPENSE
                # self.total_fixed_expense = float(self.formatted_currency_to_float(
                #     self.ui.tot_fixed_exp_auto.text()
                # ))
                self.electric = str(self.formatted_currency_to_float(
                    self.ui.electric_input.text()
                ))
                self.WandS = str(self.formatted_currency_to_float(
                    self.ui.w_and_s_input.text()
                ))
                self.PMI = str(self.formatted_currency_to_float(
                    self.ui.pmi_input.text()
                ))
                self.garbage = str(self.formatted_currency_to_float(
                    self.ui.garbage_input.text()
                ))
                self.HOA = str(self.formatted_currency_to_float(
                    self.ui.hoa_input.text()
                ))
                # REMOVE TAXES, INSURANCE, FIXED EXPENSE, VARIABLE EXPENSE
                # self.taxes = str(self.formatted_currency_to_float(
                #     self.ui.monthly_taxes_auto.text()
                # ))
                # self.insurance = str(self.formatted_currency_to_float(
                #     self.ui.insurance_auto.text()
                # ))
                # self.other_fixed_expense = str(self.formatted_currency_to_float(
                #     self.ui.other_input.text()
                # ))
                # self.total_variable_expense = str(self.formatted_currency_to_float(
                #     self.ui.tot_var_exp_auto.text()
                # ))
                self.rep_and_main = str(self.percent_to_float(
                    self.ui.r_and_m_input.text()
                ))
                # REMOVE REP & MAIN ($)
                # self.rep_and_main_dollar = str(self.formatted_currency_to_float(
                #     self.ui.r_and_m_auto.text()
                # ))
                self.cap_ex = str(self.percent_to_float(
                    self.ui.cap_ex_input.text()
                ))
                # REMOVE CAP EX ($)
                # self.cap_ex_dollar = str(self.formatted_currency_to_float(
                #     self.ui.cap_ex_auto.text()
                # ))
                self.vacancy = str(self.percent_to_float(
                    self.ui.vacancy_input.text()
                ))
                # REMOVE EXPENSE VACANCY
                # self.vacancy_dollar = str(self.formatted_currency_to_float(
                #     self.ui.vacancy_auto.text()
                # ))
                self.management = str(self.percent_to_float(
                    self.ui.manag_input.text()
                ))
                # REMOVE EXPENSE MANAGEMENT
                # self.management_dollar = str(self.formatted_currency_to_float(
                #     self.ui.manag_auto.text()
                # ))

                # Assumptions tab inputs
                self.rent_appreciation = float(
                    self.percent_to_float(self.ui.rent_appreciation_input.text())
                )
                self.exp_appreciation = float(
                    self.percent_to_float(self.ui.exp_appreciation_input.text())
                )
                self.prop_appreciation = float(
                    self.percent_to_float(self.ui.prop_appreciation_input.text())
                )
                self.selling_costs = float(
                    self.percent_to_float(self.ui.selling_costs_input.text())
                )

            except Exception as ex:
                _, _, tb = sys.exc_info()
                self.show_message(message='Save Values',
                                  details=f'Line: {tb.tb_lineno},\n {str(ex)}',
                                  msg_type='warning')

            # print(fileName)
            file = open(fileName, 'w')
            print("opened")

            # Property information tab inputs
            file.write(str("Property_Tab\n"))
            file.write(str("Property_Address:"+self.address+"\n"))
            file.write(str("Property_City:"+self.city+"\n"))
            file.write(str("Property_State:"+self.state+"\n"))
            file.write(str("Property_ZipCode:"+str(self.zip_code)+"\n"))
            file.write(str("Property_PriorYearsTaxes:"+str(self.prior_year_taxes)+"\n"))
            file.write(str("Property_LandLordInsurance:"+str(self.landford_insurance)+"\n\n"))

            # PURCHASE INFORMATION TAB INPUTS
            file.write(str("Purchase_Tab\n"))
            file.write("Purchase_AskingPrice: "+str(self.asking_price)+"\n")
            file.write("Purchase_PurchasePrice: "+str(self.purchase_price)+"\n")
            file.write("Purchase_FinanceRehab: "+str(self.finance_rehab_logical)+"\n")
            file.write("Purchase_RehabBudget: "+str(self.rehab_budget)+"\n")
            file.write("Purchase_ARV: "+str(self.arv)+"\n")
            file.write("Purchase_ClosingCost: "+str(self.closing_costs)+"\n")
            file.write("Purchase_EmergencyFund: "+str(self.emergency_fund)+"\n")
            file.write("Purchase_Downpayment(%): "+str(self.downpayment)+"\n")
            # file.write("Purchase_Downpayment($): "+str(self.downpayment_dollar)+"\n")
            # file.write("Purchase_LoanAmount: "+str(self.loan_amount)+"\n")
            file.write("Purchase_Term: "+str(self.term)+"\n")
            file.write("Purchase_AnnauLInterestRate: "+str(self.int_rate)+"\n\n")

            # INCOME TAB INPUTS
            file.write(str("Income_Tab\n"))
            file.write("Income_NumberOfUnits: "+str(self.num_units)+"\n")
            file.write("Income_AvgRent/unit: "+str(self.ave_rent)+"\n")
            # file.write("Income_TotalRentIncome: "+str(self.tot_rent_income)+"\n")
            file.write("Income_OtherIncome: "+str(self.other_income)+"\n\n")
            # file.write("Income_TotalMonthly: "+str(self.total_income_monthly)+"\n\n")

            # EXPENSE TAB INPUTS
            file.write(str("Expense_Tab\n"))
            # file.write("Expense_TotalFixedExpense: "+str(self.total_fixed_expense)+"\n")
            file.write("Expense_Electricity: "+str(self.electric)+"\n")
            file.write("Expense_WandS: "+str(self.WandS)+"\n")
            file.write("Expense_PMI: "+str(self.PMI)+"\n")
            file.write("Expense_Garbage: "+str(self.garbage)+"\n")
            file.write("Expense_HOA: "+str(self.HOA)+"\n")
            # file.write("Expense_Taxes: "+str(self.taxes)+"\n")
            # file.write("Expense_Insurance: "+str(self.insurance)+"\n")
            # file.write("Expense_FixedExpense: "+str(self.other_fixed_expense)+"\n")
            # file.write("Expense_VariableExpense: "+str(self.total_variable_expense)+"\n")
            file.write("Expense_Rep&Main(%): "+str(self.rep_and_main)+"\n")
            # file.write("Expense_Rep&Mian($): "+str(self.rep_and_main_dollar)+"\n")
            file.write("Expense_CapEX(%): "+str(self.cap_ex)+"\n")
            # file.write("Expense_CapEX($): "+str(self.cap_ex_dollar)+"\n")
            file.write("Expense_Vacancy(%): "+str(self.vacancy)+"\n")
            # file.write("Expense_Vacancy($): "+str(self.vacancy_dollar)+"\n")
            file.write("Expense_Management(%): "+str(self.management)+"\n\n")
            # file.write("Expense_Management($): "+str(self.management_dollar)+"\n")

            # ASSUMPTIONS TAB INPUTS
            file.write(str("Assumptions_Tab\n"))
            file.write("Assumptions_RentAppreciation(%): "+str(self.rent_appreciation)+"\n")
            file.write("Assumptions_ExpenseAppreciation(%): "+str(self.exp_appreciation)+"\n")
            file.write("Assumptions_PropertyAppreciation(%): "+str(self.prop_appreciation)+"\n")
            file.write("Assumptions_SellingCost: "+str(self.selling_costs)+"\n\n")

            print("success all written")
            file.close()
            QMessageBox.information(self, "Save File", "File Saved Successfully", QMessageBox.Ok)

    def saveAsPDF(self, html_report):
        import pdfkit
        pdfkit.from_file(html_report, "Report.pdf")

    def exit(self):
        exit(1)
        
    def showAbout(self):
        from about import Ui_Dialog
        d = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(d)
        d.setWindowTitle("About REI Calculator Version-1.8")
        # d.setObjectName("about_dialog")
        # d.resize(400,500)
        d.exec_()

    def focused_field(self, ui_control, ftype='dollar'):
        if ftype == 'dollar':
            self.set_decimal_format(ui_control)
        elif ftype == 'percent':
            self.set_single_float_format(ui_control)
        
    def unfocused_field(self, ui_control, ftype='dollar'):
        if ftype == 'dollar':
            self.set_currency_format(ui_control)
        elif ftype == 'percent':
            self.set_percent_format(ui_control)
            
    def set_single_float_format(self, ui_control):
        value = self.percent_to_float(ui_control.text())
        ui_control.setText(value)


        # init Signals Method initializes all the ui_controls and buttons
        # including Menu Bars and other components buttons and controls
    def init_signals(self):
        self.ui.annual_insurance_input.focused.connect(
            lambda uic=self.ui.annual_insurance_input: self.focused_field(uic)
        )
        self.ui.annual_insurance_input.unfocused.connect(
            lambda uic=self.ui.annual_insurance_input: self.unfocused_field(uic)
        )
        self.ui.Generate_Report.clicked.connect(self.generate_report)
        self.ui.actionSettings.triggered.connect(self.settings_window)
        self.ui.actionNew.triggered.connect(self.NewFile)
        self.ui.actionLoad.triggered.connect(self.loadFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.actionSave_As.triggered.connect(self.saveFile)
        self.ui.actionExecute.triggered.connect(self.generate_report)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionAbout_REI_Calculator.triggered.connect(self.showAbout)
        # auto fields
        
        self.ui.ave_rent_input.editingFinished.connect(self.ave_rent_changed)
        self.ui.other_income_month_input.editingFinished.connect(
            self.other_income_month_changed
        )
        self.ui.int_rate_input_2.valueChanged.connect(self.interest_rate_changed)
        self.ui.term_input_2.valueChanged.connect(self.term_years_changed)
        
        # calculate downpayment $ when downpayment % is changed
        self.ui.downpayment_percentage_input_2.valueChanged.connect(
            self.downpayment_percent_changed)      
        
        # expenses tab auto fields
        self.ui.vacancy_input.textChanged.connect(self.vacancy_input_changed)    
        self.ui.vacancy_input.focused.connect(
            lambda uic=self.ui.vacancy_input: self.focused_field(uic, 'percent')
        )
        self.ui.vacancy_input.unfocused.connect(
            lambda uic=self.ui.vacancy_input: self.unfocused_field(uic, 'percent')
        )    
                
        self.ui.cap_ex_input.textChanged.connect(self.cap_ex_input_changed)     
        self.ui.cap_ex_input.focused.connect(
            lambda uic=self.ui.cap_ex_input: self.focused_field(uic, 'percent')
        )
        self.ui.cap_ex_input.unfocused.connect(
            lambda uic=self.ui.cap_ex_input: self.unfocused_field(uic, 'percent')
        )    
        
        self.ui.r_and_m_input.textChanged.connect(self.r_and_m_input_changed)   
        self.ui.r_and_m_input.focused.connect(
            lambda uic=self.ui.r_and_m_input: self.focused_field(uic, 'percent')
        )
        self.ui.r_and_m_input.unfocused.connect(
            lambda uic=self.ui.r_and_m_input: self.unfocused_field(uic, 'percent')
        )           
                
        self.ui.manag_input.textChanged.connect(self.manag_input_changed)       
        self.ui.manag_input.focused.connect(
            lambda uic=self.ui.manag_input: self.focused_field(uic, 'percent')
        )
        self.ui.manag_input.unfocused.connect(
            lambda uic=self.ui.manag_input: self.unfocused_field(uic, 'percent')
        )   
        
        self.ui.electric_input.textChanged.connect(self.electric_input_changed)   
        self.ui.electric_input.focused.connect(
            lambda uic=self.ui.electric_input: self.focused_field(uic)
        )
        self.ui.electric_input.unfocused.connect(
            lambda uic=self.ui.electric_input: self.unfocused_field(uic)
        )           
        
        self.ui.w_and_s_input.textChanged.connect(self.w_and_s_input_changed)     
        self.ui.w_and_s_input.focused.connect(
            lambda uic=self.ui.w_and_s_input: self.focused_field(uic)
        )
        self.ui.w_and_s_input.unfocused.connect(
            lambda uic=self.ui.w_and_s_input: self.unfocused_field(uic)
        )     
        
        self.ui.pmi_input.textChanged.connect(self.pmi_input_changed)  
        self.ui.pmi_input.focused.connect(
            lambda uic=self.ui.pmi_input: self.focused_field(uic)
        )
        self.ui.pmi_input.unfocused.connect(
            lambda uic=self.ui.pmi_input: self.unfocused_field(uic)
        )   
        
        self.ui.garbage_input.textChanged.connect(self.garbage_input_changed)    
        self.ui.garbage_input.focused.connect(
            lambda uic=self.ui.garbage_input: self.focused_field(uic)
        )
        self.ui.garbage_input.unfocused.connect(
            lambda uic=self.ui.garbage_input: self.unfocused_field(uic)
        )   
        
        self.ui.hoa_input.textChanged.connect(self.hoa_input_changed)       
        self.ui.hoa_input.focused.connect(
            lambda uic=self.ui.hoa_input: self.focused_field(uic)
        )
        self.ui.hoa_input.unfocused.connect(
            lambda uic=self.ui.hoa_input: self.unfocused_field(uic)
        )   
        
        self.ui.other_input.textChanged.connect(self.other_input_changed)
        self.ui.other_input.focused.connect(
            lambda uic=self.ui.other_input: self.focused_field(uic)
        )
        self.ui.other_input.unfocused.connect(
            lambda uic=self.ui.other_input: self.unfocused_field(uic)
        )   
        
        self.ui.r_and_m_input.editingFinished.connect(
            self.repair_and_maintenance_changed
        )
        
        self.ui.cap_ex_input.editingFinished.connect(self.cap_ex_changed)

        # property tab
        self.ui.annual_insurance_input.textChanged.connect(
            self.annual_insurance_input_changed
        )
        self.ui.annual_insurance_input.focused.connect(
            lambda uic=self.ui.annual_insurance_input: self.focused_field(uic)
        )
        self.ui.annual_insurance_input.unfocused.connect(
            lambda uic=self.ui.annual_insurance_input: self.unfocused_field(uic)
        )
        
        self.ui.taxes_input.textChanged.connect(self.taxes_input_changed)
        self.ui.taxes_input.focused.connect(
            lambda uic=self.ui.taxes_input: self.focused_field(uic)
        )
        self.ui.taxes_input.unfocused.connect(
            lambda uic=self.ui.taxes_input: self.unfocused_field(uic)
        )
        
        # income tab
        self.ui.num_units_input.valueChanged.connect(self.num_units_value_changed)
        self.ui.ave_rent_input.textChanged.connect(self.ave_rent_input_changed)
        self.ui.ave_rent_input.focused.connect(
            lambda uic=self.ui.ave_rent_input: self.focused_field(uic)
        )
        self.ui.ave_rent_input.unfocused.connect(
            lambda uic=self.ui.ave_rent_input: self.unfocused_field(uic)
        )    
        
        self.ui.other_income_month_input.textChanged.connect(self.other_income_month_input_changed)
        self.ui.other_income_month_input.focused.connect(
            lambda uic=self.ui.other_income_month_input: self.focused_field(uic)
        )
        self.ui.other_income_month_input.unfocused.connect(
            lambda uic=self.ui.other_income_month_input: self.unfocused_field(uic)
        )          
        
        # Purchase Tab
        self.ui.purchase_price_input.textChanged.connect(self.purchase_price_changed)
        self.ui.purchase_price_input.focused.connect(
            lambda uic=self.ui.purchase_price_input: self.focused_field(uic)
        )
        self.ui.purchase_price_input.unfocused.connect(
            lambda uic=self.ui.purchase_price_input: self.unfocused_field(uic)
        )
                
        self.ui.rehab_budget_input.textChanged.connect(self.rehab_budget_changed)
        self.ui.rehab_budget_input.focused.connect(
            lambda uic=self.ui.rehab_budget_input: self.focused_field(uic)
        )
        self.ui.rehab_budget_input.unfocused.connect(
            lambda uic=self.ui.rehab_budget_input: self.unfocused_field(uic)
        )        
        
        self.ui.arv_input.textChanged.connect(self.arv_changed)
        self.ui.arv_input.focused.connect(
            lambda uic=self.ui.arv_input: self.focused_field(uic)
        )
        self.ui.arv_input.unfocused.connect(
            lambda uic=self.ui.arv_input: self.unfocused_field(uic)
        )        
        
        
        self.ui.closing_costs_input.textChanged.connect(self.closing_costs_changed)
        self.ui.closing_costs_input.focused.connect(
            lambda uic=self.ui.closing_costs_input: self.focused_field(uic)
        )
        self.ui.closing_costs_input.unfocused.connect(
            lambda uic=self.ui.closing_costs_input: self.unfocused_field(uic)
        )         
        
        self.ui.emerg_fund_input.textChanged.connect(self.emerg_fund_input)
        self.ui.emerg_fund_input.focused.connect(
            lambda uic=self.ui.emerg_fund_input: self.focused_field(uic)
        )
        self.ui.emerg_fund_input.unfocused.connect(
            lambda uic=self.ui.emerg_fund_input: self.unfocused_field(uic)
        )    
        
        self.ui.fin_rehab_logical.currentIndexChanged.connect(
            self.fin_rehab_logical_changed
        )
        
        self.ui.rent_appreciation_input.focused.connect(
            lambda uic=self.ui.rent_appreciation_input: self.focused_field(uic, 'percent')
        )
        self.ui.rent_appreciation_input.unfocused.connect(
            lambda uic=self.ui.rent_appreciation_input: self.unfocused_field(uic, 'percent')
        )   
        self.ui.exp_appreciation_input.focused.connect(
            lambda uic=self.ui.exp_appreciation_input: self.focused_field(uic, 'percent')
        )
        self.ui.exp_appreciation_input.unfocused.connect(
            lambda uic=self.ui.exp_appreciation_input: self.unfocused_field(uic, 'percent')
        )      
        self.ui.prop_appreciation_input.focused.connect(
            lambda uic=self.ui.prop_appreciation_input: self.focused_field(uic, 'percent')
        )
        self.ui.prop_appreciation_input.unfocused.connect(
            lambda uic=self.ui.prop_appreciation_input: self.unfocused_field(uic, 'percent')
        )     
        self.ui.selling_costs_input.focused.connect(
            lambda uic=self.ui.selling_costs_input: self.focused_field(uic, 'percent')
        )
        self.ui.selling_costs_input.unfocused.connect(
            lambda uic=self.ui.selling_costs_input: self.unfocused_field(uic, 'percent')
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
        
    def set_percent_format(self, ui_control):
        try:
            value = self.percent_to_float(
                ui_control.text()
            )
            percent_format = '{:0,.2f}%'.format(float(value))         
            ui_control.setText(percent_format)
        except Exception as ex:
            print('set_percent_format:', ex)
            ui_control.setText('0%')
        
    def set_currency_format(self, ui_control):
        if not ui_control.text().strip():
            return
        
        try:            
            current_value = self.formatted_currency_to_float(ui_control.text())
            current_value = float(current_value)
            currency_format = '${:0,.2f}'.format(float(current_value)) 
            ui_control.setText(str(currency_format))
        except Exception as ex:
            print('set_currency_format:', ex)
            ui_control.setText('')
        
    def set_decimal_format(self, ui_control):
        if not ui_control.text().strip():
            return
        
        try:
            current_value = ui_control.text()            
            decimal_float = self.formatted_currency_to_float(current_value)
            ui_control.setText(decimal_float)
        except Exception as ex:
            print('set_decimal_format:', ex)
            ui_control.setText('0')       
       
    
    def fin_rehab_logical_changed(self, index):
        self.finance_rehab_logical = self.ui.fin_rehab_logical.currentText()
        self.calculate_loan_amount()
        
        self.set_currency_format(self.ui.loan_amount_auto_2)
        
    def annual_insurance_input_edited(self):
        self.set_decimal_format(self.ui.annual_insurance_input)

    def annual_insurance_input_finished(self):
        self.set_currency_format(self.ui.annual_insurance_input)
            
    def emerg_fund_input(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.emerg_fund_input.text()
            )            
            self.emergency_fund = float(value)
        except ValueError:
            self.ui.emerg_fund_input.setText("0")
    
    def closing_costs_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.closing_costs_input.text()
            )            
            self.closing_costs = float(value)
        except ValueError:
            self.ui.closing_costs_input.setText("0")
    
    def arv_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.arv_input.text()
            )            
            self.arv = float(value)
        except ValueError:
            self.ui.arv_input.setText("0")
    
    def rehab_budget_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.rehab_budget_input.text()
            )
            self.rehab_budget = float(value)   
            self.calculate_loan_amount()
            
            self.set_currency_format(self.ui.loan_amount_auto_2)
        except ValueError:
            self.ui.rehab_budget_input.setText("0")
    
    def purchase_price_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.purchase_price_input.text()
            )
            self.purchase_price = float(value)#self.ui.purchase_price_input.text())
            self.calculate_downpayment_dollar()
            self.calculate_loan_amount()
            
            self.set_currency_format(self.ui.dp_dollar_auto_2)
            self.set_currency_format(self.ui.loan_amount_auto_2)
        except ValueError:
            self.ui.purchase_price_input.setText("0")
        
    def other_income_month_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.other_income_month_input.text()
            )
            
            self.other_income = float(value)
            value = self.formatted_currency_to_float(
                self.ui.tot_rent_month_auto.text()
            )
            
            self.rent_income  = float(value)
            self.total_income_monthly = REI_Calculations.total_monthly_income(
                self.rent_income, 
                self.other_income
            )
            self.ui.tot_income_month_auto.setText(str(self.total_income_monthly))
            self.set_currency_format(self.ui.tot_income_month_auto)
            
        except ValueError as ex:
            print("other income month changed:", ex)
            self.total_income_monthly = 0
            self.ui.other_income_month_input.setText("0")

    
    def ave_rent_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.num_units_input.text()
            )
            
            self.num_units = int(value)
            
            value = self.formatted_currency_to_float(
                self.ui.ave_rent_input.text()
            )
            
            self.ave_rent = float(value)
            self.total_rent_monthly = REI_Calculations.monthly_rent(
                self.num_units, 
                self.ave_rent
            )
            self.ui.tot_rent_month_auto.setText(str(self.total_rent_monthly))
            self.set_currency_format(self.ui.tot_rent_month_auto)

            # Update total monthly income
            try:
                value = self.formatted_currency_to_float(
                    self.ui.other_income_month_input.text()
                )
                self.other_income = float(value)
            except ValueError:
                self.ui.other_income_month_input.setText("0")
                return

            self.total_income_monthly = REI_Calculations.total_monthly_income(
                self.total_rent_monthly,
                self.other_income
            )
            self.ui.tot_income_month_auto.setText(str(self.total_income_monthly))
            self.set_currency_format(self.ui.tot_income_month_auto)
            
        except ValueError:
            self.ui.ave_rent_input.setText("0")
            return
    
    def num_units_value_changed(self, value):
        try:
            self.num_units = value 
            self.rental_income_monthly = REI_Calculations.monthly_rent(
                self.num_units, self.ave_rent
            )
            self.ui.tot_rent_month_auto.setText(str(self.rental_income_monthly))
            self.set_currency_format(self.ui.tot_rent_month_auto)
            
            # Update total monthly income
            try:
                value = self.formatted_currency_to_float(
                    self.ui.other_income_month_input.text()
                )                
                self.other_income = float(value)
            except ValueError:
                self.ui.other_income_month_input.setText("0")
            
            try:
                value = self.formatted_currency_to_float(
                    self.ui.tot_rent_month_auto.text()
                )                
                self.rent_income = float(value)
            except ValueError:
                self.ui.ave_rent_input.setText("0")
            
            self.total_income_monthly = REI_Calculations.total_monthly_income(
                self.rent_income,
                self.other_income
            )
            self.ui.tot_income_month_auto.setText(str(self.total_income_monthly))
            self.set_currency_format(self.ui.tot_income_month_auto)
        except ValueError as ex:            
            print('num_units_input_changed:', str(ex))
            return
        
        self.ui.monthly_taxes_auto.setText(str(self.taxes))
        self.set_currency_format(self.ui.monthly_taxes_auto)
        
        self.update_total_exp_auto()
            
    def taxes_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.taxes_input.text()
            )
            self.taxes = float(value) / 12            
        except ValueError:
            self.ui.taxes_input.setText("0")
        
        self.ui.monthly_taxes_auto.setText(str(self.taxes))
        self.update_total_exp_auto()
        self.set_currency_format(self.ui.monthly_taxes_auto)
        
    def annual_insurance_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.annual_insurance_input.text()
            )
            self.insurance = float(value) / 12            
        except ValueError:
            self.ui.insurance_auto.setText("0")
        
        self.ui.insurance_auto.setText(str(self.insurance))
        self.update_total_exp_auto()
        self.set_currency_format(self.ui.insurance_auto)
        
    
    def other_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.other_input.text()
            )
            self.other_fixed_expense = float(value)
        except ValueError:
            self.ui.other_input.setText("0")
        
        self.update_total_exp_auto()
        self.set_currency_format(self.ui.other_input)

    def garbage_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.garbage_input.text()
            )            
            self.garbage = float(value)
        except ValueError:
            self.ui.garbage_input.setText("0")
        
        self.update_total_exp_auto()
        self.set_currency_format(self.ui.garbage_input)

    def hoa_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.hoa_input.text()
            )
            
            value = self.formatted_currency_to_float(value)
            self.HOA = float(value)
        except ValueError:
            self.ui.hoa_input.setText("0")
        
        self.update_total_exp_auto()

    def pmi_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.pmi_input.text()
            )
            self.PMI = float(value)
        except ValueError:
            self.ui.pmi_input.setText("0")
        
        self.update_total_exp_auto()

    def w_and_s_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.w_and_s_input.text()
            )
            
            self.WandS = float(value)
        except ValueError:
            self.ui.w_and_s_input.setText("0")
        
        self.update_total_exp_auto()
        
    def electric_input_changed(self):
        try:
            value = self.formatted_currency_to_float(
                self.ui.electric_input.text()
            )
            
            self.electric = float(value)
        except ValueError:
            self.ui.electric_input.setText("0")
        
        self.update_total_exp_auto()
        
    def r_and_m_input_changed(self):
        """Repair and maintenance"""
        try:
            value = self.percent_to_float(
                self.ui.r_and_m_input.text()
            )            
            self.rep_and_main = float(value) / 100
        except ValueError as ex:
            print('r_and_m_input_changed', ex)
            self.ui.r_and_m_auto.setText("0")
            #self.ui.tot_var_exp_auto.setText("0")
        
        self.rep_and_main_dollar = REI_Calculations.calculate_dollar_amount(
            self.total_income_monthly,
            self.rep_and_main
        )
        self.ui.r_and_m_auto.setText(str(self.rep_and_main_dollar))
        self.set_currency_format(self.ui.r_and_m_auto)
        
        # update total (fixed, variable) expenses
        self.update_total_exp_auto()
        
    def update_total_exp_auto(self):
        """Update total expenses (fixed and variable)
        """
        self.total_variable_expense, _ = REI_Calculations.variable_expenses_monthly(
            self.rep_and_main_dollar,
            self.cap_ex_dollar,
            self.vacancy_dollar,
            self.management_dollar
        )
        self.ui.tot_var_exp_auto.setText(str(self.total_variable_expense))
        self.set_currency_format(self.ui.tot_var_exp_auto)
        
        self.total_fixed_expense, _ = REI_Calculations.fixed_expenses_monthly(
            self.electric, self.WandS, self.PMI,
            self.garbage, self.HOA, self.insurance,
            self.taxes, self.other_fixed_expense
        )
        self.ui.tot_fixed_exp_auto.setText(str(self.total_fixed_expense))
        self.set_currency_format(self.ui.tot_fixed_exp_auto)
        
    def other_income_month_changed(self):
        try:
            self.other_income_month = float(
                self.ui.other_income_month_input.text()
                .strip()
                .replace("%", "")
                .replace(",", ".")
            )
        except Exception as ex:
            self.show_message("Wrong value for other income month", msg_type="warning")

    def downpayment_percent_changed(self, value):
        self.downpayment = value / 100
        self.calculate_downpayment_dollar()                   
        self.calculate_loan_amount()    
        
    def calculate_downpayment_dollar(self):        
        self.downpayment_dollar = REI_Calculations.calculate_dollar_amount(
            self.purchase_price, self.downpayment 
        )
        self.ui.dp_dollar_auto_2.setText(str(self.downpayment_dollar))          
        
    def calculate_loan_amount(self):
        # loan amount auto calculation            
        self.loan_amount_auto = REI_Calculations.full_loan_amount(
            self.purchase_price, 
            self.finance_rehab_logical, 
            self.rehab_budget, 
            self.downpayment_dollar 
        )
        self.ui.loan_amount_auto_2.setText(str(self.loan_amount_auto))
        
    def interest_rate_changed(self, value):
        self.int_rate = value / 100        
        #self.calculate_loan_amount()

    def term_years_changed(self, value):
        self.term = value 
        #self.calculate_loan_amount()
        
    def ave_rent_changed(self):
        try:
            self.ave_rent = float(
                self.ui.ave_rent_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            self.show_message(
                message="Wrong value for average rent per unit", 
                msg_type="warning"
            )
            
    def manag_input_changed(self):
        try:
            value = self.percent_to_float(
                self.ui.manag_input.text()
            )
            self.management = float(value) / 100
        except ValueError:
            self.ui.manag_auto.setText("0")
            #self.ui.tot_fixed_exp_auto.setText("0")
            #self.ui.tot_var_exp_auto.setText("0")            
        
        self.management_dollar = REI_Calculations.calculate_dollar_amount(
            self.total_income_monthly,
            self.management
        )
        self.ui.manag_auto.setText(str(self.management_dollar))
        self.set_currency_format(self.ui.manag_auto)
        self.update_total_exp_auto()

    def cap_ex_input_changed(self):
        try:
            value = self.percent_to_float(
                self.ui.cap_ex_input.text()
            )
            self.cap_ex = float(value) / 100
        except ValueError:
            self.ui.cap_ex_auto.setText("0")
        
        self.cap_ex_dollar = REI_Calculations.calculate_dollar_amount(
            self.total_income_monthly,
            self.cap_ex
        )
        self.ui.cap_ex_auto.setText(str(self.cap_ex_dollar))
        self.set_currency_format(self.ui.cap_ex_auto)
        self.update_total_exp_auto()

    def vacancy_input_changed(self):
        try:
            value = self.percent_to_float(
                self.ui.vacancy_input.text()
            )
            self.vacancy = float(value) / 100
        except ValueError:
            self.ui.vacancy_auto.setText("0")
            return
        
        self.vacancy_dollar = REI_Calculations.calculate_dollar_amount(
            self.total_income_monthly, 
            self.vacancy
        )
        self.ui.vacancy_auto.setText(str(self.vacancy_dollar))
        self.set_currency_format(self.ui.vacancy_auto)
        self.update_total_exp_auto()

    def repair_and_maintenance_changed(self):
        try:
            self.rep_and_main = float(
                self.ui.r_and_m_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            self.show_message(
                message="Wrong value for repair and maintenance", 
                msg_type="warning"
            )

    def cap_ex_changed(self):
        try:
            self.cap_ex = float(
                self.ui.cap_ex_input.text().strip().replace("%", "").replace(",", ".")
            )
        except Exception as ex:
            self.show_message(message="Wrong value for cap. ex", 
                              msg_type="warning")


    def generate_report(self):
        if not self.validate_values():
            return
        # self.init_fake_values()
        self.run_calculations()
        if not self.data:
            print("No data after calculations")
            return
        # dataframe for plotting three totals
        plot_data = DataFrame.from_dict(self.tmp_data).iloc[[0,1,7], :]
        property_data = {
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zip_code,
            'prior_year_taxes': self.prior_year_taxes,
            'landford_insurance': self.landford_insurance
        }
        html_report = data_output.generate_report(
            self.general_analysis_and_results, 
            self.data, 
            plot_data,
            property_data
        )
        self.saveAsPDF(html_report)
        QMessageBox.information(self, "Report Generated", "Report has been Generated successfully.", QMessageBox.Ok)


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

    def percent_to_float(self, value):
        return str(value).replace(',', '.').replace('%', '')
    
    def formatted_currency_to_float(self, value):
        return re.sub(r'\$|,', '', value)

    def run_calculations(self):
        ## Initially we just need to calculate the 12 key figures.
        ## Will then build a loop for the Pro forma statement.

        # Begin by calculating the monthly payment of the loan
        try:            
            payment = REI_Calculations.loan_payment(
                self.int_rate, self.term, self.loan_amount
            )
        except Exception as ex:
            _, _, tb = sys.exc_info()
            self.show_message(message='Run calculations', \
                              details=f'run_calculations(), loan_payment: Line: {tb.tb_lineno},\n {str(ex)}', \
                              msg_type='warning')            
            return False

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
            self.taxes, self.other_fixed_expense
        )

        var_monthly, var_yearly = REI_Calculations.variable_expenses_monthly(
            self.vacancy_dollar, self.rep_and_main_dollar, 
            self.cap_ex_dollar, self.management_dollar
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
            self.downpayment_dollar,
            self.closing_costs,
            self.emergency_fund,
            self.rehab_budget,
            self.finance_rehab_logical,
        )

        # 5 Calculate Cash on Cash Return (CoCR)
        CoCR = REI_Calculations.cash_on_cash_return(NIAF, cash_2_close)

        # 6 Calculate the cap rate
        try:
            capRate = REI_Calculations.cap_rate(NOI, self.purchase_price, self.rehab_budget, self.closing_costs)
        except Exception as ex:
            _, _, tb = sys.exc_info()
            self.show_message(message='Run calculations', 
                              details=f'run_calculations(), cap_rate: Line: {tb.tb_lineno},\n {str(ex)}', 
                              msg_type='warning')            
            return False
        
        # 7 Calculate Gross Rent Multiplier
        try:
            GRM = REI_Calculations.gross_rent_mult(
                self.purchase_price, self.rehab_budget, self.total_income_monthly
            )
        except Exception as ex:
            _, _, tb = sys.exc_info()
            self.show_message(message='Run calculations', 
                              details=f'run_calculations(), gross_rent_mult: Line: {tb.tb_lineno},\n {str(ex)}', 
                              msg_type='warning')            
            return False
        
        # 8,9 Calculate the 1 and 50 percent rules
        one_perc = REI_Calculations.one_perc_rule(
            self.purchase_price, self.rehab_budget, self.total_income_monthly
        )
        fifty_perc = REI_Calculations.fifty_perc_rule(
            fixed_monthly, var_monthly, self.total_income_monthly
        )
               
        self.general_analysis_and_results = [
            [ 
                '${:0,.2f}'.format(cash_2_close),  
                '${:0,.2f}'.format(self.purchase_price), 
                '${:0,.2f}'.format(self.total_income_monthly)
            ], 
            [ 
                '${:0,.2f}'.format(var_monthly + fixed_monthly), 
                '${:0,.2f}'.format(cf_monthly), 
                '{:0,.2f}%'.format(one_perc)
            ], 
            [ 
                '${:0,.2f}'.format(NOI),  
                '${:0,.2f}'.format(NIAF), 
                '{:0,.2f}%'.format(CoCR)
            ],
            [ 
                '{:0,.2f}%'.format(capRate), 
                '{:0,.2f}%'.format(fifty_perc),  
                '{:0,.2f}'.format(GRM)
            ]
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
        length_yrs = range(1, 11)

        for year_index in length_yrs:
            # Everything will be on a yearly scale and we may calculate some
            # variables two time for this first year
            
            # Calculate total annual income for each year
            try:
                tot_income_annual = REI_Calculations.future_value(
                    self.rent_appreciation, year_index - 1, 0, \
                        self.total_income_monthly * 12
                )
            except ZeroDivisionError:
                _, _, tb = sys.exc_info()
                self.show_message(message='tot_income_anual, future_value(...)', 
                                details=f'Line: {tb.tb_lineno},\n {str(ex)}', 
                                msg_type='warning')                
                break
            
            try:
                # Calculate total fixed expenses for each year
                fixed_yearly = REI_Calculations.future_value(
                    self.exp_appreciation, year_index - 1, 0, fixed_monthly * 12
                )
            except ZeroDivisionError:
                _, _, tb = sys.exc_info()
                self.show_message(message='fixed_yearly, future_value(...)', 
                                details=f'Line: {tb.tb_lineno},\n {str(ex)}', 
                                msg_type='warning')                
                break
                        

            # Calculate total variable expenses for each year
            var_yearly = tot_income_annual * sum(
                [self.rep_and_main, self.cap_ex, self.vacancy, self.management]
            )

            # Calculate Total Expenses
            tot_expense_yearly = sum([fixed_yearly, var_yearly])

            # Calculate NOI
            NOI_inLoop = REI_Calculations.NOI_yearly(
                tot_income_annual, fixed_yearly, var_yearly
            )

            NOI_growth = REI_Calculations.growth_rate( 
                NOI_inLoop, NOI, year_index
                )

            # Calculate Debt service
            if self.term < year_index:
                payment = 0
            payment_annual = payment * 12

            #print('NOI:', NOI, 'payment:', payment)
            
            # Calculate NIAF
            NIAF = REI_Calculations.NIAF_yearly(NOI_inLoop, payment)
            
            #print('NIAF:', NIAF)
            
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
                self.int_rate/12, year_index*12, payment, self.loan_amount_auto
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
                prop_value, self.selling_costs, loan_balance, cash_2_close, 
                cum_NIAF#, self.downpayment_dollar
            )
            
           
            # Calculate the compounded annual growth rate (CAGR) if sold
            CAGR = REI_Calculations.growth_rate(
                total_profit_sold + cash_2_close, cash_2_close, year_index
            )
            
            self.tmp_data[f'Year_{year_index}'] = [
                tot_income_annual, tot_expense_yearly, fixed_yearly,
                var_yearly, NOI_inLoop, NOI_growth,
                loan_balance, NIAF, prop_value,
                CoCR, cum_CoCR, tot_equity,
                equity_perc, ROI, total_profit_sold,
                CAGR
            ]
            
            # TODO: remove after testing
            #self.tmp_data[f'Year_{year_index}'] = [randint(0, 1200) for _ in range(16)]
            
            # format numbers to two decimal values
            tot_income_annual = '{:0,.2f}'.format(tot_income_annual)
            tot_expense_yearly = '{:0,.2f}'.format(tot_expense_yearly)
            fixed_yearly = '{:0,.2f}'.format(fixed_yearly)
            var_yearly = '{:0,.2f}'.format(var_yearly)
            NOI_inLoop = '{:0,.2f}'.format(NOI_inLoop)
            NOI_growth = '{:0,.2f}'.format(NOI_growth)
            loan_balance = '{:0,.2f}'.format(loan_balance)    
            NIAF = '{:0,.2f}'.format(NIAF)
            prop_value = '{:0,.2f}'.format(prop_value)
            tot_equity = '{:0,.2f}'.format(tot_equity)
            ROI = '{:0,.2f}'.format(ROI)
            total_profit_sold= '{:0,.2f}'.format(total_profit_sold)
            equity_perc = '{:0,.2f}'.format(equity_perc)
            format_CoCR = '{:0,.2f}'.format(CoCR)
            format_cum_CoCR = '{:0,.2f}'.format(cum_CoCR)
            try:
                format_CAGR = '{:0,.2f}'.format(CAGR)
            except ValueError as ex:
                print("run_calculations: CAGR exception: ", ex)
                format_CAGR = CAGR
            
            
            self.data[f'Year_{year_index}'] = [
                f'${tot_income_annual}', f'${tot_expense_yearly}', f'${fixed_yearly}',
                f'${var_yearly}', f'${NOI_inLoop}', f'{NOI_growth}%',
                f'${loan_balance}', f'${NIAF}', f'${prop_value}',
                f'{format_CoCR}%' ,f'{format_cum_CoCR}%', f'${tot_equity}',
                f'{equity_perc}%', f'{ROI}%', f'${total_profit_sold}',
                f'{format_CAGR}%'
            ]


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = CalculatorWindow()
    application.show()
    sys.exit(app.exec())
