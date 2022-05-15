class Cache_URL(object):


    key = []
    url = []
    max_lenght = 10

    def __init__(self, max_lenght = 10):
        self.max_lenght = max_lenght


    def get_url(self,key):
        if key in self.key:
            n = self.key.index(key)
            self.key[0], self.key[n] = self.key[n], self.key[0]
            print(self)
            return self.url[self.key.index(key)]
        else:
            return None


    def save(self, key, url):
        self.key.insert(0, key)
        self.url.insert(0, url)
        if len(self.key) > self.max_lenght:
            self.key = self.key[:self.max_lenght]
        print(self)
        return


    def __str__(self):
        info = ''
        for i in range(len(self.key)):
            info+=f'{self.key[i]} - {self.url[i][0][:20]}\n'
        return info