-- SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
DELIMITER #
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    UPDATE users SET average_score = (
        SELECT IFNULL(AVG(score), 0) FROM corrections
        WHERE corrections.user_id = user_id)
        WHERE id = user_id;
END#

DELIMITER ;
