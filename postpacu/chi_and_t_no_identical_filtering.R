# chi2 and t test
library(car)
library(dplyr)
library(readxl)
source("/workspaces/WagenerPostPACU/GeneralStore/StatisticalAnalysis/comparison_tests.R")

# get args from command line 
myargs = commandArgs(trailingOnly=TRUE)

 #"/data/DATASCI/raw/EscalationsAt3Days.xlsx"
data_in = myargs[1]
data_out = myargs[2]

# removed ICD 10 codes per Wagener and Barker
chi_squared_vars= c( 'Gender',
 'Race',
 'Ethnicity',
 'CKD',
 'AKI',
 'OpioidAbuseDiagnosis',
 'SleepApneaDiagnosis',
 'AlcoholUseDiagnosis',
 'ESRDfromProblemList',
 'COPDfromProblemList',
 'AsthmafromProblemList',
 'DiabetesfromProblemList',
 'WholeBlood',
 'Starches',
 'Dextran',
 'Epidural',
 'EpinephrineInfusion',
 'VasopressinInfusion',
 'MilrinoneInfusion',
 'DobutamineInfusion',
 'DopamineInfusion',
 'NorepinephrineInfusion',
 'PhenylephrineInfusion',
 'EMERGENCY',
 'CVL',
 'ArtLine',
 'RoomAir'
)


ttests_vars = c(
'Age', 'BMI', 'MinPACULastHour_SpO2', 'LastPACU_SpO2',
       'MaxPACULastHour_O2FlowRate', 'LastPACU_O2FlowRate',
       'MaxPACULastHour_SBP', 'LastPACU_SBP', 'MinPACULastHour_MAP',
       'MaxPACULastHour_MAP', 'LastPACU_MAP', 'MaxPACULastHour_RR',
       'LastPACU_RR', 'MaxPACULastHour_PainScore', 'LastPACU_PainScore',
       'MinPACULastHour_Aldrete', 'LastPACU_Aldrete', 'AlbuminLevel',
       'MACE_Score', 'EBL', 'Urine', 'PACU_Urine_mL', 'SugammadexAmount',
       'NeostigmineAmount', 'RBCs', 'NaCl', 'Normosol', 'Albumin', 'LR',
       'Isolyte', 'BloodProductsTotal', 'CrystalloidsTotal', 'LastPACU_Temp',
        'anes_duration', 'procedure_duration', 'PreOpPlatelets'
       , 'anes_surgical_duration_diff', 'MaxPACULastHour_HR', 'LastPACU_HR'
       , 'MinPACULastHour_SBP', 'PreOpGlucose', 'PreOpBicarb', 'PreOpHemoglobin'
       , 'PreOpHematocrit', 'PostOpGlucose', 'MinPACUTemp', 'MaxPACUTemp',
       'ASAStatus', 'Total_NonBloodFluids', 'FFP', 'Cryo', 'Platelets', 'CellSaver',  'D5and10'
)

pacu_df = read.csv(data_in)

out = compare_groups(chi_squared_vars, ttests_vars, pacu_df, "escalation")

write.csv(x=out
          , file=data_out
          , row.names = FALSE)
