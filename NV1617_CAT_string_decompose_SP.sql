DELIMITER $$

USE `nv1617`$$

DROP PROCEDURE IF EXISTS `split_cat_scores_ids`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `split_cat_scores_ids`()
BEGIN

	DECLARE t_row_num INT;
	DECLARE cat_scr_str VARCHAR(64);
	DECLARE cat_scr_str_len TINYINT;
	DECLARE cat_scr CHAR(1);
	DECLARE cat_id_str VARCHAR(300);
	DECLARE cat_id_str_len SMALLINT;
	DECLARE cat_id CHAR(6);
	DECLARE cat_subtest_sequence TINYINT DEFAULT 1;
	DECLARE cat_subtest_id_sequence SMALLINT DEFAULT 1;
	DECLARE last_row INT DEFAULT 0;
	DECLARE this_cat_rcd CURSOR FOR
	   SELECT row_num, CAT_score_string, LENGTH(CAT_score_string), item_id_string, LENGTH(item_id_string)
	        FROM tests WHERE LENGTH(CAT_score_string) > 0 AND LENGTH(item_id_string) > 0 AND row_num > 169190;
	DECLARE CONTINUE HANDLER
	   FOR NOT FOUND SET last_row = 1;
	OPEN this_cat_rcd;
	FetchCAT: LOOP
	  FETCH this_cat_rcd INTO t_row_num, cat_scr_str, cat_scr_str_len, cat_id_str, cat_id_str_len;
	  IF last_row = 1 THEN
	    LEAVE FetchCAT;
	  END IF;
	  SET cat_subtest_sequence = 1;
	  WHILE cat_subtest_sequence <= cat_scr_str_len DO
	    SET cat_scr = MID(cat_scr_str, cat_subtest_sequence, 1);
	    IF cat_id_str_len > 0 THEN
	      IF cat_subtest_sequence = 1 THEN
	        SET cat_subtest_id_sequence = 1;
	      ELSE
	        SET cat_subtest_id_sequence = 1 + (6 * (cat_subtest_sequence - 1));
	      END IF;
	      SET cat_id = MID(cat_id_str, cat_subtest_id_sequence, 6);
	    ELSE 
	      SET cat_id = '';
	    END IF;
	    INSERT INTO items (test_row_num, subTest, subTestItemOrder, nvItemId, itemScore) VALUES
	         (t_row_num, 'CAT', cat_subtest_sequence, cat_id, cat_scr);
            SET cat_subtest_sequence = cat_subtest_sequence + 1;
	  END WHILE;
	END LOOP FetchCAT;
	CLOSE this_cat_rcd;

	END$$

DELIMITER ;