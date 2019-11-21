library('lme4')
library('lmerTest')
library('lattice')
library('ggplot2')
library('stringi')
library('HLMdiag')

icc <- function(modl) { 
  vars <- as.data.frame(VarCorr(modl))[4]
  total <- sum(vars)
  tau00 <- vars[1,1]
  icc <- tau00/total
  return(icc)
}

# read in the data
bully.dat<-read.table("C:/Users/Evan/Documents/HLM/Bully_data.txt",header=TRUE)

head(bully.dat)

# fix incontinuity for convenience
bully.dat$peer[length(bully.dat$peer)] = 54

# average scores on these dimensions
bully.avg <- mean(bully.dat$bully) # 1.66
fight.avg <- mean(bully.dat$fight) # 1.39
empathy.avg <- mean(bully.dat$empathy) # 12.12
pct.male <- sum(bully.dat$gender=='male')/length(bully.dat$gender) #.47
n.peers <- max(bully.dat$peer) # a total of 54 peer groups

# create overall centered variables and numeric sex variable
bully.dat$oc.bully <- bully.dat$bully-bully.avg
bully.dat$oc.fight <- bully.dat$fight-fight.avg
bully.dat$oc.empathy <- bully.dat$empathy-empathy.avg
bully.dat$sex <- ifelse(bully.dat$gender=='male',1,0)

# create group centered variables
# bully
grp.bully <- as.data.frame(aggregate(bully~peer, data=bully.dat, "mean"))
names(grp.bully) <- c('peer', 'grp.bully')
bully.dat <- merge(bully.dat,grp.bully, by=c('peer'))

bully.dat$gc.bully <- bully.dat$bully - bully.dat$grp.bully

bully.sd <- as.data.frame(aggregate(bully~peer, data=bully.dat, "sd"))
names(bully.sd) <- c('peer', 'bully.sd')
bully.dat <- merge(bully.dat,bully.sd, by=c('peer'))

bully.dat$gc.bully <- bully.dat$bully - bully.dat$grp.bully

# fight
grp.fight <- as.data.frame(aggregate(fight~peer, data=bully.dat, "mean"))
names(grp.fight) <- c('peer', 'grp.fight')
bully.dat <- merge(bully.dat,grp.fight, by=c('peer'))

bully.dat$gc.fight <- bully.dat$fight - bully.dat$grp.fight

# the mode of fight is 1 with 158 of the total 291 responses
# definitely causing downstream floor effects
# Let's make a new variable that categorizes fighters vs peaceful folk
bully.dat$peace <- ifelse(bully.dat$fight==1,1,0)

# empathy
grp.empathy <- as.data.frame(aggregate(empathy~peer, data=bully.dat, "mean"))
names(grp.empathy) <- c('peer', 'grp.empathy')
bully.dat <- merge(bully.dat,grp.empathy, by=c('peer'))

bully.dat$gc.empathy <- bully.dat$empathy - bully.dat$grp.empathy

# gender (group level only)
grp.gen.ratio <- as.data.frame(aggregate(sex~peer, data=bully.dat, "mean"))
names(grp.gen.ratio) <- c('peer', 'grp.gen.ratio')
bully.dat <- merge(bully.dat,grp.gen.ratio, by=c('peer'))

# effect of at least one girl being in the group
bully.dat$a.girl <- ifelse(bully.dat$grp.gen.ratio < 1, 1, 0)

# effect of at least one boy being in the group
bully.dat$a.boy <- ifelse(bully.dat$grp.gen.ratio > 0, 1, 0)

# effect of mixing genders
bully.dat$mixed <- ifelse(bully.dat$grp.gen.ratio%%1==0,0,1)

# group size
grp.size <- NaN

for (i in 1:max(bully.dat$peer)){
  grp.size[i] <- sum(bully.dat$peer==i)
}

mean(grp.size) # 5.39

for (i in 1:length(bully.dat$peer)){
  bully.dat$grp.size[i] <- grp.size[bully.dat$peer[i]]
}

