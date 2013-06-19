import web
import json

photos = json.load(open('photos.db'))
print photos[5]

def photo_url(item):
    return 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
            farm = item['farm'],
            server = item['server'],
            id = item['id'],
            secret = item['secret'],
            size = 'z')
print photo_url(photos[0])

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
