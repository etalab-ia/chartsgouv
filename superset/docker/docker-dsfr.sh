#!/usr/bin/env bash

for theme_filename in $(find /app/superset/static/assets -name "theme*.css"); do
    sed \
      -e "s/#20a7c9/#000091/g" \
      -e "s/#45bed6/#000091/g" \
      -e "s/#1985a0/#000091/g" \
      "$theme_filename" > temp.css && mv temp.css "$theme_filename"
done

pybabel compile -d superset/translations || true

cp /app/superset/templates_overrides/superset/base.html /app/superset/templates/superset/base.html
cp /app/superset/templates_overrides/superset/basic.html /app/superset/templates/superset/basic.html

cp /app/superset/templates_overrides/superset/public_welcome.html /app/superset/templates/superset/public_welcome.html

cp /app/superset/templates_overrides/tail_js_custom_extra.html /app/superset/templates/tail_js_custom_extra.html

cp /app/superset/static/assets/local/404.html /app/superset/static/assets/404.html
cp /app/superset/static/assets/local/500.html /app/superset/static/assets/500.html
