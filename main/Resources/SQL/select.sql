SELECT *
FROM Objects INNER JOIN Shapes ON Objects.Shape = Shapes.Id;

SELECT *
FROM Symbols INNER JOIN Shapes ON Symbols.Symbol = Shapes.Id;