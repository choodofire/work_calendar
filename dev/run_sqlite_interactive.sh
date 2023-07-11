#!/bin/sh

set -e

image_name="keinos/sqlite3"
volume_name="sqlite_samples"

if [ ! -d "$volume_name" ]; then
    mkdir $volume_name
fi

#fix db directory permission if necessary
docker_user_id=$(docker run --rm keinos/sqlite3 /bin/sh -c "id -u")
if [ $(stat -c "%u" $volume_name) -ne $docker_user_id ];then
    echo do stuff
    #sqlite suer may have some funny user id for the host system so we have to use sudo here
    sudo chown -R $docker_user_id:$(id -g) $volume_name
fi

#run sqlite docker interactively: print databases and switch to sqlite3 interactive mode
docker run \
-it \
--rm \
-v "$(pwd)/$volume_name:/$volume_name" \
$image_name /bin/sh -c "sqlite3 /$volume_name/sample.db .databases && sqlite3 /$volume_name/sample.db"