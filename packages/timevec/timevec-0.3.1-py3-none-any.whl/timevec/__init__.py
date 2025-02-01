"""Time vector representation

Time has a periodic nature due to the rotation of the earth and the position of the sun.
This affects human behavior in various ways.

Seasonality ... periodicity in a year (seasonal distinction)
Daily periodicity ... periodicity in a day (distinction between day and night)
Day of the week ... periodicity in a week (distinction between weekdays and holidays)

When dealing with these, it is desirable to vectorize with periodicity in mind.
That is, at 23:59 on a given day, it is desirable that the value is close to 00:00 on the next day.
To achieve this, the time is represented as a combination of cos and sin."""

# https://packaging-guide.openastronomy.org/en/latest/advanced/versioning.html
from ._version import __version__

try:
    from . import builtin_math
except ImportError:
    pass

try:
    from . import numpy_datetime64
except ImportError:
    pass

try:
    from . import numpy
except ImportError:
    pass


__all__ = ["builtin_math", "numpy_datetime64", "numpy", "__version__"]
