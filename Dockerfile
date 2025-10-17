
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7
# Tutorial https://docs.docker.com/guides/python/containerize/
# Exammple https://docs.docker.com/reference/samples/python/

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV MPLCONFIGDIR=/tmp

ENV XDG_RUNTIME_DIR=/tmp
ENV QT_QPA_PLATFORM=xcb
#ENV  QT_QPA_PLATFORM=wayland
#ENV XDG_SESSION_TYPE=x11
#ENV DISPLAY=


WORKDIR /.

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# native graphical liberary 
# commented out until the issue is sorted see app.py comments 
#RUN  apt update && apt upgrade -y &&  apt install -y libx11-6 libxext-dev  libxrender-dev libxinerama-dev \
#      libxi-dev libxrandr-dev libxcursor-dev libxtst-dev libglib2.0-0 \
#      libgl1-mesa-glx libxkbcommon-x11-0 libegl1 libfontconfig1 libdbus-1-3 \
#      libxcb-cursor0 

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
   

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY ./src .

# Expose the port that the application listens on.
#EXPOSE 8000

# Run the application by executing the python module (file)
CMD ["python3", "-m", "app", "-s=Y"]
