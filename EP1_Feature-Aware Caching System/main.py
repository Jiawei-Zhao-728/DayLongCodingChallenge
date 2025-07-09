from collections import defaultdict, OrderedDict
from typing import Any, List, Optional


class SmartCache:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.current_total_size = 0

        # needs to be updated: 
        self.cache = dict()  # key -> (value, size, priority, tags)
        self.usage_order = OrderedDict()  # key -> None, tracks LRU
        self.tag_map = defaultdict(set)  # tag -> set of keys
        self.priority_map = defaultdict (OrderedDict) # priority -> OrderedDict of key -> None


    def _evict_items(self):
        while self.current_total_size > self.max_size:
            # evict the lowest priority first:
            print("\nEviction: current_total_size: ", self.current_total_size, "max_size: ", self.max_size)
            for priority in sorted(self.priority_map):
                print("\npriority: ", priority, 'Order', list(self.priority_map[priority].keys()))
                key_ordered = self.priority_map[priority]
                for key in list(key_ordered):
                    if key in self.cache:
                        _, size, _, tags = self.cache.pop(key)
                        self.current_total_size -= size
                        self.usage_order.pop(key, None)
                        self.priority_map[priority].pop(key, None)
                        if not self.priority_map[priority]:
                            del self.priority_map[priority]

                        if tags:
                            for tag in tags: 
                                self.tag_map[tag].discard(key)
                        print('\nEvicting key:', key, 'from priority:', priority)
                        break
                if self.current_total_size <= self.max_size:
                    break

    def put(self, key: str, value: Any, size: int = 1, tags: List[str] = None, priority: int = 1) -> None:
        """
        Add or update an item in the cache.

        If adding this item exceeds the max_size, evict items.
        Eviction strategy: lower-priority first, then LRU.
        """
        # TODO: Implement put logic including eviction, tag tracking, and updating LRU
        # check if size is greater than max_size: 
        if size > self.max_size:
            return None
        
        # check if it's already in the cache:
        if key in self.cache:
            # remove old tags: 
            old_tags = self.cache[key][3] if self.cache[key][3] else []
            if old_tags:
                for tag in old_tags:
                    self.tag_map[tag].discard(key)
                    if not self.tag_map[tag]:
                        del self.tag_map[tag]

            # update priority map: 
            old_priority = self.cache[key][2]
            if old_priority != priority:
                self.priority_map[old_priority].pop(key, None)
                if not self.priority_map[old_priority]:
                    del self.priority_map[old_priority]

            # update cache: 
            self.current_total_size -= self.cache[key][1]
            self.cache[key] = (value, size, priority, tags)
            self.current_total_size += size

            if self.current_total_size > self.max_size:
                self._evict_items()
            
            # update usage order: 
            self.usage_order.move_to_end(key)
            # update priority map: 
            self.priority_map[priority][key] = None
            self.priority_map[priority].move_to_end(key)
            # update tag map: 
            if tags:
                for tag in tags: 
                    self.tag_map[tag].add(key)
        else: 
            # now item is not in cache: 
            # add to cache:
            self.cache[key] = (value, size, priority, tags)
            self.current_total_size += size

            if self.current_total_size > self.max_size:
                self._evict_items()

            # add to usage order:
            self.usage_order[key] = None
            # update priority map:
            self.priority_map[priority][key] = None
            self.priority_map[priority].move_to_end(key)
            # update tag map: 
            if tags:
                for tag in tags: 
                    self.tag_map[tag].add(key)
            

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve an item and update its LRU status.
        """
        # TODO: Implement get logic
        if key in self.cache: 
            self.usage_order.move_to_end(key)
            priority = self.cache[key][2]
            self.priority_map[priority].move_to_end(key)
            return self.cache[key][0]
        return None

    def invalidate(self, key: str) -> None:
        """
        Remove an item from the cache.
        """
        # TODO: Remove from cache, usage_order, and tag_map
        if key not in self.cache:
            return None
        else: 
            # remove from cache
            _, size, _, tags = self.cache.pop(key)
            self.current_total_size -= size
            # remove from usage_order
            self.usage_order.pop(key, None)
            # remove tags
            if tags:
                for tag in tags:
                    self.tag_map[tag].discard(key)
                    if not self.tag_map[tag]:
                        del self.tag_map[tag]
            # remove from priority map
            for priority in self.priority_map:
                self.priority_map[priority].pop(key, None)
                if not self.priority_map[priority]:
                    del self.priority_map[priority]

    def invalidate_tag(self, tag: str) -> None:
        """
        Invalidate all keys associated with a tag.
        """
        # TODO: Remove all keys that share the given tag
        if tag not in self.tag_map:
            return None
        else:
            keys_to_remove = list(self.tag_map[tag])
            for key in keys_to_remove:
                self.invalidate(key)
            

    def current_size(self) -> int:
        """
        Return current total size of the cache.
        """
        return self.current_total_size
    
    def print_all_structure(self):
        print("---------------All Structure-----------------")
        print("Max size: \n", self.max_size)
        print("Current total size: \n", self.current_total_size)
        print("Cache: \n", self.cache)
        print("Usage order: \n", self.usage_order)
        print("Tag map: \n", self.tag_map)
        print("Priority map: \n", self.priority_map)
        print("----------------------------------------------")

