#! /bin/ash
cd /app
pylint --errors-only --load-plugins pylint_django \
    --django-settings-module=realDealz.settings \
     $(find . -type f -name "*.py")