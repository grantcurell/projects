#!/bin/bash

# Check if the hosts file is provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <hosts_file>"
  exit 1
fi

# File containing hostnames, one per line
HOSTS_FILE=$1

# Check if the hosts file exists
if [ ! -f "$HOSTS_FILE" ]; then
  echo "Hosts file not found: $HOSTS_FILE"
  exit 1
fi

# Path to the installation files
BASEKIT_FILE="l_BaseKit_p_2024.2.1.100_offline.sh"
HPCKIT_FILE="l_HPCKit_p_2024.2.1.79_offline.sh"

# Check if the installation files exist locally
if [ ! -f "$BASEKIT_FILE" ] || [ ! -f "$HPCKIT_FILE" ]; then
  echo "Installation files not found."
  exit 1
fi

# Function to handle each host
process_host() {
  local host=$1

  echo "Processing host: $host"

  # Check if the installation files already exist on the remote host
  ssh $host "[ -f ~/l_BaseKit_p_2024.2.1.100_offline.sh ] && [ -f ~/l_HPCKit_p_2024.2.1.79_offline.sh ]"
  
  if [ $? -eq 0 ]; then
    echo "Files already exist on $host. Skipping."
    return
  fi

  # Copy the installation files to the remote host
  echo "Copying installation files to $host..."
  scp $BASEKIT_FILE $HPCKIT_FILE $host:~/

  # Check if scp was successful
  if [ $? -ne 0 ]; then
    echo "Failed to copy files to $host. Skipping."
    return
  fi

  # Execute the installation scripts on the remote host
  echo "Executing installation scripts on $host..."
  ssh $host "sh ~/l_BaseKit_p_2024.2.1.100_offline.sh -a --silent --cli --eula accept && \
             sh ~/l_HPCKit_p_2024.2.1.79_offline.sh -a --silent --cli --eula accept"

  # Check if the installation was successful
  if [ $? -ne 0 ]; then
    echo "Installation failed on $host."
  else
    echo "Installation completed successfully on $host."
  fi
}

# Process each host in parallel
while IFS= read -r host; do
  process_host $host &
done < "$HOSTS_FILE"

# Wait for all parallel jobs to finish
wait

echo "All tasks completed."
