import os
import logging
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from met import util
from met import content
from met import session

order = [
    'main',
    'intro1',
    'intro2',
    'over1',
    'over2',
    'topic1',
    'scenario/coi1',    # conflict of interest 1
    'scenario/coi2',    # conflict of interest 2
    'scenario/coi3',    # conflict of interest 3
    'scenario/coi4',    # conflict of interest 4
    'scenario/doi',     # disclosure of information
    'scenario/gifts',
    'reportline',
    'summary',
]

class MetView(webapp.RequestHandler):
    """Base class for all MET view classes."""

    view_dir = os.path.join(os.path.dirname(__file__), '../view')

    def main(self):
        """Returns the path to the 'main' view template."""
        return self.viewpath('main.djt')

    def viewpath(self,append=None):
        """Construct a view path."""
        if append:
            return os.path.join(self.view_dir, './' + append)
        return self.view_dir

    def next(self):
        """Returns the alias to the next page."""
        pass

    def previous(self):
        """Returns the alias to the previous page."""
        pass

    def template(self):
        """Returns the filename of the template to view."""
        return 'main.djt'

    def get(self):
        """The default GET request handler."""
        template_values = {
            'next': self.next(),
            'previous': self.previous(),
        }

        t = self.viewpath(append=self.template())
        self.response.out.write(template.render(t, template_values))

class Main(MetView):
    def get(self):
        path = self.viewpath(append='main.djt')
        session = self.getSession()
        try:
            session['timestamp'] += [ datetime.now() ]
        except:
            session['timestamp'] = []

        session['timestamp'] = session['timestamp'][0:3]
        self.response.out.write(template.render(path,locals()))

    post = get

Main.__bases__ += (session.SessionMixin,)


class BestGuess(MetView):
    """View class that displays the view closest to that requested."""

    def get(self):
        path = self.viewpath(append=self.template())
        self.response.out.write(template.render(path,{}))

    def template(self):
        """Return the view template that best matches the request."""
        if len(self.request.path) <= 1:
            return 'main.djt'
        if len(self.request.path) > 1:
            for t in self.list_templates():
                if self.request.path[1:] in t:
                    return t
            return 'main.djt'

    def list_templates(self):
        t = os.listdir(self.view_dir)
        t = [ x for x in t if x[0] != '.' ]
        return t

    post = get



class Scenario(MetView):

    def __init__(self):
        #self.scenario_id = scenario_id
        #logging.info("Scenario(%s)" % scenario_id)
        pass

    def get(self,scenario_id):
        if self.prerequisites():
            pass

        path = self.viewpath(append='question.djt')
        template_values = {
            'question': content.get_scenario(scenario_id),
        }
        self.response.out.write(template.render(path, template_values))

    def prerequisites(self):
        """Returns the prerequisites for showing this view."""
        return True

    def post(self,question_id):
        pass

Scenario.__bases__ += (session.SessionMixin,)

