library(plumber) 

root <- pr("plumber.R")
root
root %>% pr_run(port = 8079, host = '0.0.0.0')


