import web
import random
import json
from operator import itemgetter

photos = json.load(open('photos.db'))

def photo_url(item, size='z'):
    return 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
            farm = item['farm'],
            server = item['server'],
            id = item['id'],
            secret = item['secret'],
            size = size)

urls = (
    '/', 'Index',
    '/ranks', 'Ranks'
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

class Ranks(object):
    def GET(self):
        def div(a, b):
            if b == 0:
                return a
            else:
                return a / float(b)

        p = json.load(open('photos.db'))
        ranked = []

        for i, photo in enumerate(p):
            score = div(photo['up'], photo['down'])
            photo['score'] = score
            if score > 0:
                ranked += [photo]
        sortedranked = sorted(ranked, key=itemgetter('score'), reverse=True)
        html = '''<html>
<style type="text/css">
body {
    background-color:#050505;
  }
</style>
'''
        for photo in sortedranked:
            html += '    <a href=\
"http://www.flickr.com/photos/96822206@N03/{imageid}">\
<img src="{thumb}"></a>\n'.format(imageid = photo['id'],
                                thumb = photo_url(photo, size='m'))
        return html + '</html>'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
