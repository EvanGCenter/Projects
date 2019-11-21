#compare two skewed distributions

set.seed(1738)

n <- 20 #sample size
reps <- 10000 #n reps
pop <- n*reps #population size 
w1 <- 1.5 #set weights for skew shape
w2 <- 4
d <- 1 #pick effect size

#dist1 <- rbeta(pop,w1,w2) #pick which way you want the tails to go
dist1 <- rbeta(pop,w2,w1) 
dist1 <- scale(dist1)
dist2 <- rbeta(pop,w1,w2)
#dist2 <- rbeta(pop,w2,w1)
dist2 <- scale(dist2)
dist2 <- dist2+d #add the effect

group_As <- matrix(dist1, nrow = n) #make matrices for easy looping
group_Bs <- matrix(dist2, nrow = n)
p.values <- NULL

#do a bunch of t tests
for (i in 1:reps){
  p.values[i] <- t.test(group_As[,i],group_Bs[,i])$p.value
}

p.values <- as.numeric(p.values)
graph <- hist(p.values, breaks=c(seq(0,1,.01)), plot=FALSE) # store the graph without plotting it
graph$density <- graph$counts/(reps/100)  #convert to percentages rather than counts
type <- {'False Positive Rate ='}
plot(graph,freq=FALSE,main=paste('n =',n,'d =',d,type,mean(p.values<.05)),xlab='p value',ylab='Relative Frequency',col=c(rep('blue',5),rep('white',95)),abline(h=1, col='red'))


npp.values <- NULL

#do a bunch of WSRTs
for (i in 1:reps){
  npp.values[i] <- wilcox.test(group_As[,i],group_Bs[,i])$p.value
}

npp.values <- as.numeric(npp.values)
graph2 <- hist(npp.values, breaks=c(seq(0,1,.01)), plot=FALSE) # store the graph without plotting it
graph2$density <- graph2$counts/(reps/100)  #convert to percentages rather than counts
type <- {'Power, WSRT ='}
plot(graph2,freq=FALSE,main=paste('n =',n,'d =',d,type,mean(npp.values<.05)),xlab='p value',ylab='Relative Frequency',col=c(rep('blue',5),rep('white',95)),abline(h=1, col='red'))
