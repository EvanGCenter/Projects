# Modeling of object time perception data using generalized estimating equations

# load packages
library('readr')

# load in image size data
setwd("C:\\Users\\Evan\\Documents\\data\\objects_data")
pixels_a <- read_csv('pixels_a.csv')
colnames(pixels_a) <- 'g'
pixels_b <- read_csv('pixels_b.csv')
colnames(pixels_b) <- 'b'
pixels <- data.frame(pixels_a,pixels_b)
pixels <- as.vector(t(pixels))
quants <- quantile(pixels, probs = seq(0,1,.2))
continuous <- TRUE

# go to the rating session dir and create a dataframe of all subjects' data
setwd("C:/Users/Evan/Documents/data/objects_data/rate")
filenames <- list.files()
mas.rate <- do.call("rbind", lapply(filenames, read_csv))

# create a combined variable for later convenience
mas.rate$smash <- paste(mas.rate$participant,mas.rate$im,mas.rate$suf)

# go to the time session dir and create a dataframe of all subjects' data
setwd('C:/Users/Evan/Documents/data/objects_data/time')
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
mas.data$rate <- NaN
mas.data$pix <- NaN

obs <- length(mas.data$age) # no. iterations
id <- NaN # dummy var
dum.time <- seq(0,8,1)

# rating data and time perception data are in different dataframes
# match the ratings back up with their corresponding image and participant
for (i in 1:obs) {
  for (j in seq(18,42,3)) {
    if (mas.data$time1[i] == j) {
      mas.data$time1[i] <- dum.time[j/3-5]
    }
  }
  # Good comparison presented first
  if (mas.data$order[i] == 1) {
    id <- paste(mas.data$participant[i],mas.data$im1[i],'a.tif')
    key <- match(id,mas.rate$smash)
    mas.data$rate[i] <- mas.rate$resp[key]-1
    
    if (continuous == TRUE) {
    mas.data$pix[i] <- pixels_a$g[mas.data$im1[i]]
    }
    
    else {
      if (pixels_a$g[mas.data$im1[i]] <= quants[2]) {
        mas.data$pix[i] <- 0
      }
      else if (pixels_a$g[mas.data$im1[i]] <= quants [3]) {
        mas.data$pix[i] <- 1
      }
      else if (pixels_a$g[mas.data$im1[i]] <= quants [4]) {
        mas.data$pix[i] <- 2
      }
      else if (pixels_a$g[mas.data$im1[i]] <= quants [5]) {
        mas.data$pix[i] <- 3
      }
      else if (pixels_a$g[mas.data$im1[i]] <= quants [6]) {
        mas.data$pix[i] <- 4
      }
    }
  }
  # Good comparison presented second
  else if (mas.data$order[i] == 2) {
    id <- paste(mas.data$participant[i],mas.data$im2[i],'a.tif')
    key <- match(id,mas.rate$smash)
    mas.data$rate[i] <- mas.rate$resp[key]-1
    
    if (continuous == TRUE) {
      mas.data$pix[i] <- pixels_a$g[mas.data$im2[i]]
    }
    
    else {
      if (pixels_a$g[mas.data$im2[i]] <= quants[2]) {
        mas.data$pix[i] <- 0
      }
      else if (pixels_a$g[mas.data$im2[i]] <= quants [3]) {
        mas.data$pix[i] <- 1
      }
      else if (pixels_a$g[mas.data$im2[i]] <= quants [4]) {
        mas.data$pix[i] <- 2
      }
      else if (pixels_a$g[mas.data$im2[i]] <= quants [5]) {
        mas.data$pix[i] <- 3
      }
      else if (pixels_a$g[mas.data$im2[i]] <= quants [6]) {
        mas.data$pix[i] <- 4
      }
    }
  }
  # Bad comparison presented first
  else if (mas.data$order[i] == 3) {
    id <- paste(mas.data$participant[i],mas.data$im1[i],'b.tif')
    key <- match(id,mas.rate$smash)
    mas.data$rate[i] <- mas.rate$resp[key]-1
    
    if (continuous == TRUE) {
      mas.data$pix[i] <- pixels_b$b[mas.data$im1[i]]
    }
    
    else {
      if (pixels_b$b[mas.data$im1[i]] <= quants[2]) {
        mas.data$pix[i] <- 0
      }
      else if (pixels_b$b[mas.data$im1[i]] <= quants [3]) {
        mas.data$pix[i] <- 1
      }
      else if (pixels_b$b[mas.data$im1[i]] <= quants [4]) {
        mas.data$pix[i] <- 2
      }
      else if (pixels_b$b[mas.data$im1[i]] <= quants [5]) {
        mas.data$pix[i] <- 3
      }
      else if (pixels_b$b[mas.data$im1[i]] <= quants [6]) {
        mas.data$pix[i] <- 4
      }
    }
  }
  # Bad comparison presented second
  else if (mas.data$order[i] == 4) {
    id <- paste(mas.data$participant[i],mas.data$im2[i],'b.tif')
    key <- match(id,mas.rate$smash)
    mas.data$rate[i] <- mas.rate$resp[key]-1
    
    if (continuous == TRUE) {
      mas.data$pix[i] <- pixels_b$b[mas.data$im2[i]]
    }
    
    else {
      if (pixels_b$b[mas.data$im2[i]] <= quants[2]) {
        mas.data$pix[i] <- 0
      }
      else if (pixels_b$b[mas.data$im2[i]] <= quants [3]) {
        mas.data$pix[i] <- 1
      }
      else if (pixels_b$b[mas.data$im2[i]] <= quants [4]) {
        mas.data$pix[i] <- 2
      }
      else if (pixels_b$b[mas.data$im2[i]] <= quants [5]) {
        mas.data$pix[i] <- 3
      }
      else if (pixels_b$b[mas.data$im2[i]] <= quants [6]) {
        mas.data$pix[i] <- 4
      }
    }
  }
}

