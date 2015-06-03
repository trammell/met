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
import webapp2
from met.order import view_order


class BaseView(webapp2.RequestHandler):
    """Base class for all MET (Minneapolis Ethics Training) view classes."""

    # Define a hardcoded relative path from this file to the views.  This
    # should be automated somehow!
    view_dir = os.path.join(os.path.dirname(__file__), '../../templates')

    def main(self):
        """Returns the path to the 'main' view template."""
        return self.viewpath('main.djt')

    def viewpath(self, append=None):
        """Construct a view path."""
        return os.path.normpath(os.path.join(self.view_dir, './' + append)) \
            if append else os.path.normpath(self.view_dir)

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

        t = self.viewpath(append=self.template())
        self.response.out.write(webapp2.template.render(t, template_values))

    def post(self):
        """Default POST action is to redirect to GET."""
        self.redirect(self.request.path)
