# -*- coding: utf-8 -*-
class OutFormatMiddleware(object): 
    """
    OutFormat
    """
    def __init__(self):
        self.format = ""
        self.varname = ""        

    def process_request(self, request):
        self.format = request.GET.get("format","")
        self.varname = request.GET.get("varname","")
        
    def process_response(self, request, response):
        if response.status_code != 200:
            return response
        if self.format == "jsvar":
            #varname = self.varname
            #content = response.content
            response.content = "var "+self.varname+" = "+response.content.decode("utf-8")
            response['Content-Length'] = str(len(response.content))
            return response
        elif self.format == "jsonp":
            import json
            response.content = json.dumps(json.loads(response.content),sort_keys=True, ensure_ascii = False, indent=4)
            response['Content-Length'] = str(len(response.content))
            return response
        return response

