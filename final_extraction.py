from inital_search_results import page_extractor , llm_respond_for_link
from simplesearc import single_search

def final_process(queries):
    final_result=[]
    for query in queries:
        results=single_search(query)
        link=results['organic'][0]['link']
        result=llm_respond_for_link(query,link)
        final_result.append(result)
    return final_result
