from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

# DuckDuckGo 검색은 외부 서비스라 실패할 수 있다(차단·DNS·라이브러리 백엔드 변경 등).
# 예외가 에이전트 밖으로 새면 리포트 파이프라인 전체가 중단되므로, 실패는 문자열로 돌려주고
# 에이전트가 이미 수집된 데이터만으로 계속 진행하게 한다.
_ddg_search = DuckDuckGoSearchResults()


@tool("search_tool")
def search_tool(query: str) -> str:
    """A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events or look up specific facts on the internet. Input should be a search query."""
    try:
        return _ddg_search.invoke(query)
    except Exception as exc:  # noqa: BLE001 - 외부 검색 실패는 모두 같은 방식으로 처리한다
        return (
            f"Search unavailable ({type(exc).__name__}). "
            "Do not guess; use only the market data already provided."
        )

@tool
def calculator_tool(expression: str) -> str:
    """Calculate the result of a mathematical expression. Input the mathematical formula as a string (e.g. '150 * 1.2')."""
    try:
        # Warning: eval is used here simply for the clone scope. In production, use numexpr or ast.literal_eval.
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression."
        
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error computing expression: {e}"

tools = [search_tool, calculator_tool]
