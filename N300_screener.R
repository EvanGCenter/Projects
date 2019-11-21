library(readr)
setwd('C:/Users/Evan/Documents/MATLAB/DATA/Behavioral/N300/real')

IL_orange <- "#E84A27"
IL_blue <- "#13294b"

objSn <- list.files()

n_files <- length(objSn)

all.effects <- read_csv('C:\\Users\\Evan\\Documents\\all_effects.csv')

CBR <- matrix(NaN,n_files/6,10)
ans_global <- matrix(NaN,n_files/6)
ans_local <- matrix(NaN,n_files/6)

for (i in 1:n_files) {
  
  objSi <- read_csv(objSn[i])
  
  p <- objSi$participant[1]
  
  fail <- objSi$resp == "None"
  objSi$resp[fail] <- NaN
  objSi$resp <- as.integer(objSi$resp)
  
  if (length(grep('att_global',objSn[i]))>0) {
    CBR[p,1] <- sum(na.omit(objSi$resp))
    ans_global[p] <- length(na.omit(objSi$resp))
    }
  else if (length(grep('att_local',objSn[i]))>0) {
    CBR[p,2] <- sum(na.omit(objSi$resp))
    ans_local[p] <- length(na.omit(objSi$resp))
    }
  else if (length(grep('dst_global',objSn[i]))>0) {
    CBR[p,3] <- 1-(sum(objSi$stimAcc)/(200*360))
    CBR[p,4] <- 1-(sum(objSi$blankAcc)/(500*360))
    }
  else if (length(grep('dst_local',objSn[i]))>0) {
    CBR[p,5] <- 1-(sum(objSi$stimAcc)/(200*720))
    CBR[p,6] <- 1-(sum(objSi$blankAcc)/(500*720))
  }
  CBR[p,7] <- all.effects$P2[p]
  CBR[p,8] <- all.effects$P3[p]
  CBR[p,9] <- all.effects$N300attMain[p]
}


for (j in 1:dim(CBR)[1]){
  CBR[j,10] <- ifelse(prop.test(as.integer(CBR[j,1])+as.integer(CBR[j,2]),ans_global[j]+ans_local[j],alternative='greater')$p.value<=prop.test(12,18,alternative='greater')$p.value,'good','bad')
}

colnames(CBR) <- c('global_correct','local_correct','stimAccG',
                   'blankAccG','stimAccL','blankAccL','P2','P3','N300','sub_type')

CBR <- as.data.frame(CBR)
CBR <- cbind(sub_num = seq(1,39,1), CBR)

write_csv(CBR,'C:/Users/Evan/Documents/N300_summary.csv')
