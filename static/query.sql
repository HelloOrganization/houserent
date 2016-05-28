drop procedure sp_signUp;

select * from user;

select 'sa';

select exists (select 1 from house);

select * from house as h, save as s where h.houseid = 2 ;#and s.houseid = h.houseid;

update House set availability = 1 where houseid = 1;

update House set availability = 0 where houseid = 1;

select * from house;

select 1 from Renter where renter_email = "asd@x.com" and renter_pswd = "" or 1=1 ; -- ";
