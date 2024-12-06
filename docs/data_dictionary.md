# Data Dictionary for Perioperative Variables Used in the Scorecard Model

The following is a data dictionary for the 66 variables used in the scorecard model predicting unplanned care escalations (UCE) for post-anesthesia care unit (PACU) patients during the perioperative period. Each variable includes its name, type, units (if applicable), description, possible values (for categorical variables), and any relevant notes.

---

# Response/Dependent variable

**Variable: escalation**

- **Type**: Boolean
- **Description**: Indicates whether the patient experienced an unexpected escalation of care within 3 midnights after PACU discharge.
- **Possible Values**:
  - `True` (Yes): The patient had an unexpected escalation of care.
  - `False` (No): The patient did not have an unexpected escalation of care.
  
---

### Definition of Escalation:

An **unexpected escalation of care** is defined as any of the following events occurring within 3 midnights after discharge from the Post-Anesthesia Care Unit (PACU):

1. **Medical Emergency Team (MET) Activation**:
   - The patient required intervention by the MET due to acute clinical deterioration.
   - **Indicator**: `MET_Team == 1`

2. **Unplanned ICU Admission Without Prior Order**:
   - The patient was transferred from a general inpatient floor to an Intensive Care Unit (ICU) without a pre-existing ICU bed order before PACU discharge.
   - **Indicator**:
     - `ICUafterPACU_Days == 1` **AND**
     - `ICU_Bed_Order == 0`

3. **Admission to Step-Down Unit After General Floor**:
   - The patient was initially admitted to a general inpatient floor and then unexpectedly transferred to a step-down or intermediate care unit.
   - **Indicator**: `StepDownUnitAfterGeneralCareTime_Days` is **not** missing (`not NA`)

4. **ICU Transfer from Step-Down Unit Without Prior Order**:
   - The patient was transferred from a step-down/intermediate care unit to an ICU without a prior ICU bed order before PACU discharge.
   - **Indicator**: `ICU_AfterStepDown_NoOrderBeforePacuDepart_Days == 1`

---

### Notes:

- **Timeframe**:
  - The escalation must occur within **3 midnights** after PACU discharge.
  - The 3-midnights period is used because the risk of postoperative complications, such as major adverse cardiac events (MACE), significantly decreases after this period.

- **Unexpected Nature**:
  - Escalations are considered **unexpected** if they occur without prior planning or orders placed before the patient left the PACU.
  - Planned admissions to higher levels of care (e.g., scheduled ICU admission) are **not** counted as unexpected escalations.

- **Aggregated Variable**:
  - The `escalation` variable combines several indicators of patient deterioration requiring higher acuity care.
  - It captures a range of events that signify an unanticipated need for increased monitoring or interventions.

- **Clinical Relevance**:
  - Identifying unexpected escalations helps in assessing the quality of perioperative care and predicting patients at risk for deterioration.
  - Understanding factors associated with escalations can guide interventions to improve patient safety.

---

### Related Variables and Indicators:

- **MET_Team**:
  - **Type**: Boolean
  - **Description**: Indicates if the MET was activated for the patient within the specified timeframe.

- **ICUafterPACU_Days**:
  - **Type**: Boolean
  - **Description**: Indicates if the patient was admitted to the ICU after PACU discharge within 3 midnights.

- **ICU_Bed_Order**:
  - **Type**: Boolean
  - **Description**: Indicates if there was an ICU bed order placed before PACU discharge.

- **StepDownUnitAfterGeneralCareTime_Days**:
  - **Type**: DateTime or Indicator
  - **Description**: Timestamp of transfer to a step-down unit after initial admission to a general floor.

- **ICU_AfterStepDown_NoOrderBeforePacuDepart_Days**:
  - **Type**: Boolean
  - **Description**: Indicates if the patient was transferred from a step-down unit to ICU without a prior ICU bed order.

---

### Data Handling:

