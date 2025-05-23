BEGIN TRANSACTION;

DROP TABLE IF EXISTS Contract_Data;
CREATE TABLE "Contract_Data"(
    "Symbol" TEXT NOT NULL,
    "Contract_Type" TEXT NOT NULL,
    "Strike" DOUBLE PRECISION NOT NULL,
    "Bid" DOUBLE PRECISION NOT NULL,
    "Midpoint" DOUBLE PRECISION NOT NULL,
    "Ask" DOUBLE PRECISION NOT NULL,
    "Last" DOUBLE PRECISION NOT NULL,
    "Volume" INTEGER NOT NULL,
    "Open_Int" DOUBLE PRECISION NOT NULL,
    "Obs_Date" DATE,
    "Exp_Date" DATE NOT NULL
);

-- DROP TABLE IF EXISTS Price_Data;
-- CREATE TABLE "Price_Data"(
--     "Symbol" TEXT NOT NULL,
--     "Price_close" DOUBLE PRECISION NOT NULL,
--     "Volume" BIGINT,
--     "Date_of" DATE NOT NULL
-- );

END TRANSACTION;
