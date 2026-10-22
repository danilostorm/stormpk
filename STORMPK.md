# StormPK — Priston Tale EU

Fresh replacement of the old Etervale implementation, based on the
[dwSize-PE/PristonTale-EU-main](https://github.com/dwSize-PE/PristonTale-EU-main)
Windows/C++ source code. Upstream attribution is preserved in README.md.

**Build:** Visual Studio 2022 (MSVC v143), Windows SDK and platform Win32.
The game and server projects build native DLLs and need the matching
Windows executables from the supplied game files. The server uses
Microsoft SQL Server (ODBC). This is not the former .NET/Docker game.

**AEROCOOL local source:** `/mnt/user/appdata/stormpk`.

**User-supplied installer:** `/mnt/user/Games/install/StormPK/Files.7z`.
This archive contains Windows game data, server binaries and database
backups. Never commit proprietary game data, SQL backups, credentials,
or other deployment secrets to GitHub.

Do not start the new EU game with the previous Etervale client.