- **Calculation in Data Processing**:
  - The `escalation` variable is calculated during data preprocessing using the following logic:

    ```python
    escalation = (
        (MET_Team == 1) |
        ((ICUafterPACU_Days == 1) & (ICU_Bed_Order == 0)) |
        (StepDownUnitAfterGeneralCareTime_Days is not NA) |
        (ICU_AfterStepDown_NoOrderBeforePacuDepart_Days == 1)
    )
    ```

- **Missing Data**:
  - Care is taken to handle missing values appropriately.
  - If certain indicators are missing, the logic ensures that only available data contribute to determining if an escalation occurred.

---

### Importance in the Model:

- The `escalation` variable serves as the **response variable** (dependent variable) in the predictive model.
- It represents the outcome that the model aims to predict based on various perioperative factors.
- Understanding and accurately defining this variable is crucial for model training, validation, and interpretation.

---

### Contextual Background:

- **Unplanned Care Escalations (UCE)**:
  - UCEs are significant events that can increase patient morbidity, prolong hospital stays, and escalate healthcare costs.
  - Early prediction of UCE risk allows clinicians to make informed decisions regarding patient monitoring, intervention, and resource allocation.

- **Clinical Significance**:
  - By analyzing factors associated with `escalation`, healthcare providers can identify at-risk patients and implement strategies to mitigate adverse events.

---

### Usage Considerations:

- **For Collaborators**:
  - When reproducing the model, ensure that the `escalation` variable is derived using the exact definitions and logic provided.
  - Consistent application of this definition is essential for the validity and comparability of the predictive model.

- **Data Integrity**:
  - Verify that all contributing indicators (`MET_Team`, `ICUafterPACU_Days`, etc.) are accurately recorded and timestamped.
  - Timeframes should be computed based on standardized date and time formats to ensure consistency.

---

# Explanatory/Independent variables

**Variable 0: Gender**

- **Type**: Categorical (String)
- **Description**: Patient's self-reported gender at the time of surgery.
- **Possible Values**: 'Female', 'Male', 'Undetermined'

---

**Variable 1: Age**

- **Type**: Numeric (Integer)
- **Units**: Years
- **Description**: Patient's age at the time of surgery.

---

**Variable 2: BMI**

- **Type**: Numeric (Float)
- **Units**: kg/m²
- **Description**: Patient's Body Mass Index (BMI).

---

**Variable 3: Race**

- **Type**: Categorical (String)
- **Description**: Patient's self-reported race.
- **Possible Values**:
  - 'American Indian or Alaska Native'
  - 'Asian'
  - 'African American'
  - 'Hispanic or Latino'
  - 'Multiple'
  - 'Native Hawaiian/Other Pacific Islander'
  - 'Other'
  - 'Unknown'
  - 'Caucasian'

---

**Variable 4: Ethnicity**

- **Type**: Categorical (String)
- **Description**: Patient's self-reported ethnicity.
- **Possible Values**:
  - 'Hispanic/Latino'
  - 'Multiple'
  - 'Non-Hispanic/Latino'
  - 'Not reported'

---

**Variable 5: MinPACULastHour_SpO2**

- **Type**: Numeric (Float)
- **Units**: Percentage (%)
- **Description**: Minimum oxygen saturation (SpO₂) recorded during the last hour before PACU discharge.

---

**Variable 6: LastPACU_SpO2**

- **Type**: Numeric (Float)
- **Units**: Percentage (%)
- **Description**: Last oxygen saturation (SpO₂) value recorded before PACU discharge.

---

**Variable 7: MaxPACULastHour_O2FlowRate**

- **Type**: Numeric (Float)
- **Units**: Liters per minute (L/min)
- **Description**: Maximum oxygen flow rate administered during the last hour before PACU discharge.

---

**Variable 8: LastPACU_O2FlowRate**

- **Type**: Numeric (Float)
- **Units**: Liters per minute (L/min)
- **Description**: Oxygen flow rate administered at the time of PACU discharge.

