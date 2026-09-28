
<a href="https://rapidfort.com?utm_source=github&utm_medium=ci_rf_link&utm_campaign=sep_01_sprint&utm_term=ci_main_landing&utm_content=main_landing_logo">
<img src="/contrib/github_logo.png" alt="RapidFort" width="200" />
</a>

<h1> community-images </h1>

[![RF Hardened][rf-h-badge]][rf-link-hardened-badge]
[![Dockerhub][dh-rf-badge]][dh-rf]
[![Slack][slack-badge]][slack-link]
[![License][license-badge]][license]
[![FOSSA Status][fossa-badge]][fossa-link]
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6087/badge)](https://bestpractices.coreinfrastructure.org/projects/6087)
[![CodeQL](https://github.com/rapidfort/community-images/actions/workflows/codeql.yml/badge.svg)](https://github.com/rapidfort/community-images/actions/workflows/codeql.yml)

<b>Near Zero CVE images available at <a style="color:blue;" href="https://hub.rapidfort.com/repositories">hub.rapidfort.com/repositories</a></b>


[Getting started](#getting-started) ·
[Supported containers](#supported-containers) ·
[Contributing](CONTRIBUTING.md) ·
[Build Process](#how-community-images-are-built) ·
[Additional resources](#additional-resources)

**RapidFort is a solution for building secure, optimized Docker containers.**

RapidFort provides free, <b>Hardened Images</b> on its GitHub community page, empowering developers to build secure and reliable applications effortlessly. These <b>Hardened Images</b> are optimized versions of popular base images, significantly reducing vulnerabilities and attack surfaces. Leveraging its innovative optimization and vulnerability management tools, RapidFort analyzes container images, removes unnecessary components, and ensures that only essential, secure elements remain. This proactive approach removes most of Common Known Vulnerabilities (CVEs), minimizes potential entry points for attackers, enhances compliance, and improves overall security posture.

To explore RapidFort's <b>Near-Zero CVE Curated Images</b> (and start building with confidence, visit [hub.rapidfort.com](hub.rapidfort.com).

RapidFort’s RapidFort Platform and Near-Zero CVE Curated Images remediate 95% of software vulnerabilities.

For more information please visit [rapidfort.com](rapidfort.com).



## Getting Started

![Demo][demo]

[RapidFort][rf-link-getting-started] scans your Docker containers for vulnerabilities and looks for unused components that can be removed.

<h2 id="supported-containers">What containers are supported?</h2>

We’ve optimized and hardened some of the most popular container images on Docker Hub and are making them available to the community.

| Repository                        | View Report                                   | RapidFort Image                     | Pull Count |
|-----------------------------------| ------------------------------------------     | ------------------------------- | ------------------------------- |
| [PostgreSQL Official][ postgresql-official-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/docker.io%2Flibrary%2Fpostgres?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=postgresql-official&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/postgresql-official"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 348,410 </b> |
| [Fluent-Bit Ironbank][ fluent-bit-ib-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/registry1.dso.mil%2Fironbank%2Fopensource%2Ffluent%2Ffluent-bit?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=fluent-bit-ib&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/fluent-bit-ib"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 273,166 

[...截断...]

</b> |
| [MongoDB® Official][ mongodb-official-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/docker.io%2Flibrary%2Fmongo?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=mongodb-official&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/mongodb-official"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 221,771 </b> |
| [HAProxy Official][ haproxy-official-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/docker.io%2Flibrary%2Fhaproxy?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=haproxy-official&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/haproxy-official"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 200,200 </b> |
| [NGINX IronBank][ nginx-ib-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/registry1.dso.mil%2Fironbank%2Fopensource%2Fnginx%2Fnginx?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=nginx-ib&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/nginx-ib"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 195,914 </b> |
| [NGINX Official][ nginx-official-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/docker.io%2Flibrary%2Fnginx?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=nginx-official&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/nginx-official"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 191,641 </b> |
| [Microsoft SQL Server 2019][ microsoft-sql-server-2019-ib-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/registry1.dso.mil%2Fironbank%2Fmicrosoft%2Fmicrosoft%2Fmicrosoft-sql-server-2019?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=microsoft-sql-server-2019-ib&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/microsoft-sql-server-2019-ib"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 166,953 </b> |
| [Redis™ Official][ redis-official-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/docker.io%2Flibrary%2Fredis?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=redis-official&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/redis-official"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 154,660 </b> |
| [Redis™ IronBank][ redis-ib-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/registry1.dso.mil%2Fironbank%2Fopensource%2Fredis%2Fredis6?utm_source=github&utm_medium=ci_view_report&utm_campaign=sep_01_sprint&utm_term=redis-ib&utm_content=landing_get_full_report_button"> <img src="/contrib/full_report_sm.svg" alt="View Report" height="25" /> </a> | <a href="https://hub.docker.com/r/rapidfort/redis6-ib"> <img src="/contrib/view_dockerhub_sm.svg" alt="View on Dockerhub" height="25" /> </a> | <b> 144,348 </b> |
| [Consul IronBank][ consul-ib-github-link]| <a href="https://us01.rapidfort.com/app/community/imageinfo/registry1.dso.mil%2Fironbank%2Fhashicorp%2Fconsul?utm_source=github