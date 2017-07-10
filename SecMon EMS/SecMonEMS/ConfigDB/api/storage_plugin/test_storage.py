#    Copyright (c) 2016 Intel Corporation.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from yapsy.PluginManager import PluginManager
# from serializers_ikepolicy import IKEPolicy
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('yapsy').setLevel(logging.DEBUG)


class Dog:
    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name


def main():
    # Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["storage_plugin/consul"])
    manager.collectPlugins()

    # Loop round the plugins and print their names.
    for plugin in manager.getAllPlugins():
        # plugin.plugin_object.put_record('ikepolicies',Dog('12345','hello'))
        plugin.plugin_object.get_record('ikepolicies', '12345')
        plugin.plugin_object.get_record('ikepolicies', 'hello', 'name')


if __name__ == "__main__":
    main()
