import copy
import logging
from typing import Any, Dict

from django.conf import settings
from django.templatetags.static import static

from .utils import get_admin_url, get_model_meta, hex_to_rgb

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: Dict[str, Any] = {
    # title of the window (Will default to current_admin_site.site_title)
    "site_title": "Admin Dashboard",
    # Title on the login screen (19 chars max) (will default to current_admin_site.site_header)
    "site_header": None,
    # Title on the brand (19 chars max) (will default to current_admin_site.site_header)
    "site_brand": None,
    # URL of the logo for your site, used for brand on top left
    "site_logo": "https://cdn.practet.com/static/logo-new.webp",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    ############
    # Top Menu #
    ############
    # Links to put along the nav bar
    "topmenu_links": [],
    #############
    # User Menu #
    #############
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_with_respect_to": [],
    "order_menus": [],
    # Custom links to append to side menu app groups, keyed on lower case app label
    # or makes a new group if the given app label doesnt exist in installed apps
    "custom_links": {},
    # Custom icons for side menu apps/models See the link below
    "icons": {"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users"},
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {},
    # Add a language dropdown into the admin
    "language_chooser": False,
    "theme_color": "#e31837",
}

CHANGEFORM_TEMPLATES = {
    "single": "practet_dashboard/includes/single.html",
    "carousel": "practet_dashboard/includes/carousel.html",
    "collapsible": "practet_dashboard/includes/collapsible.html",
    "horizontal_tabs": "practet_dashboard/includes/horizontal_tabs.html",
    "vertical_tabs": "practet_dashboard/includes/vertical_tabs.html",
}


def get_settings() -> Dict:
    practet_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "PRACTET_DASHBOARD_SETTINGS", {}).items() if y is not None}
    practet_settings.update(user_settings)

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if isinstance(practet_settings["hide_apps"], str):
        practet_settings["hide_apps"] = [practet_settings["hide_apps"]]
    practet_settings["hide_apps"] = [x.lower() for x in practet_settings["hide_apps"]]

    if isinstance(practet_settings["hide_models"], str):
        practet_settings["hide_models"] = [practet_settings["hide_models"]]
    practet_settings["hide_models"] = [x.lower() for x in practet_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    practet_settings["icons"] = {x.lower(): y.lower() for x, y in practet_settings.get("icons", {}).items()}

    # Default the site icon using the site logo
    practet_settings["site_icon"] = practet_settings["site_icon"] or practet_settings["site_logo"]

    # ensure all model names are lower cased
    practet_settings["changeform_format_overrides"] = {
        x.lower(): y.lower() for x, y in practet_settings.get("changeform_format_overrides", {}).items()
    }

    practet_settings["theme_color_rgb"] = hex_to_rgb(practet_settings.get("theme_color", "#30AA99"))
    return practet_settings
