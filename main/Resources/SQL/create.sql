CREATE TABLE Shapes
(
    Id INTEGER PRIMARY KEY,
    Type INTEGER,
    Height INTEGER,
    Width INTEGER,
    Color INTEGER
);

CREATE TABLE Symbols
(
    Shape INTEGER NOT NULL,
    Symbol INTEGER NOT NULL,
    PRIMARY KEY(Shape, Symbol),
    FOREIGN KEY (Shape) REFERENCES Shapes(Id),
    FOREIGN KEY (Symbol) REFERENCES Shapes(Id)
);

CREATE TABLE Objects
(
    Id INTEGER PRIMARY KEY,
    Shape INTEGER,
    FOREIGN KEY (Shape) REFERENCES Shapes(Id)
);
