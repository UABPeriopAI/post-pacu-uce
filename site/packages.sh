#!/bin/sh

Rscript -e "options(download.file.method='libcurl'); install.packages(c(
        'scorecard'
        , 'plyr'
        , 'glmnet'
        , 'doParallel'
        , 'readxl'
        , 'MASS'
        , 'car'
        , 'snow'
        , 'ggpubr'
        , 'nortest'
        , 'tidyverse'
    ))"