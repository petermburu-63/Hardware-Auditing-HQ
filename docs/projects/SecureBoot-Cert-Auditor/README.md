# Secure Boot Certificate Auditor

> **Project brief · Work in progress · v0.1.0**

A read-only PowerShell auditing project for inspecting UEFI Secure Boot certificate state and producing JSON and HTML reports. This project is a focused part of the hardware and firmware auditing work in Hardware-Auditing-HQ.

This document summarizes the project information supplied by the author. It is a project brief, not the implementation. Status and test claims below have not been independently verified in this repository.

## Why it matters

Microsoft's Secure Boot certificate refresh replaces certificates issued in 2011 with newer certificates issued in 2023. The 2011 certificate lifecycle schedule reaches dates in 2026; as those dates have passed or may be changing in current servicing guidance, verify the latest Microsoft documentation and device-specific rollout information before making claims about impact or urgency.

Microsoft documentation:

- [Update Secure Boot Certificates for Windows Devices](https://learn.microsoft.com/en-us/troubleshoot/windows-client/windows-security/update-secure-boot-certificates)
- [When Secure Boot certificates expire on Windows devices](https://support.microsoft.com/en-us/servicing/os/secure-boot/2026/02/when-secure-boot-certificates-expire-on-windows-devices)
- [Windows Production CA 2011 expiration and bootloader updates](https://support.microsoft.com/en-us/servicing/os/secure-boot/2026/10/kb5132953-windows-production-ca-2011-expiration-bootloader-updates)

Certificate state and servicing behavior can depend on Windows version, firmware, OEM updates, and configuration. This auditor is intended to report observations, not to apply changes or replace Microsoft's or an OEM's supported guidance.

## Planned / reported checks

| Check | Described method |
| --- | --- |
| Secure Boot state | `Confirm-SecureBootUEFI` |
| KEK and `db` content | `Get-SecureBootUEFI`, followed by a custom EFI signature-list parser and certificate inspection |
| Certificate generation | Subject matching against a known-certificate table for 2011 and 2023 generations |
| Certificate validity window | Read `NotAfter` from the certificate; informational only |
| TPM and BitLocker | `Get-Tpm` and `Get-BitLockerVolume` |
| VBS, HVCI, and Credential Guard | CIM `Win32_DeviceGuard` |
| Servicing state | Registry values, informational only and subject to verification against current Microsoft documentation |
| Machine context | Model, BIOS version/date, and OS build |

### Verdict intent

| Verdict | Intended interpretation |
| --- | --- |
| **GREEN** | The project-defined 2023 certificate set is present in the expected databases |
| **AMBER** | Secure Boot is enabled but one or more expected newer certificates are missing; review supported firmware and Windows servicing guidance |
| **RED** | Secure Boot is disabled |
| **N/A** | The check is unsupported or state could not be collected, such as legacy boot or insufficient privileges |

A verdict is an audit summary, not proof of boot-chain integrity or device security. Certificate presence alone does not establish that all relevant boot components, revocation data, or servicing updates are current.

## Read-only safety boundary

The project is intended only to read firmware variables and system state. It must not write UEFI variables, alter Secure Boot keys, change registry settings, or make network requests. Inspect the source and verify these properties before running any build. Do not modify Secure Boot settings without understanding the device-specific recovery path and following supported OEM/Microsoft instructions.

Reports may contain device model, BIOS details, and certificate thumbprints. Review and redact sensitive machine information before sharing reports publicly.

## Usage described by the project brief

Requires a supported Windows system using UEFI Secure Boot and an elevated PowerShell session for the relevant probes. Exact script options may change; verify them against the implementation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\Invoke-SecureBootAudit.ps1 -OutDir .\out
```

## Parser overview

UEFI signature databases contain packed `EFI_SIGNATURE_LIST` structures. The supplied project description says the parser walks lists and entries, handles X.509 data as certificates, and preserves non-X.509 entries as hexadecimal previews. Malformed sizes and unsupported structures should be handled safely; inspect the implementation and tests before relying on parser output.

## Status reported by the author

The supplied project README reports a parser, certificate classification, verdict logic, and JSON/HTML report generation, exercised with synthetic signature lists on PowerShell 7.4 on Linux. It reports that the Pester test suite has been written but not yet run. This status has not been independently verified in this repository.

Live firmware reads on Windows hardware, servicing registry values across Windows builds, and HP-specific tooling were identified as needing validation. Planned follow-up includes `dbx` analysis, optional HP CMSL inventory, fleet reporting, audit diffs, and Windows CI for Pester.

## Limitations

- Requires UEFI firmware and may require administrator privileges; unsupported states should be reported as unavailable rather than guessed.
- Subject-name matching is a heuristic and can require updates if certificate naming or trust arrangements change.
- Certificate expiry and presence should be interpreted using current Microsoft and OEM guidance, not in isolation.
- Third-party bootloaders may depend on different trust anchors; validate a specific configuration before taking action.
- A GREEN result does not prove that the entire boot chain or device is secure.

## Tests, license, and author

The supplied project brief gives this test command; run it from the actual project source directory and check current Pester installation guidance:

```powershell
Install-Module Pester -MinimumVersion 5.0 -Scope CurrentUser
Invoke-Pester .\tests
```

The supplied brief states MIT; see the source project's license file for the applicable terms.  
Peter M. Mburu — IT & Cybersecurity student, Kenya.
