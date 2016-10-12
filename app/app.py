from config import BaseConfig
from flask import Flask
from flask import request, render_template
from functools import wraps
from SPARQLWrapper import SPARQLWrapper, JSON
from logging import DEBUG

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['DEBUG'] = True
app.logger.setLevel(DEBUG)

sparql_query_tpl = """
prefix map: <{base_uri}:{port}/resource/vocab/monuments_>
select ?name ?region ?ato ?address
where {{
filter isLiteral(?name && ?region && ?ato && ?address)

?monument map:address        ?address       ;
          map:ansid          ?ansid         ;
          map:ato            ?ato           ;
          map:condition      ?condition     ;
          map:dating         ?dating        ;
          map:id             ?id            ;
          map:monprotaction  ?monprotaction ;
          map:montype        ?montype       ;
          map:name           ?name          ;
          map:protactiondoc  ?protactiondoc ;
          map:region         ?region        .

}} limit {sparql_limit}"""

endpoint = 'http://rdfserver:{rdfserver_port}/sparql'.format(
    rdfserver_port=BaseConfig.RDFSERVER_PORT)

sparql = SPARQLWrapper(endpoint)
sparql_query = sparql_query_tpl.format(base_uri=BaseConfig.RDFSERVER_BASE_URI,
                                       port=BaseConfig.RDFSERVER_PORT,
                                       sparql_limit=BaseConfig.SPARQL_LIMIT)
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)

class Monument(object):
    def __init__(self, name, region, ato, address):
        self.name = name['value']
        self.region = region['value']
        self.ato = ato['value']
        self.address = address['value']
        self.fullladdress = ", ".join((self.region, self.ato, self.address))


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def log(msg, level=DEBUG):
    app.logger.log(level, msg)


@app.route('/', methods=['GET', 'POST'])
@templated('index.html')
def index():
    monuments = []
    city = request.form.get('city', None)
    if city:
        results = sparql.query().convert()

        monuments = [Monument(**result)
                     for result in results["results"]["bindings"]
                     if city in result['ato']['value']
                     ]

    return dict(city=city, monuments=monuments)


if __name__ == '__main__':
    app.run()