---

**Variable 9: MaxPACULastHour_HR**

- **Type**: Numeric (Float)
- **Units**: Beats per minute (bpm)
- **Description**: Maximum heart rate recorded during the last hour before PACU discharge.

---

**Variable 10: MinPACULastHour_SBP**

- **Type**: Numeric (Float)
- **Units**: Millimeters of mercury (mmHg)
- **Description**: Minimum systolic blood pressure recorded during the last hour before PACU discharge.

---

**Variable 11: MaxPACULastHour_SBP**

- **Type**: Numeric (Float)
- **Units**: mmHg
- **Description**: Maximum systolic blood pressure recorded during the last hour before PACU discharge.

---

**Variable 12: MinPACULastHour_MAP**

- **Type**: Numeric (Float)
- **Units**: mmHg
- **Description**: Minimum mean arterial pressure recorded during the last hour before PACU discharge.

---

**Variable 13: MaxPACULastHour_MAP**

- **Type**: Numeric (Float)
- **Units**: mmHg
- **Description**: Maximum mean arterial pressure recorded during the last hour before PACU discharge.

---

**Variable 14: LastPACU_MAP**

- **Type**: Numeric (Float)
- **Units**: mmHg
- **Description**: Last mean arterial pressure recorded before PACU discharge.

---

**Variable 15: MaxPACULastHour_RR**

- **Type**: Numeric (Float)
- **Units**: Breaths per minute
- **Description**: Maximum respiratory rate recorded during the last hour before PACU discharge.

---

**Variable 16: MaxPACULastHour_PainScore**

- **Type**: Numeric (Integer)
- **Description**: Maximum pain score recorded during the last hour before PACU discharge.
- **Scale**: 0 (no pain) to 10 (worst possible pain)

---

**Variable 17: MinPACULastHour_Aldrete**

- **Type**: Numeric (Integer)
- **Description**: Minimum Aldrete score recorded during the last hour before PACU discharge.
- **Scale**: 0 to 10
- **Notes**: The Aldrete score assesses patient recovery from anesthesia based on activity, respiration, circulation, consciousness, and oxygen saturation.

---

**Variable 18: CKD**

- **Type**: Boolean
- **Description**: Indicates if the patient had a diagnosis of Chronic Kidney Disease prior to surgery.
- **Possible Values**: `True` (Yes), `False` (No)

---

**Variable 19: AKI**

- **Type**: Boolean
- **Description**: Indicates if the patient had a diagnosis of Acute Kidney Injury prior to surgery.

---

**Variable 20: AlbuminLevel**

- **Type**: Numeric (Float)
- **Units**: Grams per deciliter (g/dL)
- **Description**: Preoperative serum albumin level.

---

**Variable 21: OpioidAbuseDiagnosis**

- **Type**: Boolean
- **Description**: Indicates if the patient had a diagnosis of opioid abuse.

---

**Variable 22: SleepApneaDiagnosis**

- **Type**: Boolean
- **Description**: Indicates if the patient had a diagnosis of sleep apnea.

---

**Variable 23: AlcoholUseDiagnosis**

- **Type**: Boolean
- **Description**: Indicates if the patient had a diagnosis related to alcohol use or abuse.

---

**Variable 24: ESRDfromProblemList**

- **Type**: Boolean
- **Description**: Indicates if End-Stage Renal Disease was listed in the patient's problem list.

---

**Variable 25: COPDfromProblemList**

- **Type**: Boolean
- **Description**: Indicates if Chronic Obstructive Pulmonary Disease was listed in the patient's problem list.

---

**Variable 26: AsthmafromProblemList**

- **Type**: Boolean
- **Description**: Indicates if asthma was listed in the patient's problem list.

---

**Variable 27: DiabetesfromProblemList**

- **Type**: Boolean
- **Description**: Indicates if diabetes was listed in the patient's problem list.

---

