library(readr)
N300s <- read_csv('C:\\Users\\Evan\\Documents\\N300_effect_all.csv')
colnames(N300s) <- c("GAG","BAG","GDG","BDG","GALmaj","BALmin","GALmin","BALmaj","GDLmaj","BDLmin","GDLmin","BDLmaj")
P2s <- read_csv('C:\\Users\\Evan\\Documents\\P2_effect_all.csv')
colnames(P2s) <- c("GAG","BAG","GDG","BDG","GALmaj","BALmin","GALmin","BALmaj","GDLmaj","BDLmin","GDLmin","BDLmaj")
P3s <- read_csv('C:\\Users\\Evan\\Documents\\P3_effect_all.csv')
colnames(P3s) <- c("P3att","P3dst")

alpha = c(0,.33,.34,.19,.24,.06,.12,.07,.05,.09,.03,.09,.05,.11,.02,.05,.22,.12,.02,.02,.02,.08,.04,.04,.09,.03,.02,.09,.1,.05,.06,.08,.04,.16,.07,.04,.15,.07,.02)
sixtyHz = c(9,10,11,12,15,21,23,29,33,39)

P2s$attentionGlb <- rowMeans(P2s[c('GDG','BDG')])-rowMeans(P2s[c('GAG','BAG')])

N300s$goodBadGlb <- rowMeans(N300s[c('BAG','BDG')])-rowMeans(N300s[c('GAG','GDG')])

P2s$attentionLoc <- rowMeans(P2s[c('GDLmaj','BDLmin','GDLmin','BDLmaj')])-rowMeans(P2s[c('GALmaj','BALmin','GALmin','BALmaj')])

N300s$goodBadLoc <- rowMeans(N300s[c('BALmin','BALmaj','BDLmin','BDLmaj')])-rowMeans(N300s[c('GALmaj','GALmin','GDLmaj','GDLmin')])

P2s$attentionAll <- rowMeans(P2s[c('GDG','BDG','GDLmaj','BDLmin','GDLmin','BDLmaj')])-rowMeans(P2s[c('GAG','BAG','GALmaj','BALmin','GALmin','BALmaj')])

N300s$goodBadAll <- rowMeans(N300s[c('BAG','BDG','BALmin','BALmaj','BDLmin','BDLmaj')])-rowMeans(N300s[c('GAG','GDG','GALmaj','GALmin','GDLmaj','GDLmin')])

P3s$attentionAll <- P3s$P3dst-P3s$P3att

N300s$goodBadAttentionEffect <- (N300s$BAG-N300s$GAG)-(N300s$BDG-N300s$GDG)
N300s$goodBadDstOnly <- N300s$BDG-N300s$GDG
N300s$goodBadAttOnly <- N300s$BAG-N300s$GAG

all.effects <- data.frame(seq(1,39,1))
all.effects$P2 <- P2s$attentionAll
all.effects$P3 <- P3s$attentionAll
all.effects$N300 <- N300s$goodBadAll
all.effects$N300attMain <- N300s$goodBadAttentionEffect
# write_csv(all.effects,'C:/Users/Evan/Documents/all_effects.csv')

library(TOSTER)
TOSTpaired(m1=mean(N300s$GAG-N300s$BAG),
           m2=mean(N300s$GDG-N300s$BDG),
           sd1=sd(N300s$GAG-N300s$BAG),
           sd2=sd(N300s$GDG-N300s$BDG),
           n=dim(N300s)[1],r12=cor(N300s$GAG-N300s$BAG,N300s$GDG-N300s$BDG),
           low_eqbound_d=-0.3,high_eqbound_d=0.3,alpha=.05)

library(effsize)
N300btn.dz.ci <- cohen.d(N300s$GAG-N300s$BAG,N300s$GDG-N300s$BDG,paired=T,conf.level=.95)
