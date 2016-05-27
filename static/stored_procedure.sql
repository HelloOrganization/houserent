DELIMITER $$
CREATE PROCEDURE sp_signUp(
    IN u_email VARCHAR(20),
    IN u_pswd VARCHAR(20),
    IN u_enter_date date,
    IN u_type bool
)
BEGIN
    if ( select exists (select 1 from User where user_email = u_email) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into User
        (
            user_email,
            user_pswd,
            user_enter_date,
            user_type
        )
        values
        (
            u_email,
            u_pswd,
            u_enter_date,
            u_type
        );

    END IF;
END$$
DELIMITER ;
