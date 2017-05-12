from collections import namedtuple


class Position(namedtuple('Position', 'x, y')):
    def left(self, n):
        return self._replace(x=self.x - n)

    def up(self, n):
        return self._replace(y=self.y - n)

    def right(self, n):
        return self._replace(x=self.x + n)

    def down(self, n):
        return self._replace(y=self.y + n)

    def move(self, dx, dy):
        return self._replace(x=self.x + dx,
                             y=self.y + dy)


class ElementPosition(namedtuple('Relative', 'x1, y1, x2, y2')):
    @classmethod
    def fromWebElement(cls, element):
        """从 WebElement 创建 Relative 对象

        :type element: appium.webdriver.WebElement
        """
        location = element.location
        size = element.size

        x1 = location['x']
        y1 = location['y']
        width = size['width']
        height = size['height']

        x2 = x1 + width
        y2 = y1 + height

        return cls(x1, y1, x2, y2)

    @property
    def center(self):
        # noinspection PyTypeChecker
        return Position((self.x1 + self.x2) // 2,
                        (self.y1 + self.y2) // 2)

    def left(self, n):
        return Position(self.x1, self.center.y).left(n)

    def up(self, n):
        return Position(self.center.x, self.y1).up(n)

    def right(self, n):
        return Position(self.x2, self.center.y).right(n)

    def down(self, n):
        return Position(self.center.x, self.y2).down(n)

    def move(self, dx, dy):
        if dx < 0:
            x = self.x1
        elif dx > 0:
            x = self.x2
        else:
            x = self.center.x

        if dy < 0:
            y = self.y1
        elif dy > 0:
            y = self.y2
        else:
            y = self.center.y

        return Position(x, y).move(dx, dy)
