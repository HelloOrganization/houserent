/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2016/5/27 22:09:04                           */
/*==============================================================*/

drop table if exists Save;

<<<<<<< HEAD
drop table if exists Save;
drop table if exists House;

drop table if exists Community;
=======
drop table if exists Environment;
>>>>>>> 658dffafdc4c1f2eb3e3de78510441536edd1965


drop table if exists Realty;

drop table if exists Renter;


/*==============================================================*/
/* Table: Environment                                           */
/*==============================================================*/
create table Environment
(
   env_city             varchar(64) not null,
   env_street           varchar(64) not null,
   env_nearbymarket     int,
   env_nearbyschool     int,
   env_safety           int,
   primary key (env_city, env_street)
);

/*==============================================================*/
/* Table: House                                                 */
/*==============================================================*/
create table House
(
   houseid              int not null auto_increment,
   realty_email         varchar(64) not null,
   env_city             varchar(64) not null,
   env_street           varchar(64) not null,
   availability         bool not null,
   rent                 int not null,
   bedroom              int not null,
   bathroom             int not null,
   house_floor          int not null,
   house_size           int not null,
   primary key (houseid)
);

/*==============================================================*/
/* Table: Realty                                                */
/*==============================================================*/
create table Realty
(
   realty_email         varchar(64) not null,
   realty_pswd          varchar(64) not null,
   realty_name          varchar(64) not null,
   realty_setup_date    date,
   website              varchar(256),
   realty_register_date date not null,
   primary key (realty_email)
);

/*==============================================================*/
/* Table: Renter                                                */
/*==============================================================*/
create table Renter
(
   renter_email         varchar(64) not null,
   renter_pswd          varchar(64) not null,
   renter_register_date date not null,
   primary key (renter_email)
);

/*==============================================================*/
/* Table: Save                                                  */
/*==============================================================*/
create table Save
(
   renter_email         varchar(64) not null,
   houseid              int not null,
   primary key (renter_email, houseid)
);

alter table House add constraint FK_Belong foreign key (env_city, env_street)
      references Environment (env_city, env_street) on delete restrict on update restrict;

alter table House add constraint FK_Own foreign key (realty_email)
      references Realty (realty_email) on delete restrict on update restrict;

alter table Save add constraint FK_Save foreign key (renter_email)
      references Renter (renter_email) on delete restrict on update restrict;

alter table Save add constraint FK_Save2 foreign key (houseid)
      references House (houseid) on delete restrict on update restrict;

