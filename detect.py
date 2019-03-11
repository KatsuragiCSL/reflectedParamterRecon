import re, requests, json, os, argparse

#arparse part

parser = argparse.ArgumentParser()

parser.add_argument('domain', help = 'domain to be crawled')
parser.add_argument('-o', help = 'output file, default = $domain.txt')

args = parser.parse_args()

#argparse part end

links = []
out = ''
indexes = ['CC-MAIN-2019-09','CC-MAIN-2019-04','CC-MAIN-2018-51','CC-MAIN-2018-47','CC-MAIN-2018-43','CC-MAIN-2018-39','CC-MAIN-2018-34','CC-MAIN-2018-30']

#get links for one index

def getLink(index):
    global links
    global out
    data = requests.get('http://index.commoncrawl.org/' + index + '-index?url=*.' + args.domain + '&output=json')
    
    data = data.text.split('\n')
    for entry in data:
        #ignore empty strings
        if entry:
            link = json.loads(entry)['url']
            if link not in links:
                out = out + (link + '\n')

#get links for all index

for index in indexes:
    getLink(index)

if out:
    if args.o:
        path = os.path.abspath(args.out)
        result = open(path, 'w')
        output = str(args.o)
    else:
        result = open('./' + args.domain + '.txt', 'w')
        output = str(args.domain + '.txt')
    result.write(out)


#test for url with strange get parameters

def changeValue(param):
    value = param.split("=")
    value[-1] = "123Test321"
    return '='.join(value)

for l in out.split("\n"):
    regex = r"\?[a-zA-Z0-9]*=.+"
    entry = re.findall(regex, l)
    if len(entry) > 0:
        print("Testing url: " + l)
        params = ''.join(entry).split("&")
        params = list(map(changeValue, params))
        entry = '&'.join(params)

        #fetch the redacted url
        url = re.sub(regex, entry, l)
        test = requests.get(l).text
        #check if value reflected
        reflected = re.search("123Test321", test)
        if reflected:
            print(l + "has reflected parameter.")
        
