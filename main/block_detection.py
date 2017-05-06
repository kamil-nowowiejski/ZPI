from enums import Block
from enums import Shape


def recognise_block(shape1, shape2, shape3, shape4):
    if shape1 is shape2 is shape3 is shape4 is Shape.CIRCLE:
        return Block.BALL
    if shape1 is shape2 is shape3 is shape4 is Shape.SQUARE:
        return Block.CUBE
    if (((shape1 is shape3 is Shape.RECTANGLE) or (shape1 is shape3 is Shape.SQUARE)) and (
            shape2 is shape4 is Shape.CIRCLE)) or (
        ((shape2 is shape4 is Shape.RECTANGLE) or (shape2 is shape4 is Shape.SQUARE)) and (
            shape1 is shape3 is Shape.CIRCLE)):
        return Block.ROLLER
    if (shape1 is Shape.RECTANGLE or shape1 is Shape.SQUARE) and (
            shape2 is Shape.RECTANGLE or shape2 is Shape.SQUARE) and (
            shape3 is Shape.RECTANGLE or shape3 is Shape.SQUARE) and (
            shape4 is Shape.RECTANGLE or shape4 is Shape.SQUARE):
        return Block.CUBOID
    if ((shape1 is Shape.TRIANGLE) or (shape1 is Shape.EQUILATERAL_TRIANGLE) or (
        shape1 is Shape.ISOSCELES_TRIANGLE)) and (
            (shape2 is Shape.TRIANGLE) or (shape2 is Shape.EQUILATERAL_TRIANGLE) or (
            shape2 is Shape.ISOSCELES_TRIANGLE)) and (
            (shape3 is Shape.TRIANGLE) or (shape3 is Shape.EQUILATERAL_TRIANGLE) or (
            shape3 is Shape.ISOSCELES_TRIANGLE)) and (
            (shape4 is Shape.TRIANGLE) or (shape4 is Shape.EQUILATERAL_TRIANGLE) or (
            shape4 is Shape.ISOSCELES_TRIANGLE)):
        return Block.PYRAMID
    return Block.INVALID
