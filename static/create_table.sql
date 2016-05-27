/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2016/5/27 13:31:19                           */
/*==============================================================*/


drop table if exists Community;

drop table if exists House;

drop table if exists Realty;

drop table if exists Save;

drop table if exists User;

/*==============================================================*/
/* Table: Community                                             */
/*==============================================================*/
create table Community
(
   com_id               varchar(64) not null,
   realty_email         varchar(64) not null,
   com_name             varchar(256) not null,
   com_city             varchar(64) not null,
   com_street           varchar(64) not null,
   com_nearbymarket     int,
   com_nearbyschool     int,
   com_safety           int,
   primary key (com_id)
);

/*==============================================================*/
/* Table: House                                                 */
/*==============================================================*/
create table House
(
   houseid              varchar(64) not null,
   com_id               varchar(64) not null,
   house_size           int,
   avail_date           date not null,
   rent                 int not null,
   bedroom              int not null,
   bathroom             int not null,
   house_floor          int not null,
   primary key (houseid)
);

/*==============================================================*/
/* Table: Realty                                                */
/*==============================================================*/
create table Realty
(
   realty_email         varchar(64) not null,
   realty_name          varchar(64) not null,
   realty_setupdate     date,
   website              varchar(256),
   primary key (realty_email)
);

/*==============================================================*/
/* Table: Save                                                  */
/*==============================================================*/
create table Save
(
   user_email           varchar(64) not null,
   houseid              varchar(64) not null,
   primary key (user_email, houseid)
);

/*==============================================================*/
/* Table: User                                                  */
/*==============================================================*/
create table User
(
   user_email           varchar(64) not null,
   user_pswd            varchar(64) not null,
   user_enter_date      date not null,
   user_type            bool not null,
   primary key (user_email)
);

alter table Community add constraint FK_Own foreign key (realty_email)
      references Realty (realty_email) on delete restrict on update restrict;

alter table House add constraint FK_Belong foreign key (com_id)
      references Community (com_id) on delete restrict on update restrict;

alter table Save add constraint FK_Save foreign key (user_email)
      references User (user_email) on delete restrict on update restrict;

alter table Save add constraint FK_Save2 foreign key (houseid)
      references House (houseid) on delete restrict on update restrict;

