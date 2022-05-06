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
    Gallery_Name text,
    Collection text
);

CREATE TABLE Patron(
    First_Name text,
    Last_Name text,
    Patron_ID integer primary key not null unique
);

CREATE TABLE OwnershipContract(
    Artwork_Title text,
    Patron_ID text,
    ContractId integer not null,
    percent_share float
);

INSERT INTO Gallery Values("Smithsonian American Art Museum", "Washington, D.C., United States");
INSERT INTO Gallery Values("National Gallery of Art", "Washington, D.C., United States");
INSERT INTO Gallery Values("National Gallery of Canada", "Ottawa, Ontario, Canada");
INSERT INTO Gallery Values("The Met Museum", "New York, New York, United States");
INSERT INTO Gallery Values("Museum Of Modern Art", "New York, New York, United States");

INSERT INTO Artwork Values("Death of Rubén Salazar", "Frank Romero", "https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1993/SAAM-1993.19_1.jpg?itok=ISPh0ext", 1986, "Smithsonian American Art Museum", "Smithsonian American Art Museum Collection");
INSERT INTO Artwork Values('Miss Liberty Celebration', 'Malcah Zeldis', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1988/SAAM-1988.74.14_1.jpg?itok=IUl6RGg2', 1987, 'Smithsonian American Art Museum', 'Luce Foundation Center');
INSERT INTO Artwork Values('Hindu Merchants', 'Edwin Lord Weeks', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1924/SAAM-1924.7.1_1.jpg?itok=lBS_ggw1', 1885, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The Thundershower', 'H. Lyman Saÿen', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1967/SAAM-1967.6.19_1.jpg?itok=-jR3R2tb', 1918, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Stevenson Memorial', 'Abbott Handerson Thayer', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1929/SAAM-1929.6.127_1.jpg?itok=mTle_53X', 1903, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('People in the Sun', 'Edward Hopper', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1969/SAAM-1969.47.61_2.jpg?itok=hKAbVkRF', 1960, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('The South Ledges, Appledore', 'Childe Hassam', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1929/SAAM-1929.6.62_2.jpg?itok=nvu3WpJ_', 1913, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Lamentations over the Death of the First-Born of Egypt', 'Charles Sprague Pearce', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1985/SAAM-1985.28_1.jpg?itok=MOEgJ5Mh', 1877, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Still Life with Fruit', 'Severin Roesen', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1981/SAAM-1981.114_1.jpg?itok=QlDg62fn', 1852, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
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
INSERT INTO Artwork Values('The Iron Mine, Port Henry, New York', 'Homer Dodge Martin', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1910/SAAM-1910.9.11_1.jpg?itok=fhrw-nUI', 1862, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');
INSERT INTO Artwork Values('Stag at Echo Rock', 'Unidentified', 'https://s3.amazonaws.com/assets.saam.media/files/styles/x_large/s3/files/images/1986/SAAM-1986.65.117_1.jpg?itok=0AMH1DPc', 1899, 'Smithsonian American Art Museum', 'Smithsonian American Art Museum');


INSERT INTO Artwork Values('BALLING', 'JOYCE WIELAND', 'https://www.gallery.ca/sites/default/files/7999172_0.jpg', 1961, 'National Gallery of Canada', 'Later Canadian Art');
INSERT INTO Artwork Values("ROCK NEEDLE SEEN THROUGH THE PORTE D'AVAL, ÉTRETAT", 'CLAUDE MONET', 'https://www.gallery.ca/sites/default/files/11973558_0.jpg', 1886, 'National Gallery of Canada', 'European and American Painting, Sculpture, and Decorative Arts');
INSERT INTO Artwork Values('PERSPECTIVE', 'JEAN PAUL LEMIEUX', 'https://www.gallery.ca/sites/default/files/Perspective.jpg', 1929, 'National Gallery of Canada', 'Canadian Prints and Drawings');
INSERT INTO Artwork Values('QUEBEC FROM THE CITADEL', 'JEAN PAUL LEMIEUX', 'https://www.gallery.ca/sites/default/files/Quebec%20from%20the%20Citadel.jpg', 1929, 'National Gallery of Canada', 'Canadian Prints and Drawings');
INSERT INTO Artwork Values('BEACH POOLS AT NIGHT', 'GORDON SMITH', 'https://www.gallery.ca/sites/default/files/Beach%20Pools%20at%20Night.jpg', 1963, 'National Gallery of Canada', 'Later Canadian Art');
INSERT INTO Artwork Values('FRANK SINATRA, NEW YORK', 'LISETTE MODEL', 'https://www.gallery.ca/sites/default/files/Frank%20Sinatra%2C%20New%20York.jpg', 1944, 'National Gallery of Canada', 'Photography');
INSERT INTO Artwork Values('UNTITLED', 'OSCAR CAHÉN', 'https://www.gallery.ca/sites/default/files/Untitled_106.jpg', 1956, 'National Gallery of Canada', 'Canadian Prints and Drawings');
INSERT INTO Artwork Values('VERIDITAS', 'JOYCE WIELAND', 'https://www.gallery.ca/sites/default/files/Veriditas.jpg', 1987, 'National Gallery of Canada', 'Later Canadian Art');
INSERT INTO Artwork Values('GATHERING', 'ALLEN SAPP', 'https://www.gallery.ca/sites/default/files/Gathering.jpg', 2000, 'National Gallery of Canada', 'Indigenous Art');
INSERT INTO Artwork Values('FONTAINEBLEAU', 'IAN PATERSON', 'https://www.gallery.ca/sites/default/files/Fontainebleau_0.jpg', 1992, 'National Gallery of Canada', 'Photography');
INSERT INTO Artwork Values('UNDERPASS, MONTREAL', 'GHITTA CAISERMAN', 'https://www.gallery.ca/sites/default/files/Underpass%2C%20Montreal.jpg', 1950, 'National Gallery of Canada', 'Later Canadian Art');

INSERT INTO Artwork Values('The Fortress of Königstein', 'Bernardo Bellotto', 'https://media.nga.gov/iiif/8b3b5c3e-0b36-4229-bbcf-645cd16126f9/full/!588,600/0/default.jpg', 1758, 'National Gallery of Art', 'West Building, Main Floor');
INSERT INTO Artwork Values("Haskell's House", 'Edward Hopper', 'https://media.nga.gov/iiif/744963be-8367-45b0-b40f-097bc554bb88/full/!588,600/0/default.jpg', 1924, 'National Gallery of Art', 'Not on View');
INSERT INTO Artwork Values('The House of Representatives', 'Samuel F. B. Morse', 'https://media.nga.gov/iiif/48b6e029-9d34-4ed3-957e-36e4252d34d2/full/!588,600/0/default.jpg', 1822, 'National Gallery of Art', 'West Building, Main Floor');
INSERT INTO Artwork Values('The Island and Bridge of San Bartolomeo', 'Jean-Baptiste-Camille Corot', 'https://media.nga.gov/iiif/b65ea558-0cd2-4abc-8a76-56d9b6c44f7f/full/!588,600/0/default.jpg', 1928,'National Gallery of Art', 'Not on View');
INSERT INTO Artwork Values('Keelmen Heaving in Coals by Moonlight', 'Joseph Mallord William Turner', 'https://media.nga.gov/iiif/c1e33e8d-ffe4-4d20-a267-87ffcf94f7ce/full/!588,600/0/default.jpg', 1835, 'National Gallery of Art', 'Not on View');
INSERT INTO Artwork Values('The Japanese Footbridge', 'Claude Monet', 'https://media.nga.gov/iiif/0b9cefb5-1ee4-401a-8154-8d4039191a28/full/!588,600/0/default.jpg', 1899, 'National Gallery of Art', 'West Building, Main Floor');

INSERT INTO Artwork Values('Double Transparency', 'Jesús Rafael Soto', 'https://www.moma.org/media/W1siZiIsIjQzNDEwOSJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA5MCAtcmVzaXplIDc2OHg3NjhcdTAwM2UiXV0.jpg?sha=644de8b221d23f85', 1956, 'Museum Of Modern Art', 'The David Geffen Galleries');
INSERT INTO Artwork Values('Large Check: 6', 'Sherrie Levine', 'https://www.moma.org/media/W1siZiIsIjE1MTIzNiJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA5MCAtcmVzaXplIDE0NDB4MTA4MFx1MDAzZSJdXQ.jpg?sha=fda3f8f8c4307bad', 1987, 'Museum Of Modern Art', 'Floor 2');


INSERT INTO Artwork Values('Porte de la Reine at Aigues-Mortes', 'Jean-Frédéric Bazille', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/435626/1885041/main-image', 1867, 'The Met Museum', 'European Paintings');
INSERT INTO Artwork Values('The Great Wave', 'Katsushika Hokusai', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/45434/134438/main-image', 1832, 'The Met Museum', 'Asian Art');
INSERT INTO Artwork Values("The Titan's Goblet", 'Thomas Cole', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/10499/1660910/main-image', 1833, 'The Met Museum', 'The American Wing');
INSERT INTO Artwork Values('Ocean Life', 'James M. Sommerville', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/12544/32461/main-image', 1859, 'The Met Museum', 'The American Wing');
INSERT INTO Artwork Values('The Oxbow', 'Thomas Cole', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/10497/1655152/main-image', 1836, 'The Met Museum', 'The American Wing');
INSERT INTO Artwork Values('The Gulf Stream', 'Winslow Homer', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/11122/2018691/main-image', 1899, 'The Met Museum', 'The American Wing');
INSERT INTO Artwork Values('Two Men Contemplating the Moon','Caspar David Friedrich','https://collectionapi.metmuseum.org/api/collection/v1/iiif/438417/796421/main-image', 1830,'The Met Museum','European Paintings');
INSERT INTO Artwork Values('A Sunday on La Grande Jatte','Georges Seurat','https://collectionapi.metmuseum.org/api/collection/v1/iiif/437658/802352/main-image', 1884,'The Met Museum','European Paintings');
INSERT INTO Artwork Values('The Constitution and the Guerriere','Thomas Chambers','https://collectionapi.metmuseum.org/api/collection/v1/iiif/10431/33677/main-image', 1845,'The Met Museum','The American Wing');


INSERT INTO Patron Values('Jonathon', 'Steeves', 101);
INSERT INTO Patron Values('Alexander', 'Steeves', 102);
INSERT INTO Patron Values('Owen', 'McAdams', 103);
INSERT INTO Patron Values('Matthew', 'Marshall', 104);
INSERT INTO Patron Values('Alison', 'Sa', 105);
INSERT INTO Patron Values('Louis', 'Nel', null);
INSERT INTO Patron Values('Robert', 'Collier', null);
INSERT INTO Patron Values('Alexa', 'Sharp', null);
INSERT INTO Patron Values('Elon', 'Musk', null);
INSERT INTO Patron Values('Bill', 'Gates', null);
INSERT INTO Patron Values('Jeff', 'Bezos', null);

INSERT INTO OwnershipContract Values('Death of Rubén Salazar', 101, 300501, 25.0);
INSERT INTO OwnershipContract Values('Death of Rubén Salazar', 102, 300501, 25.0);
INSERT INTO OwnershipContract Values('Hindu Merchants', 103, 300502, 10.0);
INSERT INTO OwnershipContract Values('An Interlude', 101, 300503, 20.0);
INSERT INTO OwnershipContract Values('An Interlude', 103, 300503, 20.0);
INSERT INTO OwnershipContract Values('An Interlude', 104, 300503, 20.0);
INSERT INTO OwnershipContract Values('An Interlude', 105, 300503, 20.0);
INSERT INTO OwnershipContract Values('The Thundershower', 102, 300504, 5.0);
INSERT INTO OwnershipContract Values('The Thundershower', 102, 300504, 5.0);
INSERT INTO OwnershipContract Values('The Thundershower', 102, 300504, 5.0);
INSERT INTO OwnershipContract Values('Large Check: 6', 109, 300505, 50.1);
INSERT INTO OwnershipContract Values('Large Check: 6', 110, 300505, 10.0);
INSERT INTO OwnershipContract Values('Large Check: 6', 111, 300505, 10.0);
INSERT INTO OwnershipContract Values('Double Transparency', 106, 300506, 10.0);
INSERT INTO OwnershipContract Values('Double Transparency', 109, 300506, 50.1);
INSERT INTO OwnershipContract Values("Haskell's House", 107, 300506, 99.0);

COMMIT;

