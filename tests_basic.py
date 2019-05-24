
import ray
import unittest

from HelloRayActors import Counter


class HelloRayActorTests(unittest.TestCase):
    """
    Some basic test cases.
    """

    @classmethod
    def setUpClass(cls):
        # Initialize runtime environment
        ray.init()

    def test_increment(self):
        # Simple usage
        a1 = Counter.remote()

        result = ray.get(a1.get_value.remote())
        assert result == 0, "Initial Counter value should be zero"

        result = ray.get(a1.increment.remote())
        assert result == 1, "Counter value was incremented to 1"

        result = ray.get(a1.increment.remote())
        assert result == 2, "Counter value was incremented to 2"

        result = ray.get(a1.increment.remote())
        assert result == 3, "Counter value was incremented to 3"

    def test_two_counters(self):
        # Multiple Counters usage
        a1 = Counter.remote()
        a2 = Counter.remote()

        result = ray.get(a1.get_value.remote())
        assert result == 0, "Initial Counter #1 value should be zero"

        result = ray.get(a2.get_value.remote())
        assert result == 0, "Initial Counter #2 value should be zero"

        result = ray.get(a2.increment.remote())
        assert result == 1, "Counter #2 value was incremented to 1"

        result = ray.get(a2.increment.remote())
        assert result == 2, "Counter #2 value was incremented to 2"

        result = ray.get(a2.increment.remote())
        assert result == 3, "Counter #2 value was incremented to 3"

        result = ray.get(a1.increment.remote())
        assert result == 1, "Counter #1 value was incremented to 1"

        result = ray.get(a1.increment.remote())
        assert result == 2, "Counter #1 value was incremented to 2"


if __name__ == '__main__':
    unittest.main()