#####

library('geepack')
library('MuMIn')
library('glmnet')
# 
# data.net <- data.frame(mas.data$cjl,mas.data$time1,mas.data$order_1,mas.data$rt,mas.data$GvB,
#                      mas.data$rate,mas.data$pix)
# colnames(data.net) <- c('cjl','time1','order','rt','GvB','rate','pix')
# 
# f <- as.formula(y ~ .*.)
# y <- data.net$cjl
# x <- model.matrix(f, data.net[,2:7])
# #x <- as.matrix(data.net[,2:7])
# cvfit<-cv.glmnet(x,na.omit(y),family="binomial",alpha=.5) # cross validated elastic net
# plot(cvfit)
# opt.lam = c(cvfit$lambda.min,cvfit$lambda.1se) # pull out optimal lambdas
# coef(cvfit, s = opt.lam)
# 
# fit.net1 <- geeglm(cjl ~ time1+time1:order_1+time1:rt+time1:GvB+time1:rate+time1:pix+order:rt+order:pix+rt:GvB, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.net1)
# QIC(fit.net1) # 6350
# 
# fit.net2 <- geeglm(cjl ~ time1+time1:rt+order:rt+rt:GvB, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.net2)
# QIC(fit.net2) # 6356
# 
# fit.net3 <- geeglm(cjl ~ time1+order:rt, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.net3)
# QIC(fit.net3) #6411
# 
# #####
# 
# fit.sat <- geeglm(cjl ~ GvB*time1*order_1*pix*rate*rt, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.sat)
# QIC(fit.sat) # 6253
# 
# fit.m.sat <- geeglm(cjl ~ time1+GvB:time1:order_1+GvB:time1:order:rate+GvB:time1:order_1:rt+GvB:time1:order_1:pix:rate+GvB:time1:order_1:rate:rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.m.sat)
# QIC(fit.m.sat) # 6440
# 
# fit.m.sat.2 <- geeglm(cjl ~ time1+GvB:time1:order_1:pix:rate, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.m.sat.2)
# QIC(fit.m.sat.2) # 6429
# 
# fit.GTORRt <- geeglm(cjl ~ GvB*time1*order_1*rate*rt, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTORRt)
# QIC(fit.GTORRt) # 6235
# 
# fit.GTOR <- geeglm(cjl ~ GvB*time1*order_1*rate, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTOR)
# QIC(fit.GTOR) # 6380
# 
# fit.GTRt <- geeglm(cjl ~ GvB*time1*rt, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTRt)
# QIC(fit.GTRt) # 6288
# 
# fit.GPR.T <- geeglm(cjl ~ GvB*pix*rate + time1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GPR.T)
# QIC(fit.GPR.T) # 6444
# 
# fit.GT.P.R <- geeglm(cjl ~ GvB*time1+pix+rate, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT.P.R)
# QIC(fit.GT.P.R) # 6438
# 
# fit.GT.PR <- geeglm(cjl ~ GvB*time1 + pix*rate, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT.PR)
# QIC(fit.GT.PR) # 6439
# 
# fit.GT.P.R <- geeglm(cjl ~ GvB*time1 + pix + rate, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT.P.R)
# QIC(fit.GT.P.R) # 6438
# 
# fit.GTP <- geeglm(cjl ~ GvB*time1*pix, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTP)
# QIC(fit.GTP) # 6441
# 
# fit.HA <- geeglm(cjl ~ GvB*time1 + GvB*pix + time1*pix, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.HA)
# QIC(fit.HA) # 6439
# 
# fit.G.TP <- geeglm(cjl ~ GvB + time1*pix, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TP)
# QIC(fit.G.TP) # 6437
# 
# fit.G.TPR <- geeglm(cjl ~ GvB + time1*pix*rate, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TPR)
# QIC(fit.G.TPR) # 6441
# 
# fit.GT.P <- geeglm(cjl ~ GvB*time1 + pix, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT.P)
# QIC(fit.GT.P) # 6436
# 
# fit.GP.T <- geeglm(cjl ~ GvB*pix + time1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GP.T)
# QIC(fit.GP.T) # 6438
# 
# fit.GT <- geeglm(cjl ~ GvB*time1, data = mas.data, id = participant,
#                 family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT)
# QIC(fit.GT) # 6437
# 
# fit.TP <- geeglm(cjl ~ time1*pix, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TP)
# QIC(fit.TP) # 6442
# 
# fit.GTO <- geeglm(cjl ~ GvB*time1*order_1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTO)
# QIC(fit.GTO) # 6375
# 
# fit.G.TO <- geeglm(cjl ~ GvB+time1*order_1, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TO)
# QIC(fit.G.TO) # 6371
# 
# fit.GT.O <- geeglm(cjl ~ GvB*time1+order_1, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GT.O)
# QIC(fit.GT.O) # 6416
# 
# fit.GO.T <- geeglm(cjl ~ GvB*order_1+time1, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GO.T)
# QIC(fit.GO.T) # 6417
# 
# fit.haGOT <- geeglm(cjl ~ GvB:time1+GvB:order_1+time1:order_1, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.haGOT)
# QIC(fit.haGOT) # 7410
# 
# fit.HAGOT <- geeglm(cjl ~ GvB*time1+GvB*order_1+time1*order_1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.HAGOT)
# QIC(fit.HAGOT) # 6373
# 
# fit.GTOPRt <- geeglm(cjl ~ GvB*time1*order_1*pix*rt, data = mas.data, id = participant,
#                          family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTOPRt)
# QIC(fit.GTOPRt) # 6221
# 
# fit.GTORt <- geeglm(cjl ~ GvB*time1*order_1*rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTORt)
# QIC(fit.GTORt) # 6214
# 
# fit.G.TORt <- geeglm(cjl ~ GvB+time1*order_1*rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TORt)
# QIC(fit.G.TORt) # 6209
# 
# fit.G.TO.Rt <- geeglm(cjl ~ GvB+time1*order_1+rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TO.Rt)
# QIC(fit.G.TO.Rt) # 6371
# 
# fit.G.T.ORt <- geeglm(cjl ~ GvB+time1+order_1*rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.ORt)
# QIC(fit.G.T.ORt) # 6381
# 
# fit.G.O.TRt <- geeglm(cjl ~ GvB+order_1+time1*rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.O.TRt)
# QIC(fit.G.O.TRt) # 6258
# 
# ###################################################################################
# 
# fit.G.TORt.ha <- geeglm(cjl ~ GvB+time1*order_1+time1*rt+order_1*rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TORt.ha)
# QIC(fit.G.TORt.ha) # 6207
# 
# ###################################################################################
# 
# fit.G.TORt.ham <- geeglm(cjl ~ GvB+time1*order_1+time1*rt, data = mas.data, id = participant,
#                         family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TORt.ham)
# QIC(fit.G.TORt.ham) # 6218
# 
# fit.TORt.ham <- geeglm(cjl ~ time1*order_1+time1*rt, data = mas.data, id = participant,
#                          family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TORt.ham)
# QIC(fit.TORt.ham) # 6224
# 
# fit.GRt.TORt <- geeglm(cjl ~ GvB*rt+time1*order_1+time1*rt+order_1*rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GRt.TORt)
# QIC(fit.GRt.TORt) # 6206
# 
# fit.GRt.TORt.2 <- geeglm(cjl ~ GvB:rt+time1*order_1+time1*rt+order_1*rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GRt.TORt.2)
# QIC(fit.GRt.TORt.2) # 6205 BEST MODEL?????
# 
# fit.GRt.TORt.3 <- geeglm(cjl ~ GvB:rt+time1*order_1+time1*rt, data = mas.data, id = participant,
#                          family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GRt.TORt.3)
# QIC(fit.GRt.TORt.3) # 6216
# 
# fit.TORt<- geeglm(cjl ~ time1*order_1*rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TORt)
# QIC(fit.TORt) # 6217
# 
# fit.TO.Rt <- geeglm(cjl ~ time1:order_1+time1*rt, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TO.Rt)
# QIC(fit.TO.Rt) # 6296
# 
# fit.TO.GRt <- geeglm(cjl ~ time1:order_1+time1*rt+GvB:rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TO.GRt)
# QIC(fit.TO.GRt) # 6289
# 
# fit.T.GRt <- geeglm(cjl ~ time1*rt+GvB:rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.T.GRt)
# QIC(fit.T.GRt) # 6285
# 
# fit.TRt <- geeglm(cjl ~ time1*rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TRt)
# QIC(fit.TRt) # 6292
# 
# fit.TORt.ha <- geeglm(cjl ~ time1*order_1+time1*rt+order_1*rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.TORt.ha)
# QIC(fit.TORt.ha) # 6215
# 
# fit.420 <- geeglm(cjl ~ GvB*time1 + GvB*order_1 + GvB*rt + time1*order_1 + time1*rt + order_1*rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.420)
# QIC(fit.420) # 6209
# 
# fit.GTRt <- geeglm(cjl ~ GvB*time1*rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTRt)
# QIC(fit.GTRt) # 6288
# 
# fit.G.TRt <- geeglm(cjl ~ GvB+time1*rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TRt)
# QIC(fit.G.TRt) # 6286
# 
# fit.Tint <- geeglm(cjl ~ GvB*time1+order_1*time1+rt*time1, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.Tint)
# QIC(fit.Tint) # 6218
# 
# fit.G.Tint <- geeglm(cjl ~ GvB+time1+order_1*time1+rt*time1, data = mas.data, id = participant,
#                    family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.Tint)
# QIC(fit.G.Tint) # 6218
# 
# ##### independence models
# 
# fit.ind <- geeglm(cjl ~ GvB+time1+pix+rate+rt+order_1, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.ind)
# QIC(fit.ind) # 6414
# 
# fit.G.T.P <- geeglm(cjl ~ GvB+time1+pix, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.P)
# QIC(fit.G.T.P) # 6436
# 
# fit.G.T<- geeglm(cjl ~ GvB+time1, data = mas.data, id = participant,
#                  family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T)
# QIC(fit.G.T) # 6437
# 
# fit.G.T.R <- geeglm(cjl ~ GvB+time1+rate, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.R)
# QIC(fit.G.T.R) # 6438
# 
# fit.G.T.Rt <- geeglm(cjl ~ GvB+time1+rt, data = mas.data, id = participant,
#                      family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.Rt)
# QIC(fit.G.T.Rt) # 6435
# 
# fit.G.T.O <- geeglm(cjl ~ GvB+time1+order_1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.O)
# QIC(fit.G.T.O) # 6416
# 
# fit.G.T.O.P <- geeglm(cjl ~ GvB+time1+order_1+pix, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.O.P)
# QIC(fit.G.T.O.P) # 6415
# 
# fit.G.T <- geeglm(cjl ~ GvB + time1, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T)
# QIC(fit.G.T) # 6437
# 
# fit.G.T.O.P.Rt <- geeglm(cjl ~ GvB+time1+order_1+pix+rt, data = mas.data, id = participant,
#                          family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.O.P.Rt)
# QIC(fit.G.T.O.P.Rt) # 6413
# 
# fit.G.T.O.Rt <- geeglm(cjl ~ GvB+time1+order_1+rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.O.Rt)
# QIC(fit.G.T.O.Rt) # 6414
# 
# fit.T <- geeglm(cjl ~ time1, data = mas.data, id = participant,
#                 family = binomial(link = "logit"), corstr = "exch")
# summary(fit.T)
# QIC(fit.T) # 6443
# 
# fit.G.P.T.RT <- geeglm(cjl ~ GvB+pix+time1+rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.P.T.RT)
# QIC(fit.G.P.T.RT) # 6434
# 
# fit.G.P.T.O <- geeglm(cjl ~ GvB+pix+time1+order_1, data = mas.data, id = participant,
#                       family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.P.T.O)
# QIC(fit.G.P.T.O) # 6415

