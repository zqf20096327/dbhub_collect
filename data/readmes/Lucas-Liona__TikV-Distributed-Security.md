# Phase 1: Legacy Key-Value Store & Security Audit

### Overview
This is the baseline architecture for a distributed key-value store, supporting standard `PUT`, `GET`, and `DELETE` operations. 

It was originally built with standard Crash Fault Tolerance (CFT) and at-most-once semantics in mind. The server utilizes TCP via Go's `net/rpc` and `encoding/gob` packages, relying on global Mutex locks to ensure atomic operations. While functionally correct for a trusted environment, this Phase 1 snapshot demonstrates critical security flaws when exposed to a hostile network layer.

### Program Structure
The codebase is divided into two primary domains:
* **Application Layer (`/gateway-go`):**
    * `server.go`: The central KV store engine. Maintains a shared dictionary and a history deduplication table.
    * `client.go`: Simulates concurrent legitimate clients interacting with the store via `.txt` instruction files.
* **Audit Layer (`/attacks`):**
    * `fuzzer.py`: A malicious script designed to test protocol robustness.
    * `state_exhaustion_ddos.go`: An asynchronous exploit targeting the deduplication logic.
    * `legacy_traffic.pcap`: Raw packet capture demonstrating transport vulnerabilities.

### Baseline Concurrency and Synchronization
* **Clients:** Read operational files via the OS package, spawning one goroutine per file. Each maintains an independent TCP connection. Instead of synchronous `client.Call()`, they utilize asynchronous `client.Go()` coupled with `time.After()` select statements to trigger 400ms timeouts and execute up to 3 retries.
* **Server:** Spawns one goroutine per client connection (`rpc.ServeConn()`). Because the server maintains shared state (the KV dictionary and the deduplication history), it relies heavily on a global `sync.Mutex` lock to guarantee operational atomicity and prevent race conditions.

### The Vulnerability Audit (Phase 1 Findings)
The primary focus of this project phase was auditing the legacy assumptions. We successfully executed three attacks:

1.  **Transport Eavesdropping (No Confidentiality):** Standard network traffic was captured via `tcpdump` on the loopback interface (`lo`). Because `net/rpc` lacks encryption, the `.pcap` file proves that all RPC methods and database values are transmitted in plaintext.
2.  **Protocol Confusion (Fuzzing):** By directing `fuzzer.py` to send raw, malformed binary payloads (`\xDE\xAD\xBE\xEF`) directly to the TCP socket, we bypassed standard RPC formatting. The `encoding/gob` decoder panicked upon receiving unvalidated input, abruptly terminating the connection (`Errno 104`) and exposing a potential Denial of Service (DoS) vector.
3.  **State Exhaustion & Resource Starvation (OOM DoS):** To guarantee idempotency, the server caches all previous requests in an unbounded `map[int]map[int]CachedResult`. `state_exhaustion_ddos.go` exploits this by deploying 50 concurrent attackers sending 50MB payloads with spoofed Client IDs. The `net/rpc` framework allocates RAM for these payloads asynchronously *before* acquiring the global Mutex lock, causing rapid memory exhaustion and a kernel-level node crash within 60 seconds.

### Execution & Testing
**To run the legitimate application:**
1. Start the server: `go run server.go`
2. Run standard clients: `go run client.go ops1.txt ops2.txt`

**To run the exploits (against a running server):**
* **Fuzzer:** `python3 attacks/fuzzer.py`
* **State Exhaustion:** `go run attacks/state_exhaustion_ddos.go` (Monitor with `top -p $(pgrep legacy_server)`)

### Roadmap to Phase 2
This baseline proves that application-layer logic (like Mutexes and deduplication maps) cannot substitute for robust network security. Phase 2 will deprecate `net/rpc` in favor of a gRPC/Protobuf API Gateway, decoupling the network listener from the database and implementing TLS encryption.
