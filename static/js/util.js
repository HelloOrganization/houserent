function AntiSqlValid(oField){
   re= /select|update|delete|exec|count|’|"|=|;|>|<|%/i;
   if(re.test(oField.value)){
		alert("请您不要在参数中输入特殊字符和SQL关键字！"); 
		return false;
   }