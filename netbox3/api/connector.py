# pylint: disable=R0902,R0903

"""Base for connectors."""

from __future__ import annotations

import json

from requests import Response
from vhelpers import vdict

from netbox3.api.base_c import BaseC
from netbox3.types_ import DAny, LDAny, LDList


class Connector(BaseC):
    """Connector to Netbox entry point for different models.

    For example, ``NbApi.ipam.ip_addresses.{method}``, where ``{method}``
    can be any of the described methods below.
    """

    # ============================= methods ==============================

    def create(self, **kwargs) -> Response:
        """Create object in Netbox.

        :param kwargs: Parameters of new object to create.
        :type kwargs: dict

        :return: Session response.

            - <Response [201]> Object successfully created,
            - <Response [400]> Object already exist.
        :rtype: Response
        """
        response: Response = self._session.post(
            url=self.url,
            data=json.dumps(kwargs),
            headers=self._headers(),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    def create_d(self, **kwargs) -> DAny:
        """Create object in Netbox.

        :param kwargs: Data of new object to create.
        :type kwargs: dict

        :return: Data of newly crated object.
        :rtype: dict
        """
        response: Response = self.create(**kwargs)
        if not response.status_code == 201:
            return {}
        html: str = response.content.decode("utf-8")
        data: DAny = dict(json.loads(html))
        return data

    # noinspection PyShadowingBuiltins
    def delete(self, id: int) -> Response:  # pylint: disable=redefined-builtin
        """Delete object in Netbox.

        :param id: Object ID.
        :type id: int

        :return: Session response.

            - <Response [204]> Object successfully deleted,
            - <Response [404]> Object not found.
        :rtype: Response
        """
        response: Response = self._session.delete(
            url=f"{self.url}{id}",
            headers=self._headers(),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    # noinspection PyIncorrectDocstring
    def get(self, **kwargs) -> LDAny:
        """Request data from Netbox using filtering parameters.

        The filtering parameters are identical to those in the web interface
        filter form. The value of each parameter can be either a single value
        or a list of multiple values.

        Split the query to multiple requests if the URL length exceeds maximum
        length due to a long list of GET parameters.

        Multithreading can be used to request a large amount of data rapidly,
        with intervals between threads (to optimize session spikes and achieve
        script stability in Docker with limited resources).

        To determine the filtering parameters for various models, you can use:

        - API schema https://demo.netbox.dev/api/schema/swagger-ui,
        - Example https://github.com/vladimirs-git/netbox3/tree/main/examples,
        - Oficial documentation (if you're lucky).

        :param kwargs: Filtering parameters.
        :type kwargs: dict

        :return: List of dictionaries containing Netbox objects.
        :rtype: List[dict]
        """
        params_ld: LDList = self._validate_params(**kwargs)
        items: LDAny = self._query_params_ld(params_ld)
        self._check_keys(items=items, denied=self._reserved_ipam_keys)
        return items

    # noinspection PyIncorrectDocstring
    def update(self, **kwargs) -> Response:
        """Update object in Netbox.

        :param id: Netbox object id to update.
        :type id: int

        :param kwargs: Parameters to update object in Netbox.
        :type kwargs: dict

        :return: Session response.

            - <Response [200]> Object successfully updated,
            - <Response [400]> Invalid data.
        :rtype: Response
        """
        id_ = vdict.pop("id", kwargs)
        if not id_:
            raise ValueError("id expected in the data.")

        response: Response = self._session.patch(
            url=f"{self.url}{id_}/",
            data=json.dumps(kwargs),
            headers=self._headers(),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    # noinspection PyIncorrectDocstring
    def update_d(self, **kwargs) -> DAny:
        """Update object in Netbox.

        :param id: Netbox object id to update.
        :type id: int

        :param kwargs: Parameters to update object in Netbox.
        :type kwargs: dict

        :return: Data of updated object.
        :rtype: dict
        """
        response: Response = self.update(**kwargs)
        if not response.status_code == 200:
            return {}
        html: str = response.content.decode("utf-8")
        data: DAny = dict(json.loads(html))
        return data
