BEGIN TRANSACTION;

DROP TABLE IF EXISTS Gallery;
DROP TABLE IF EXISTS Artwork;
DROP TABLE IF EXISTS Patron;
DROP TABLE IF EXISTS OwnershipContract;

CREATE TABLE Gallery(
    Gallery_Name text primary key not null unique,
    Location text
);

CREATE TABLE Artwork(
    Title text primary key not null unique,
    Artist text,
    Year integer, 
    Gallery text,
    Collection text,
    Image_Address text
);

CREATE TABLE Patron(
    First_Name text,
    Last_Name text,
    Patron_ID text primary key not null unique
);

CREATE TABLE OwnershipContract(
    Artwork_Title text,
    Patron_ID text,
    ContractId primary key unique,
    percent_share float
);

INSERT INTO Gallery Values("Smithsonian American Art Museum", "Washington, D.C., United States");
INSERT INTO Gallery Values("National Gallery of Art", "Washington, D.C., United States");
INSERT INTO Gallery Values("National Gallery of Canada", "Ottawa, Ontario, Canada");
INSERT INTO Gallery Values("The Met Museum", "New York, New York, United States");
INSERT INTO Gallery Values("The Louvre Museum", "Paris, Ile-de-France, France");

INSERT INTO Artwork Values("Death of Rubén Salazar", "Frank Romero", "https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1993/SAAM-1993.19_1.jpg?itok=ISPh0ext", 1986, "Smithsonian American Art Museum", "Smithsonian American Art Museum Collection");




COMMIT;

