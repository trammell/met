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


class InvalidScenarioException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class InvalidAnswerException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class InvalidLearnerException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