# check null model
# not much between group variance according to null model
null.model <- lmer(bully ~ 1 + ( 1 | peer), data = bully.dat, REML=F)
summary(null.model)
BIC(null.model)
-2*logLik(null.model)

# This scatterplot would indicate otherwise
plot(bully.dat$peer, bully.dat$grp.bully,
     main = 'Variability in bully levels among peer groups', ylim = c(0.9,4.5))
arrows(bully.dat$peer, bully.dat$grp.bully-bully.dat$bully.sd,
      bully.dat$peer, bully.dat$grp.bully+bully.dat$bully.sd, length=0.02, 
       angle=90, code=3,col=1)


# graph some parameters to get a feel ###########
# strong postitive relationship between fight and bully
xyplot(bully ~ fight, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ fight relationship')

xyplot(bully ~ fight, data=bully.dat, col.line='black', type=c('p','smooth'), 
       main='Smoothed bully ~ fight relationship')

# lots of variability by peer group for fight - random slope for fight?
xyplot(bully ~ oc.fight | peer, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Variability in bully ~ fight relationship')

# pretty strong negative relationship between empathy and bully
xyplot(bully ~ empathy, data=bully.dat, col.line='black', type=c('p','r'),
       main='Overall bully ~ empathy relationship')

# exponential?
xyplot(bully ~ empathy, data=bully.dat, col.line='black', type=c('p','smooth'), 
       main='Smoothed bully ~ empathy relationship')

# lots of variability in empathy bully relationship - random slope for empathy?
xyplot(bully ~ oc.empathy | peer, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Variability in bully ~ empathy relationship')

# boys more likely to bully than girls, but only a subset of boys?
xyplot(bully ~ gender, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ gender relationship')

xyplot(bully ~ gender, data=bully.dat, col.line='black', type=c('p','smooth'), 
       main='Smoothed bully ~ gender relationship')

# peer group size doesn't seem to have much effect
xyplot(bully ~ grp.size, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ size relationship')

# gender ratio tells a similar story to regular gender
# not many balanced ratios; either all girl, all boy, or mostly girls and a few boys
xyplot(bully ~ grp.gen.ratio, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ gender ratio relationship')

plot(bully.dat$peer,bully.dat$grp.gen.ratio,main = "Distribution of Gender Ratios")

xyplot(bully ~ grp.gen.ratio, data=bully.dat, col.line='black', type=c('p','smooth'), 
       main='Smoothed bully ~ gender ratio relationship')

# just having a boy present makes bullying more likely
xyplot(bully ~ a.boy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ boy presence relationship')

# just having a girl present makes bullying less likely
xyplot(bully ~ a.girl, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ girl presence relationship')

# not much effect for mixing genders vs all one gender
xyplot(bully ~ mixed, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ mixing genders relationship')

# females are more likely to be empathetic; interaction?
xyplot(empathy ~ gender, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall empathy ~ gender relationship')

# males are more likely to fight; interaction?
xyplot(fight ~ gender, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ gender relationship')

xyplot(fight ~ empathy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ empathy relationship')

# similar effects for group level variables
xyplot(bully ~ grp.bully, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ group bully relationship')

xyplot(bully ~ grp.fight, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ group fight relationship')

xyplot(bully ~ grp.empathy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall bully ~ group empathy relationship')

xyplot(empathy ~ grp.empathy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall empathy ~ group empathy relationship')

xyplot(fight ~ grp.fight, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ group fight relationship')

xyplot(fight ~ grp.empathy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ group empathy relationship')

xyplot(bully ~ grp.fight, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ group fight relationship')

xyplot(bully ~ grp.empathy, data=bully.dat, col.line='black', type=c('p','r'), 
       main='Overall fight ~ group fight relationship')

# some other models to try ########
ind.model <- lmer(bully ~ 1 + gender + fight + empathy + ( 1 | peer), 
                  data = bully.dat, REML=F)
summary(ind.model)
BIC(ind.model)
-2*logLik(ind.model)

peace.model <- lmer(bully ~ 1 + gender + peace + gc.empathy +
                    + (1|peer), data = bully.dat, REML=F)
summary(peace.model)
BIC(peace.model)
-2*logLik(peace.model)

ind.exp.model <- lmer(bully ~ 1 + gender + fight + empathy^2 + ( 1 | peer), data = bully.dat, REML=F)
summary(ind.exp.model)
BIC(ind.exp.model)
-2*logLik(ind.exp.model)

# no gender
nogen.model <- lmer(bully ~ 1 + fight + empathy + ( 1 | peer), data = bully.dat, REML=F)
summary(nogen.model)
BIC(nogen.model)
-2*logLik(nogen.model)

# looking good. gender not coming through, but maybe an interaction
some.boys.model1 <- lmer(bully ~ 1 + gender*fight + empathy + ( 1 | peer), 
                         data = bully.dat, REML=F)
summary(some.boys.model1)
BIC(some.boys.model1)
-2*logLik(some.boys.model1)

some.boys.model2 <- lmer(bully ~ 1 + gender*empathy + fight + ( 1 | peer), 
                         data = bully.dat, REML=F)
summary(some.boys.model2)
BIC(some.boys.model2)
-2*logLik(some.boys.model2)

some.boys.model3 <- lmer(bully ~ 1 + gender*empathy + gender*fight + ( 1 | peer), 
                         data = bully.dat, REML=F)
summary(some.boys.model3)
BIC(some.boys.model3)
-2*logLik(some.boys.model3)

some.boys.model4 <- lmer(bully ~ 1 + gender*empathy*fight + ( 1 | peer), 
                         data = bully.dat, REML=F)
summary(some.boys.model4)
BIC(some.boys.model4)
-2*logLik(some.boys.model4)

opp.emo.model <- lmer(bully ~ 1 + gender + empathy*fight + ( 1 | peer), 
                   data = bully.dat, REML=F)
summary(opp.emo.model)
BIC(opp.emo.model)
-2*logLik(opp.emo.model)

# some group centered type models
gc.ind.model <- lmer(bully ~ 1 + gender + gc.fight + gc.empathy + ( 1 | peer), 
                     data = bully.dat, REML=F)
summary(gc.ind.model)
BIC(gc.ind.model)
-2*logLik(gc.ind.model)

gc.raw.model <- lmer(bully ~ 1 + gender + fight + empathy + gc.fight + gc.empathy + 
                          ( 1 | peer), data = bully.dat, REML=F)
summary(gc.raw.model)
BIC(gc.raw.model)
-2*logLik(gc.raw.model)

gc.ind.exp.model <- lmer(bully ~ 1 + gender + gc.fight + gc.empathy^2 + ( 1 | peer), 
                     data = bully.dat, REML=F)
summary(gc.ind.exp.model)
BIC(gc.ind.exp.model)
-2*logLik(gc.ind.exp.model)

gc.sbm3 <- lmer(bully ~ 1 + gender*gc.fight + gender*gc.empathy + (1 | peer),
            data = bully.dat, REML=F)
summary(gc.sbm3)
BIC(gc.sbm3)
-2*logLik(gc.sbm3)

# so BIC likes the regular old independent models the best with nogen a little better
anova(ind.model,nogen.model)
# but the log-likelihood test is not significant, so we'll keep gender

# some models with random slopes

rs.fight.model <- lmer(bully ~ 1 + gender + fight + empathy + (1+fight|peer), data = bully.dat, 
                       REML=F)
summary(rs.fight.model)
BIC(rs.fight.model)
-2*logLik(rs.fight.model)

rs.empath.model <- lmer(bully ~ 1 + gender + fight + empathy + (1+empathy|peer), 
                        data = bully.dat, REML=F)
summary(rs.empath.model)
BIC(rs.empath.model)
-2*logLik(rs.empath.model)

rs.gender.model <- lmer(bully ~ 1 + gender + fight + empathy + (1+gender|peer), 
                        data = bully.dat, REML=F)
summary(rs.gender.model)
BIC(rs.gender.model)
-2*logLik(rs.gender.model)

rs.emo.model <- lmer(bully ~ 1 + gender + fight + empathy + (1+fight+empathy|peer), 
                        data = bully.dat, REML=F)
summary(rs.emo.model)
BIC(rs.emo.model)
-2*logLik(rs.emo.model)

rs.all.model <- lmer(bully ~ 1 + gender + empathy + fight + (1+fight+empathy+gender|peer), 
                     data = bully.dat, REML=F)
summary(rs.all.model)
BIC(rs.all.model)
-2*logLik(rs.all.model)

rs.nogen.model <- lmer(bully ~ 1 + empathy + fight + (1+fight+empathy|peer), 
                                       data = bully.dat, REML=F)
summary(rs.nogen.model)
BIC(rs.nogen.model)
-2*logLik(rs.nogen.model)

rs.emo.int.model <- lmer(bully ~ 1 + gender*empathy + fight + (1+fight+empathy+gender|peer), 
                     data = bully.dat, REML=F)
summary(rs.emo.int.model)
BIC(rs.emo.int.model)
-2*logLik(rs.emo.int.model)

rs.emo.model.bul <- lmer(bully ~ 1 + gender + fight + empathy + grp.bully + (1+fight+empathy|peer), 
                     data = bully.dat, REML=F)
summary(rs.emo.model.bul)
BIC(rs.emo.model.bul)
-2*logLik(rs.emo.model.bul)

# BIC likes the random slope for empathy best, let's test vs one for empath and fight
anova(rs.empath.model,rs.emo.model)
# very close to significant

# try w/o gender
rs.emp.nogen.model <- lmer(bully ~ 1 + fight + empathy + (1+empathy|peer), 
                           data = bully.dat, REML=F)
summary(rs.empath.model)
BIC(rs.empath.model)
-2*logLik(rs.empath.model)

# not a significant difference
anova(rs.empath.model,rs.emp.nogen.model)

# add in group level vars to account for peer environment
group.model <- lmer(bully ~ 1 + gender + fight + empathy + grp.bully + grp.empathy + 
                      grp.fight + (1|peer), data = bully.dat, REML=F)
summary(group.model)
BIC(group.model)

gc.model <- lmer(bully ~ 1 + gender + gc.fight + gc.empathy + grp.bully
                 + (1|peer), data = bully.dat, REML=F)
summary(gc.model)
BIC(gc.model)

gc.oc.model <- lmer(oc.bully ~ 1 + gender + gc.fight + gc.empathy + grp.bully
                 + (1|peer), data = bully.dat, REML=F)
summary(gc.oc.model)
BIC(gc.oc.model)

gc.nogen.model <- lmer(bully ~ 1 + gc.fight + gc.empathy + grp.bully + 
                 + (1|peer), data = bully.dat, REML=F)
summary(gc.nogen.model)
BIC(gc.nogen.model)

group.nogen.model <- lmer(bully ~ 1 + fight + empathy + grp.bully + grp.empathy + 
                            grp.fight + (1|peer), data = bully.dat, REML=F)
summary(group.nogen.model)
BIC(group.nogen.model)

group.rs.emp.model <- lmer(bully ~ 1 + fight + empathy + grp.bully + grp.empathy + 
                             grp.fight + (1+empathy|peer), data = bully.dat, REML=F)
summary(group.rs.emp.model)
BIC(group.rs.emp.model)

group.rs.bully.model <- lmer(bully ~ 1 + fight + empathy + grp.bully + grp.empathy + 
                             grp.fight + (1+grp.bully|peer), data = bully.dat, REML=F)
summary(group.rs.bully.model)
BIC(group.rs.bully.model)

group.nofight <- lmer(bully ~ 1 + gender + fight + empathy + grp.bully + grp.empathy + 
                        (1|peer), data = bully.dat, REML=F)
group.noempathy <- lmer(bully ~ 1 + gender + fight + empathy + grp.bully + grp.fight + 
                        (1|peer), data = bully.dat, REML=F)
group.nobully <- lmer(bully ~ 1 + gender + fight + empathy + grp.empathy + grp.fight + 
                        (1|peer), data = bully.dat, REML=F)
summary(group.nobully)

groupz.model <- lmer(bully ~ 1 + gender + fight + empathy + grp.empathy + grp.fight +
                       (1|peer), data = bully.dat, REML=F)
summary(groupz.model)

groupy.model <- lmer(bully ~ 1 + gender + empathy + fight + grp.empathy +
                       (1|peer), data = bully.dat, REML=F)
summary(groupy.model)


# still no big difference removing gender
anova(group.model,group.nogen.model)

# random slope for empathy no longer gives big improvement
anova(group.model,group.rs.emp.model)

# all the group variables help a lot
anova(group.model,group.nofight)
anova(group.model,group.noempathy)
anova(group.model,group.nobully)
anova(group.model,ind.model)

group.all.model <-lmer(bully ~ 1 + gender + fight + empathy + grp.bully + grp.empathy + 
                          grp.fight + grp.size + grp.gen.ratio + (1|peer), data = bully.dat, REML=F)
summary(group.all.model)
BIC(group.all.model)
-2*logLik(group.all.model)

group.sig.model <-lmer(bully ~ 1 + gender + fight + empathy + grp.bully + grp.empathy + 
                         grp.fight + (1|peer), data = bully.dat, REML=F)
summary(group.sig.model)
BIC(group.sig.model)
-2*logLik(group.sig.model)

anova(group.all.model,group.sig.model)

group.emp.rs <- lmer(bully ~ 1 + gender + empathy + fight + grp.bully + grp.empathy + 
                         grp.fight + (1+empathy|peer), data = bully.dat, REML=F)
summary(group.emp.rs)
BIC(group.emp.rs)
-2*logLik(group.emp.rs)

anova(group.sig.model,group.emp.rs)

group.fight.rs <- lmer(bully ~ 1 + gender + empathy + fight + grp.bully + grp.empathy + 
                       grp.fight + (1+fight|peer), data = bully.dat, REML=F)
summary(group.fight.rs)
BIC(group.fight.rs)
-2*logLik(group.fight.rs)

anova(group.sig.model,group.fight.rs)

# gender explains a lot on its own
# but the other variables explain way more over and above what gender can do
gen.model <-lmer(bully ~ 1 + gender + (1|peer), data = bully.dat, REML=F)
summary(gen.model)
BIC(gen.model)

anova(group.model,group.all.model)


modela <- lmer(bully ~ 1 + gender + empathy + fight + grp.bully + grp.empathy + grp.fight +
                       ( 1 | peer), data = bully.dat, REML=F)
summary(modela)
BIC(modela)
-2*logLik(modela)

modelb <- lmer(bully ~ 1 + gender + empathy + fight + 
                 ( 1 + empathy + fight | peer), data = bully.dat, REML=F)
summary(modelb)
BIC(modelb)
-2*logLik(modelb)

anova(modela,modelb)

modelc <- lmer(bully ~ 1 + gender + empathy + fight + grp.bully +
                 ( 1 + gender*empathy + fight | peer), data = bully.dat, REML=F)
summary(modelc)
BIC(modelc)
-2*logLik(modelc)

anova(modela,modelc)





# some diagnostics ############
plot(rs.nogen.model, xlab='Fitted Conditional', ylab='Pearson Residuals')

# Get y-(X*gamma+Z*U) where U estimated by Empricial Bayes
res1 <- HLMresid(rs.nogen.model, level=1, type="EB", 
                 standardize=TRUE)

head(res1)                     # look at what is here

# Plot of random effects with confidence bars
dotplot(ranef(rs.nogen.model,condVar=TRUE),
        lattice.options=list(layout=c(1,2)))

# mimic SAS
par(mfrow=c(2,2))

fit <- fitted(rs.nogen.model)  # get conditional fitted values

plot(fit,res1, 
     xlab='Conditional Fitted Values',
     ylab='Pearson Std Residuals',
     main='Conditional Residuals')

qqnorm(res1)                 # draws plot
abline(a=0,b=.45, col='blue')   # reference line

h <- hist(res1,breaks=15,density=20)        # draw historgram
xfit <- seq(-40, 40, length=50)  # sets range & number quantiles
yfit <- dnorm(xfit, mean=0, sd=7.17)      # should be normal
yfit <- yfit*diff(h$mids[1:2])*length(res1)# use mid-points 
#lines(xfit, yfit, col='darkblue', lwd=2)   # draws normal


plot.new( )                   # a plot with nothing in it.
text(.5,1.0,'rs.nogen.model')        # potentially useful text
text(.5,0.8,'Deviance: 335.9')
text(.5,0.6,'AIC: 355.9')
text(.5,0.4,'BIC: 392.6')


# Cook's distances
par(mfrow=c(2,2))

cook <- cooks.distance(rs.nogen.model, group="peer")

dotplot_diag(x=cook, cutoff="internal", 
             name="cooks.distance", ylab=("Cook's distance"), xlab=("Peer Group"))

mdfit <- mdffits(rs.nogen.model,group="peer")

dotplot_diag(x=mdfit, cutoff="internal", name="mdffits", 
             ylab=("MDFits"), xlab=("Peer Group"))

# Let's try taking out the big influence outliers
baddies = c(27,30,39,40)

pruned.bully <- bully.dat

for (i in 1:length(baddies)){
  pruned.bully <- pruned.bully[pruned.bully$peer!=baddies[i],]
}

p.rs.nogen.model <- lmer(bully ~ 1 + empathy + fight +
                 + (1+empathy+fight|peer), data = pruned.bully, REML=F)
summary(p.rs.nogen.model)
BIC(p.rs.nogen.model)

# new diagnostics
plot(p.rs.nogen.model, xlab='Fitted Conditional', ylab='Pearson Residuals')

# Get y-(X*gamma+Z*U) where U estimated by Empricial Bayes
res1 <- HLMresid(p.rs.nogen.model, level=1, type="EB", 
                 standardize=TRUE)

head(res1)                     # look at what is here

# Plot of random effects with confidence bars
dotplot(ranef(p.rs.nogen.model,condVar=TRUE),
        lattice.options=list(layout=c(1,2)))

# mimic SAS
par(mfrow=c(2,2))

fit <- fitted(p.rs.nogen.model)  # get conditional fitted values

plot(fit,res1, 
     xlab='Conditional Fitted Values',
     ylab='Pearson Std Residuals',
     main='Conditional Residuals')

qqnorm(res1)                 # draws plot
abline(a=0,b=.45, col='blue')   # reference line

h <- hist(res1,breaks=15,density=20)        # draw historgram
xfit <- seq(-40, 40, length=50)  # sets range & number quantiles
yfit <- dnorm(xfit, mean=0, sd=.1)      # should be normal
yfit <- yfit*diff(h$mids[1:2])*length(res1)# use mid-points 
#lines(xfit, yfit, col='darkblue', lwd=2)   # draws normal


plot.new( )                   # a plot with nothing in it.
text(.5,1.0,'rs.nogen.model')        # potentially useful text
text(.5,0.8,'Deviance: 258.4')
text(.5,0.6,'AIC: 278.4')
text(.5,0.4,'BIC: 314.1')


# Cook's distances
par(mfrow=c(2,2))

cook <- cooks.distance(p.rs.nogen.model, group="peer")

dotplot_diag(x=cook, cutoff="internal", 
             name="cooks.distance", ylab=("Cook's distance"), xlab=("Peer Group"))

mdfit <- mdffits(p.rs.nogen.model,group="peer")

dotplot_diag(x=mdfit, cutoff="internal", name="mdffits", 
             ylab=("MDFits"), xlab=("Peer Group"))

# Let's try taking out the big influence outliers and peer groups of n=1
baddies = c(17,44,16,40,22)

pruned2.bully <- pruned.bully

for (i in 1:length(baddies)){
  pruned2.bully <- pruned2.bully[pruned2.bully$peer!=baddies[i],]
}

pruned2.bully <- pruned2.bully[pruned2.bully$grp.size>1,]

p2.rs.nogen.model <- lmer(bully ~ 1 + empathy + fight +
                           + (1+empathy+fight|peer), data = pruned2.bully, REML=F)
summary(p2.rs.nogen.model)
BIC(p2.rs.nogen.model)

# new diagnostics
plot(p2.rs.nogen.model, xlab='Fitted Conditional', ylab='Pearson Residuals')

# Get y-(X*gamma+Z*U) where U estimated by Empricial Bayes
res1 <- HLMresid(p2.rs.nogen.model, level=1, type="EB", 
                 standardize=TRUE)

head(res1)                     # look at what is here

# Plot of random effects with confidence bars
dotplot(ranef(p2.rs.nogen.model,condVar=TRUE),
        lattice.options=list(layout=c(1,2)))

# mimic SAS
par(mfrow=c(2,2))

fit <- fitted(p2.rs.nogen.model)  # get conditional fitted values

plot(fit,res1, 
     xlab='Conditional Fitted Values',
     ylab='Pearson Std Residuals',
     main='Conditional Residuals')

qqnorm(res1)                 # draws plot
abline(a=0,b=.45, col='blue')   # reference line

h <- hist(res1,breaks=15,density=20)        # draw historgram
xfit <- seq(-40, 40, length=50)  # sets range & number quantiles
yfit <- dnorm(xfit, mean=0, sd=.1)      # should be normal
yfit <- yfit*diff(h$mids[1:2])*length(res1)# use mid-points 
#lines(xfit, yfit, col='darkblue', lwd=2)   # draws normal


plot.new( )                   # a plot with nothing in it.
text(.5,1.0,'rs.nogen.model')        # potentially useful text
text(.5,0.8,'Deviance: 258.4')
text(.5,0.6,'AIC: 278.4')
text(.5,0.4,'BIC: 314.1')


# Cook's distances
par(mfrow=c(2,2))

cook <- cooks.distance(p2.rs.nogen.model, group="peer")

dotplot_diag(x=cook, cutoff="internal", 
             name="cooks.distance", ylab=("Cook's distance"), xlab=("Peer Group"))

mdfit <- mdffits(p2.rs.nogen.model,group="peer")

dotplot_diag(x=mdfit, cutoff="internal", name="mdffits", 
             ylab=("MDFits"), xlab=("Peer Group"))

# setup for a loop
nj <- table(pruned2.bully$peer)  # number level 1 units per cluster
nj <- as.numeric(nj)
nclusters <- max(pruned2.bully$peer)          # number of schools
csum <- cumsum(table(pruned2.bully$peer))    # cumulative frequencies

cut2 <- csum                       # end index
cut1 <- c(0, csum) + 1             # start index
cut1 <- cut1[1:nclusters]

ssmodel <- (0)             # object to hold model SS
sstotal <- (0)             # object to hold total SS
R2 <- (99)                 # create object to hold Rsquares

#### 12b ####

# loopin'
for (i in 1:nclusters){
  model0 <- lm(bully[cut1[i]:cut2[i]] 
               ~ fight[cut1[i]:cut2[i]] + empathy[cut1[i]:cut2[i]], data=pruned2.bully)
  a <- anova(p2.rs.nogen.model)
  ssmodel <- ssmodel + a[1,2] 
  sstotal <- sstotal + sum(a[,2])
  R2 <- rbind(R2,summary(p2.rs.nogen.model)$r.squared)
}

R2meta <- ssmodel/sstotal

R2.mod1 <- R2[2:length(R2)]

#### 12c ####

# plottin'
plot(nj,R2.mod1, ylim= c(0,1), main='bully ~ fight + empathy')
abline(h=R2meta,col='blue')          # line for R2meta
text(70,0.95,'R2meta=.45')           # value for R2meta
