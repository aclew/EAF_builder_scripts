#Rlena package installation script

library(devtools)
devtools::install_github("HomeBankCode/rlena", dependencies=FALSE)
print('installed')
library(rlena)
library(dplyr, warn.conflicts = FALSE)