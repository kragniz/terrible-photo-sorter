import web
import random
import json

photos = json.load(open('photos.db'))

def photo_url(item):
    return 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
            farm = item['farm'],
            server = item['server'],
            id = item['id'],
            secret = item['secret'],
            size = 'z')

urls = (
    '/', 'Index',
)

class Index(object):
    def GET(self):
        imageOne = random.randint(0, len(photos) - 1)
        imageTwo = random.randint(0, len(photos) - 1)

        return '''<html>
<style type="text/css">
#centered {{
    margin-left: 100px ;
    margin-top: 50px ;
  }}

body {{
    background-color:#050505;
  }}
</style>

<div id="centered">
    <div style='float:left'>
        <form name="one" action="" method="POST">
            <input type="hidden" name="image" value="{oneid}">
            <input type="hidden" name="downimage" value="{twoid}">
            <input type="image" src="{image1}" name="image">
        </form>
    </div>

    <div>
        <form name="two" action="" method="POST">
            <input type="hidden" name="image" value="{twoid}">
            <input type="hidden" name="downimage" value="{oneid}">
            <input type="image" src="{image2}" name="image">
        </form>
    </div>
</div>

</html>'''.format(image1 = photo_url(photos[imageOne]),
                  image2 = photo_url(photos[imageTwo]),
                  oneid = imageOne,
                  twoid = imageTwo)

    def POST(self):
        s = web.input()
        print s.image, s.downimage
        photos[int(s.image)]['up'] = int(photos[int(s.image)]['up']) + 1
        photos[int(s.downimage)]['down'] = int(photos[int(s.downimage)]['down']) + 1
        with open('photos.db', 'w') as f:
            json.dump(photos, f,
                      sort_keys=True, indent=4, separators=(',', ': '))
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
