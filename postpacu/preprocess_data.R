# Original paper method
library(dplyr)
library(readxl)
library(tidyverse)

# get args from command line 
myargs = commandArgs(trailingOnly=TRUE)

 #"/data/DATASCI/raw/EscalationsAt3Days.xlsx"
raw_data = myargs[1]

#"/data/DATASCI/intermediate/variable_setup_3days.csv"
data_out = myargs[2]

# "/data/DATASCI/intermediate/variable_setup_for_scorecard_3days.csv"
scorecard_data_out = myargs[3]

#"/data/DATASCI/results/missingness_report_3days.csv"
missingness_out = myargs[4]

# "/data/DATASCI/results/scorecard_missingness_report_3days.csv"
scorecard_missingness_out = myargs[5]



# Read data in from raw folder
# adjust path once R is working in a container
postpacu_df = read_excel(raw_data
                         , na="NA", guess_max =150000)

# treat surgical specialty as categorical
postpacu_df$SurgicalSpecialty = as.factor(postpacu_df$SurgicalSpecialty)

# make sure numeric variables are numeric
postpacu_df$MACE_Score = as.numeric(postpacu_df$MACE_Score)
postpacu_df$MaxPACULastHour_HR = as.numeric(postpacu_df$MaxPACULastHour_HR)
postpacu_df$LastPACU_HR = as.numeric(postpacu_df$LastPACU_HR)
postpacu_df$MinPACULastHour_SBP = as.numeric(postpacu_df$MinPACULastHour_SBP)
postpacu_df$MaxPACULastHour_SBP = as.numeric(postpacu_df$MaxPACULastHour_SBP)
postpacu_df$LastPACU_SBP = as.numeric(postpacu_df$LastPACU_SBP)
postpacu_df$MinPACULastHour_MAP = as.numeric(postpacu_df$MinPACULastHour_MAP)
postpacu_df$MaxPACULastHour_MAP = as.numeric(postpacu_df$MaxPACULastHour_MAP)
postpacu_df$LastPACU_MAP  = as.numeric(postpacu_df$LastPACU_MAP )
postpacu_df$MaxPACULastHour_O2FlowRate  = as.numeric(postpacu_df$MaxPACULastHour_O2FlowRate )
postpacu_df$LastPACU_O2FlowRate  = as.numeric(postpacu_df$LastPACU_O2FlowRate )
postpacu_df$MaxPACULastHour_RR  = as.numeric(postpacu_df$MaxPACULastHour_RR )
postpacu_df$MaxPACULastHour_PainScore  = as.numeric(postpacu_df$MaxPACULastHour_PainScore )
postpacu_df$LastPACU_PainScore  = as.numeric(postpacu_df$LastPACU_PainScore )
postpacu_df$MinPACULastHour_Aldrete  = as.numeric(postpacu_df$MinPACULastHour_Aldrete )
postpacu_df$LastPACU_Temp  = as.numeric(postpacu_df$LastPACU_Temp )
postpacu_df$MinPACUTemp  = as.numeric(postpacu_df$MinPACUTemp )
postpacu_df$MaxPACUTemp  = as.numeric(postpacu_df$MaxPACUTemp )

#consider only inpatient 
inpatient_df = subset(postpacu_df, InpatientStat==1)

# Use surgical specialty based on surgeon name is surgical specialty is missing
inpatient_df$SurgicalSpecialty = ifelse(
  (is.na(inpatient_df$SurgicalSpecialty)) & (!is.na(inpatient_df$SurgeonSpecialty)),
  inpatient_df$SurgeonSpecialty, inpatient_df$SurgicalSpecialty
)


# make diagnoses and conditions binary
inpatient_df$CKD = !is.na(inpatient_df$CKD)
inpatient_df$AKI = !is.na(inpatient_df$AKI)
inpatient_df$OpioidAbuseDiagnosis = !is.na(inpatient_df$OpioidAbuseDiagnosis)
inpatient_df$SleepApneaDiagnosis = !is.na(inpatient_df$SleepApneaDiagnosis)
inpatient_df$AlcoholUseDiagnosis = !is.na(inpatient_df$AlcoholUseDiagnosis)
inpatient_df$ESRDfromProblemList = !is.na(inpatient_df$ESRDfromProblemList)
inpatient_df$COPDfromProblemList = !is.na(inpatient_df$COPDfromProblemList)
inpatient_df$AsthmafromProblemList = !is.na(inpatient_df$AsthmafromProblemList)
inpatient_df$DiabetesfromProblemList = !is.na(inpatient_df$DiabetesfromProblemList)

# Make room air flag binary
inpatient_df$RoomAir = !is.na(inpatient_df$RoomAirDateTime)



