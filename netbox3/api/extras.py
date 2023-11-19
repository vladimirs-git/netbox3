# pylint: disable=R0902,R0903

"""Extras connectors."""

from netbox3.api.connector import Connector


class ExtrasAC:
    """Extras connectors."""

    def __init__(self, **kwargs):
        """Init ExtrasAC."""
        self.bookmarks = self.BookmarksC(**kwargs)
        self.config_contexts = self.ConfigContextsC(**kwargs)
        self.config_templates = self.ConfigTemplatesC(**kwargs)
        self.content_types = self.ContentTypesC(**kwargs)
        self.custom_field_choice_sets = self.CustomFieldChoiceSetsC(**kwargs)
        self.custom_fields = self.CustomFieldsC(**kwargs)
        self.custom_links = self.CustomLinksC(**kwargs)
        self.export_templates = self.ExportTemplatesC(**kwargs)
        self.image_attachments = self.ImageAttachmentsC(**kwargs)
        self.journal_entries = self.JournalEntriesC(**kwargs)
        self.object_changes = self.ObjectChangesC(**kwargs)
        self.reports = self.ReportsC(**kwargs)
        self.saved_filters = self.SavedFiltersC(**kwargs)
        self.scripts = self.ScriptsC(**kwargs)
        self.tags = self.TagsC(**kwargs)
        self.webhooks = self.WebhooksC(**kwargs)

    class BookmarksC(Connector):
        """BookmarksC."""

        path = "extras/bookmarks/"

    class ConfigContextsC(Connector):
        """ConfigContextsC."""

        path = "extras/config-contexts/"

    class ConfigTemplatesC(Connector):
        """ConfigTemplatesC."""

        path = "extras/config-templates/"

    class ContentTypesC(Connector):
        """ContentTypesC."""

        path = "extras/content-types/"

        def __init__(self, **kwargs):
            """Init ContentTypesC."""
            super().__init__(**kwargs)
            items = ["id", "app_label", "model"]
            self._need_split.extend(items)

    class CustomFieldChoiceSetsC(Connector):
        """CustomFieldChoiceSetsC."""

        path = "extras/custom-field-choice-sets/"

    class CustomFieldsC(Connector):
        """CustomFieldsC."""

        path = "extras/custom-fields/"

    class CustomLinksC(Connector):
        """CustomLinksC."""

        path = "extras/custom-links/"

    class ExportTemplatesC(Connector):
        """ExportTemplatesC."""

        path = "extras/export-templates/"

    class ImageAttachmentsC(Connector):
        """ImageAttachmentsC."""

        path = "extras/image-attachments/"

    class JournalEntriesC(Connector):
        """JournalEntriesC."""

        path = "extras/journal-entries/"

    class ObjectChangesC(Connector):
        """ObjectChangesC."""

        path = "extras/object-changes/"

    class ReportsC(Connector):
        """ReportsC."""

        path = "extras/reports/"

    class SavedFiltersC(Connector):
        """SavedFiltersC."""

        path = "extras/saved-filters/"

    class ScriptsC(Connector):
        """ScriptsC."""

        path = "extras/scripts/"

    class TagsC(Connector):
        """TagsC."""

        path = "extras/tags/"

    class WebhooksC(Connector):
        """WebhooksC."""

        path = "extras/webhooks/"
