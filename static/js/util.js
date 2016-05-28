function AntiSqlValid(oField){
   re= /select|update|delete|exec|count|'|"|=|;|>|<|%/i;
   if(re.test(oField.value)){
		alert("不要插入特殊字符！");
		return false;
   }
