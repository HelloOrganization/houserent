DELIMITER $$
CREATE PROCEDURE sp_renterSignUp(
    IN u_email VARCHAR(20),
    IN u_pswd VARCHAR(20),
    IN u_register_date date
)
BEGIN
    if ( select exists (select 1 from Renter where renter_email = u_email) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into User
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
CREATE PROCEDURE sp_realtySignUp(
    IN r_email VARCHAR(20),
    IN r_name VARCHAR(20),
    IN r_pswd VARCHAR(20),
    IN r_setup_date date,
    IN r_website VARCHAR(20),
    IN r_register_date date
)
BEGIN
    if ( select exists (select 1 from Realty where renter_email = r_email) ) THEN

        select 'Realty Exists !!';

    ELSE

        insert into User
        (
            realty_email,
            realty_name,
            realty_setup_date,
            website,
            realty_register_date
        )
        values
        (
            r_email,
            r_name,
            r_pswd,
            r_setup_date,
            r_website,
            r_register_date
        );

    END IF;
END$$
DELIMITER ;
