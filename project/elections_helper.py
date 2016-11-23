import pymongo
from pymongo import MongoClient
from plotly.offline import plot
import pprint

def setup_mongo_client(properties_file='db.properties', db_url='mongodb://%s:%s@ds161487.mlab.com:61487/election_tweets'):
    properties = dict(line.strip().split('=') 
          for line in open(properties_file)
          if not line.startswith('#') and not line.startswith('\n'))

    uri = db_url % (properties['username'], properties['password'])
    client = MongoClient(uri)
    
    return client


def print_mongo_results(coll):
    for res in coll:
        pprint.pprint(res)


def get_figure(data, title, xaxis, yaxis):
    layout = dict(title=title,
                  xaxis=dict(title=xaxis),
                  yaxis=dict(title=yaxis),
                  )

    # If not a list, need to put in a list for plotly
    if not isinstance(data, list):
        data = [data]

    fig = dict(data=data, layout=layout)

    return fig


def save_plot_as_html(figure, filename):
    return plot(figure, filename=filename)


def save_plot_as_div(figure, include_plotlyjs=False, filename=None):
    div_content = plot(figure, include_plotlyjs=include_plotlyjs, output_type='div')

    # Save div to file
    if filename:
        with open(filename, 'w') as f:
            f.write(div_content)
    else:
        # Return content if not
        return div_content
