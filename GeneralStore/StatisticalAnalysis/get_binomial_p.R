# Get binomial p-value

get_binomial_p = function(x, y, data){
  model_form = as.formula(paste(y,x,sep="~"))
  model = glm(model_form, family="binomial", data=data)
  pv = coef(summary(model))[-1,4,drop=FALSE]
  or = exp(coef(model))[-1]
  ci = exp(confint(model))[-1,]
  if(is.null(dim(ci))){
    ci_formatted = paste("(", round(ci[1],2),", ",round(ci[2],2), ")", sep="")
  }else{
    ci_formatted = paste(
      "(", round(ci[,1],2), ", ", round(ci[,2],2), ")", sep=""
    )
  }
  output=data.frame(
    formula_name=x, variable=row.names(pv), pvalue=pv, odds_ratio=or, confint=ci_formatted, significant=any(pv<0.05)
  )
  return(output)
}
