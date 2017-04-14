CREATE TABLE Cuboids
(
    Id INTEGER PRIMARY KEY,
    Height INTEGER,
    Width INTEGER,
    Depth INTEGER,
    Color INTEGER
);

CREATE TABLE Spheres
(
    Id INTEGER PRIMARY KEY,
    Size INTEGER,
    Color INTEGER
);

CREATE TABLE Objects
(
    Id INTEGER PRIMARY KEY,
    Cuboid INTEGER,
    Sphere INTEGER,
    FOREIGN KEY (Cuboid) REFERENCES Cuboids(Id),
    FOREIGN KEY (Sphere) REFERENCES Spheres(Id),
    CONSTRAINT ck_OnlyOne CHECK((Cuboid IS NULL AND Sphere IS NOT NULL) OR (Cuboid IS NOT NULL AND Sphere IS NULL))
);
