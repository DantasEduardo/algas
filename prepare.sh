echo "Installing docker"

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker

echo "Creating MySQL database"
cd database
sudo docker build mysql_container .
sudo docker run --name bd -p 3306:3306 -e MYSQL_ROOT_PASSWORD=urubu100 -d mysql_container