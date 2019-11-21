library(readr)
N300s <- read_csv('C:\\Users\\Evan\\Documents\\N300_effects.csv')
colnames(N300s) <- c("AG","DG","ALmaj","ALmin","DLmaj","DLmin")
N300 <- stack(N300s)[1]
N300 <- unlist(N300)

nconds <- length(colnames(N300s))
subs <- dim(N300s)[1]

PID = rep(seq(from = 1, to = subs, by = 1), nconds)
attention <- c(rep('attended',subs),rep('distracted',subs),rep('attended',subs),rep('attended',subs),rep('distracted',subs),rep('distracted',subs))
context <- c(rep('global',subs*2),rep('local',subs*4))
freq <- c(rep('same',subs*2),rep('good_maj',subs),rep('good_min',subs),rep('good_maj',subs),rep('good_min',subs))
# subject <- c('bad','good','bad','good','bad','good','bad','bad','good','good','good','good','good','bad','bad','good','good','bad','bad','good','bad','bad','good','good','good','bad','good','good','good','good','good','bad','good','bad')

myData <- data.frame(PID,N300,attention,context,freq)

myData$CB <- ifelse(PID==1,3,NaN)
myData$CB <- ifelse(PID==2,1,myData$CB)
myData$CB <- ifelse(PID==3,3,myData$CB)
myData$CB <- ifelse(PID==4,2,myData$CB)
myData$CB <- ifelse(PID==5,3,myData$CB)
myData$CB <- ifelse(PID==6,2,myData$CB)
myData$CB <- ifelse(PID==7,1,myData$CB)
myData$CB <- ifelse(PID==8,2,myData$CB)
myData$CB <- ifelse(PID==9,1,myData$CB)
myData$CB <- ifelse(PID==10,2,myData$CB)
myData$CB <- ifelse(PID==11,1,myData$CB)
myData$CB <- ifelse(PID==12,2,myData$CB)
myData$CB <- ifelse(PID==13,3,myData$CB)
myData$CB <- ifelse(PID==14,2,myData$CB)
myData$CB <- ifelse(PID==15,2,myData$CB)
myData$CB <- ifelse(PID==16,1,myData$CB)
myData$CB <- ifelse(PID==17,2,myData$CB)
myData$CB <- ifelse(PID>17,4,myData$CB)

myData <- within(myData, {
  PID   <- factor(PID)
  attention <- factor(attention)
  context <- factor(context)
  freq <- factor(freq)
  CB <- factor(CB)
})

myData <- myData[order(myData$PID), ]


N300.aov <- with(myData, aov(N300 ~ attention*context + 
                                    Error(PID / (attention*context)))
)
summary(N300.aov)

library('ez')
library('lme4')
N300.CB.aov <- ezANOVA(myData,N300,PID,within=c(attention,context),between=CB,type=3,return_aov=T)

# N300.full.aov <- ezMixed(data=myData,dv=N300,family=gaussian,random=c(PID),fixed=c(attention,context,freq,CB))
# print(N300.full.aov$summary)

library('TOSTER')
TOSTpaired(m1=mean(myData$N300[myData$attention=="attended" & myData$context=="global"]),
           m2=mean(myData$N300[myData$attention=="distracted" & myData$context=="global"]),
           sd1=sd(myData$N300[myData$attention=="attended" & myData$context=="global"]),
           sd2=sd(myData$N300[myData$attention=="distracted" & myData$context=="global"]),
           n=20,r12=cor(myData$N300[myData$attention=="attended" & myData$context=="global"],myData$N300[myData$attention=="distracted" & myData$context=="global"]),
           low_eqbound_d=-0.3,high_eqbound_d=0.3,alpha=.05)

TOSTpaired(m1=mean(myData$N300[myData$attention=="attended" & myData$context=="local"]),
           m2=mean(myData$N300[myData$attention=="distracted" & myData$context=="local"]),
           sd1=sd(myData$N300[myData$attention=="attended" & myData$context=="local"]),
           sd2=sd(myData$N300[myData$attention=="distracted" & myData$context=="local"]),
           n=20,r12=cor(myData$N300[myData$attention=="attended" & myData$context=="local"],myData$N300[myData$attention=="distracted" & myData$context=="local"]),
           low_eqbound_d=-0.3,high_eqbound_d=0.3,alpha=.05)
