# 🧠 DayLongCodingChallenge

A collection of advanced coding challenges that blend technical interview-style questions with real-world software engineering design. Each challenge is designed to take a few hours to a full day, depending on the depth of implementation.

## 📁 Projects

### EP1: Feature-Aware Caching System 🚀

**Status**: ✅ **COMPLETED** - All tests passing (19/19)

A sophisticated caching system implementation that demonstrates advanced data structure design and algorithmic thinking.

#### 🎯 Key Features

- **Size-based Eviction**: Total cache size cannot exceed `max_size`
- **Tagging System**: Group cached items with tags for bulk operations
- **Priority-based Eviction**: Lower priority items evicted first
- **LRU within Priority**: Least Recently Used strategy within same priority levels
- **Partial Invalidation**: Invalidate items by tag or individual keys
- **Comprehensive Testing**: 19 unit tests covering all edge cases

#### 🏗️ Architecture

The implementation uses four core data structures working together:

1. **`cache`** (dict): Stores items with metadata `(value, size, priority, tags)`
2. **`usage_order`** (OrderedDict): Tracks LRU order across all items
3. **`tag_map`** (defaultdict(set)): Maps tags to sets of keys for fast invalidation
4. **`priority_map`** (defaultdict(OrderedDict)): Groups keys by priority with LRU tracking

#### 📊 Performance Characteristics

- **Time Complexity**:
  - Get/Set: O(1) average case
  - Eviction: O(k) where k is number of priority levels
  - Tag invalidation: O(n) where n is items with that tag
- **Space Complexity**: O(n) where n is number of cached items

#### 🧪 Example Usage

```python
from main import SmartCache

# Create cache with max size 5
cache = SmartCache(max_size=5)

# Add items with different priorities and tags
cache.put("a", "apple", size=2, tags=["fruit"], priority=1)
cache.put("b", "banana", size=2, tags=["fruit"], priority=2)
cache.put("c", "carrot", size=2, tags=["vegetable"], priority=1)

# "a" gets evicted (lower priority) to make room
print(cache.get("a"))  # None
print(cache.get("b"))  # "banana"

# Invalidate all fruit items
cache.invalidate_tag("fruit")
print(cache.get("b"))  # None
print(cache.get("c"))  # "carrot"
```

#### 🧪 Running Tests

```bash
cd "EP1_Feature-Aware Caching System"
python -m pytest test_smart_cache.py -v
```

**Test Results**: ✅ All 19 tests passing

#### 📋 Test Coverage

- ✅ Basic put/get operations
- ✅ Priority-based eviction
- ✅ LRU within same priority
- ✅ Tag-based invalidation
- ✅ Size constraints and eviction
- ✅ Edge cases (empty cache, nonexistent keys/tags)
- ✅ Stress testing with complex scenarios
- ✅ Update existing keys with new metadata

#### 🎯 Challenge Requirements Met

- ✅ **Core Features**: Size eviction, tagging, priority-based eviction, LRU
- ✅ **Class Interface**: All required methods implemented
- ✅ **Unit Tests**: 19 comprehensive tests (exceeds 5 minimum)
- ✅ **Data Structures**: Proper use of `OrderedDict`, `defaultdict`
- ✅ **Code Quality**: Readable, modular, well-documented

#### 🔧 Technical Implementation Details

The solution elegantly handles complex scenarios:

1. **Eviction Strategy**: Iterates through priorities from lowest to highest, using LRU within each priority level
2. **Tag Management**: Automatically cleans up empty tag sets and handles multi-tag items
3. **Priority Updates**: Efficiently moves items between priority levels when updated
4. **Memory Management**: Tracks total size and prevents oversized items from being added

#### 🚀 Future Enhancements

While the core challenge is complete, potential extensions include:

- TTL (Time-to-Live) expiration
- Thread safety with `threading.Lock`
- Flask API interface
- Persistence to disk
- Performance benchmarking

---

## 🎯 About This Repository

This repository contains carefully crafted coding challenges that test:

- **System Design**: Architecture decisions and trade-offs
- **Algorithm Design**: Efficient data structure usage
- **Code Quality**: Readability, maintainability, and testing
- **Problem Solving**: Breaking down complex requirements

Each challenge is designed to be completed in a day-long coding session, making them perfect for:

- Technical interview preparation
- Learning new concepts
- Improving coding skills
- Building portfolio projects

## 🛠️ Technology Stack

- **Language**: Python 3.12+
- **Testing**: pytest
- **Data Structures**: collections.OrderedDict, collections.defaultdict
- **Type Hints**: Full type annotation support

## 📝 License

This project is open source and available under the MIT License.

---

_Built with ❤️ for the coding community_
