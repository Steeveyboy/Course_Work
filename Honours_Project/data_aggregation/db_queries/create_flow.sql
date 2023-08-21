BEGIN TRANSACTION;

CREATE TABLE if not exists "Contract_Data"(
    "Symbol" TEXT NOT NULL,
    "Contract_Type" TEXT NOT NULL,
    "Strike" DOUBLE NOT NULL,
    "Bid" DOUBLE PRECISION NOT NULL,
    "Midpoint" DOUBLE NOT NULL,
    "Ask" DOUBLE PRECISION NOT NULL,
    "Volume" INTEGER,
    "Obs_Date" DATE NOT NULL,
    "Exp_Date" DATE
);

CREATE INDEX option_index
on Contract_Data (Symbol, Obs_Date)
;

CREATE TABLE if not exists "Price_Data"(
    "Symbol" TEXT NOT NULL,
    "open" float NOT NULL,
    "close" float NOT NULL,
    "volume" int,
    "date_of" DATE,
    "date_of_close" DATE NOT NULL,
    FOREIGN KEY("Symbol", "date_of_close") REFERENCES Contract_Data(Symbol, Obs_Date)
);

CREATE TABLE if not exists'treasury_rates'(
        "date_of" DATE NOT NULL,
        '1Mo' float,
        '2Mo' float,
        '3Mo' float,
        '4Mo' float,
        '6Mo' float,
        '1Yr' float,
        '2Yr' float,
        '3Yr' float,
        '5Yr' float,
        '7Yr' float,
        '10Yr' float,
        '20Yr' float,
        '30Yr' float
    );

END TRANSACTION;