**Variable 28: MACE_Score**

- **Type**: Numeric (Float)
- **Description**: Major Adverse Cardiac Events score estimating the patient's risk for cardiac complications.
- **Notes**: Higher scores indicate greater risk.

---

**Variable 29: EBL**

- **Type**: Numeric (Float)
- **Units**: Milliliters (mL)
- **Description**: Estimated blood loss during the surgical procedure.

---

**Variable 30: SugammadexAmount**

- **Type**: Numeric (Float)
- **Units**: Milligrams (mg)
- **Description**: Total dose of Sugammadex administered during surgery.
- **Notes**: Sugammadex is a medication used to reverse neuromuscular blockade.

---

**Variable 31: NeostigmineAmount**

- **Type**: Numeric (Float)
- **Units**: Milligrams (mg)
- **Description**: Total dose of Neostigmine administered during surgery.
- **Notes**: Neostigmine is another medication used to reverse neuromuscular blockade.

---

**Variable 32: RBCs**

- **Type**: Numeric (Float)
- **Units**: Units or Milliliters (mL)
- **Description**: Amount of red blood cell transfusions administered during surgery.

---

**Variable 33: WholeBlood**

- **Type**: Numeric (Float)
- **Units**: Units or mL
- **Description**: Amount of whole blood transfusions administered during surgery.

---

**Variable 34: FFP**

- **Type**: Numeric (Float)
- **Units**: Units or mL
- **Description**: Amount of Fresh Frozen Plasma transfused during surgery.

---

**Variable 35: Cryo**

- **Type**: Numeric (Float)
- **Units**: Units or mL
- **Description**: Amount of Cryoprecipitate transfused during surgery.

---

**Variable 36: Platelets**

- **Type**: Numeric (Float)
- **Units**: Units or mL
- **Description**: Amount of platelets transfused during surgery.

---

**Variable 37: CellSaver**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of autologous blood returned to the patient using cell saver technology during surgery.

---

**Variable 38: D5and10**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of Dextrose 5% and Dextrose 10% intravenous fluids administered during surgery.

---

**Variable 39: Normosol**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of Normosol intravenous fluids administered during surgery.
- **Notes**: Normosol is a balanced electrolyte solution.

---

**Variable 40: Albumin**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of albumin solution administered during surgery.

---

**Variable 41: Starches**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of starch-based colloids administered during surgery.
- **Notes**: Includes solutions like hydroxyethyl starch.

---

**Variable 42: Isolyte**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of Isolyte intravenous fluids administered during surgery.
- **Notes**: Isolyte is an isotonic, balanced electrolyte solution.

---

**Variable 43: Dextran**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Volume of Dextran solution administered during surgery.

---

**Variable 44: Epidural**

- **Type**: Boolean
- **Description**: Indicates if an epidural procedure was performed during anesthesia care.

---

**Variable 45: EpinephrineInfusion**

- **Type**: Boolean
- **Description**: Indicates if an epinephrine infusion was administered during surgery.

---

**Variable 46: VasopressinInfusion**

- **Type**: Boolean
- **Description**: Indicates if a vasopressin infusion was administered during surgery.

---

**Variable 47: MilrinoneInfusion**

- **Type**: Boolean
- **Description**: Indicates if a milrinone infusion was administered during surgery.

---

**Variable 48: DobutamineInfusion**

- **Type**: Boolean
- **Description**: Indicates if a dobutamine infusion was administered during surgery.

---

**Variable 49: DopamineInfusion**

- **Type**: Boolean
- **Description**: Indicates if a dopamine infusion was administered during surgery.

---

**Variable 50: NorepinephrineInfusion**

- **Type**: Boolean
- **Description**: Indicates if a norepinephrine infusion was administered during surgery.

---

**Variable 51: PhenylephrineInfusion**

- **Type**: Boolean
- **Description**: Indicates if a phenylephrine infusion was administered during surgery.

---

