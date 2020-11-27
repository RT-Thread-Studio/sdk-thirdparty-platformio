# Copyright 2019-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from tools.notifier import Notifier


class PlatformioFakeNotifier(Notifier):

    def get_output(self):
        pass

    def notify(self, event):
        pass

    def print_notify(self, event):
        pass

    def print_notify_verbose(self, event):
        pass

    def colorstring_to_escapecode(self, color_string):
        pass

    def print_in_color(self, event, msg):
        pass
