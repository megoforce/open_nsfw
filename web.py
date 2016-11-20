from flask import Flask
from flask import request
import urllib2
import urlparse, os, sys
import subprocess

app = Flask(__name__)

@app.route("/")
def hello():
    imageurl=request.args.get('url')
    path = urlparse.urlparse(imageurl).path
    ext = os.path.splitext(imageurl)[1]
#     sys.stdout("test."+ext)
    filename="test"+ext
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(imageurl, headers=hdr)

    response = urllib2.urlopen(req)
    with open(filename, 'wb') as outfile:
        outfile.write(response.read())
    cmd = ["/usr/bin/python","/workspace/classify_nsfw.py","--model_def","/workspace/nsfw_model/deploy.prototxt","--pretrained_model","/workspace/nsfw_model/resnet_50_1by2_nsfw.caffemodel",filename]
    # cmd = ["ls", " -l","/workspace"]
    p = subprocess.Popen(cmd, 
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdin=subprocess.PIPE)
    out,err = p.communicate()
    json="{success:true,score:"+out.replace("NSFW score: ","").strip()+"}"
    return json

if __name__ == "__main__":
    app.run()