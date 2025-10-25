FROM telegraf:1.28

# Install Python3 for the XML parser script
RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*

# The config and script will be mounted as volumes
