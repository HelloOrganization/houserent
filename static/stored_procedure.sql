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
   IN city             varchar(64),
   IN street           varchar(64),
   IN avail         bool,
   IN rt                 int,
   IN bed              int,
   IN bath             int,
   IN floor          int,
   IN size           int
)
BEGIN
    if ( select not exists (select 1 from Environment where env_city = city and env_street = street ) ) THEN
        insert into Environment
            (
                env_city,
                env_street
            )
            values
            (
                city,
                street
            );
    END if;
    insert into House
    (
       realty_email,
       env_city,
       env_street,
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
       city,
       street,
       avail,
       rt,
       bed,
       bath,
       floor,
       size
    );
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_save $$
CREATE PROCEDURE sp_save(
   IN email        varchar(64),
   IN hid           int
)
BEGIN
    if ( select exists (select 1 from Save where renter_email = email and houseid = hid ) ) THEN

        select 'Already saved!';

    else
        insert into Save
            (
                renter_email,
                houseid
            )
            values
            (
                email,
                hid
            );
    END if;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_favorite $$
CREATE PROCEDURE sp_favorite(
   IN email        varchar(64)
)
BEGIN
    select H.*, R.realty_name, R.website, E.env_nearbymarket, E.env_nearbyschool, E.env_safety
    from Save as S, House as H, Realty as R, Environment as E
    where S.renter_email = email
    and S.houseid = H.houseid
    and H.realty_email = R.realty_email
    and H.env_city = E.env_city
    and H.env_street = E.env_street;
END$$
DELIMITER ;