# Some missings are actually 0
inpatient_df$SugammadexAmount[is.na(inpatient_df$SugammadexAmount)] = 0
inpatient_df$NeostigmineAmount[is.na(inpatient_df$NeostigmineAmount)] = 0
inpatient_df$RBCs[is.na(inpatient_df$RBCs)] = 0
inpatient_df$WholeBlood[is.na(inpatient_df$WholeBlood)] = 0
inpatient_df$FFP[is.na(inpatient_df$FFP)] = 0
inpatient_df$Cryo[is.na(inpatient_df$Cryo)] = 0
inpatient_df$Platelets[is.na(inpatient_df$Platelets)] = 0
inpatient_df$CellSaver[is.na(inpatient_df$CellSaver)] = 0
inpatient_df$D5and10[is.na(inpatient_df$D5and10)] = 0
inpatient_df$NaCl[is.na(inpatient_df$NaCl)] = 0
inpatient_df$Normosol[is.na(inpatient_df$Normosol)] = 0
inpatient_df$Albumin[is.na(inpatient_df$Albumin)] = 0
inpatient_df$Starches[is.na(inpatient_df$Starches)] = 0
inpatient_df$LR[is.na(inpatient_df$LR)] = 0
inpatient_df$Isolyte[is.na(inpatient_df$Isolyte)] = 0
inpatient_df$Dextran[is.na(inpatient_df$Dextran)] = 0
# if no flow rate and patient on room air, set flow rate to 0
inpatient_df$MaxPACULastHour_O2FlowRate = ifelse(
  (is.na(inpatient_df$MaxPACULastHour_O2FlowRate)) & (inpatient_df$RoomAir),
  0, inpatient_df$MaxPACULastHour_O2FlowRate
)
inpatient_df$LastPACU_O2FlowRate = ifelse(
  (is.na(inpatient_df$LastPACU_O2FlowRate)) & (inpatient_df$RoomAir),
  0, inpatient_df$LastPACU_O2FlowRate
)


# create binary version of vitals from expert-determined thresholds 
inpatient_df$LastSpO2lte92 = inpatient_df$LastPACU_SpO2 <= 92 
inpatient_df$LastO2Flowgt2= inpatient_df$LastPACU_O2FlowRate > 2 
inpatient_df$LastHRgte90= inpatient_df$LastPACU_HR >= 90 
inpatient_df$LastSBPlte100 = inpatient_df$LastPACU_SBP <= 100 
inpatient_df$LastSBPgte100 = inpatient_df$LastPACU_SBP >= 160 
inpatient_df$LastMAPlte60 = inpatient_df$LastPACU_MAP <= 60 
inpatient_df$LastMAPgte85 = inpatient_df$LastPACU_MAP >= 85 
inpatient_df$LastRRgte20 = inpatient_df$LastPACU_RR >= 20
inpatient_df$LastPaingte5 = inpatient_df$LastPACU_PainScore >= 5


# length-of-time variables
inpatient_df$anes_duration = as.numeric(difftime(inpatient_df$AnesthesiaEnd, inpatient_df$AnesthesiaStart, units="mins"))
inpatient_df$procedure_duration = as.numeric(difftime(inpatient_df$PROCEDUREEND, inpatient_df$PROCEDURESTART, units="mins"))
inpatient_df$anes_surgical_duration_diff = as.numeric(inpatient_df$anes_duration - inpatient_df$procedure_duration)


# build response variable
# Was there a post-PACU escalation?
inpatient_df$escalation = (inpatient_df$MET_Team==1) | 
  (inpatient_df$ICUafterPACU_Days==1 & inpatient_df$ICU_Bed_Order==0) |
  (!is.na(inpatient_df$StepDownUnitAfterGeneralCareTime_Days)) |
  (inpatient_df$ICU_AfterStepDown_NoOrderBeforePacuDepart_Days==1)

# delete phi and redundant variables
phi_vars = c( 
  "InternalCaseID"
  , "FinancialNumber"
  , "surgicalCaseNumber"
  , "MinPACUOut"
  , "AnesthesiaStart"
  , "AnesthesiaEnd"
  , "PROCEDUREEND"
  , "PROCEDURESTART"
  , "GeneralFloorAdmitTime"
  , "MEDICALRECORDNUMBER"
  #, "MET_Team"
  , "ICUafterPACU"
  #, "ICU_Bed_Order"
  , "ICU_BedOrder_BeforePacuDepart"
  #, "StepDownUnitAfterGeneralCareTime_Days"
  #, "ICU_AfterStepDown_NoOrderBeforePacuDepart"
  , "StepDownUnitAfterGeneralCareTime"
  , "EncounterType"
  , "InpatientStat"
  , "Inpatient"
  #, "ICUafterPACU_Days"
  , "RoomAirDateTime"
  , "PRIMARYSURGEON"
  , "SurgeonSpecialty"
)
postpacu_to_use_for_scorecard = inpatient_df[ , -which(names(inpatient_df) %in% phi_vars)]

