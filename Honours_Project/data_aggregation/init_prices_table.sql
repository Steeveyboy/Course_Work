BEGIN TRANSACTION;

DROP TABLE IF EXISTS Price_Data;
CREATE TABLE "Price_Data"(
    "Symbol" TEXT NOT NULL,
    "open" float NOT NULL,
    "close" float NOT NULL,
    "high" float NOT NULL,
    "low" float NOT NULL,
    "volume" int,
    "date_of" DATE NOT NULL

);

-- DROP TABLE IF EXISTS Price_Data;
-- CREATE TABLE "Price_Data"(
--     "Symbol" TEXT NOT NULL,
--     "Price_close" DOUBLE PRECISION NOT NULL,
--     "Volume" BIGINT NOT NULL,
--     "Date_of" DATE NOT NULL
-- );

END TRANSACTION;