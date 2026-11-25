<div align="center">

# Linux Infrastructure Lab

**12 real-world infrastructure projects on openEuler and openGauss, built, broken and rebuilt in a private virtual lab.**

![openEuler](https://img.shields.io/badge/OS-openEuler-c7000b)
![Database](https://img.shields.io/badge/DB-openGauss%20%7C%20MySQL-blue)
![Projects](https://img.shields.io/badge/projects-12-success)
![Status](https://img.shields.io/badge/status-in%20progress-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

## What this is

Each project solves a problem a real organization has: hosting websites, protecting data, keeping services up when a server fails, deploying machines automatically. Every project ships with a charter, an architecture diagram, pass or fail requirements, a rebuild runbook, a failure drill with timings, and evidence that it works.

Built while studying the Huawei HCIA/HCIP openEuler and openGauss track, with AI-assisted tooling used under written rules (see [AGENTS.md](AGENTS.md)).

## Projects

| # | Project | Skills | Status |
| --- | --- | --- | --- |
| P1 | [Web hosting and DNS server](p1-web-dns/) | Apache, NGINX, BIND, TLS, MySQL, firewalld, SELinux | In progress (M1 of 8 done) |
| P2 | File storage and automated backup | LVM, RAID, Samba, NFS, rsync, cron | Planned |
| P3 | Infrastructure monitoring platform | Zabbix, Bash, alerting | Planned |
| P4 | Automated server deployment | Ansible, YAML, Git | Planned |
| P5 | High-availability web hosting | HAProxy, Keepalived, LVS, GlusterFS | Planned |
| P6 | Database replication and failover | MySQL or openGauss, backups, failover | Planned |
| P9 | Security and intrusion detection | auditd, AIDE, OpenSCAP, SELinux | Planned |
| P7 | University virtual computer lab | KVM, libvirt, virtual networks | Planned |
| P12 | Small business cloud platform | Integration of P1 to P5 and P7 | Planned |
| P8 | Private cloud | OpenStack | Planned |
| P10 | Distributed data processing | Hadoop, HDFS, MapReduce | Planned |
| P11 | Intelligent resource optimization | Python, machine learning | Planned |

## How every project is built

1. **Charter:** the problem, scope, risks and success criteria, written first.
2. **Requirements:** each one has a command and an expected result.
3. **Build in milestones:** one snapshot and one Git commit per milestone.
4. **Failure drill:** break it on purpose, recover it, record the time.
5. **Runbook:** a stranger can rebuild it from the template VM.

## Repository layout

```text
infra-projects/
  AGENTS.md            rules for the coding agent
  p1-web-dns/
    docs/              charter, architecture, requirements, milestones, drills
    configs/           configuration files copied from the servers
    scripts/           automation and verify.sh
    evidence/          screenshots, logs, timings
    runbook.md         rebuild steps
```

## Lab

All work runs in VirtualBox on openEuler 24.03 LTS (SP3), on virtual machines on a private network (192.168.56.0/24, domain `angaspace.lan`). Nothing is exposed to the internet. Attacks and scans are run only against my own lab machines.

## Progress

- [x] P1 M1: base setup, fixed IPs, key-only SSH ([evidence](p1-web-dns/evidence/m1-r1-r2-r3.txt))
- [ ] P1 M2 to M8: Apache, NGINX, BIND, TLS, MySQL, hardening, drills

## About

Built by George Robert Thobias, Huawei Club Academy. Computing track: openEuler HCIA/HCIP and openGauss.
Contact: add your email or LinkedIn link here.
