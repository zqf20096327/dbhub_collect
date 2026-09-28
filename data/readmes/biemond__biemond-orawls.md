# Oracle WebLogic / Fusion Middleware puppet module V2
[![Build Status](https://travis-ci.org/biemond/biemond-orawls.svg?branch=master)](https://travis-ci.org/biemond/biemond-orawls) ![Puppet Forge Version](https://img.shields.io/puppetforge/v/biemond/orawls.svg) ![Puppet Forge Score](https://img.shields.io/puppetforge/f/biemond/orawls.svg) ![Puppet Forge Downloads](http://img.shields.io/puppetforge/dt/biemond/orawls.svg) [![Code Climate](https://codeclimate.com/github/biemond/biemond-orawls/badges/gpa.svg)](https://codeclimate.com/github/biemond/biemond-orawls) [![Coverage Status](https://coveralls.io/repos/biemond/biemond-orawls/badge.svg?branch=master&service=github)](https://coveralls.io/github/biemond/biemond-orawls?branch=master)

Install, configures and manages WebLogic version 10.3 - 12.2.1

This module should work for all Linux & Solaris versions like RedHat, CentOS, Ubuntu, Debian, Suse SLES, OracleLinux, Solaris 10,11 sparc / x86

Only for Puppet >= 4.3 and this module uses the latest puppet 4 features like

- Strong data typing
- Internal hiera/lookup module data
- uses Facts array
- epp templating instead of erb
- puppet 4 ruby functions

For Puppet 3, 4 you have to use the latest 1.x version of this orawls module

source code is located at [puppet4 branch](https://github.com/biemond/biemond-orawls/tree/puppet4)


Please check the manifests and vagrant examples because there are some breaking changes especially on the manifest part ( I don't do hiera lookups. Just use the weblogic class and I will use those parameters as reference for the other manifest parameters)


## Author

Edwin Biemond email biemond at gmail dot com

[biemond.blogspot.com](http://biemond.blogspot.com)

[Github homepage](https://github.com/biemond/biemond-orawls)

## Contributors

Special thanks to all the contributors

More: https://github.com/biemond/biemond-orawls/graphs/contributors

## Support

If you need support, checkout the [wls_install](https://www.enterprisemodules.com/shop/products/puppet-wls_install-module) and [wls_config](https://www.enterprisemodules.com/shop/products/puppet-wls_config-module) modules from [Enterprise Modules](https://www.enterprisemodules.com/)

[![Enterprise Modules](https://www.enterprisemodules.com/images/puppet-logo.png)](https://www.enterprisemodules.com)

## Dependencies

- hajee/easy_type >=0.10.0
- adrien/filemapper >= 1.1.1
- reidmv/yamlfile >=0.2.0
- fiddyspence/sleep => 1.1.2
- puppetlabs/stdlib => 4.9.0

## Complete vagrant examples

- Docker with WebLogic 12.1.3 Cluster [docker-weblogic-puppet](https://github.com/biemond/docker-weblogic-puppet)
- WebLogic 11g Reference implementation, the vagrant test case for full working WebLogic 10.3.6 cluster example [biemond-orawls-vagrant-puppet4](https://github.com/biemond/biemond-orawls-vagrant-puppet4)
- WebLogic 12.2.1.2 MT multi tenancy / Puppet 4 Reference implementation, the vagrant test case for full working WebLogic 12.2.1 cluster example [biemond-orawls-vagrant-12.2.1-puppet4](https://github.com/biemond/biemond-orawls-vagrant-12.2.1-puppet4)
- WebLogic 12.2.1.2 infra (JRF + JRF restricted), the vagrant test case for full working WebLogic 12.2.1 infra cluster example with WebTier (Oracle HTTP Server) [biemond-orawls-vagrant-12.2.1-infra-puppet4](https://github.com/biemond/biemond-orawls-vagrant-12.2.1-infra-puppet4)
- WebLogic 12.2.1.2 infra (JRF + JRF restricted), the vagrant test case for full working WebLogic 12.2.1 infra SOA Suite/BAM/OSB cluster example [biemond-orawls-vagrant-12.2.1-infra-soa-puppet](https://github.com/biemond/biemond-orawls-vagrant-12.2.1-infra-soa-puppet4)
- WebLogic OHS webtier standalone, the vagrant test case for full working Webtier 12.1.2 and 12.2.1 [biemond-orawls-vagrant-ohs-puppet4](https://github.com/biemond/biemond-orawls-vagrant-ohs-puppet4)
- WebCenter Sites 12.2.1 Reference implementation, the vagrant test case [biemond-orawls-vagrant-12.2.1-infra-wcs-puppet4](https://github.com/biemond/biemond-orawls-vagrant-1

[...截断...]

2.2.1-infra-wcs-puppet4)
- Reference OIM / OAM with WebTier, Webgate & Oracle Unified Directory, the vagrant test case for Oracle Identity Manager & Oracle Access Manager 11.1.2.3 example [biemond-orawls-vagrant-oim_oam-puppet](https://github.com/biemond/biemond-orawls-vagrant-oim_oam-puppet4)
- Reference OIM / OAM Cluster, the vagrant test case for Oracle Identity Manager & Oracle Access Manager 11.1.2.3 cluster example [biemond-orawls-vagrant-oim_oam_cluster](https://github.com/biemond/biemond-orawls-vagrant-oim_oam_cluster)
- Oracle Forms, Reports 11.1.1.7 & 11.1.2 Reference implementation, the vagrant test case [biemond-orawls-vagrant-11g-forms-puppet4](https://github.com/biemond/biemond-orawls-vagrant-11g-forms-puppet4)


## Orawls WebLogic Features

- [Installs WebLogic](#weblogic), version 10g, 11g, 12c ( 12.1.1, 12.1.2, 12.1.3, 12.2.1, 12.2.1.X + FMW infrastructure editions )
- [Apply a BSU patch](#bsu) on a Middleware home ( < 12.1.2 )
- [Apply a OPatch](#opatch) on a Middleware home ( >= 12.1.2 ) or a Oracle product home
- [Opatch upgrade](#opatchupgrade) on a Middleware home ( >= 12.1.2 )
- [Create a WebLogic domain](#domain)
- [Pack a WebLogic domain](#packdomain)
- [Copy a WebLogic domain](#copydomain) to a other node with SSH, unpack and enroll to a nodemanager
- [JSSE](#jsse) Java Secure Socket Extension support
- [Override the default file location, applicable for running as non-root user](#default_override)
- [Custom Identity and Trust Store support](#identity)
- [Linux low on entropy or urandom fix](#urandom)
- [Startup a nodemanager](#nodemanager)
- [start or stop AdminServer, Managed or a Cluster](#control)
- [StoreUserConfig](#storeuserconfig) for storing WebLogic Credentials and using in WLST
- [Dynamic targetting](#Dynamictargetting) by using the notes field in WebLogic for resource targetting
- 12.2.1 Multi Tenancy features

### Fusion Middleware Features 11g & 12c

- installs [FMW](#fmw) software(add-on) to a middleware home, like OSB,SOA Suite, Oracle Identity & Access Management, Oracle Unified Directory, WebCenter Portal + Content
- [WebTier](#webtier) Oracle HTTP server Standalone and Collocated
- [Configure Oracle HTTP Server](#configure-oracle-http-server)
- [OSB, SOA Suite](#fmwcluster) with BPM and BAM Cluster configuration support ( convert single osb/soa/bam servers to clusters and migrate 11g OPSS to the database )
- [ADF/JRF support](#fmwclusterjrf), Assign JRF libraries to a Server or Cluster target
- [OIM IDM](#oimconfig) / OAM 11.1.2.3 configurations with Oracle OHS OAM WebGate, Also it has Cluster support for OIM OAM
- [OUD](#instance) OUD Oracle Unified Directory install, WebLogic domain, instances creation & [OUD control](#oud_control)
- [Forms/Reports](#forms) Oracle Forms & Reports 11.1.1.7, 11.1.2 or 12.2.1
- [WC, WCC, WCS](#Webcenter) Webcenter portal, content, sites 11g or 12.2.1
- [Change FMW log](#fmwlogdir) location of a managed server
- [Resource Adapter](#resourceadapter) plan and entries for AQ, DB, MQ, FTP, File and JMS

## Wls types and providers

This will use WLST to retrieve the current state and to the changes. With WebLogic 12.2.1 we can also use the rest management api's, it's already working in this module but we will slowly support this for all wls types

- [wls_setting](#wls_setting), set the default wls parameters for the other types and also used by puppet resource
- [wls_adminserver](#wls_adminserver) control the adminserver or subscribe to changes
- [wls_managedserver](#wls_managedserver) control the managed server,cluster or subscribe to changes
- [wls_ohsserver](#wls_ohsserver) control the ohs standalone server or subscribe to changes
- [wls_domain](#wls_domain)
- [wls_deployment](#wls_deployment)
- [wls_domain](#wls_domain)
- [wls_group](#wls_group)
- [wls_role](#wls_role)
- [wls_user](#wls_user)
- [wls_authentication_provider](#wls_authentication_provider)
- [wls_identity_asserter](#wls_identity_asserter)
- [wls_machine](#wls_machine)
- [wls_server](#wls_