BEGIN TRANSACTION;

DELETE FROM Price_Data where date_of = 't';

ALTER TABLE Price_Data
ADD date_of_close DATE;

UPDATE Price_Data
set date_of_close = DATE(date_of, '+4 days');


END TRANSACTION;