# some features have special values for purposes of scorecard building
# should we use -9999 instead? Make it clearer?
# if ESRD is true and Urine is empty, then mark urine special (-1)
postpacu_to_use_for_scorecard$Urine = ifelse(
(is.na(postpacu_to_use_for_scorecard$Urine)) & (postpacu_to_use_for_scorecard$ESRDfromProblemList),
-1, postpacu_to_use_for_scorecard$Urine
)

postpacu_to_use_for_scorecard$PACU_Urine_mL = ifelse(
  (is.na(postpacu_to_use_for_scorecard$PACU_Urine_mL)) & (postpacu_to_use_for_scorecard$ESRDfromProblemList),
  -1, postpacu_to_use_for_scorecard$PACU_Urine_mL
)

# if diabetes is false and glucose is empty, then mark glucose as special (-1)
postpacu_to_use_for_scorecard$PreOpGlucose = ifelse(
  (is.na(postpacu_to_use_for_scorecard$PreOpGlucose)) & (!postpacu_to_use_for_scorecard$DiabetesfromProblemList),
  -1, postpacu_to_use_for_scorecard$PreOpGlucose
)

postpacu_to_use_for_scorecard$PostOpGlucose = ifelse(
  (is.na(postpacu_to_use_for_scorecard$PostOpGlucose)) & (!postpacu_to_use_for_scorecard$DiabetesfromProblemList),
  -1, postpacu_to_use_for_scorecard$PostOpGlucose
)



write.csv(x=postpacu_to_use_for_scorecard
          , file=scorecard_data_out
          , row.names = FALSE)

# missingness for scorecard
postpacu_to_use_for_scorecard_missing_table = t(as.data.frame(map(postpacu_to_use_for_scorecard, ~mean(is.na(.))) ))
write.csv(file=scorecard_missingness_out, x=postpacu_to_use_for_scorecard_missing_table)


# If a min/max last hour is null, use the last value recorded
inpatient_df$MaxPACULastHour_HR = ifelse(is.na(inpatient_df$MaxPACULastHour_HR), inpatient_df$LastPACU_HR, inpatient_df$MaxPACULastHour_HR)
inpatient_df$MaxPACULastHour_O2FlowRate = ifelse(is.na(inpatient_df$MaxPACULastHour_O2FlowRate), inpatient_df$LastPACU_O2FlowRate, inpatient_df$MaxPACULastHour_O2FlowRate)
inpatient_df$MaxPACULastHour_SBP = ifelse(is.na(inpatient_df$MaxPACULastHour_SBP), inpatient_df$LastPACU_SBP, inpatient_df$MaxPACULastHour_SBP)
inpatient_df$MaxPACULastHour_MAP = ifelse(is.na(inpatient_df$MaxPACULastHour_MAP ), inpatient_df$LastPACU_MAP, inpatient_df$MaxPACULastHour_MAP)
inpatient_df$MaxPACULastHour_RR = ifelse(is.na(inpatient_df$MaxPACULastHour_RR ), inpatient_df$LastPACU_RR, inpatient_df$MaxPACULastHour_RR)
inpatient_df$MaxPACULastHour_PainScore = ifelse(is.na(inpatient_df$MaxPACULastHour_PainScore ), inpatient_df$LastPACU_PainScore, inpatient_df$MaxPACULastHour_PainScore)
inpatient_df$MaxPACUTemp = ifelse(is.na(inpatient_df$MaxPACUTemp ), inpatient_df$LastPACU_Temp, inpatient_df$MaxPACUTemp)

inpatient_df$MinPACULastHour_SpO2 = ifelse(is.na(inpatient_df$MinPACULastHour_SpO2 ), inpatient_df$LastPACU_SpO2, inpatient_df$MinPACULastHour_SpO2)
inpatient_df$MinPACULastHour_SBP = ifelse(is.na(inpatient_df$MinPACULastHour_SBP ), inpatient_df$LastPACU_SBP, inpatient_df$MinPACULastHour_SBP)
inpatient_df$MinPACULastHour_MAP = ifelse(is.na(inpatient_df$MinPACULastHour_MAP ), inpatient_df$LastPACU_MAP, inpatient_df$MinPACULastHour_MAP)
inpatient_df$MinPACULastHour_Aldrete = ifelse(is.na(inpatient_df$MinPACULastHour_Aldrete ), inpatient_df$LastPACU_Aldrete, inpatient_df$MinPACULastHour_Aldrete)
inpatient_df$MinPACUTemp = ifelse(is.na(inpatient_df$MinPACUTemp ), inpatient_df$LastPACU_Temp, inpatient_df$MinPACUTemp)


postpacu_to_use = inpatient_df[ , -which(names(inpatient_df) %in% phi_vars)]

write.csv(x=postpacu_to_use
          , file=data_out
          , row.names = FALSE)


# missingness
postpacu_missing_table = t(as.data.frame(map(postpacu_to_use, ~mean(is.na(.))) ))
write.csv(file=missingness_out, x=postpacu_missing_table)
