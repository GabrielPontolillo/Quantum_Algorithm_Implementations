#install.packages("xlsx")
library("xlsx")
library("readxl")
library("dplyr")
my_data <- read_excel("C:\\Users\\Gabriel\\Desktop\\University\\Quantum Computing Algorithms\\QFT\\QFT-R\\QFTres0000.xlsx")
str(my_data)
my_data = my_data/5000
my_data = my_data*2
my_data = my_data-1
my_data = acos(my_data)
my_data = my_data*(180/pi)
ans_lst = list("Qubit  1" = 1)
#message(names(my_data)[2])
# go through each row and calc lowest / second lowest
for (j in 1:nrow(my_data)) {
  low_ctr <- 400
  low_ctr_phase <- "+"
  low_ctr2 <- 400
  low_ctr2_phase <- "+"
  for (i in 1:ncol(my_data)){
    if (my_data[j,i] < low_ctr){
      low_ctr2 = low_ctr
      low_ctr2_phase = low_ctr_phase
      low_ctr = my_data[j,i]
      low_ctr_phase = names(my_data)[i]
    } else if (my_data[j,i] < low_ctr2 ){
      low_ctr2 = my_data[j,i]
      low_ctr2_phase = names(my_data)[i]
    }
  }
  message("Current lowest: ", low_ctr)
  message(low_ctr_phase)
  message("Second lowest:", low_ctr2)
  message(low_ctr2_phase)
  overallPhase <- 0
  if(low_ctr_phase == "+"){
    if(low_ctr2_phase == "i"){
      overallPhase <- 0 + low_ctr
    } else if (low_ctr2_phase == "-i"){
      overallPhase <- 360 - low_ctr
      if (low_ctr == 0){
        overallPhase <- 0
      }
    }
  } else if (low_ctr_phase == "i"){
    if(low_ctr2_phase == "+"){
      overallPhase <- 90 - low_ctr
    } else if (low_ctr2_phase == "-"){
      overallPhase <- 90 + low_ctr
    }
  } else if (low_ctr_phase == "-"){
    if(low_ctr2_phase == "i"){
      overallPhase <- 180 - low_ctr
    } else if (low_ctr2_phase == "-i"){
      overallPhase <- 180 + low_ctr
    }
  } else if (low_ctr_phase == "-i"){
    if(low_ctr2_phase == "+"){
      overallPhase <- 270 + low_ctr
    } else if (low_ctr2_phase == "-"){
      overallPhase <- 270 - low_ctr
    }
  }
  ans_lst[paste("Qubit ", toString(j))] <- overallPhase
}
str(ans_lst[])
my_data <- my_data %>% mutate("Calculated Phase" = ans_lst)
write.xlsx(my_data, 
           file = "C:\\Users\\Gabriel\\Desktop\\University\\Quantum Computing Algorithms\\QFT\\QFT-R\\QFTres0000Calc.xlsx",
           sheetName="QFT0111Results", append=FALSE)

