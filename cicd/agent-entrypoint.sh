#!/bin/bash
set -e

echo "==> Attente de Jenkins ($JENKINS_URL)..."
until wget -qO- --http-user="$JENKINS_USER" --http-password="$JENKINS_PASSWORD" \
    "$JENKINS_URL/api/json" > /dev/null 2>&1; do
    echo "Jenkins pas encore pret, nouvelle tentative dans 10s..."
    sleep 10
done

echo "==> Jenkins disponible, recuperation du secret pour '$JENKINS_AGENT_NAME'..."
SECRET=""
while [ -z "$SECRET" ]; do
    SECRET=$(wget -qO- --http-user="$JENKINS_USER" --http-password="$JENKINS_PASSWORD" \
        "$JENKINS_URL/computer/$JENKINS_AGENT_NAME/slave-agent.jnlp" 2>/dev/null | \
        grep -oE '[a-f0-9]{64}' | head -1 || true)
    if [ -z "$SECRET" ]; then
        echo "Secret non disponible (noeud pas encore cree?), nouvelle tentative dans 10s..."
        sleep 10
    fi
done

echo "==> Demarrage de l'agent '$JENKINS_AGENT_NAME'..."
exec java -jar /usr/share/jenkins/agent.jar \
    -url "$JENKINS_URL" \
    -name "$JENKINS_AGENT_NAME" \
    -secret "$SECRET" \
    -workDir /home/jenkins/agent
