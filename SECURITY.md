# Security and sensitive deployment data

This app has host networking, USB/debug access and network administration
permissions because it initializes the radio and configures border routing.
Install only source/images you trust. It is experimental and has no promised
security response SLA.

Keep OTBR REST/web ports disabled by default. They provide network-management
access without a Home Assistant login. Do not expose them to the internet.
Debugger TCP ports stay disabled. Select the intended board explicitly.

Never post Thread datasets, Matter fabric storage/setup codes, HA access tokens,
private SSH keys, complete flash readbacks or HA backups in public issues.
`.gitignore` and repository checks help prevent accidental inclusion; review
every staged change before publishing.

For a vulnerability, use the Git host's private vulnerability reporting feature
if enabled. If it is unavailable, open an issue asking for a private contact
without including exploit details or credentials. This local repository has no
public reporting endpoint yet. Until a fix is available, disable exposed ports
and stop the app if the vulnerability requires it.
