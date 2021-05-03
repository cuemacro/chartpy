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

from abc import ABC, abstractmethod

import pandas as pd

from chartpy.dashboard.sketchcomponents import SketchComponents

class LayoutCanvas(ABC):
    """Abstract class which is used to create a web dashboard, to specify the layout and also to write the callbacks
    which react to user events (like clicking buttons and selecting from dropdown boxes).
    """

    def __init__(self, app=None, constants=None, url_prefix=''):
        self._app = app
        self._sc = SketchComponents(app, constants=constants, url_prefix=url_prefix)

        self._constants = constants

    def flatten_list_of_strings(self, list_of_lists):
        """Flattens lists of strings, into a single list of strings (rather than characters, which is default behavior).

        Parameters
        ----------
        list_of_lists : str (list)
            List to be flattened

        Returns
        -------
        str (list)
        """

        rt = []
        for i in list_of_lists:
            if isinstance(i, list):
                rt.extend(self.flatten_list_of_strings(i))
            else:
                rt.append(i)
        return rt

    def convert_boolean(self, boolean_val):

        boolean_val = boolean_val.lower()

        if boolean_val == 'true' or boolean_val == 'yes':
            return True
        elif boolean_val == 'false' or boolean_val == 'no':
            return False

    def convert_date(self, date_val, date=True):
        if date:
            if date_val is None:
                return date_val

            if isinstance(date_val, str):

                if ',' in date_val or ";" in date_val:
                    date_val = date_val.split(',')

                    return [pd.Timestamp(pd.Timestamp(d).date()) for d in date_val]

                return pd.Timestamp(pd.Timestamp(date_val).date())

            elif isinstance(date_val, list):
                return [pd.Timestamp(pd.Timestamp(d).date()) for d in date_val]

        return date_val

    def convert_float(self, float_val):

        if isinstance(float_val, float):
            return float_val

        if isinstance(float_val, list):
            return [float(i) for i in float_val]

        if ',' in float_val:
            float_val = float_val.split(',')

            return [float(i) for i in float_val]

        return float(float_val)

    def convert_int(self, int_val, listify=False):

        if listify:
            if not(isinstance(int_val, list)):
                int_val = [int_val]

        if isinstance(int_val, int):
            return int_val

        if isinstance(int_val, list):
            return [int(i) for i in int_val]

        if ',' in int_val:
            int_val = int_val.split(',')

            return [int(i) for i in int_val]

        return int(int_val)

    def convert_str(self, str_val, listify=False):

        if str_val is None:
            return None

        if listify:
            if not(isinstance(str_val, list)):
                str_val = [str_val]

        if isinstance(str_val, list):
            return str_val

        if ',' in str_val:
            str_val = str_val.split(',')

            return [x.strip() for x in str_val]

        if ';' in str_val:
            str_val = str_val.split(';')

            return [x.strip() for x in str_val]


        return str_val

    @abstractmethod
    def calculate_button(self):
        pass

    @abstractmethod
    def page_name(self):
        pass

    @abstractmethod
    def attach_callbacks(self):
        pass

    @abstractmethod
    def construct_layout(self):
        pass