# setwd('~/code/rahulvaity25/stock_prediction/stock_prediction/r_docker/')
library(plumber) 

root <- pr("plumber.R")
root
root %>% pr_run(port = 8079, host = '0.0.0.0')


