library(readr)

#setwd('C:/Users/Evan/Documents/data/objects_data/time')
#setwd('C:/Users/Evan/Documents/data/scene_vs_scene_winners')
#setwd('C:/Users/Evan/Documents/data/scene_vs_scene')
# setwd('C:/Users/Evan/Documents/data/ori_real')
#setwd('C:/Users/Evan/Documents/data/ori_acc_plus60')
# setwd('C:/Users/Evan/Documents/data/PF_TP_word_audio/success')
# setwd('C:/Users/Evan/Documents/data/PF_TP_word_audio/pilot_no_acro/auditory')
setwd('C:/Users/Evan/Documents/data/PF_TP_word_audio/pilot_no_acro/visual')


IL_orange <- "#E84A27"
IL_blue <- "#13294b"

#IL_orange <- "orange"
#IL_blue <- "blue"

objSn <- list.files()

n_files <- length(objSn)

PSE_G <- matrix(NaN,n_files,1)
PSE_B <- matrix(NaN,n_files,1)
accs <- matrix(NaN,n_files,1)
ChiSq <- matrix(NaN,n_files,2)

for (i in 1:n_files) {

  objSi <- read_csv(objSn[i])
  
  objSi <- objSi[!(objSi$rt < .05),]
  objSi$acc <- ifelse(objSi$comp_frames == median(objSi$comp_frames), NaN, objSi$acc)
  
  fail <- objSi$cjl == "None"
  objSi$cjl[fail] <- NaN
  objSi$cjl <- as.integer(objSi$cjl)
  
  yg <- objSi$cjl[objSi$comp_id=="word"]
  xg <- objSi$comp_frames[objSi$comp_id=="word"]

  yb <- objSi$cjl[objSi$comp_id=="pseudoword"]
  xb <- objSi$comp_frames[objSi$comp_id=="pseudoword"]
  
  fit_G <- glm(yg ~ xg, family = binomial(link = "logit"))
  fit_B <- glm(yb ~ xb, family = binomial(link = "logit"))
  
  # plot(xg,fit_G$fitted.values, ylim = c(0,1))
  # curve(predict(fit_G,data.frame(xg = x),type = "response"),add = TRUE)
  # 
  # plot(xb,fit_B$fitted.values, ylim = c(0,1))
  # curve(predict(fit_B,data.frame(xb = x),type = "response"),add = TRUE)
  
  PSE_G[i] <- ((log(.5/(1-.5)) - coef(fit_G)[1])/coef(fit_G)[2])*(1/60)*1000
  PSE_B[i] <- ((log(.5/(1-.5)) - coef(fit_B)[1])/coef(fit_B)[2])*(1/60)*1000
  accs[i] <- mean(na.omit(objSi$acc))
  ChiSq[i] <- prop.test(sum(na.omit(objSi$acc)),length(na.omit(objSi$acc)))$p.val
}

ChiSq[,2] <- ifelse(ChiSq[,1] < .05, "PASS", "FAIL")
ChiSq[,2] <- ifelse(accs > .05, ChiSq[,2], "FAIL")

hist(PSE_G, breaks = seq(310,690,20), col = 'blue', main = 'Good Exemplar PSEs',
     xlab = 'milliseconds')
hist(PSE_B, breaks = seq(310,690,20), col = 'orange', main = 'Bad Exemplar PSEs',
     xlab = 'milliseconds')

norm_G <- shapiro.test(PSE_G)
qqnorm(scale(PSE_G),col=4,main = "Normal Q-Q Plot, Good Exemplars")
abline(0,1)

norm_B <- shapiro.test(PSE_B)
qqnorm(scale(PSE_B),col=4,main = "Normal Q-Q Plot, Bad Exemplars")
abline(0,1)

stats <- t.test(PSE_B,PSE_G, paired = TRUE)
stats.np <- wilcox.test(PSE_B,PSE_G,paired = TRUE)
PSE_diff <- PSE_B-PSE_G
Dz <- mean(PSE_diff)/sd(PSE_diff)

