__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2021 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

import uuid

try:
    from flask import session

    from dash.dependencies import Output, Input, State
except:
    pass

class CallbackManager(object):
    """This creates the appropriate Input, State and Output objects to wrap around Dash components. It abstracts away
    some of the complexity of Dash, by allowing the user simplify to specify the string of the dash component.

    It will then work out the dash type from the component name. Users need to be careful to name the Dash components
    with the correct names. For examples, all plots, must have 'plot' within their name.
    """

    def __init__(self, constants):
        self._constants = constants

    def input_callback(self, page, input):
        """Create input callbacks for Dash components, which can be used to trigger callbacks. We can have multiple
        input callbacks for methods.

        Parameters
        ----------
        page : str
            Name of the page (eg. 'magic-carpet')

        input : str (list)
            Dash components where we wish to add dash based input callbacks

        Returns
        -------
        dash.dependencies.Input (list)
        """
        if not (isinstance(input, list)):
            input = [input]

        return [Input(page + '-' + i.split(':')[0], self._find_type(i, input_output_state='input')) for i in input]

    def output_callback(self, page, output):
        """Create a output callback for a Dash component, which can be used to trigger callbacks. Note, that we can have multiple callbacks.

        Parameters
        ----------
        page : str
            Name of the page (eg. 'magic-carpet')

        output : str
            Dash component where we wish to add dash based output callbacks

        Returns
        -------
        dash.dependencies.Output (list)
        """

        if not (isinstance(output, list)):
            return Output(page + '-' + output.split(':')[0], self._find_type(output, input_output_state='output'))

        return [Output(page + '-' + out.split(':')[0], self._find_type(out, input_output_state='output')) for out in output]

        # return Output(page + '-' + output.split(':')[0], self._find_type(output))

    def state_callback(self, page, state):
        """Create state callbacks for Dash components, which can be used to trigger callbacks. We can have multiple
        state callbacks for methods.

        Parameters
        ----------
        page : str
            Name of the page (eg. 'magic-carpet')

        state : str (list)
            Dash components where we wish to add dash based state callbacks

        Returns
        -------
        dash.dependencies.State (list)
        """
        if not (isinstance(state, list)):
            state = [state]

        return [State(page + '-' + s.split(':')[0], self._find_type(s, input_output_state='state')) for s in state]

    def _find_type(self, tag, input_output_state='input'):
        """Returns the dash type for a dash component.

        Parameters
        ----------
        tag : str
            Tag for a Dash component

        Returns
        -------
        str
        """

        if ":" in tag:
            return tag.split(":")[1]

        # datepicker
        if 'dtpicker' in tag:
            return 'date'

        # HTML links
        if 'link' in tag:
            return 'href'

        # table like objects
        if 'table' in tag:
            if self._constants.gui_table_type == 'dash':
                return 'data'

            return 'children'

        # labels
        if 'status' in tag:
            return 'children'

        # container/div to be filled
        if 'container' in tag:
            return 'children'

        # plotly objects
        if 'plot' in tag and 'val' not in tag:
            return 'figure'

        # plotly objects
        if 'fig' in tag and 'val' not in tag:
            return 'figure'

        # drop down values
        if 'val' in tag or 'dropdown' in tag:
            if input_output_state == 'output':
                return 'value'

            return 'value'

        # HTML ordinary buttons
        if 'button' in tag:
            return 'n_clicks'

        # HTML upload buttons
        if 'upbutt' in tag:
            return 'contents'

        if 'uploadbox' in tag:
            return 'contents'

import base64
import flask

