
rlena_extraction<- function(file,output_dir){
	round_to_5min= function(x) gsub(":(.)([01234])",":\\10",gsub(":(.)([56789])",":\\15",gsub("(.*):(.*)","\\1",x)))
	its <- read_its_file(file)
	x<-gather_segments(its)
	x$rnd=round_to_5min(x$startClockTimeLocal)
	x$is_CT=ifelse(x$convTurnType %in% c("TIFR","TIMR"),1,0)# don't count: "TIMI","TIFE","TIFI","TIME", "NT
	# NT TIFE TIFI TIFR TIME TIMI TIMR
	tab1 <- aggregate(x$is_CT,by=list(x$rnd),sum,na.rm=T) #CTC 
	tab2 <- aggregate(x$childUttCnt,by=list(x$rnd),sum,na.rm=T) #child utterence count
	x$adultWordCnt=ifelse(is.na(x$femaleAdultWordCnt),0,x$femaleAdultWordCnt) + ifelse(is.na(x$maleAdultWordCnt),0,x$maleAdultWordCnt)
	tab3 <- aggregate(x$adultWordCnt,by=list(x$rnd),sum,na.rm=T)#AdultWordCount
	csv_ctc=paste(output_dir,"CTC.csv",sep='/')
	csv_cvc=paste(output_dir,"CVC.csv",sep='/')
	csv_awc=paste(output_dir,"AWC.csv",sep='/')
	csv_time=paste(output_dir,"Time_info.csv",sep='/')
	write.csv(tab1, csv_ctc, append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"), fileEncoding = "")
	write.csv(tab2, csv_cvc, append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"),fileEncoding = "")
	write.csv(tab3, csv_awc, append = FALSE, quote = TRUE, sep = ",", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"), fileEncoding = "")
	write.csv(x["startClockTime"], csv_time, append = FALSE, quote = TRUE, sep =",", eol="\n", na = "NA",dec = ".", row.names = TRUE,col.names = TRUE, qmethod = c("escape","double"),fileEncoding = "")
}