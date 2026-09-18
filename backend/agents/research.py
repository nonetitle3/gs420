class ResearchAgent:
    def research(self,query,search_tool=None):
        if search_tool:return search_tool(query)
        return {"query":query,"status":"no_search_tool_configured"}