#####

# fit.sat <- geeglm(cjl ~ GvB*time1*order_1*pix*rate*rt, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.sat)
# QIC(fit.sat) # 6253

# fit.ind <- geeglm(cjl ~ GvB+time1+order_1+pix+rate+rt, data = mas.data, id = participant,
#                   family = binomial(link = "logit"), corstr = "exch")
# summary(fit.ind)
# QIC(fit.ind) # 6414
# 
# fit.GTORt <- geeglm(cjl ~ GvB*time1*order_1*rt, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.GTORt)
# QIC(fit.GTORt) # 6214
# 
# fit.G.TORt.ha <- geeglm(cjl ~ GvB+time1*order_1+time1*rt+order_1*rt, data = mas.data, id = participant,
#                         family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.TORt.ha)
# QIC(fit.G.TORt.ha) # 6207
# 
# fit.HA <- geeglm(cjl ~ GvB*time1 + GvB*order_1 + GvB*pix + GvB*rt + time1*order_1 + time1*pix + time1*rt + order_1*pix + order_1*rt + pix*rt, data = mas.data, id = participant,
#                         family = binomial(link = "logit"), corstr = "exch")
# summary(fit.HA)
# QIC(fit.HA) # 6214
# 
# fit.G.T.O.Rt <- geeglm(cjl ~ GvB+time1+order_1+rt, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.O.Rt)
# QIC(fit.G.T.O.Rt) # 6414
# 
# fit.G.T.P <- geeglm(cjl ~ GvB+time1+pix, data = mas.data, id = participant,
#                        family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T.P)
# QIC(fit.G.T.P) # 6436
# 
# fit.G.T <- geeglm(cjl ~ GvB+time1, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.G.T)
# QIC(fit.G.T) # 6437
# 
# fit.T.P <- geeglm(cjl ~ time1+pix, data = mas.data, id = participant,
#                     family = binomial(link = "logit"), corstr = "exch")
# summary(fit.T.P)
# QIC(fit.T.P) # 6441

