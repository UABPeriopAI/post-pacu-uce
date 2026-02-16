# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.224.2/containers/python-3-miniconda/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.11-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}


# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="lts/*"
RUN if [ "${NODE_VERSION}" != "none" ]; then \
        su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1 && corepack enable && corepack prepare yarn@stable --activate"; \
    fi

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends sqlite3 \
    && apt-get -y install --no-install-recommends git-flow \
    && apt-get -y install --no-install-recommends mkdocs \
    && apt-get -y install --no-install-recommends cmake \
    && rm -rf /var/lib/apt/lists/*

# Setup R
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends dirmngr gnupg apt-transport-https ca-certificates software-properties-common \
    && apt-get install -y --no-install-recommends r-base \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R vscode:vscode /usr/local/lib/R/site-library

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
 COPY docs/dev_requirements.txt /tmp/pip-tmp/
 RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/dev_requirements.txt \
    && rm -rf /tmp/pip-tmp
    
USER vscode 

# [Optional] If your R requirements rarely change, uncomment this section to add them to the image.
RUN mkdir -p /tmp/r
COPY docs/packages.sh /tmp/r
RUN /bin/bash /tmp/r/packages.sh && rm -rf /tmp/r
