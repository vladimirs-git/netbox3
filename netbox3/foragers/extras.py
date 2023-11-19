# pylint: disable=R0902,R0903

"""Extras Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class ExtrasAF(BaseAF):
    """Extras Forager."""

    def __init__(self, root: NbTree, api: NbApi):
        """Init ExtrasAF.

        :param root: NbTree object where data from Netbox needs to be saved.
        :param api: NbApi object, connector to Netbox API.
        """
        super().__init__(root, api)
        self.bookmarks = self.BookmarksF(self)
        self.config_contexts = self.ConfigContextsF(self)
        self.config_templates = self.ConfigTemplatesF(self)
        self.content_types = self.ContentTypesF(self)
        self.custom_field_choice_sets = self.CustomFieldChoiceSetsF(self)
        self.custom_fields = self.CustomFieldsF(self)
        self.custom_links = self.CustomLinksF(self)
        self.export_templates = self.ExportTemplatesF(self)
        self.image_attachments = self.ImageAttachmentsF(self)
        self.journal_entries = self.JournalEntriesF(self)
        self.object_changes = self.ObjectChangesF(self)
        self.reports = self.ReportsF(self)
        self.saved_filters = self.SavedFiltersF(self)
        self.scripts = self.ScriptsF(self)
        self.tags = self.TagsF(self)
        self.webhooks = self.WebhooksF(self)

    class BookmarksF(Forager):
        """BookmarksF."""

    class ConfigContextsF(Forager):
        """ConfigContextsF."""

    class ConfigTemplatesF(Forager):
        """ConfigTemplatesF."""

    class ContentTypesF(Forager):
        """ContentTypesF."""

    class CustomFieldChoiceSetsF(Forager):
        """CustomFieldChoiceSetsF."""

    class CustomFieldsF(Forager):
        """CustomFieldsF."""

    class CustomLinksF(Forager):
        """CustomLinksF."""

    class ExportTemplatesF(Forager):
        """ExportTemplatesF."""

    class ImageAttachmentsF(Forager):
        """ImageAttachmentsF."""

    class JournalEntriesF(Forager):
        """JournalEntriesF."""

    class ObjectChangesF(Forager):
        """ObjectChangesF."""

    class ReportsF(Forager):
        """ReportsF."""

    class SavedFiltersF(Forager):
        """SavedFiltersF."""

    class ScriptsF(Forager):
        """ScriptsF."""

    class TagsF(Forager):
        """TagsF."""

    class WebhooksF(Forager):
        """WebhooksF."""
