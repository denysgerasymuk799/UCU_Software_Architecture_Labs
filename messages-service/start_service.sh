# Clear file content
> ./messages_service.env

echo "ADDRESS=127.0.0.1" > ./messages_service.env
echo "PORT=${1}" >> ./messages_service.env

uvicorn messages_controller:app --workers 2 --reload --port ${1}