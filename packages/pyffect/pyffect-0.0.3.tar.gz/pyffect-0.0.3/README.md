# Pyffect

Get inspiration from https://github.com/MaT1g3R/option and Scala type system

Try to support `mypy` type annotation.

You can use following types from this library
- Option
- Some
- NONE
- Either
- Left 
- Right
- Unit

### Option Type Usage
```python
from pyffect import Option, NONE, Some


def find_distance_from_sun(planet_name: str) -> Option[str]:
    planet_and_distance = {
        "Mercury": "0.39 AU",
        "Venus": "0.72 AU",
        "Earth": "1.00 AU",
        "Mars": "1.52 AU",
        "Jupiter": "5.20 AU",
        "Saturn": "9.54 AU",
        "Uranus": "19.20 AU",
        "Neptune": "30.06 AU",
    }

    if planet_name in planet_and_distance:
        return Some(planet_and_distance[planet_name])
    else:
        return NONE()


distanceFromJupiterOrNone: Option[str] = find_distance_from_sun("Jupiter")
assert distanceFromJupiterOrNone.is_defined
assert distanceFromJupiterOrNone.value == "5.20 AU"

distanceFromUnknownPlanetOrNone: Option[str] = find_distance_from_sun("Unknown Planet")
assert distanceFromUnknownPlanetOrNone.is_empty
assert distanceFromUnknownPlanetOrNone.get_or_else("Unknown Distance") == "Unknown Distance"
```

### Either Type Usage
```python
from pyffect import Either, Right, Left


def divide(numerator: int, denominator: int) -> Either[str, float]:
    try:
        value = numerator / denominator
        return Right(value)
    except:
        return Left('unable to perform the operation.')


firstValue: Either[str, float] = divide(5, 0)
assert firstValue.is_left
assert firstValue.left_value == 'unable to perform the operation.'
secondValue: Either[str, float] = divide(5, 2)
assert secondValue.is_right
assert secondValue.right_value == 2.5

```