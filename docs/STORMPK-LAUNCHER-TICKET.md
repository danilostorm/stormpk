# StormPK Launcher Gate — SOURCE ONLY (not deployed)

The current server checks `PacketLoginUser.iVersion == GAME_VERSION (1309)`, which does **not** prove launch via official launcher. For stronger friction against old clients, a future build can opt in to `STORMPK_REQUIRE_LAUNCH_PROOF` on **both** client and Login Server:

- Launcher requests short-lived (60–90s), 96-bit cryptographically random, single-use ticket via an authenticated HTTPS issuer with IP/account rate limits.
- Launcher launches `Game.exe` with environment variable `STORMPK_LAUNCH_PROOF` set to 24 hex characters; launcher should clear its own secret copy and **not** persist in logs or files.
- Source in `GameCore::SendLoginData` packs the 12 bytes into previously zeroed `PacketLoginUser.dwUnk[3]`; no packet size change.
- Login Server source consumes the token via an **atomic** DELETE OUTPUT from `ServerDB.dbo.StormPKLauncherTickets` (hash match, expiration checked), BEFORE invoking PHAccountLogin. Expired/reused/missing proofs are rejected.

Prerequisites: Windows C++ build toolchain, SQL table + restricted ticket issuer API, staging integration test with two-client race, old/new client version rollout, backup of old executables, and emergency rollback. Do not define `STORMPK_REQUIRE_LAUNCH_PROOF` until all are operational. No token issuance URL is currently published and Login Server in production is unchanged.

**Limits:** anyone controls their own client computer. Without hardware-backed remote attestation it is not possible to prove that a user did not run a modified game binary or third-party launcher. The ticket system prevents basic direct launch/replay and strengthens update compliance, but does not provide perfect anti-tamper security. A public anonymous ticket issuer would make bypass easier; authentication and abuse controls matter.

**IMPORTANT:** Do not enable in production from these source changes alone: server binaries were not compiled/tested on Windows; no ticket issuer or SQL table have been installed. Existing players continue to use login version 1309. The code is staged on a feature branch only.
