#!/bin/bash

PROD_USER="root"
SSH_HOST="5.182.18.114"
PROD_FOLDER="/home/news_radar"

echo "Starting Manual Deploy"
sleep 1

# Suppression du dossier local dist s'il existe
rm -rf dist

# Clonage du dépôt
git clone git@github.com:arkansoap/news_radar.git dist/
rm -rf dist/.git

# Copie du fichier .env.prod
cp -f .env.prod dist/.env || exit

# Suppression du dossier distant news_radar
ssh $PROD_USER@$SSH_HOST "rm -rf $PROD_FOLDER"

# Synchronisation des nouveaux fichiers
rsync -av --progress dist/ $PROD_USER@$SSH_HOST:$PROD_FOLDER

# Configuration de l'environnement
ssh $PROD_USER@$SSH_HOST << EOF
    cd $PROD_FOLDER
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
EOF

echo "Manual Deploy Done"
