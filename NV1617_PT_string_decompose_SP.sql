DELIMITER $$

USE `nv1617`$$

DROP PROCEDURE IF EXISTS `split_pt_scores`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `split_pt_scores`()
BEGIN
	DECLARE t_row_num INT;
	DECLARE pt_scr_str VARCHAR(6);
	DECLARE pt_scr_str_len TINYINT;
	DECLARE pt_scr VARCHAR(1);
	DECLARE pt_subtest_sequence TINYINT DEFAULT 1;
	DECLARE last_row INT DEFAULT 0;
	DECLARE this_pt_str CURSOR FOR
	   SELECT row_num, PT_score_string, LENGTH(PT_score_string) 
	        FROM tests WHERE LENGTH(PT_score_string) > 0 AND row_num > 398967;
	DECLARE CONTINUE HANDLER
	   FOR NOT FOUND SET last_row = 1;
	OPEN this_pt_str;
	FetchPT: LOOP
	  FETCH this_pt_str INTO t_row_num, pt_scr_str, pt_scr_str_len;
	  IF last_row = 1 THEN
	    LEAVE FetchPT;
	  END IF;
	  SET pt_subtest_sequence = 1;
	  WHILE pt_subtest_sequence <= pt_scr_str_len DO
	    SET pt_scr = MID(pt_scr_str, pt_subtest_sequence, 1);
	      INSERT INTO items (test_row_num, subTest, subTestItemOrder, itemScore) VALUES
	         (t_row_num, 'PT', pt_subtest_sequence, pt_scr);
            SET pt_subtest_sequence = pt_subtest_sequence + 1;
	  END WHILE;
	END LOOP FetchPT;
	CLOSE this_pt_str;
	END$$

DELIMITER ;