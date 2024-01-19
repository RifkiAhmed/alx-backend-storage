-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for a student.

DELIMITER #
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    DECLARE result FLOAT;
    SELECT (SUM(corrections.score * projects.weight) / SUM(projects.weight))
    INTO result
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    UPDATE users SET average_score = result
    WHERE users.id = user_id;
END #

DELIMITER ;
