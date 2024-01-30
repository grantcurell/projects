# Notes on HSM

## How Does HSM for Manufacturing Work?

The process of creating a trusted baseline of the server's firmware and hardware components involves measuring the components and creating a hash of the measurements.

The measurements can be taken at various stages of the server's lifecycle, such as during manufacturing, configuration, or deployment. The measurements can include data such as the firmware version, BIOS settings, boot configuration, hardware components, and other system settings. These measurements are then stored securely in a trusted repository, such as an HSM.

When the server is booted up, the measurements of the current firmware and hardware components are taken and hashed. These current measurements are then compared to the measurements stored in the trusted repository. If the current measurements match the trusted baseline, it indicates that the server is running in a trusted state and has not been tampered with. If the measurements do not match, it suggests that the firmware or hardware components have been modified, and the server may not be running in a trusted state.

Overall, the process of creating a trusted baseline, measuring the firmware and hardware components, and comparing them to the trusted baseline is used to ensure the integrity and authenticity of the server's components, and to provide assurance that the server is running in a trusted state. This is an important part of a security strategy, particularly in environments where data security and privacy are critical.