DELIMITER $$
DROP PROCEDURE IF EXISTS sp_renterSignUp $$
CREATE PROCEDURE sp_renterSignUp(
    IN u_email VARCHAR(64),
    IN u_pswd VARCHAR(64),
    IN u_register_date date
)
BEGIN
    if ( select exists (select 1 from Renter where renter_email = u_email
        union select 2 from Realty where realty_email = u_email) ) THEN

        select 'Email Exists !!';

    ELSE

        insert into Renter
        (
            renter_email,
            renter_pswd,
            renter_register_date
        )
        values
        (
            u_email,
            u_pswd,
            u_register_date
        );

    END IF;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_realtySignUp $$
CREATE PROCEDURE sp_realtySignUp(
    IN r_email VARCHAR(64),
    IN r_pswd VARCHAR(64),
    IN r_name VARCHAR(64),
    IN r_setup_date date,
    IN r_website VARCHAR(256),
    IN r_register_date date
)
BEGIN
    if ( select exists (select 1 from Realty where realty_email = r_email
        union select 2 from Renter where renter_email = r_email) ) THEN
        select 'Email Exists !!';

    ELSE

        insert into Realty
        (
            realty_email,
            realty_pswd,
            realty_name,
            realty_setup_date,
            website,
            realty_register_date
        )
        values
        (
            r_email,
            r_pswd,
            r_name,
            r_setup_date,
            r_website,
            r_register_date
        );

    END IF;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_addHouse $$
CREATE PROCEDURE sp_addHouse(
   IN email        varchar(64),
   IN c_city             varchar(64),
   IN c_street           varchar(64),
   IN h_city           varchar(64),
   IN h_street         varchar(256),
   IN avail         bool,
   IN rt                 int,
   IN bed              int,
   IN bath             int,
   IN floor          int,
   IN size           int
)
BEGIN
    insert into House
    (
       realty_email,
       com_city,
       com_street,
       house_city,
       house_street,
       availability,
       rent,
       bedroom,
       bathroom,
       house_floor,
       house_size
    )
    values
    (
       email,
       c_city,
       c_street,
       h_city,
       h_street,
       avail,
       rt,
       bed,
       bath,
       floor,
       size
    );
END$$
DELIMITER ;
