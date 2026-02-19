# Perform t-test across two groups
library(ggpubr)
library(nortest)

compare_means = function(binary_group, var, data){
  
  t = t.test(data[[var]][which(data[[binary_group]]==0)]
             , data[[var]][which(data[[binary_group]]==1)]
             , var.equal = FALSE
  )

  if(
    length(data[[var]][which(data[[binary_group]]==1)])<5000 &
     length(data[[var]][which(data[[binary_group]]==0)])<5000) {
  # check t-test assumption
  # Shapiro-Wilk normality test for control
  control_assumption = shapiro.test(data[[var]][which(data[[binary_group]]==0)])$p.value>0.05
  # Shapiro-Wilk normality test for positive
  positive_assumption = shapiro.test(data[[var]][which(data[[binary_group]]==1)])$p.value>0.05
  
    w = wilcox.test(data[[var]][which(data[[binary_group]]==0)]
                  , data[[var]][which(data[[binary_group]]==1)]
                  , conf.int = TRUE)

  if(control_normality_assumption & positive_normality_assumption){
    test_different = t$p.value<0.0
    test_p = t$p.value
    difference_estimate_low95 = t$conf.int[[1]][1]
    difference_estimate_high95 = t$conf.int[[2]][1]
  }else{
    warning("t-test assumptions not met, using Wilcox instead")
    test_different = w$p.value<0.0
    test_p = w$p.value
    difference_estimate_low95 = w$conf.int[[1]][1]
    difference_estimate_high95 = w$conf.int[[2]][1]
  }

  output=data.frame(
    variable = var
    , control_mean = t$estimate[1]
    , positive_mean = t$estimate[2]
    , test_different = test_different
    , test_p = test_p
    , difference_estimate_low95 = difference_estimate_low95
    , difference_estimate_high95 = difference_estimate_high95
  )
  }else{
  
  output=data.frame(
    variable = var
    , control_mean = t$estimate[1]
    , positive_mean = t$estimate[2]
    , test_different = t$p.value<0.05
    , test_p = t$p.value
    , difference_estimate_low95 = t$conf.int[[1]][1]
    , difference_estimate_high95 = t$conf.int[[2]][1]
  )
  }
  rownames(output) <- NULL
  return(output)
}