"""Optional web-search adapter. No search provider is mandatory."""
class WebSearchTool:
    def __init__(self,provider=None):self.provider=provider
    def search(self,query):
        if not self.provider:return {"query":query,"results":[],"status":"not_configured"}
        return self.provider(query)
