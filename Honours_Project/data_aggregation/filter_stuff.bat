@echo off

set dbconn=sqlite3 flow_database.db

%dbconn% "DROP table if exists Contract_Data;"
%dbconn% "DROP table if exists Price_Data;"
%dbconn% "DROP table if exists Treasury_Rates;"

%dbconn% ".read create_flow.sql"

%dbconn% ".read test_query.sql"