class SessionManager(object):
    """Manages the caching of properties for a user's session. We use this extensively, to identify users and also to
    store variables relating to users on the server side.

    It is used for example, for keeping track of which lines have plotted, user's zoom actions, whether tcapy has already
    plotted a particular dataset etc.

    """

    def __init__(self):
        pass

    # session ID management functions

    def get_session_id(self):
        """Gets the current user's session ID and generates a unique one if necessary.

        Returns
        -------
        str
        """
        if 'id' not in session:
            id = str(uuid.uuid4())

            username = self.get_username()

            if username is not None:
                username = '_' + username
            else:
                username = ''

            session['id'] = id + username
        else:
            id = session['id']

        if not isinstance(id, str):
            id = id.decode("utf-8")

        return id

    def get_username(self):
        header = flask.request.headers.get('Authorization', None)

        if not header:
            return None

        username_password = base64.b64decode(header.split('Basic ')[1])
        username_password_utf8 = username_password.decode('utf-8')
        username, password = username_password_utf8.split(':')

        return username

    def set_session_flag(self, tag, value=None):
        """Sets a value with a specific _tag in the session dictionary, which is essentially unique for every user.

        Parameters
        ----------
        tag : str (dict)
            The "hash key" for our variable
        value : str
            What to set the value in our hash table

        Returns
        -------

        """
        if isinstance(tag, str):
            tag = [tag]

        if isinstance(tag, dict):
            for t in tag:
                self.set_session_flag(t, value=tag[t])

            return

        tag = self.flatten_list_of_lists(tag)

        for t in tag:
            session[t] = value

    def get_session_flag(self, tag):
        """Gets the value of a _tag in the user's session

        Parameters
        ----------
        tag : str
            Tag to be fetched

        Returns
        -------
        str
        """
        if tag in session:

            if isinstance(session[tag], bool):
                return session[tag]

            return str(session[tag])

        return None

    ##### these methods are for keeping track of which lines, user zooms have been plotted for each chart in the user's
    ##### session object

    def check_lines_plotted(self, lines_to_plot, tag):
        """Checks if the lines have been plotted for a particular user, by checking the plot's _tag in their user session

        Parameters
        ----------
        lines_to_plot : str (list)
            Lines to be plotted

        tag : str
            Tag of plotted lines

        Returns
        -------
        bool
        """

        if tag in session:
            lines_plotted = session[tag]

            if set(lines_to_plot) == set(lines_plotted):
                return True

        return False

    def check_relayoutData_plotted(self, relayoutData, tag):
        """Checks if the relayout data (ie. related to user's clicks, such as when they zoom in) has already been plotted.

        Parameters
        ----------
        relayoutData : dict

        tag : str
            Tag referring to a particular plot

        Returns
        -------

        """

        if tag in session:
            if relayoutData == session[tag]:
                return True

        return False

    def set_lines_plotted(self, lines_to_plot, tag):
        """Sets the lines plotted for a particular chart _tag in the user's session

        Parameters
        ----------
        lines_to_plot : str (list)
            Lines plotted

        tag : str
            Tag of the plot

        Returns
        -------

        """
        session[tag] = lines_to_plot

    def set_relayoutData_plotted(self, relayoutData, tag):
        """Sets the user's clicks (typically for zooming into charts) for a particular chart

        Parameters
        ----------
        relayoutData : dict
            Details a user's click on the chart

        tag : str
            Tag referring to the plot

        Returns
        -------

        """
        session[tag] = relayoutData

    def set_username(self, username):
        session['username'] = username

    ##### We identify when a user has "clicked" a button by change in the number of clicks (Dash documentation recommends
    ##### this to handle user clicks)
    def get_session_clicks(self, tag):
        """Gets the number of clicks for the _tag. If doesn't exist, we automatically set the _tag as 0.

        Parameters
        ----------
        tag : str
            The _tag for which we want to return the number of clicks

        Returns
        -------
        Number of clicks by current user
        """

        if tag not in session:
            return 0

        return session[tag]

    def set_session_clicks(self, tag, n_clicks, old_clicks=None):
        """Sets the number of clicks in the current user's session

        Parameters
        ----------
        tag : str
            Tag to store the user's clicks under
        n_clicks : int
            Number of clicks to set
        Returns
        -------

        """

        if old_clicks is None:
            session[tag] = n_clicks
        elif old_clicks > n_clicks:
            session[tag] = n_clicks

    def check_session_tag(self, tag):
        """Checks if a _tag exists in the user's session, and if so returns the value of that _tag in the user's session

        Parameters
        ----------
        tag : str
            Tag to check

        Returns
        -------
        str or bool
        """
        if tag in session:
            return session[tag]

        return False

    def exists_session_tag(self, tag):
        """Does a _tag exist in the current user session?

        Parameters
        ----------
        tag : str

        Returns
        -------
        bool
        """
        return tag in session

    def check_session_reset_tag(self, tag):
        """Checks if a _tag is in session (if that _tag exists already and is "True", then we reset it to "False"), otherwise
        return "False"

        Parameters
        ----------
        tag : str
            Tags to check

        Returns
        -------
        bool
        """
        if tag in session:
            old_tag = session[tag]

            if old_tag:
                session[tag] = False

                return True

            return False

        return False

    def create_calculated_flags(self, prefix, lst=None, lst2=None):
        """Creates a list for a combination of prefix and list elements.

        Parameters
        ----------
        prefix : str
            Prefix (typically a page name like 'magic-carpet')

        lst : str (list)
            Tags will contain these

        lst2 : str (list)
            Tags will contain these

        Returns
        -------
        str (list)
        """

        if isinstance(prefix, list):
            prefix = self.flatten_list_of_lists(prefix)
            lst = [x + '-' + lst for x in prefix]
        elif isinstance(lst, list):
            lst = self.flatten_list_of_lists(lst)
            lst = [prefix + '-' + x for x in lst]

        if lst2 is None:
            return lst

        lst3 = []

        for i in lst2:
            for j in lst:
                lst3.append(j + '-' + i)

        return lst3

    def flatten_list_of_lists(self, list_of_lists):
        """Flattens lists of obj, into a single list of strings (rather than characters, which is default behavior).

        Parameters
        ----------
        list_of_lists : obj (list)
            List to be flattened

        Returns
        -------
        str (list)
        """

        if isinstance(list_of_lists, list):
            rt = []
            for i in list_of_lists:
                if isinstance(i, list):
                    rt.extend(self.flatten_list_of_lists(i))
                else:
                    rt.append(i)

            return rt

        return list_of_lists