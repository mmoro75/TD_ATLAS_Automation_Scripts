#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <lh_name>"
  exit 1
fi

LH_NAME=$1
PERSIST_FILE="/tmp/${LH_NAME}_persist.txt"
DOCKER_CONTAINER=${LH_NAME}

# Navigate to the persist-viewer directory and run the command
sudo docker exec ${DOCKER_CONTAINER} /bin/bash -c "python3 /opt/installed-components/engine/bin/persist-viewer/persist-viewer.py --feed-instance ${LH_NAME} B --engine-path /refinitiv/installed-components/engine/bin/ sqlite --dbfolder sqlite --dbfolder /refinitiv/runtime/persistence >>${PERSIST_FILE}"

# Check if the file was created successfully
if [ $? -eq 0 ]; then
  echo "Persist file created successfully at ${PERSIST_FILE}"
  sudo docker cp ${LH_NAME}:${PERSIST_FILE} ${PERSIST_FILE}
else
  echo "Failed to create persist file."
fi
 