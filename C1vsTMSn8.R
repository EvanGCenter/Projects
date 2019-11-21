### with 30 Hz low pass and 40 to 140 auto peak analysis but no high pass whoops
#C1ps30 <- c(87,58,83,86,127,86,93,93)
#C1fpl30 <- c(72,47,70,70,81,72,78,78)
#pseudo.sd.c1 <- C1ps30-C1fpl30
#grp.sd.C1 <- sd(C1ps30)
subs <- seq(1,8,1)
#ages <- c()

# same but with high pass yay
C1ps30 <- c(87,99,82,87,86,101,90,92)
C1fpl30 <- c(66,90,71,70,71,72,75,78)
pseudo.sd.c1 <- C1ps30-C1fpl30
grp.sd.C1 <- sd(C1ps30)

TMSsm <- c(126,100,110,119,117,119,113,132) # smoothed peak estimates
TMSfpl <- c(108,77,75,96,98,102,91,114) # smoothed fpl estimates
pseudo.sd.TMS <- TMSsm-TMSfpl
grp.sd.TMS <- sd(TMSsm)

gaps7 <- TMSsm - C1ps30 # smooth peak - peak
gaps8 <- TMSsm - C1fpl30 # smooth peak - fpl
gaps9 <- TMSfpl - C1fpl30 # smooth fpl - fpl

fatty <- 3
dot <- 19
plot(subs,C1ps30,col=2,ylim = c(40,180),main = 'C1 Window vs Suppression Window',xlab = 'Subject',
     ylab = 'Latency (ms)', lwd = fatty, pch = dot)
arrows(subs, C1ps30-pseudo.sd.c1, subs, C1ps30+pseudo.sd.c1, length=0.075, angle=90, code=3,col=2, lwd = fatty)
points(TMSsm, col=4, lwd = fatty, pch = dot)
arrows(subs,TMSsm-pseudo.sd.TMS, subs, TMSsm+pseudo.sd.TMS, length=.075,angle=90,code=3,col=4, lwd = fatty)
grid(NA,NULL)
legend("bottomright",legend = (c("C1","suppression")), col = c('red','blue'), pch = dot,
       cex = .8, border = F)

grp.TMS.sm.pk <- 118
grp.TMS.sm.fl <- 91
#grp.C1.30.pk <- 88
#grp.C1.30.fl <- 73

grp.C1.30.pk <- 88
grp.C1.30.fl <- 73

conds <- seq(1,2,1)

plot(c(grp.C1.30.pk,grp.TMS.sm.pk),conds,col=1,ylim = c(0,3),main = 'C1 Window vs Suppression Window, Group Level',xlab = 'Latency (ms)',
     ylab = 'Condition', xlim = c(60,140), lwd = fatty, pch = dot)
arrows(grp.C1.30.pk-grp.sd.C1, 1, grp.C1.30.pk+grp.sd.C1, 1, length=0.075, angle=90, code=3,col=2, lwd = fatty)
arrows(grp.TMS.sm.pk-grp.sd.TMS, 2, grp.TMS.sm.pk+grp.sd.TMS, 2, length=.075,angle=90,code=3,col=4, lwd = fatty)
grid(NULL,NA)
legend("bottomright",legend = (c("C1","suppression")), col = c('red','blue'), pch = dot,
       cex = .7, border = F)

plot(C1ps30,subs,col=2,xlim = c(40,180),main = 'C1 Window vs Suppression Window',xlab = 'Latency (ms)',
     ylab = 'Subject', lwd = fatty, pch = dot)
arrows(C1ps30-pseudo.sd.c1, subs, C1ps30+pseudo.sd.c1, subs, length=0.075, angle=90, code=3,col=2, lwd = fatty)
points(TMSsm,subs, col=4, lwd = fatty, pch = dot)
arrows(TMSsm-pseudo.sd.TMS, subs, TMSsm+pseudo.sd.TMS, subs, length=.075,angle=90,code=3,col=4, lwd = fatty)
grid(NULL,NA)
legend("bottomright",legend = (c("C1","suppression")), col = c('red','blue'), pch = dot,
       cex = .7, border = F)


C1.ret <- c(C1ps30[3],C1ps30[6],C1ps30[2],C1ps30[1],C1ps30[4],C1ps30[7],C1ps30[5],C1ps30[8])
TMS.ret <- c(TMSsm[3],TMSsm[6],TMSsm[2],TMSsm[1],TMSsm[4],TMSsm[7],TMSsm[5],TMSsm[8])
C1.win.ret <- c(pseudo.sd.c1[3],pseudo.sd.c1[6],pseudo.sd.c1[2],pseudo.sd.c1[1],pseudo.sd.c1[4],pseudo.sd.c1[7],pseudo.sd.c1[5],pseudo.sd.c1[8])
TMS.win.ret <- c(pseudo.sd.TMS[3],pseudo.sd.TMS[6],pseudo.sd.TMS[2],pseudo.sd.TMS[1],pseudo.sd.TMS[4],pseudo.sd.TMS[7],pseudo.sd.TMS[5],pseudo.sd.TMS[8])

