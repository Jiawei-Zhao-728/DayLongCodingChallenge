# SmartCache: Data Structure Overview

The `SmartCache` class uses several key data structures to efficiently manage cache entries, eviction, tagging, and priority-based logic. Here is an overview of each:

## 1. `self.cache`

- **Type:** `dict`
- **Purpose:** Stores the actual cached items and their metadata.
- **Structure:**
  - Key: `str` (the cache key)
  - Value: `tuple` of `(value, size, priority, tags)`
    - `value`: The cached value (any type)
    - `size`: Integer size of the item (for eviction calculations)
    - `priority`: Integer priority (lower = evicted first)
    - `tags`: List of strings (for tag-based invalidation)
- **Example:**
  ```python
  {
    'user1': ('profile_data', 3, 2, ['user', 'profile']),
    'img42': ('image_bytes', 5, 1, ['image', 'gallery'])
  }
  ```

## 2. `self.usage_order`

- **Type:** `OrderedDict`
- **Purpose:** Tracks the Least Recently Used (LRU) order of cache keys.
- **Structure:**
  - Key: `str` (cache key)
  - Value: `None` (only the order matters)
- **Behavior:**
  - Most recently used keys are moved to the end.
  - The first key is the least recently used.
- **Example:**
  ```python
  OrderedDict([('user1', None), ('img42', None), ('user2', None)])
  # 'user1' is LRU, 'user2' is MRU
  ```

## 3. `self.tag_map`

- **Type:** `defaultdict(set)`
- **Purpose:** Maps tags to sets of cache keys for efficient tag-based invalidation.
- **Structure:**
  - Key: `str` (tag)
  - Value: `set` of cache keys
- **Example:**
  ```python
  {
    'user': {'user1', 'user2'},
    'profile': {'user1'},
    'image': {'img42'}
  }
  ```

## 4. `self.priority_map`

- **Type:** `defaultdict(OrderedDict)`
- **Purpose:** Groups cache keys by priority and tracks LRU order within each priority.
- **Structure:**
  - Key: `int` (priority)
  - Value: `OrderedDict` of cache keys (order = LRU within that priority)
- **Example:**
  ```python
  {
    1: OrderedDict([('img42', None)]),
    2: OrderedDict([('user1', None), ('user2', None)])
  }
  ```

---

These structures work together to provide fast lookups, efficient eviction, and flexible invalidation by tag or priority.