#####

fit.ind.PFTP <- geeglm(cjl ~ time1+GvB+pix, data = mas.data, id = participant,
                  family = binomial(link = "logit"), corstr = "exch")
summary(fit.ind.PFTP)
QIC(fit.ind.PFTP)

fit.ind.VS <- geeglm(cjl ~ GvB+pix, data = mas.data, id = participant,
                       family = binomial(link = "logit"), corstr = "exch")
summary(fit.ind.VS)
QIC(fit.ind.VS)

fit.full <- geeglm(cjl ~ time1*GvB*pix, data = mas.data, id = participant,
                     family = binomial(link = "logit"), corstr = "exch")
summary(fit.full)
QIC(fit.full)

#####

# library('pROC')
# fit.a <- fit.G.TORt.ha
# fit.b <- fit.sat
# 
# roc1 <- roc(as.numeric(fit.a$y), as.numeric(fit.a$fitted.values), ci = T, plot = T)
# roc2 <- roc(as.numeric(fit.b$y), as.numeric(fit.b$fitted.values), ci = T, plot = T)
# roc.test(roc1,roc2)
# 
# anova(fit.a,fit.b)

#####
setwd('C:/Users/Evan/Documents/objects_data/time')
filenames <- list.files()
plotty.data <- do.call("rbind", lapply(filenames, read_csv))

