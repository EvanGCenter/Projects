# Modeling of scene time perception data using multi-level logistic regression

# load packages
library('readr')

setwd('C:/Users/Evan/Documents/data/old_scene_ratings')

ratingsObj <- list.files()
n_files <- length(ratingsObj)

arousal <- matrix(NaN,721,n_files)
valence <- matrix(NaN,721,n_files)
aesthetics <- matrix(NaN,721,n_files)

for (s in 1:n_files) {
  
  ROi <- read_csv(ratingsObj[s])
  names(ROi)[1] <- "pic_index"
  names(ROi)[2] <- "arousal"
  names(ROi)[3] <- "valence"
  names(ROi)[4] <- "aesthetics"
  
  
  for (i in 1:length(ROi$pic_index)) {
    arousal[ROi$pic_index[i],s] <- ROi$arousal[i]
    valence[ROi$pic_index[i],s] <- ROi$valence[i] 
    aesthetics[ROi$pic_index[i],s] <- ROi$aesthetics[i] 
  }
}

mean_arousal <- rowMeans(arousal,na.rm = T)
mean_valence <- rowMeans(valence,na.rm = T)
mean_aesthetics <- rowMeans(aesthetics,na.rm = T)


setwd("C:\\Users\\Evan\\Documents\\data\\scene_vs_scene")

filenames <- list.files()
mas.data <- do.call("rbind", lapply(filenames, read_csv))

# remove trials in which subject responded inhumanly fast
mas.data <- mas.data[!(mas.data$rt < .05),]

# "None" is included when subjects didn't respond within the window
# R doesn't like that, find them all and swith to NA then force to integer
fail <- mas.data$cjl == "None"
mas.data$cjl[fail] <- NaN
mas.data <- mas.data[!(is.nan(mas.data$cjl)),]
mas.data$cjl <- as.integer(mas.data$cjl)
mas.data$GvB <- ifelse(mas.data$order < 3, 1, 0)
mas.data$order_1 <- ifelse(mas.data$order%%2 == 1, 1, 0)

mas.data$arousal <- NaN
mas.data$valence <- NaN
mas.data$aesthetics <- NaN

for (j in 1:length(mas.data$order)) {
  if (mas.data$order[j] < 3) {
    mas.data$arousal[j] <- mean_arousal[mas.data$im1[j]]
    mas.data$valence[j] <- mean_valence[mas.data$im1[j]]
    mas.data$aesthetics[j] <- mean_aesthetics[mas.data$im1[j]]
  }
  else if (mas.data$order[j] > 2) {
    mas.data$arousal[j] <- mean_arousal[mas.data$im1[j]+360]
    mas.data$valence[j] <- mean_valence[mas.data$im1[j]+360]
    mas.data$aesthetics[j] <- mean_aesthetics[mas.data$im1[j]+360]
  }
}

#####

library('geepack')
library('MuMIn')
library('glmnet')
library('lme4')
library('lmerTest')

# gee.fit.ind <- geeglm(cjl ~ GvB+time1+order_1+rt+gender, data = mas.data, id = participant,
#                     family = binomial, corstr = "exch")
# summary(gee.fit.ind)
# 
gee.fit.int <- geeglm(cjl ~ GvB*time1, data = mas.data, id = participant,
                          family = binomial, corstr = "exch")
summary(gee.fit.int)
# 
# gee.fit.indless <- geeglm(cjl ~ GvB+time1, data = mas.data, id = participant,
#                       family = binomial, corstr = "exch")
# summary(gee.fit.indless)
# 
# gee.gvb <- geeglm(cjl ~ GvB, data = mas.data, id = participant,
#                   family = binomial, corstr = "exch")
# summary(gee.gvb)
# 
# glm.fit <- glmer(cjl ~ 1 + (1|participant), data = mas.data, 
#                family = binomial)
# summary(glm.fit)
# 
# glm.time <- glmer(cjl ~ 1 + time1 + (1|participant), data = mas.data, 
#                      family = binomial)
# summary(glm.time)
# 
# glm.scene.time <- glmer(cjl ~ 1 + time1*GvB + (1|participant), data = mas.data, 
#                   family = binomial)
# summary(glm.scene.time)
# 
# glm.scene <- glmer(cjl ~ 1 + GvB + (1|participant), data = mas.data, 
#                    family = binomial)
# summary(glm.scene)

gee.fit.rate <- geeglm(cjl ~ time1+GvB+aesthetics+valence+arousal, data = mas.data, id = participant,
                    family = binomial, corstr = "exch")
summary(gee.fit.rate)

gee.fit.mulint <- geeglm(cjl ~ time1*GvB+time1*aesthetics+time1*valence+time1*arousal, data = mas.data, id = participant,
                         family = binomial, corstr = "exch")
summary(gee.fit.mulint)
