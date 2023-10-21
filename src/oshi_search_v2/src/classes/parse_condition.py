from .interfaces.oshi_search_condition import OshiSearchCondition

def parse_json_file(file):
    return [
        OshiSearchCondition(
            id=idx,
            name=t["name"],
            keywords=t["keywords"],
            success=t["success"],
            error=t["error"],
        ) for idx, t in enumerate(file)
    ]
