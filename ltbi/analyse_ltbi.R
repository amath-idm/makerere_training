######################################## 
# Analyse LTBI data
######################################## 

ltbi <- read.csv("ltbi_data.csv")
classifier <- lm(infected ~ bar_hours + school_hours, data=ltbi)
summary(classifier)
