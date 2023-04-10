#!/bin/ash

if ps -ef | awk '$1 == 1 && /python3 manage.py runserver/ {exit 0} END {exit 1}'; then
    echo >&2 "Docker Container or Server Not Detected, Exiting..."
    exit 1
fi


function createDockerAdminUser {
    # forcibly creates super user with username & password: docker
    # This should be removed before the app is deployed
    if ! cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username = 'docker').exists():
    User.objects.get(username = 'docker').delete()
User.objects.create_superuser('docker', 'docker@docker.local', 'docker')
EOF
#                                ^user          ^email            ^pass
    then
        return 1
    else
        return 0
    fi
}


pip install -r dev_tools.txt --no-cache-dir > /dev/null &

createDockerAdminUser

if [ $? -ne 0 ]; then
    clear_models.sh
    createDockerAdminUser
else
    LOCAL_DIR="$(pwd)"
    cd /app
    python manage.py makemigrations
    python manage.py migrate
    cd $LOCAL_DIR
fi
