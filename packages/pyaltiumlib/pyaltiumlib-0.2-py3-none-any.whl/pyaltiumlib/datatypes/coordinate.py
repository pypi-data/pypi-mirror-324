import math

# =============================================================================
#     Single Coordinate
# =============================================================================   

class Coordinate:
    def __init__(self, value):
        self.value = value
        
    @classmethod
    def parse_dpx(cls, key, data, scale=1.0):        
        num = int(data.get(key, 0))
        frac = int(data.get(key + "_frac", 0))
        
        coord = (num * 10.0 + frac / 10000.0)
        
        return cls( scale * coord / 10 )
 
    @classmethod
    def parse_bin(cls, x_bytes, scale=1.0):
        x = int.from_bytes(x_bytes, byteorder="little", signed=True)
        
        return cls( scale * x / 10000.0 )
       
    def __repr__(self):
        return f"{self.value}"       

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

# ================== Math Functions =========================================
    
    def __abs__(self):
        return abs( int(self.value) )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return Coordinate(self.value / other)
        elif isinstance(other, Coordinate):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return Coordinate(self.value / other.value)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value * other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value * other.value)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value + other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value + other.value)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.value - other)
        elif isinstance(other, Coordinate):
            return Coordinate(self.value - other.value)
        return NotImplemented

    def __rtruediv__(self, other):
        return self.__div__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def __lt__(self, other):
        if isinstance(other, Coordinate):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Coordinate):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
  
# =============================================================================
#     2D Coordinate Point
# =============================================================================   

class CoordinatePoint:
    def __init__(self, x, y):
        if not isinstance(x, Coordinate):
            x = Coordinate(x)
        if not isinstance(y, Coordinate):
            y = Coordinate(y)
            
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"({self.x};{self.y})" 
    
    def to_int(self):
        return CoordinatePoint( int(self.x), int(self.y))

    def to_int_tuple(self):
        return ( int(self.x), int(self.y))
    
    def expand(self, size):
        if isinstance(size, (int, float)):
            return CoordinatePoint(self.x + size, self.y + size)
        if isinstance(size, (int, Coordinate)):
            return CoordinatePoint(self.x + size.value, self.y - size.value)
        
    def rotate(self, center, angle):
        
            theta = math.radians(angle)
            x_rel = self.x - center.x
            y_rel = self.y - center.y
    
            x_rot = x_rel * math.cos(theta) - y_rel * math.sin(theta)
            y_rot = x_rel * math.sin(theta) + y_rel * math.cos(theta)
    
            self.x = x_rot + center.x
            self.y = y_rot + center.y
            return self

    def offset(self, offset_x, offset_y):
        
            self.x = self.x + offset_x
            self.y = self.y + offset_y
            return self
    
    def copy(self):
        return CoordinatePoint(self.x, self.y)

# ================== Math Functions =========================================

    def __abs__(self):
        return CoordinatePoint( abs(self.x), abs(self.y))
    
    
    def __add__(self, other):
        if isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return CoordinatePoint(self.x / other, self.y / other)
        elif isinstance(other, Coordinate):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return  CoordinatePoint(self.x / other.x, self.y / other.y)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return CoordinatePoint(self.x * other, self.y * other)
        elif isinstance(other, CoordinatePoint):
            return CoordinatePoint(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return self.__sub__(other)

