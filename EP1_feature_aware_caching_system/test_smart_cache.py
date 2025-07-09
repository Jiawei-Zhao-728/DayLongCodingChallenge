import unittest
from main import SmartCache


class TestSmartCache(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh cache instance before each test."""
        pass
    
    def test_basic_put_and_get(self):
        """Test basic put and get operations."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=2)
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.current_size(), 2)
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        cache = SmartCache(max_size=10)
        self.assertIsNone(cache.get("nonexistent"))
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=2)
        cache.put("key1", "new_value", size=3)
        self.assertEqual(cache.get("key1"), "new_value")
        self.assertEqual(cache.current_size(), 3)
    
    def test_size_eviction(self):
        """Test eviction when cache exceeds max_size."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=4)
        cache.put("key2", "value2", size=4)
        cache.put("key3", "value3", size=4)  # This should trigger eviction
        
        # The first item should be evicted (LRU)
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key3"), "value3")
        self.assertEqual(cache.current_size(), 8)
    
    def test_priority_based_eviction(self):
        """Test that lower priority items are evicted first, and within the same priority, LRU is used."""
        # Set max_size so that not all items can fit
        cache = SmartCache(max_size=7)
        # Add two low priority items (total size = 3 + 4 = 7)
        cache.put("low1", "value1", size=3, priority=1)
        cache.put("low2", "value2", size=4, priority=1)
        # Add a medium and a high priority item (should trigger eviction)
        cache.put("medium", "value3", size=3, priority=2)
        cache.put("high", "value4", size=3, priority=3)

        # After all puts, only the highest priority items that fit should remain
        # The two low priority items should be evicted first to make room
        self.assertIsNone(cache.get("low1"))
        self.assertIsNone(cache.get("low2"))
        self.assertEqual(cache.get("medium"), "value3")
        self.assertEqual(cache.get("high"), "value4")
    
    def test_lru_within_same_priority(self):
        """Test LRU eviction within the same priority level."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=2, priority=1)
        cache.put("key2", "value2", size=2, priority=1)
        cache.put("key3", "value3", size=2, priority=1)
        cache.put("key4", "value4", size=2, priority=1)
        cache.put("key5", "value5", size=2, priority=1)
        cache.put("key6", "value6", size=2, priority=1)  # Should trigger eviction
        
        # The least recently used (first added) should be evicted
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.get("key6"), "value6")
    
    def test_get_updates_lru(self):
        """Test that getting an item updates its LRU status and triggers eviction when max_size is exceeded."""
        cache = SmartCache(max_size=6)
        cache.put("key1", "value1", size=2, priority=1)
        cache.put("key2", "value2", size=2, priority=1)
        cache.put("key3", "value3", size=2, priority=1)


        # Access key1 to make it most recently used
        cache.get("key1")

        # Add another item to trigger eviction
        cache.put("key4", "value4", size=2, priority=1)

        # key2 should be evicted (not key1 since it was recently accessed)
        self.assertIsNone(cache.get("key2"))
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.get("key3"), "value3")
        self.assertEqual(cache.get("key4"), "value4")
    
    def test_tagging_functionality(self):
        """Test that items can be tagged and retrieved."""
        cache = SmartCache(max_size=10)
        cache.put("apple", "red_apple", size=2, tags=["fruit", "red"])
        cache.put("banana", "yellow_banana", size=2, tags=["fruit", "yellow"])
        cache.put("carrot", "orange_carrot", size=2, tags=["vegetable", "orange"])
        
        # All items should be retrievable
        self.assertEqual(cache.get("apple"), "red_apple")
        self.assertEqual(cache.get("banana"), "yellow_banana")
        self.assertEqual(cache.get("carrot"), "orange_carrot")
    
    def test_invalidate_single_key(self):
        """Test invalidating a single key."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=2, tags=["tag1"])
        cache.put("key2", "value2", size=2, tags=["tag1", "tag2"])
        
        cache.invalidate("key1")
        
        self.assertIsNone(cache.get("key1"))
        self.assertEqual(cache.get("key2"), "value2")
        self.assertEqual(cache.current_size(), 2)
    
    def test_invalidate_tag(self):
        """Test invalidating all items with a specific tag."""
        cache = SmartCache(max_size=10)
        cache.put("apple", "red_apple", size=2, tags=["fruit", "red"])
        cache.put("banana", "yellow_banana", size=2, tags=["fruit", "yellow"])
        cache.put("carrot", "orange_carrot", size=2, tags=["vegetable", "orange"])
        
        # Invalidate all fruit items
        cache.invalidate_tag("fruit")
        
        # Fruit items should be gone
        self.assertIsNone(cache.get("apple"))
        self.assertIsNone(cache.get("banana"))
        # Vegetable item should remain
        self.assertEqual(cache.get("carrot"), "orange_carrot")
        self.assertEqual(cache.current_size(), 2)
    
    def test_invalidate_nonexistent_tag(self):
        """Test invalidating a tag that doesn't exist."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=2, tags=["tag1"])
        
        # Should not raise an error
        cache.invalidate_tag("nonexistent_tag")
        
        # Original item should still exist
        self.assertEqual(cache.get("key1"), "value1")
    
    def test_invalidate_nonexistent_key(self):
        """Test invalidating a key that doesn't exist."""
        cache = SmartCache(max_size=10)
        # Should not raise an error
        cache.invalidate("nonexistent_key")
        self.assertEqual(cache.current_size(), 0)
    
    def test_empty_cache_operations(self):
        """Test operations on an empty cache."""
        cache = SmartCache(max_size=10)
        self.assertEqual(cache.current_size(), 0)
        self.assertIsNone(cache.get("any_key"))
        cache.invalidate("any_key")  # Should not raise error
        cache.invalidate_tag("any_tag")  # Should not raise error
    
    def test_zero_size_item(self):
        """Test adding an item with zero size."""
        cache = SmartCache(max_size=10)
        cache.put("key1", "value1", size=0)
        self.assertEqual(cache.get("key1"), "value1")
        self.assertEqual(cache.current_size(), 0)
    
    def test_large_item_eviction(self):
        """Test eviction when a single item is larger than max_size."""
        cache = SmartCache(max_size=10)
        # Try to add an item larger than max_size
        cache.put("large_item", "value", size=15)
        
        # The item should not be added since it exceeds max_size
        self.assertIsNone(cache.get("large_item"))
        self.assertEqual(cache.current_size(), 0)
    
    def test_multiple_tags_invalidation(self):
        """Test that items with multiple tags are properly handled during invalidation."""
        cache = SmartCache(max_size=10)
        cache.put("item1", "value1", size=2, tags=["tag1", "tag2"])
        cache.put("item2", "value2", size=2, tags=["tag2", "tag3"])
        cache.put("item3", "value3", size=2, tags=["tag1", "tag3"])
        
        # Invalidate tag2
        cache.invalidate_tag("tag2")
        
        # Items with tag2 should be gone
        self.assertIsNone(cache.get("item1"))
        self.assertIsNone(cache.get("item2"))
        # Item3 should remain (only has tag1 and tag3)
        self.assertEqual(cache.get("item3"), "value3")
    
    def test_priority_and_lru_combination(self):
        """Test complex scenario with priority and LRU working together."""
        cache = SmartCache(max_size=8)
        cache.put("low1", "value1", size=2, priority=1)
        cache.put("high1", "value2", size=2, priority=3)
        cache.put("low2", "value3", size=2, priority=1)
        cache.put("medium1", "value4", size=2, priority=2)
        
        # Access low1 to make it more recently used than low2
        cache.get("low1")
        
        # Add another item to trigger eviction
        cache.put("low3", "value5", size=2, priority=1)
        
        # low2 should be evicted (least recently used among low priority)
        self.assertIsNone(cache.get("low2"))
        self.assertEqual(cache.get("low1"), "value1")
        self.assertEqual(cache.get("high1"), "value2")
        self.assertEqual(cache.get("medium1"), "value4")
        self.assertEqual(cache.get("low3"), "value5")

    def test_put_behavior(self):
        """Extensive test of the put method including updates and tag handling."""
        cache = SmartCache(max_size=10)
        cache.put("a", "alpha", size=2, tags=["x"], priority=1)
        self.assertEqual(cache.get("a"), "alpha")
        self.assertEqual(cache.current_size(), 2)
        self.assertIn("a", cache.usage_order)
        self.assertIn("a", cache.priority_map[1])
        self.assertIn("a", cache.tag_map["x"])

        cache.put("b", "bravo", size=2, tags=["x", "y"], priority=2)
        self.assertEqual(cache.get("b"), "bravo")
        self.assertEqual(cache.current_size(), 4)
        self.assertIn("b", cache.usage_order)
        self.assertIn("b", cache.priority_map[2])
        self.assertIn("b", cache.tag_map["x"])
        self.assertIn("b", cache.tag_map["y"])

        cache.put("c", "charlie", size=7, tags=["z"], priority=1)
        self.assertLessEqual(cache.current_size(), 10)
        self.assertEqual(cache.get("c"), "charlie")
        self.assertIsNone(cache.get("a"))  # Should be evicted
        self.assertNotIn("a", cache.usage_order)
        self.assertNotIn("a", cache.priority_map[1])
        self.assertNotIn("a", cache.tag_map.get("x", set()))

        cache.put("b", "beta", size=1, tags=["y"], priority=2)
        self.assertEqual(cache.get("b"), "beta")
        self.assertLessEqual(cache.current_size(), 10)
        self.assertNotIn("b", cache.tag_map.get("x", set()))
        self.assertIn("b", cache.tag_map["y"])

    def test_heavy_stress_test(self):
        """Stress test: fill the cache, update, access, and invalidate under heavy load."""
        max_size = 100
        cache = SmartCache(max_size=max_size)
        num_items = 200
        # Add 200 items, each with size 1, alternating priorities and tags
        for i in range(num_items):
            key = f"key{i}"
            value = f"value{i}"
            size = 1
            priority = (i % 5) + 1  # Priorities 1-5
            tags = [f"tag{i%10}", f"group{i%3}"]
            cache.put(key, value, size=size, tags=tags, priority=priority)
        # The cache should not exceed max_size
        self.assertLessEqual(cache.current_size(), max_size)
        self.assertLessEqual(len(cache.cache), max_size)
        # Access some items to update LRU
        for i in range(50, 60):
            cache.get(f"key{i}")
        # Update some items
        for i in range(60, 70):
            cache.put(f"key{i}", f"new_value{i}", size=1, tags=["updated"], priority=2)
        # Invalidate a tag
        cache.invalidate_tag("tag5")
        # After invalidation, no key with tag5 should remain
        for k, v in cache.cache.items():
            tags = v[3]
            if tags:
                self.assertNotIn("tag5", tags)
        # The cache should still not exceed max_size
        self.assertLessEqual(cache.current_size(), max_size)
        self.assertLessEqual(len(cache.cache), max_size)


if __name__ == "__main__":
    unittest.main(verbosity=2)