fail <- plotty.data$cjl == "None"
plotty.data$cjl[fail] <- .5
plotty.data$cjl <- as.integer(plotty.data$cjl)

yg <- plotty.data$cjl[plotty.data$order<3]
xg <- plotty.data$time1[plotty.data$order<3]*(1/60)*1000

yb <- plotty.data$cjl[plotty.data$order>2]
xb <- plotty.data$time1[plotty.data$order>2]*(1/60)*1000

fit.G <- glm(yg ~ xg, family = binomial(link = "logit")) 
fit.B <- glm(yb ~ xb, family = binomial(link = "logit"))

# PSE_G <- ((log(.5/(1-.5)) - coef(fit.G)[1])/coef(fit.G)[2])
# PSE_B <- ((log(.5/(1-.5)) - coef(fit.B)[1])/coef(fit.B)[2])

PSE.G <- mean(PSE_G)
PSE.B <- mean(PSE_B)

plot(xg,fit.G$fitted.values, ylim = c(0,1), xlab = 'milliseconds', 
     ylab = 'est. % perceived longer', col = 'blue')
curve(predict(fit.G,data.frame(xg = x),type = "response"),add = TRUE, col = 'blue')
par(new = TRUE)
plot(xb,fit.B$fitted.values, ylim = c(0,1), xlab = 'milliseconds', 
     ylab = 'est. % perceived longer', col = 'orange', main = 'Group PSEs')
curve(predict(fit.B,data.frame(xb = x),type = "response"),add = TRUE, col = 'orange')
abline(h = .5, col = 'red')
abline(v = PSE.G, col = 'blue')
abline(v = PSE.B, col = 'orange')
legend('bottomright', inset = .02, legend=c("Canonical", "Non-canonical"), 
       col=c("blue", "orange"), lty=1, cex=0.7)

#####pixelz#####
# cutoff <- median(plotty.data$pix)
# 
# yh <- plotty.data$cjl[plotty.data$order<3]
# xh <- plotty.data$time1[plotty.data$order<3]*(1/60)*1000
# 
# yl <- plotty.data$cjl[plotty.data$order>2]
# xl <- plotty.data$time1[plotty.data$order>2]*(1/60)*1000
# 
# fit.H <- glm(yh ~ xh, family = binomial(link = "logit")) 
# fit.L <- glm(yl ~ xl, family = binomial(link = "logit"))