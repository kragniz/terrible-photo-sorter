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
            <input type="image" src="{image_one}" name="image">
        </form>
    </div>

    <div>
        <form name="two" action="" method="POST">
            <input type="hidden" name="image" value="{twoid}">
            <input type="hidden" name="downimage" value="{oneid}">
            <input type="image" src="{image_two}" name="image">
        </form>
    </div>
</div>

</html>'''.format(image_one = photo_url(photos[imageOne]),
                  image_two = photo_url(photos[imageTwo]),
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
        p = json.load(open('photos.db'))
        ranked = []
        for i, photo in enumerate(p):
            score = photo['up'] - photo['down']
            photo['score'] = score
            ranked += [photo]
        sortedranked = sorted(ranked, key=itemgetter('score'), reverse=True)
        html = '''<html>
<style type="text/css">
body {
    background-color:#050505;
  }

.box-thing {
  position: relative;
  background: #050505;
  padding: 10px;
  float: left;
  height: 240px;
  width: 240px;
}

img {
vertical-align:top;
}

.score {
  position:absolute;
  top:20px;
  left:20px;
  font-size: 2em;
  background: #AAAAAA;
  font-family: monospace;
}
</style>
'''
        for photo in sortedranked:
            html += '''
    <div class="box-thing">
        <a href="http://www.flickr.com/photos/96822206@N03/{imageid}"><img src="{thumb}"/></a>
        <div class="score">
            {score}
        </div>
    </div>'''.format(imageid = photo['id'],
           thumb = photo_url(photo, size='m'),
           score = photo['score'])
        return html + '</html>'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
