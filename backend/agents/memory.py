class MemoryAgent:
    def recall(self,query,memory_manager):
        return memory_manager.search(query)
