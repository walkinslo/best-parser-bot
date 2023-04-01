import requests

class Rule34:

    
    def __init__(self, url, limit, tags):
        self.url = url
        self.limit = limit
        self.tags = tags

        self.payload = {
            'limit': f'{self.limit}',
            'tags': f'{self.tags}',
            'json': '1'
        }
    
    
    def request(self):

        try:
            request = requests.get(self.url, params = self.payload) 
            response = request.json()
            urls = []
            for i in response:
                if 'sample_url' in i:
                    urls.append(i['sample_url'])
        
            return urls
        
        except Exception:
            urls = []
            return urls


