#Sys.which("make")
install.packages("xlsx")
install.packages("readxl")
install.packages("dplyr")
install.packages("ggplot2")
library("ggplot2")
library("xlsx")
library("readxl")
library("dplyr")

print(getwd())

my_data <- read_excel("QPEDataClean.xlsx")

print(head(my_data))

boxplot(my_data[, c(1,2,4)], show.names=TRUE, 
        main="Relative Time taken for 10,000 executions of QPE",
        ylab="time taken (ms)",
        cex.lab = 2,
        cex.axis = 2,
        cex.main = 2,
        cex.sub = 2)

boxplot(my_data[,1:2], show.names=TRUE, ylim = c(0,150))

boxplot(my_data[,3:5], show.names=TRUE, ylim = c(0, 50000))



