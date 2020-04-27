read -p 'Container name: ' CONTAINER_NAME
echo Building container $CONTAINER_NAME.
docker build -t $CONTAINER_NAME .
