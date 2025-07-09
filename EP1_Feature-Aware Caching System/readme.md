

# 🧠 Day-long Python Coding Challenge

This challenge blends technical interview-style questions with real-world software engineering design. It should take a few hours to a full day, depending on depth of implementation.

---


# 🧠 SmartCache Challenge: Feature-Aware Caching System

You're tasked with building a sophisticated caching system with the following features:

1. **Eviction based on total size constraint** (e.g., total cache size cannot exceed `max_size`).
2. **Tagging support** for grouping cached items (e.g., `"user_123"`, `"fruit"`, etc.).
3. **Partial invalidation based on tags** (invalidate all items with a given tag).
4. **Priority-based eviction**:
   - Lower priority items are evicted first when space is needed.
   - Within the same-priority level, use **Least Recently Used (LRU)** strategy.

---

---

## 🚀 Class Signature

```python
class SmartCache:
    def __init__(self, max_size: int): ...

    def put(self, key: str, value: Any, size: int = 1, tags: List[str] = None, priority: int = 1) -> None: ...

    def get(self, key: str) -> Optional[Any]: ...

    def invalidate(self, key: str) -> None: ...

    def invalidate_tag(self, tag: str) -> None: ...

    def current_size(self) -> int: ...
```

---

## ✅ Bonus Challenges

- Write at least **5 unit tests** for your implementation.
- Add optional **TTL (time-to-live)** expiration.
- Add **thread safety** using `threading.Lock`.
- Add a simple **Flask API interface** if you’re done early.

Use Python standard libraries (`collections`, `time`, `threading`, etc.). You may optionally explore others.

## 🧪 Example

```python
cache = SmartCache(max_size=5)
cache.put("a", "apple", size=2, tags=["fruit"], priority=1)
cache.put("b", "banana", size=2, tags=["fruit"], priority=2)
cache.put("c", "carrot", size=2, tags=["vegetable"], priority=1)

# "a" should be evicted to make room, since it's lower priority
# Current cache should contain: "b" and "c"

print(cache.get("a"))  # None
print(cache.get("b"))  # "banana"
cache.invalidate_tag("vegetable")
print(cache.get("c"))  # None
```

## 📈 Bonus / Extension Ideas

- Add persistence (store cache to disk as JSON and reload)
- Implement TTL (time-to-live) per item and background cleanup
- Add thread-safety (if you’re up for some concurrency work)
- Expose a simple REST API using Flask to interact with the cache

## 🧠 Evaluation Criteria

- Correctness of eviction policy
- Code readability and modularity
- Proper use of data structures (`OrderedDict`, `defaultdict`, etc.)
- Testing coverage (write at least 5 unit tests)
- Optional: benchmarking / performance analysis