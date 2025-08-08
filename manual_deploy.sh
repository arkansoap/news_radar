# Serveur perso
PROD_USER="root"
SSH_HOST="5.182.18.114"
PROD_FOLDER="/home/news_radar"



echo "Starting Manual Deploy"
sleep 1

rm -rf dist
git clone git@github.com:ReworldMedia/news_radar.git dist/
rm -rf dist/.git
cp -f .env.prod dist/.env || exit

# Synchronize the new files
rsync -av --progress dist/ $PROD_USER@$SSH_HOST:$PROD_FOLDER

# Set up the environment
ssh $PROD_USER@$SSH_HOST << EOF
    cd $PROD_FOLDER
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
EOF

echo "Manual Deploy Done"