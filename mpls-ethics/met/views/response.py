# Copyright 2015 John J. Trammell.
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

from met.decorators import ordered
from met.model import Answer
from met.state import LearnerState
from met.views.base import BaseView


class Response(BaseView):

    @ordered
    def get(self, scenario_id):
        state = LearnerState(self.session)
        answer_id = state.last_answer_id(scenario_id) or "--none--"
        answer = Answer.get_by_key_name(answer_id)

        if answer is None:
            self.redirect("/%s/question" % scenario_id)
            return

        if state.is_completed(scenario_id):
            link_next = "/%s/disc1" % scenario_id
        else:
            link_next = "/%s/question" % scenario_id

        context = dict(next=self.next(),
                       previous=self.previous(),
                       state=state.as_string(),
                       show_prevnext=False,
                       correct=state.is_completed(scenario_id),
                       response=answer.response,
                       link_next=link_next)

        jt = self.jinja_environment().get_template('response.djt')
        self.response.write(jt.render(context))
