function AntiSqlValid(oField){
   re= /select|update|delete|exec|count|��|"|=|;|>|<|%/i;
   if(re.test(oField.value)){
		alert("������Ҫ�ڲ��������������ַ���SQL�ؼ��֣�"); 
		return false;
   }