#!/usr/bin/env bash

for theme_filename in $(find /app/superset/static/assets -name "theme*.css"); do
    sed \
      -e "s/#20a7c9/#000091/g" \
      -e "s/#45bed6/#000091/g" \
      -e "s/#1985a0/#000091/g" \
      "$theme_filename" > temp.css && mv temp.css "$theme_filename"
done

# Compile translations if folder exists
if [ -d /app/superset/translations ]; then
  echo "Compiling translations..."
  pybabel compile -d superset/translations || true
  echo "Translations compiled."
fi

# Copy templates overrides if folder exists
if [ -d /app/superset/templates_overrides ]; then
  echo "Copying template overrides..."
  cp -r /app/superset/templates_overrides/* /app/superset/templates/
  echo "Template overrides copied."
fi

# Copy local assets if folder exists
if [ -d /app/superset/static/assets/local ]; then
  echo "Copying local assets..."
  cp -r /app/superset/static/assets/local/* /app/superset/static/assets/
  echo "Local assets copied."
fi