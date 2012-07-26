import sqlite3
import pyes

es = pyes.ES(['localhost:9200'])
db = sqlite3.connect('devdata.sqlite')
cur = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()
cur.execute('SELECT * from trefwoorden ORDER BY idtref')

idx = batch = 0
for trefwoord in cur:        
    cur2.execute('SELECT betvar.meaningvar, boeken.* FROM bronnen, betvar, boeken ' +
    'WHERE bronnen.trefnum = ? AND bronnen.idbronnen = betvar.bronid AND boeken.idboeken = bronnen.boekid', 
    (trefwoord[5],))

    citaten = cur2.fetchall()
    body = []
    for c in citaten:
        citaat = {}
        for i, col in enumerate(['meaningvar', 'naam1', 'naam2', 'titel', 'boekcode', \
                    'boekaanduiding', 'uitgever', \
                    'plaats', 'jaartal', 'druk', 'fiction', 'lijstcode', 'genrecode', \
                    'idboeken', 'eerste_uitgave', 'annotator', 'sortorder']):
            citaat[col] = c[i]        
        body.append(citaat)

    cur3.execute('SELECT boeken.boekcode FROM bronnen, boeken WHERE bronnen.trefnum = ? '+
                 'AND bronnen.boekid = boeken.idboeken', (trefwoord[5],))
    boeken = [x[0] for x in cur3.fetchall()]


    data = {'trefwoord': trefwoord[0],
            'woordsoort': trefwoord[1],
            'taal': trefwoord[2],
            'sfeer': trefwoord[3],
            'citaten': body,
            'trefnum': trefwoord[5],
            'betekenis': trefwoord[4],
            'boeken': boeken,
            'trefwoord_a': trefwoord[0],
             }
    
    es.index(data, 'nedind', 'trefwoord', trefwoord[-1])
    idx = idx + 1
    batch += 1
    if batch > 1999:
        batch = 0
        print 'At', idx
        # break

print 'Now doing naslag'
cur.execute('SELECT * from naslag')
for naslag in cur.fetchall():
    data = {}
    data['naam1'] = naslag[0]
    data['naam2'] = naslag[1]
    data['naam3'] = naslag[2]
    data['titel'] = naslag[3]
    data['boekcode'] = naslag[4]
    data['uitgever'] = naslag[5]
    data['plaats'] = naslag[6]
    data['delen'] = naslag[7]
    data['jaartal'] = naslag[8]
    data['druk'] = naslag[9]
    data['herzien'] = naslag[10]
    data['vermeerder'] = naslag[11]
    data['sortorder'] = naslag[12]
    es.index(data, 'nedind', 'naslag', hash(naslag[4]))

print 'Now doing boeken'
cur.execute('SELECT * from boeken')
for boek in cur.fetchall():
    data = {
        'naam1': boek[0],
        'naam2': boek[1],
        'titel': boek[2],
        'boekcode': boek[3],
        'boekaanduiding': boek[4],
        'uitgever': boek[5],
        'plaats': boek[6],
        'jaartal': boek[7],
        'druk': boek[8],
        'fiction': boek[9],
        'lijstcode': boek[10],
        'genrecode': boek[11],
        'idboeken': boek[12],
        'eerste_uitgave': boek[13],
        'annotator': boek[14],
        'sortorder': boek[15]
    }
    es.index(data, 'nedind', 'boek', boek[12])
'''        
        
curl -XDELETE http://localhost:9200/nedind
curl -XPUT 'http://localhost:9200/nedind/' -d @es_settings.json 

curl -XPOST http://localhost:9200/nedind -d '{"index": 
  { "number_of_shards": 1,
    "analysis": {
       "filter": {
                "snowball": {
                    "type" : "snowball",
                    "language" : "Dutch"
                }
                 },
       "analyzer": { "a2" : {
                    "type":"custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "snowball"]
                    }
                  }
     }
  }
}
}'
curl -XPUT http://localhost:9200/nedind/trefwoord/_mapping -d '{
    "trefwoord" : {
      "properties" : {
            "body" : {"type" : "string", "store": false, "analyzer":"a2"},
            "trefwoord" : {"type" : "string", "store": false, "index": "analyzed"},
            "trefnum" : {"type" : "string", "store": false, "index": "not_analyzed"},
            "woordsoort" : {"type" : "string", "store": false, "index": "not_analyzed"},
            "taal" : {"type" : "string", "store": false, "index": "not_analyzed"},
            "sfeer" : {"type" : "string", "store": false, "index": "not_analyzed"}
        }
    }
}'

curl -XPUT http://localhost:9200/nedind/trefwoord/1 -d '{ "body": "Een twee drie en nu gaan wij kijken of het zoeken werkt.", "woordsoort": "aap" }'

curl -XGET localhost:9200/nedind/trefwoord/_search?q=body:een

'''