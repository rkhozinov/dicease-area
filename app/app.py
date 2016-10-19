from config import BaseConfig
import logging
from flask import Flask
from flask import request, render_template
from functools import wraps

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
console = logging.StreamHandler()
log = logging.getLogger("app")
log.addHandler(console)
log.setLevel(logging.DEBUG)

from models import *
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

@app.route('/', methods=['GET', 'POST'])
@templated('index.html')
def index():

    city="city"
    monuments=[]
    return dict(city=city, monuments=monuments)


if __name__ == '__main__':
    app.run()