par(mar=c(4, 6, 4, 4) + 0.1)
plot(C1.ret,subs,col=2,xlim = c(40,180),main = 'C1 Window vs Suppression Window', yaxt = "n",
     xlab = 'Latency (ms)', ylab = '', lwd = fatty, pch = dot)
arrows(C1.ret-C1.win.ret, subs, C1.ret+C1.win.ret, subs, length=0.075, angle=90, code=3,col=2, lwd = fatty)
points(TMS.ret,subs, col=4, lwd = fatty, pch = dot)
arrows(TMS.ret-TMS.win.ret, subs, TMS.ret+TMS.win.ret, subs, length=.075,angle=90,code=3,col=4, lwd = fatty)
grid(NULL,NA)
legend("bottomright",legend = (c("C1","suppression")), col = c('red','blue'), pch = dot,
       cex = .6, border = F)
axis(2, subs, labels = c("S3(V1)","S6(V1)","S2(V1/V2)","S1(V2)","S4(V2)","S7(V2?)","S5(V3)","S8(V3)"),las = 2, cex = .5)
mtext("Subject", side=2, line=5, cex.lab=1, las=0)

# bandpass .016 to 30 Hz
#diff.wave.peaks <- c(85,98,83,86,85,94,88,92)
#diff.wave.fpl <- c(68,88,70,71,73,73,76,79)

# same but with high .1 pass
diff.wave.peaks <- c(87,99,82,87,86,101,90,92)
diff.wave.fpl <- c(66,90,71,70,71,72,75,78)

pseudo.sd.diff <- diff.wave.peaks-diff.wave.fpl
diff.wave.ret <- c(diff.wave.peaks[3],diff.wave.peaks[6],diff.wave.peaks[2],diff.wave.peaks[7],diff.wave.peaks[4],diff.wave.peaks[1],diff.wave.peaks[5],diff.wave.peaks[8])
diff.wave.win.ret <- c(pseudo.sd.diff[3],pseudo.sd.diff[6],pseudo.sd.diff[2],pseudo.sd.diff[7],pseudo.sd.diff[4],pseudo.sd.diff[1],pseudo.sd.diff[5],pseudo.sd.diff[8])
TMS.ret <- c(TMSsm[3],TMSsm[6],TMSsm[2],TMSsm[7],TMSsm[4],TMSsm[1],TMSsm[5],TMSsm[8])
TMS.win.ret <- c(pseudo.sd.TMS[3],pseudo.sd.TMS[6],pseudo.sd.TMS[2],pseudo.sd.TMS[7],pseudo.sd.TMS[4],pseudo.sd.TMS[1],pseudo.sd.TMS[5],pseudo.sd.TMS[8])

fatty = 5

par(mar=c(4, 6, 4, 4) + 0.1)
plot(diff.wave.ret,subs,col=2,xlim = c(60,160),ylim = c(.75,8.25),main = 'C1 Window (red) vs Suppression Window (blue)', yaxt = "n",
     xlab = 'Latency (ms)', ylab = '', lwd = fatty, pch = dot)
arrows(diff.wave.ret-diff.wave.win.ret, subs, diff.wave.ret+diff.wave.win.ret, subs, length=0.075, angle=90, code=3,col=2, lwd = fatty)
points(TMS.ret,subs, col=4, lwd = fatty, pch = dot)
arrows(TMS.ret-TMS.win.ret, subs, TMS.ret+TMS.win.ret, subs, length=.075,angle=90,code=3,col=4, lwd = fatty)
grid(NULL,NA)
#legend(137,4.5,legend = (c("C1","Suppression")), col = c('red','blue'), pch = dot, bg = NULL,
#       cex = 1, box.lty = 0)
axis(2, subs, labels = c("S3(V1)","S6(V1)","S2(V1/V2)","S7(V2?)","S4(V2)","S1(V2)","S5(V3)","S8(V3)"),las = 2, cex = .5)
mtext("Subject", side=2, line=5, cex.lab=1, las=0)
cex = 1.5

diff.wave.fpl.fir30 <- c(68,88,70,71,73,73,76,79)
diff.wave.fpl.fir50 <- c(67,91,73,71,73,73,77,81)
diff.wave.fpl.wsf50 <- c(69,93,75,73,75,74,78,83)

diff.wave.peaks.fir30 <- c(85,98,83,86,85,94,88,92)
diff.wave.peaks.fir50 <- c(90,98,82,88,86,103,90,93)
diff.wave.peaks.wsf50 <- c(91,96,80,87,89,87,92,94)

confidence_interval <- function(vector, interval) {
  # Standard deviation of sample
  vec_sd <- sd(vector)
  # Sample size
  n <- length(vector)
  # Mean of sample
  vec_mean <- mean(vector)
  # Error according to t distribution
  error <- qt((interval + 1)/2, df = n - 1) * vec_sd / sqrt(n)
  # Confidence interval as a vector
  result <- c("lower" = vec_mean - error, "upper" = vec_mean + error)
  return(result)
}
