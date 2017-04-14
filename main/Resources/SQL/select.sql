SELECT *
FROM Objects INNER JOIN Cuboids ON Objects.Cuboid = Cuboids.Id;

SELECT *
FROM Objects INNER JOIN Spheres ON Objects.Sphere = Spheres.Id;