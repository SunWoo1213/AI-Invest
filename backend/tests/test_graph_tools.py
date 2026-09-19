from app.services.graph import tools as graph_tools


def test_search_tool_returns_message_instead_of_raising(monkeypatch):
    class BrokenSearch:
        def invoke(self, query):
            raise RuntimeError("dns failure")

    monkeypatch.setattr(graph_tools, "_ddg_search", BrokenSearch())

    result = graph_tools.search_tool.invoke("gold price")

    assert result.startswith("Search unavailable (RuntimeError)")


def test_search_tool_passes_through_results(monkeypatch):
    class FakeSearch:
        def invoke(self, query):
            return f"results for {query}"

    monkeypatch.setattr(graph_tools, "_ddg_search", FakeSearch())

    assert graph_tools.search_tool.invoke("gold price") == "results for gold price"
