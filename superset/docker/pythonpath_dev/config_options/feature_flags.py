FEATURE_FLAGS: dict[str, bool] = {
    # When using a recent version of Druid that supports JOINs turn this on
    "DRUID_JOINS": False,
    "DYNAMIC_PLUGINS": False,
    # Authorize jinja templating
    "ENABLE_TEMPLATE_PROCESSING": True,
    # Allow for javascript controls components
    # this enables programmers to customize certain charts (like the
    # geospatial ones) by inputting javascript in controls. This exposes
    # an XSS security vulnerability
    "ENABLE_JAVASCRIPT_CONTROLS": True,  # deprecated
    # When this feature is enabled, nested types in Presto will be
    # expanded into extra columns and/or arrays. This is experimental,
    # and doesn't work with all nested types.
    "PRESTO_EXPAND_DATA": False,
    # Exposes API endpoint to compute thumbnails
    "THUMBNAILS": False,
    # Enables the endpoints to cache and retrieve dashboard screenshots via webdriver.
    # Requires configuring Celery and a cache using THUMBNAIL_CACHE_CONFIG.
    "ENABLE_DASHBOARD_SCREENSHOT_ENDPOINTS": False,
    # Generate screenshots (PDF or JPG) of dashboards using the web driver.
    # When disabled, screenshots are generated on the fly by the browser.
    # This feature flag is used by the download feature in the dashboard view.
    # It is dependent on ENABLE_DASHBOARD_SCREENSHOT_ENDPOINT being enabled.
    "ENABLE_DASHBOARD_DOWNLOAD_WEBDRIVER_SCREENSHOT": True,
    "TAGGING_SYSTEM": True,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": False,
    # When True, this escapes HTML (rather than rendering it) in Markdown components
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_VIRTUALIZATION": True,
    # This feature flag is stil in beta and is not recommended for production use.
    "GLOBAL_ASYNC_QUERIES": False,
    "EMBEDDED_SUPERSET": True,
    # Enables Alerts and reports new implementation
    "ALERT_REPORTS": True,
    "ALERT_REPORT_TABS": True,
    "ALERT_REPORT_SLACK_V2": False,
    "DASHBOARD_RBAC": True,
    "ENABLE_ADVANCED_DATA_TYPES": False,
    # Enabling ALERTS_ATTACH_REPORTS, the system sends email and slack message
    # with screenshot and link
    # Disables ALERTS_ATTACH_REPORTS, the system DOES NOT generate screenshot
    # for report with type 'alert' and sends email and slack message with only link;
    # for report with type 'report' still send with email and slack message with
    # screenshot and link
    "ALERTS_ATTACH_REPORTS": True,
    # Allow users to export full CSV of table viz type.
    # This could cause the server to run out of memory or compute.
    "ALLOW_FULL_CSV_EXPORT": True,
    "ALLOW_ADHOC_SUBQUERY": False,
    "USE_ANALOGOUS_COLORS": False,
    # Apply RLS rules to SQL Lab queries. This requires parsing and manipulating the
    # query, and might break queries and/or allow users to bypass RLS. Use with care!
    "RLS_IN_SQLLAB": False,
    # Try to optimize SQL queries — for now only predicate pushdown is supported.
    "OPTIMIZE_SQL": False,
    # When impersonating a user, use the email prefix instead of the username
    "IMPERSONATE_WITH_EMAIL_PREFIX": False,
    # Enable caching per impersonation key (e.g username) in a datasource where user
    # impersonation is enabled
    "CACHE_IMPERSONATION": False,
    # Enable caching per user key for Superset cache (not database cache impersonation)
    "CACHE_QUERY_BY_USER": False,
    # Enable sharing charts with embedding
    "EMBEDDABLE_CHARTS": True,
    "DRILL_TO_DETAIL": True,  # deprecated
    "DRILL_BY": True,
    "DATAPANEL_CLOSED_BY_DEFAULT": False,
    # The feature is off by default, and currently only supported in Presto and Postgres,  # noqa: E501
    # and Bigquery.
    # It also needs to be enabled on a per-database basis, by adding the key/value pair
    # `cost_estimate_enabled: true` to the database `extra` attribute.
    "ESTIMATE_QUERY_COST": False,
    # Allow users to enable ssh tunneling when creating a DB.
    # Users must check whether the DB engine supports SSH Tunnels
    # otherwise enabling this flag won't have any effect on the DB.
    "SSH_TUNNELING": False,
    "AVOID_COLORS_COLLISION": True,
    # Do not show user info in the menu
    "MENU_HIDE_USER_INFO": False,
    # Allows users to add a ``superset://`` DB that can query across databases. This is
    # an experimental feature with potential security and performance risks, so use with
    # caution. If the feature is enabled you can also set a limit for how much data is
    # returned from each database in the ``SUPERSET_META_DB_LIMIT`` configuration value
    # in this file.
    "ENABLE_SUPERSET_META_DB": False,
    # Set to True to replace Selenium with Playwright to execute reports and thumbnails.
    # Unlike Selenium, Playwright reports support deck.gl visualizations
    # Enabling this feature flag requires installing "playwright" pip package
    "PLAYWRIGHT_REPORTS_AND_THUMBNAILS": False,
    # Set to True to enable experimental chart plugins
    "CHART_PLUGINS_EXPERIMENTAL": False,
    # Regardless of database configuration settings, force SQLLAB to run async using Celery  # noqa: E501
    "SQLLAB_FORCE_RUN_ASYNC": False,
    # Set to True to to enable factory resent CLI command
    "ENABLE_FACTORY_RESET_COMMAND": False,
    # Whether Superset should use Slack avatars for users.
    # If on, you'll want to add "https://avatars.slack-edge.com" to the list of allowed
    # domains in your TALISMAN_CONFIG
    "SLACK_ENABLE_AVATARS": False,
    # Allow users to optionally specify date formats in email subjects, which will be parsed if enabled. # noqa: E501
    "DATE_FORMAT_IN_EMAIL_SUBJECT": False,
    # Allow metrics and columns to be grouped into (potentially nested) folders in the
    # chart builder
    "DATASET_FOLDERS": False,
}
