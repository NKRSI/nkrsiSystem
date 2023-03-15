
for server in "plaster" "walter"
do
  echo $server
  ssh ${server} "sudo rm -r /opt/external_microservices/resource_monitoring"
  ssh ${server} "sudo mkdir -p /opt/external_microservices; sudo chmod 777 /opt/external_microservices"
  scp -r resource_monitoring ${server}:/opt/external_microservices/./
  ssh ${server} "if [ ! -d /opt/external_microservices/venv ]; then python3 -m venv /opt/external_microservices/venv; source /opt/external_microservices/venv/bin/activate; pip3 install -r /opt/external_microservices/resource_monitoring/requirements.txt; fi"
  ssh ${server} "cd /opt/external_microservices/resource_monitoring; sudo cp resource_monitoring.service /etc/systemd/system/.; sudo systemctl daemon-reload; sudo systemctl restart resource_monitoring"
done