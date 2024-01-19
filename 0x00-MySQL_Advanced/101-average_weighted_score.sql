-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for all student.

DELIMITER #
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE result FLOAT;
    DECLARE user_id INT;
    DECLARE done BOOLEAN DEFAULT FALSE;
    -- Cursor to iterate over users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    -- Handle NOT FOUND condition
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;
    user_loop: LOOP
        -- Fetch the next user_id
        FETCH user_cursor INTO user_id;
        -- Exit the loop if no more users
        IF done THEN
            LEAVE user_loop;
        END IF;

        SELECT (SUM(corrections.score * projects.weight) / SUM(projects.weight))
        INTO result FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        UPDATE users SET average_score = result
        WHERE users.id = user_id;
    END LOOP user_loop;
    CLOSE user_cursor;
END #
DELIMITER ;
