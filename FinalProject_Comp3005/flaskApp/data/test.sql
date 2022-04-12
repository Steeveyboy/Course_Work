

-- Find a patrons art collection
with 
    contracts(Artwork_Title, Patron_ID, percent_share, ContractId, First_Name, Last_Name) AS (select Artwork_Title, Patron.Patron_ID, percent_share, ContractId, First_Name, Last_Name from OwnershipContract 
    join Patron on OwnershipContract.Patron_ID = Patron.Patron_ID)
Select * from contracts where Patron_ID = 101;

-- with 
--     merged(Title, Year, Artist, Gallery, Location) AS (select Title, Year, Artist, Artwork.Gallery, Location from Artwork
--     join Gallery on Artwork.Gallery = Gallery.Gallery_Name)
-- select * from merged where Gallery = "National Gallery of Art";

-- with contracts(Title, Patron_id, ContractId, percent_share) AS
--     (select Artwork_Title, Patron_id, ContractId, percent_share from OwnershipContract where Artwork_Title = "An Interlude")
-- select distinct Title, First_Name, Last_Name, Patron.Patron_ID from Patron join contracts on contracts.Patron_ID = Patron.Patron_ID;
-- select Title, Year, Artist, Artwork.Gallery, Location from Artwork join Gallery on Artwork.Gallery = Gallery.Gallery_Name;
