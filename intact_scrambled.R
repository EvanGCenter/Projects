library(readr)
setwd('C:/Users/Evan/Documents/data/intact_scrambled/experiment_data/main')

IL_orange <- "#E84A27"
IL_blue <- "#13294b"

objSn <- list.files()

n_files <- length(objSn)
sum.space <- matrix(NaN,n_files,10)
colnames(sum.space) <- c('acc','frames','chiSq','dPrimeG','dPrimeB','gAcc','bAcc','fCI','gRT','bRT')

for (i in 1:n_files) {
  
  objSi <- read_csv(objSn[i])

  fail <- objSi$acc == "None"
  objSi$acc[fail] <- NaN
  objSi$acc <- as.integer(objSi$acc)
  
  failrt <- objSi$rt == "None"
  objSi$rt[failrt] <- NaN
  objSi$rt <- as.integer(objSi$rt)
  
  objSi$imType <- gsub("_.*$","",objSi$im)
  objSi$GvB <- gsub("[^ab]","",objSi$im)
  
  for (j in 1:length(objSi$acc)) {
    if (objSi$imType[j] == 'IM'){
      if (objSi$resp[j] == 'intact'){
        objSi$Hit[j] <- 1
        objSi$Miss[j] <- 0
        objSi$FA[j] <- 0
        objSi$CR[j] <- 0
      }
      else if (objSi$resp[j] == 'scrambled'){
        objSi$Hit[j] <- 0
        objSi$Miss[j] <- 1
        objSi$FA[j] <- 0
        objSi$CR[j] <- 0
      }
    }
    else if (objSi$imType[j] == 'DM'){
      if (objSi$resp[j] == 'intact'){
        objSi$Hit[j] <- 0
        objSi$Miss[j] <- 0
        objSi$FA[j] <- 1
        objSi$CR[j] <- 0
      }
      else if (objSi$resp[j] == 'scrambled'){
        objSi$Hit[j] <- 0
        objSi$Miss[j] <- 0
        objSi$FA[j] <- 0
        objSi$CR[j] <- 1
      }
    }
    else {
      objSi$Hit[j] <- NaN
      objSi$Miss[j] <- NaN
      objSi$FA[j] <- NaN
      objSi$CR[j] <- NaN
    }
  }
  
  sum.space[i,1] <- mean(na.omit(objSi$acc))
  sum.space[i,2] <- objSi$duration[1]
  sum.space[i,3] <- prop.test(sum(na.omit(objSi$acc)),length(na.omit(objSi$acc)))$p.val
  
  gH_index <- objSi$GvB == 'a' & objSi$imType == 'IM'
  gHits <- objSi$resp[gH_index]
  gHits <- ifelse(gHits=='intact',1,0)
  
  sum.space[i,9] <- mean(na.omit(objSi$rt[gH_index]))
  
  gFA_index <- objSi$GvB == 'a' & objSi$imType == 'DM'
  gFAs <- objSi$resp[gFA_index]
  gFAs <- ifelse(gFAs=='intact',1,0)
  
  bH_index <- objSi$GvB == 'b' & objSi$imType == 'IM'
  bHits <- objSi$resp[bH_index]
  bHits <- ifelse(bHits=='intact',1,0)
  
  sum.space[i,10] <- mean(na.omit(objSi$rt[bH_index]))
  
  bFA_index <- objSi$GvB == 'b' & objSi$imType == 'DM'
  bFAs <- objSi$resp[bFA_index]
  bFAs <- ifelse(bFAs=='intact',1,0)
  
  if (mean(gFAs)>0){
    dprimeG <- qnorm(mean(gHits))-qnorm(mean(gFAs))
  }
  else{dprimeG <- qnorm(mean(gHits))}
  if (mean(bFAs)>0){
    dprimeB <- qnorm(mean(bHits))-qnorm(mean(bFAs))
  }
  else{dprimeB <- qnorm(mean(bHits))}
  
  sum.space[i,4] <- dprimeG
  sum.space[i,5] <- dprimeB
  
  g_index <- objSi$GvB == 'a'
  g_acc <- mean(na.omit(objSi$acc[g_index]))
  b_index <- objSi$GvB == 'b'
  b_acc <- mean(na.omit(objSi$acc[b_index]))
  
  sum.space[i,6] <- g_acc
  sum.space[i,7] <- b_acc
  
}

setwd('C:/Users/Evan/Documents/data/intact_scrambled/pilot_4/quest')
objSn <- list.files()

for (i in 1:n_files) {
  objSi <- read_csv(objSn[i])
  sum.space[i,8] <- tail(objSi$upperCI,n=1)-tail(objSi$lowerCI,n=1)
}

library('effsize')
CD.ci.dp <- cohen.d(sum.space[,4],sum.space[,5],paired=T,conf.level=.95)
CD.ci.rt <- cohen.d(sum.space[,10],sum.space[,9],paired=T,conf.level=.95)