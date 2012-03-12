import simplejson


def search(elements):
    result = [] 
    out_res = {}    
    for element in elements:
        result.append({'name':element.name,
                        'id':element.id})                
    out_res['counts'] = len(result)
    out_res['names'] = result    
    out_json = simplejson.dumps(out_res) 
    return out_json