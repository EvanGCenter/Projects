
lag.first <- runif(7,.65,.9) #first bit of target curve, good accuracy
lag.supp <- runif(6,.4,.9) #chance for suppression
lag.last <- runif(3,.65,.9) #last bit of target curve, good accuracy
target <- c(lag.first,lag.supp,lag.last) #combine to make target suppression curvve
control <- runif(16,.65,.9) #control suppression curve
plot(target,type = 'b', ylim = c(.25,1),col=4,main = 'Simulated Suppression Curves',
     ylab = 'proportion correct', xlab = 'TMS lag') #plot the data
points(control,type = 'b', col=2) 
cutoff <- mean(control)-.05
abline(cutoff,0,col=3) #line under which we need 3 consecutive target points
legend('bottomleft', legend=c('target','control'),pch = 'o',col = c('blue','red'))
sd(target) #and sd needs to be over .1
sd.thresh <- .1

check <- ifelse(target<cutoff,1,0)
trio <- rep(0,16)

for (i in 1:(length(target)-2)){
  bound = i+2
  if (sum(check[i:bound])>2){
    trio[i] = 1
  }
}

ifelse(any(trio==1), '3 consecutive pass', '3 consecutive fail')
ifelse(sd(target)>sd.thresh, 'SD pass', 'SD fail')
a = ifelse(any(trio==1),1,0)
b = ifelse(sd(target)>sd.thresh,1,0)
ifelse(a+b==2,'PASS','FAIL')