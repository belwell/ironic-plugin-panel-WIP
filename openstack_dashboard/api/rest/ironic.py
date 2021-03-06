#
# Copyright 2015 Hewlett Packard Enterprise Development Company LP
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
"""API over the ironic service.
"""

from django.views import generic

from openstack_dashboard import api
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils


@urls.register
class Nodes(generic.View):
    """API for ironic nodes.
    """

    url_regex = r'ironic/nodes/$'

    @rest_utils.ajax()
    def get(self, request):
        """Retrieve a list of nodes.

        The listing result is an object with property "items".
        """
        result = api.ironic.node_list(request)
        return {
            'items': [i.to_dict() for i in result],
        }


@urls.register
class Node(generic.View):
    """API for ironic node.
    """

    url_regex = r'ironic/nodes/(?P<node_id>[0-9a-f-]+)$'

    @rest_utils.ajax()
    def get(self, request, node_id):
        """Retrieve a node.
        """
        return api.ironic.node_get(request, node_id).to_dict()


@urls.register
class Ports(generic.View):
    """API for ironic ports.
    """

    url_regex = r'ironic/ports/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of ports associated with a given node.
        """
        node_id = request.GET.get('node_id')
        result = api.ironic.node_list_ports(request, node_id)
        return {
            'items': [i.to_dict() for i in result],
        }


@urls.register
class StatesPower(generic.View):
    """API for power state of a node.
    """

    url_regex = r'ironic/nodes/(?P<node_id>[0-9a-f-]+)/states/power$'

    @rest_utils.ajax(data_required=True)
    def patch(self, request, node_id):
        """Set power state for a given node.
        """
        state = request.DATA.get('state')
        return api.ironic.node_set_power_state(request, node_id, state)


@urls.register
class Maintenance(generic.View):
    """API for maintenance state of a node.
    """

    url_regex = r'ironic/nodes/(?P<node_id>[0-9a-f-]+)/maintenance$'

    @rest_utils.ajax()
    def patch(self, request, node_id):
        return api.ironic.node_set_maintenance(request, node_id, 'on')

    @rest_utils.ajax()
    def delete(self, request, node_id):
        return api.ironic.node_set_maintenance(request, node_id, 'off')
