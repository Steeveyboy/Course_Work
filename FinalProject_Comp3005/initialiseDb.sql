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
    Image_Address text,
    Year integer, 
    Gallery text,
    Collection text
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
INSERT INTO Artwork Values('Miss Liberty Celebration', 'Malcah Zeldis', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1988/SAAM-1988.74.14_1.jpg?itok=IUl6RGg2', 1987, 'Smithsonian American Art Museum', 'Luce Foundation Center');
INSERT INTO Artwork Values('Hindu Merchants', 'Edwin Lord Weeks', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1924/SAAM-1924.7.1_1.jpg?itok=lBS_ggw1', 1885, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The Thundershower', 'H. Lyman Saÿen', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1967/SAAM-1967.6.19_1.jpg?itok=-jR3R2tb', 1918, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Stevenson Memorial', 'Abbott Handerson Thayer', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1929/SAAM-1929.6.127_1.jpg?itok=mTle_53X', 1903, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('People in the\xa0Sun', 'Edward Hopper', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1969/SAAM-1969.47.61_2.jpg?itok=hKAbVkRF', 1960, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The South Ledges, Appledore', 'Childe Hassam', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1929/SAAM-1929.6.62_2.jpg?itok=nvu3WpJ_', 1913, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Lamentations over the Death of the First-Born of\xa0Egypt', 'Charles Sprague Pearce', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1985/SAAM-1985.28_1.jpg?itok=MOEgJ5Mh', 1877, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Still Life with\xa0Fruit', 'Severin Roesen', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1981/SAAM-1981.114_1.jpg?itok=QlDg62fn', 1852, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Buffalo Grain Elevators', 'Ralston Crawford', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1976/SAAM-1976.133_2.jpg?itok=IJDrnof_', 1937, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Design Made at Airlie Gardens', 'Minnie Evans', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1972/SAAM-1972.44_1.jpg?itok=5SiCD1Ut', 1967, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Elizabeth Winthrop Chanler (Mrs. John Jay Chapman)', 'John Singer Sargent', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1980/SAAM-1980.71_3.jpg?itok=ptCtPrLM', 1893, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The Great Horseshoe Fall, Niagara', 'Alvan Fisher', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1966/SAAM-1966.82.1_1.jpg?itok=KNGlXT48', 1820, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Man with the Cat (Henry Sturgis Drinker)', 'Cecilia Beaux', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1952/SAAM-1952.10.1_1.jpg?itok=3D-_0Otv', 1898, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Yliaster (Paracelsus)', 'Marsden Hartley', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1988/SAAM-1988.53_1.jpg?itok=NRds2j0W', '1932', 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Portrait of Mrs. Barbara Baker Murphy (Wife of Sea Captain)', 'Joshua Johnson', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1983/SAAM-1983.95.56_1.jpg?itok=uZVeHJmY', 1810, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('An Interlude', 'William Sergeant Kendall', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1909/SAAM-1909.7.36_1.jpg?itok=tprAZnxq', 1907, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Torre di Schiavi', 'Thomas Hiram Hotchkiss', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1977/SAAM-1977.52_1.jpg?itok=wg3qQk2T', 1865, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Achelous and Hercules', 'Thomas Hart Benton', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1985/SAAM-1985.2_5.jpg?itok=6YeJj02l', 1947, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The Iron Mine, Port Henry, New\xa0York', 'Homer Dodge Martin', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1910/SAAM-1910.9.11_1.jpg?itok=fhrw-nUI', 1862, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Stag at Echo\xa0Rock', 'Unidentified', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1986/SAAM-1986.65.117_1.jpg?itok=0AMH1DPc', 1899, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');


COMMIT;

