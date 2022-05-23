# Clear file content
> ./facade_service.env

echo "ADDRESS=127.0.0.1" > ./facade_service.env
echo "PORT=${1}" >> ./facade_service.env

uvicorn facade_controller:app --workers 2 --reload --port ${1}