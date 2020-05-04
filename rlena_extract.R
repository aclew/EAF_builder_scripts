
library(devtools)
devtools::install_github("HomeBankCode/rlena", dependencies=FALSE)
print('installed')
library(rlena)
library(dplyr, warn.conflicts = FALSE)

rlena_extraction<- function(file){
	round_to_5min= function(x) gsub(":(.)([01234])",":\\10",gsub(":(.)([56789])",":\\15",gsub("(.*):(.*)","\\1",x)))
	its <- read_its_file(file)
	x<-gather_segments(its)
	x$rnd=round_to_5min(x$startClockTime)
	x$is_CT=ifelse(x$convTurnType %in% c("TIFR","TIMR"),1,0)# don't count: "TIMI","TIFE","TIFI","TIME", "NT
	# NT TIFE TIFI TIFR TIME TIMI TIMR
	tab1 <- aggregate(x$is_CT,by=list(x$rnd),sum,na.rm=T) #CTC 
	tab2 <- aggregate(x$childUttCnt,by=list(x$rnd),sum,na.rm=T) #child utterence count
	x$adultWordCnt=ifelse(is.na(x$femaleAdultWordCnt),0,x$femaleAdultWordCnt) + ifelse(is.na(x$maleAdultWordCnt),0,x$maleAdultWordCnt)
	tab3 <- aggregate(x$adultWordCnt,by=list(x$rnd),sum,na.rm=T)#AdultWordCount
	write.table(tab1, file = "CTC.csv", append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"), fileEncoding = "")
	write.table(tab2, file = "CVC.csv", append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"),fileEncoding = "")
	write.table(tab3, file = "AWC.csv", append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"), fileEncoding = "")
	write.table(x["startClockTime"], file = "Time_info.csv", append = FALSE, quote = TRUE, sep =",", eol="\n", na = "NA",dec = ".", row.names = TRUE,col.names = TRUE, qmethod = c("escape","double"),fileEncoding = "")
}