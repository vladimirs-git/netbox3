# pylint: disable=R0902,R0903

"""Core connectors."""

from netbox3.api.connector import Connector


class CoreAC:
    """Core connectors."""

    def __init__(self, **kwargs):
        """Init CoreAC."""
        self.data_files = self.DataFilesC(**kwargs)
        self.data_sources = self.DataSourcesC(**kwargs)
        self.jobs = self.JobsC(**kwargs)

    class DataFilesC(Connector):
        """DataFilesC."""

        path = "core/data-files/"

    class DataSourcesC(Connector):
        """DataSourcesC."""

        path = "core/data-sources/"

    class JobsC(Connector):
        """JobsC."""

        path = "core/jobs/"
