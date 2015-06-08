# Copyright 2012 John J. Trammell.
#
# This file is part of the Mpls-ethics software package.  Mpls-ethics
# is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Mpls-ethics is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mpls-ethics.  If not, see <http://www.gnu.org/licenses/>.

import os
import jinja2
import webapp2
import logging
import met
from met.order import view_order


class BaseView(webapp2.RequestHandler):
    """Base class for all MET (Minneapolis Ethics Training) view classes."""

    def viewpath(self):
        """Construct a view path relative to met.app.TEMPLATE_DIR."""
        return 'main.djt'

    def view_index(self):
        request_path = self.request.path[1:]
        i = view_order.index(request_path)
        return i

    def next(self):
        """Returns the alias to the next page."""
        try:
            i = self.view_index()
            if i < len(view_order):
                return view_order[i + 1]
        except:
            return None

    def previous(self):
        """Returns the alias to the previous page."""
        try:
            i = self.view_index()
            if i > 0:
                return view_order[i - 1]
        except:
            return None

    def jinja_environment(self):
        """Return the Jinja2 environment object"""
        return jinja2.Environment(
            loader = jinja2.FileSystemLoader(met.app.TEMPLATE_PATH),
            extensions = ['jinja2.ext.autoescape'],
            autoescape = True)

    def template(self):
        """Returns the filename of the template to view."""
        return 'main.djt'

    def get(self):
        """The default GET request handler."""
        template_values = {
            'next': self.next(),
            'previous': self.previous(),
            'show_prevnext': True,
        }

        tfile = self.viewpath(append=self.template())
        jtemplate = self.jinja_environment().get_template(tfile)
        self.response.write(jtemplate.render(template_values))

    def post(self):
        """Default POST action is to redirect to GET."""
        self.redirect(self.request.path)