**Variable 52: BloodProductsTotal**

- **Type**: Numeric (Float)
- **Units**: Units or mL
- **Description**: Total amount of blood products (RBCs, Whole Blood, FFP, Cryo, Platelets) administered during surgery.

---

**Variable 53: CrystalloidsTotal**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Total volume of crystalloid solutions administered during surgery.
- **Notes**: Includes solutions like Normal Saline (NaCl), Lactated Ringer's (LR), Normosol, Isolyte, Dextrose solutions, etc.

---

**Variable 54: EMERGENCY**

- **Type**: Boolean
- **Description**: Indicates if the surgery was classified as an emergency case.

---

**Variable 55: CVL**

- **Type**: Boolean
- **Description**: Indicates if a central venous line (central line) was placed during surgery.

---

**Variable 56: ArtLine**

- **Type**: Boolean
- **Description**: Indicates if an arterial line was placed during surgery.

---

**Variable 57: PreOpBicarb**

- **Type**: Numeric (Float)
- **Units**: Milliequivalents per liter (mEq/L)
- **Description**: Preoperative bicarbonate level from labs collected before surgery.

---

**Variable 58: PreOpHemoglobin**

- **Type**: Numeric (Float)
- **Units**: Grams per deciliter (g/dL)
- **Description**: Preoperative hemoglobin level from labs collected before surgery.

---

**Variable 59: PreOpPlatelets**

- **Type**: Numeric (Float)
- **Units**: Thousands per microliter (×10³/µL)
- **Description**: Preoperative platelet count from labs collected before surgery.

---

**Variable 60: LastPACU_Temp**

- **Type**: Numeric (Float)
- **Units**: Degrees Fahrenheit (°F)
- **Description**: Last recorded temperature before PACU discharge.

---

**Variable 61: PACU_Urine_mL**

- **Type**: Numeric (Float)
- **Units**: Milliliters (mL)
- **Description**: Total urine output measured during the PACU stay.

---

**Variable 62: Total_NonBloodFluids**

- **Type**: Numeric (Float)
- **Units**: mL
- **Description**: Total volume of non-blood fluids administered during surgery.
- **Notes**: Includes crystalloids and colloids such as D5W, Normal Saline, Lactated Ringer's, Albumin, etc.

---

**Variable 63: ASAStatus**

- **Type**: Categorical (Integer)
- **Description**: American Society of Anesthesiologists (ASA) physical status classification score assigned before surgery.
- **Possible Values**:
  - 1: Normal healthy patient
  - 2: Patient with mild systemic disease
  - 3: Patient with severe systemic disease
  - 4: Patient with severe systemic disease that is a constant threat to life
  - 5: Moribund patient who is not expected to survive without the operation
  - 6: Declared brain-dead patient whose organs are being removed for donor purposes

---

**Variable 64: RoomAir**

- **Type**: Boolean
- **Description**: Indicates if the patient was breathing room air (not receiving supplemental oxygen) at the time of PACU discharge.

---

**Variable 65: anes_surgical_duration_diff**

- **Type**: Numeric (Float)
- **Units**: Minutes
- **Description**: Difference between total anesthesia time and surgical procedure time.
- **Calculation**: `Anesthesia Duration - Procedure Duration`
- **Notes**: Represents non-surgical anesthesia time, potentially accounting for procedures like line placements, airway management, or delays.

---

### General Notes:

- **Boolean Variables**: Represented as `True` (Yes) or `False` (No).
- **Numeric Variables**: Missing values may be represented as `NA` or might be handled specially in the analysis.
- **Units**: Units are specified where applicable. Consistent units should be used throughout the dataset.
- **Time Variables**: Durations are calculated in minutes to ensure consistency.
- **Data Sources**: Variables are derived from electronic medical records, including clinical events, labs, medications administered, and problem lists.
- **Variable Handling**: Some variables may have special considerations in data processing, such as handling missing values or combining related variables.