library('effsize')
CD.ci <- cohen.d(as.numeric(PSE_B),as.numeric(PSE_G),paired=T,conf.level=.95)

library('ggplot2')
labelg <- rep("Good",length(PSE_G))
labelb <- rep("Bad",length(PSE_B))
Exemplar <- as.factor(c(labelg,labelb))
PSE <- c(PSE_G,PSE_B)
data <- as.data.frame(cbind(Exemplar,PSE))
data$Exemplar <- as.factor(data$Exemplar)
p <- ggplot(data, aes(x=Exemplar, y=PSE, fill=Exemplar)) + geom_violin() + labs(title = "Distribution of PSEs") + scale_fill_discrete(name="Exemplar\nType", breaks=c("1", "2"), labels=c("Bad", "Good"))


h <- hist(PSE_diff,breaks = 22,col=4,main='Bad minus Good PSEs',xlab='difference(ms)',xlim=c(-110,110))
xfit <- seq(-100, 100, length=10000)  # sets range & number quantiles
yfit <- dnorm(xfit, mean=0, sd=sd(PSE_diff)) #sd=7.177)      # should be normal
yfit <- yfit*diff(h$mids[1:2])*length(PSE_diff)# use mid-points 
lines(xfit, yfit, col=2, lwd=2)   # draws normal

yfit2 <- dnorm(xfit, mean=mean(PSE_diff), sd=sd(PSE_diff)) #sd=7.177)      # should be normal
yfit2 <- yfit2*diff(h$mids[1:2])*length(PSE_diff)# use mid-points 
lines(xfit, yfit2, col=3, lwd=2)   # draws normal
legend("topright",legend = c("0 difference normal","observed normal"), lwd=2, col = c(2,3), cex = .7)

d <- density(PSE_diff)
plot(d, main="Kernel Density of PSE Differences (ms)")
polygon(d, col="blue")

q <- ggplot(as.data.frame(PSE_diff), aes(x='density',y=PSE_diff, fill=2)) + geom_violin() + theme(legend.position="none") + labs(title = "Bad minus Good PSEs")

daterz <- as.data.frame(cbind(PSE_B,PSE_G)) # dataframe of PSEs

library('boot')
fc <- function(daterz, i){  # function to pass to boot
  d2 <- daterz[i,]          # draw a new sample of 87 from my sample, with replacement
  return(mean(d2$V1-d2$V2)) # take a mean of the difference in PSEs each time
}

boot.est <- boot(daterz, fc, R=10000) # run the process 10,000 times
boot.ci(boot.est) # give the confidence intervals on the mean of the difference in PSEs

bootsy <- replicate(10000,sample(PSE_diff,length(PSE_diff),replace = T))
boot.m <- mean(bootsy)
boot.sd <- sd(bootsy)
hist(bootsy)
boot.t <- boot.m/(boot.sd/sqrt(length(PSE_diff)))
1-pt(boot.t,length(PSE_diff)-1)

perform <- data.frame(accs,PSE_diff)
library(Hmisc)
relate <- rcorr(as.matrix(perform), type="pearson") # type can be pearson or spearman

library(ggplot2)
vio_PSEs <- data.frame(c(labelg,labelb),c(PSE_G,PSE_B))
names(vio_PSEs) <- c('Exemplar', 'PSE')
my_gg <- ggplot(data=vio_PSEs,aes(x = PSE, fill = Exemplar))+
         geom_density(alpha=.7)+geom_vline(aes(xintercept=mean(PSE_G)),
                                        color="orange", linetype="dashed", size=1)+
                             geom_vline(aes(xintercept=mean(PSE_B)),
                                        color="blue", linetype="dashed", size=1)+
                             scale_fill_manual(values=c(IL_blue,IL_orange))+
                             labs(title="PSE Distributions")

my_gg <- my_gg + theme(text = element_text(size = 44))
my_gg
