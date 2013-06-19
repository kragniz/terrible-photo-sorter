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
    '/', 'Index',
)

class Index(object):
    def GET(self):
        return '''<html>
<form name="one" action="" method="POST">
<input type="hidden" name="image" value="one">
<input type="image" src="{image1}" name="image">
</form>

<form name="two" action="" method="POST">
<input type="hidden" name="image" value="two">
<input type="image" src="{image2}" name="image">
</form>

</html>'''.format(image1 = photo_url(photos[34]),
                  image2 = photo_url(photos[1000]))

    def POST(self):
        s = web.input()
        print s.image
        return 'hello there my friend, you clicked image %s' % s.image

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
