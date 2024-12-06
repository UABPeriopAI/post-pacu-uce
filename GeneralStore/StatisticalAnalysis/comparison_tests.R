source("GeneralStore/StatisticalAnalysis/compare_means.R")

compare_groups = function(chi_squared_vars, ttests_vars, data, y){
    # Chi-squared tests
    output_df = NULL

    for( var in chi_squared_vars){
        print(var)
    twoway_table = table(data[[var]]
                        , data[[y]]
                        , dnn=c(var, y) 
                        #, row.names=c("No", "Yes")
    )

    # simulate option uses Fisher's exact test -- conditioning on the margins
    x2 = chisq.test(twoway_table, simulate.p.value = TRUE) 
    
    # assemble table
        output_row=data.frame(
        Variable=paste(var,"-",rownames(twoway_table))
        , PositiveGroup=twoway_table[,2]
        , NegativeGroup = twoway_table[,1]
        , P = c(round(x2$p.value,3), rep(NaN, length(rownames(twoway_table))-1))
    )
    output_df = rbind(output_df, output_row)
    }

    # t-tests
    for(var in ttests_vars){
        print(var)
    comparison_tests = compare_means(binary_group = y
    , var = var, data = data)
    testp = comparison_tests$test_p
    output_row=data.frame(
        Variable= var
        , PositiveGroup=round(comparison_tests$positive_mean,2)
        , NegativeGroup = round(comparison_tests$control_mean,2)
        , P = round(testp,4)
    )
    output_df = rbind(output_df, output_row)
    }
return(output_df)
}