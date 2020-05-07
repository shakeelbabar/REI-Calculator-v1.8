#!/bin/sh

TMP_GUI="gui_tmp.py"
FINAL_GUI="gui2.py"

echo "Converting ui to py..."
pyuic5 FinalGUI.ui -o $TMP_GUI

if [ ! -e $TMP_GUI ]; then
    printf "%s does not exist\n" $TMP_GUI
    exit
fi

currency_inputs=("taxes_input" "annual_insurance_input" "asking_price_input"
"purchase_price_input" "rehab_budget_input" "arv_input"
"closing_costs_input" "emerg_fund_input" "other_income_month_input"
"ave_rent_input" "electric_input" "w_and_s_input" "pmi_input"
"garbage_input" "hoa_input" "other_input" "r_and_m_input"
"cap_ex_input" "vacancy_input" "manag_input" "rent_appreciation_input"
"exp_appreciation_input" "prop_appreciation_input" "selling_costs_input"
"")


#currency_inputs=("taxes_input" "annual_insurance_input" "asking_price_input"
#"purchase_price_input" "rehab_budget_input" "arv_input"
#"closing_costs_input" "emerg_fund_input" "dp_dollar_auto_2"
#"loan_amount_auto_2" "ave_rent_input" "tot_rent_month_auto"
#"tot_income_month_auto" "tot_fixed_exp_auto" "tot_var_exp_auto"
#"electric_input" "w_and_s_input" "pmi_input" "garbage_input"
#"hoa_input" "monthly_taxes_auto" "insurance_auto" "other_input"
#"r_and_m_auto" "cap_ex_auto" "vacancy_auto" "manag_auto"
#"")

echo "Number of inputs: ${#currency_inputs[*]}"

echo "Replacing qlineedit by MyQlineEdit..."

for item in ${currency_inputs[*]}
do
    #printf "%s\n" $item
    sed -i "s/self.$item = QtWidgets.QLineEdit/self.$item = MyQlineEdit/g" $TMP_GUI
done


#echo "Replacing qlineedit by MyQlineEdit..."
#sed "s/QtWidgets.QLineEdit/MyQlineEdit/g" $TMP_GUI >$FINAL_GUI

echo "Setting imports..."
sed -i "11i from custom_qlineedit import MyQlineEdit" $TMP_GUI
sed -i "12i import resources" $TMP_GUI

echo "Removing not needed imports..."
sed -i "s/import SFI-white_rc//g" $TMP_GUI

echo "Renaming $TMP_GUI to $FINAL_GUI..."

mv $TMP_GUI $FINAL_GUI

echo "Done"
