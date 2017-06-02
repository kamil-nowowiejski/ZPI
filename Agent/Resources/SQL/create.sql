CREATE TABLE Shapes
(
    Id INTEGER PRIMARY KEY,
    Type INTEGER,
    Width INTEGER,
    Height INTEGER,
    Color INTEGER,
    Pattern INTEGER,
    PatternColor INTEGER
);

CREATE TABLE Symbols
(
    Shape INTEGER NOT NULL,
    Symbol INTEGER NOT NULL,
    PRIMARY KEY(Shape, Symbol),
    FOREIGN KEY (Shape) REFERENCES Shapes(Id),
    FOREIGN KEY (Symbol) REFERENCES Shapes(Id)
);

CREATE TABLE CombinedObjects
(
    Id INTEGER PRIMARY KEY,
    Type INTEGER,
    Width INTEGER,
    Height INTEGER
);

CREATE TABLE Objects
(
    Id INTEGER PRIMARY KEY,
    Shape INTEGER,
    CombinedObject INTEGER,
    FOREIGN KEY (Shape) REFERENCES Shapes(Id),
    FOREIGN KEY (CombinedObject) REFERENCES CombinedObjects(Id)
);

CREATE TABLE CombinedObjectsParts
(
  CombinedObjectId INTEGER,
  BasicPartObjectId INTEGER,
  PRIMARY KEY (CombinedObjectId, BasicPartObjectId),
  FOREIGN KEY (CombinedObjectId) REFERENCES CombinedObjects(Id),
  FOREIGN KEY (BasicPartObjectId) REFERENCES Objects(Id)

);