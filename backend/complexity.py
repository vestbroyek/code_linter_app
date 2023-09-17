import json
from radon.complexity import cc_visit, cc_rank
from radon.metrics import h_visit, h_visit_ast, mi_visit, mi_rank


def calculate_metrics(code_snippet: str) -> dict:
    # Calculate Cyclomatic Complexity
    cc_results = cc_visit(code_snippet)

    # Calculate Halstead Complexity Metrics
    h_results = h_visit(code_snippet)

    # Calculate Maintainability Index
    mi_results = mi_visit(code_snippet, 0)

    # Rank the code based on complexity
    cc_rank_results = cc_rank(cc_results[0].complexity)
    h_rank_results = h_visit_ast(h_results)
    mi_rank_results = mi_rank(mi_results)

    # Create a summary dictionary
    summary = {
        "CyclomaticComplexity": cc_results,
        "HalsteadMetrics": h_results,
        "MaintainabilityIndex": mi_results,
        "CyclomaticComplexityRank": cc_rank_results,
        "HalsteadRank": h_rank_results,
        "MaintainabilityIndexRank": mi_rank_results,
    }

    # Format the summary as JSON
    return json.dumps(summary, indent=4)
