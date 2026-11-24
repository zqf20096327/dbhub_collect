<h1 align="center">cvewatch</h1> <p align="center"> <b>Automated CVE tracking for Linux hosts.</b><br> Know every morning which of your servers are vulnerable, which three findings matter, and get an alert only when something new does. </p> <p align="center"> <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-3776AB"> <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2DD4BF"> <img alt="Agentless over SSH" src="https://img.shields.io/badge/agentless-SSH-F97316"> <img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-4ADE80"> </p> <p align="center"></p>


<h1 align="center">cvewatch</h1>

<p align="center">
  <b>Automated CVE tracking for Linux hosts.</b><br>
  Know every morning which of your servers are vulnerable, which three findings matter, and get an alert only when something new does.
</p>

<hr>

<p>cvewatch collects the installed packages of every host you list, locally or <strong>agentless over SSH</strong>. It looks them up in <strong><a href="https://osv.dev">OSV.dev</a></strong>, which carries the security data of Debian, Ubuntu, AlmaLinux, Rocky Linux and Alpine, including backported fixes. Every CVE is enriched with the <strong><a href="https://www.cisa.gov/known-exploited-vulnerabilities-catalog">CISA KEV</a></strong> catalogue and <strong><a href="https://www.first.org/epss/">FIRST EPSS</a></strong> scores and ranked <strong>P1 to P4</strong> by exploitation, exposure, severity and fix availability. History is kept in <strong>SQLite</strong>. Each scan writes an <strong>HTML/CSV/JSON report</strong> and <strong>Prometheus metrics</strong>, and new P1/P2 findings are sent to <strong>ntfy, a webhook or email</strong>.</p>
<p>One Python file. Standard library only. Read-only on the hosts it checks.</p>
<h2 id="contents">Contents</h2>
<ul>
<li><a href="#why-cvewatch">Why cvewatch</a></li>
<li><a href="#features">Features</a></li>
<li><a href="#quick-start">Quick start</a></li>
<li><a href="#how-it-works">How it works</a></li>
<li><a href="#prioritisation">Prioritisation</a></li>
<li><a href="#scanning-remote-hosts">Scanning remote hosts</a></li>
<li><a href="#configuration">Configuration</a></li>
<li><a href="#commands">Commands</a></li>
<li><a href="#supported-systems">Supported systems</a></li>
<li><a href="#files">Files</a></li>
<li><a href="#security-model">Security model</a></li>
<li><a href="#network-and-privacy">Network and privacy</a></li>
<li><a href="#limitations">Limitations</a></li>
<li><a href="#faq">FAQ</a></li>
<li><a href="#contributing">Contributing</a></li>
<li><a href="#licence">Licence</a></li>
</ul>
<h2 id="why-cvewatch">Why cvewatch</h2>
<p><code>unattended-upgrades</code> and <code>dnf-automatic</code> install fixes. They do not tell you:</p>
<ul>
<li><strong>which hosts are affected</strong> when a serious CVE is published,</li>
<li>whether updates actually <strong>installed</strong> and whether the running kernel is the patched one,</li>
<li><strong>what to fix first</strong> among hundreds of open CVEs,</li>
<li>whether things are <strong>getting better</strong> over time.</li>
</ul>
<p>Network scanners see ports and banners, not package versions. Commercial vulnerability platforms cost money per asset. cvewatch fills the gap for home labs, small teams and anyone who wants a transparent, auditable tool they can read in an afternoon.</p>
<h2 id="features">Features</h2>
<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Inventory</strong></td>
<td>dpkg, rpm and apk packages, source package names, running kernel, reboot-required state, pending security updates</td>
</tr>
<tr>
<td><strong>Matching</strong></td>
<td>OSV.dev querybatch with distro ecosystems (<code>Ubuntu:24.04:LTS</code>, <code>Debian:13</code>, <code>AlmaLinux:9</code>, ...), native dpkg and rpm version comparison</td>
</tr>
<tr>
<td><strong>Enrichment</strong></td>
<td>CISA KEV (incl. ransomware flag), FIRST EPSS, CVSS 3.x base score and attack vector</td>
</tr>
<tr>
<td><strong>Prioritisation</strong></td>
<td>P1-P4 from KEV, EPSS, exposure, attack vector, severity, fix availability and host criticality</td>
</tr>
<tr>
<td><strong>Collection</strong></td>
<td>local, SSH push mode (nothing installed on targets), SSH installed mode, offline <code>file:</code> inventories</td>
</tr>
<tr>
<td><strong>Least privilege</strong></td>
<td>dedicated <code>cvewatch</code> user, SSH key restricted to one forced command and the scanner's IP</td>
</tr>
<tr>
<td><strong>History</strong></td>
<td>SQLite: first seen, resolved, reopened, mean time to remediate</td>
</tr>
<tr>
<td><strong>Exceptions</strong></td>
<td>accepted risks in a CSV with expiry dates</td>
</tr>
<tr>
<td><strong>Output</strong></td>
<td>static HTML report with filters, CSV, JSON summary, Prometheus textfile metrics</td>
</tr>
<tr>
<td><strong>Alerts</strong></td>
<td>ntfy (phone push), generic webhook (Slack, Teams, Discord, Mattermost), email; only new P1/P2 by default</td>
</tr>
<tr>
<td><strong>Operations</strong></td>
<td>hardened systemd service and timer, <code>--fail-on</code> exit codes for CI gates, offline self-test</td>
</tr>
</tbody>
</table>
<h2 id="quick-start">Quick start</h2>
<p>On the machine that will be the <strong>scanner</strong> (Debian/Ubuntu/RHEL family, Python 3.8+):</p>
<pre><code class="language-bash">git clone https://github.com/&lt;your-account&gt;/cvewatch.git
cd cvewatch
sudo ./install.sh                          # program, user, config, SSH key, self-test, daily timer
sudo -u cvewatch cvewatch scan --local-only
sudo -u cvewatch cvewatch status
</code></pre>
<p>Open the report at <code>/var/lib/cvewatch/reports/cvewatch-report.html</code>.</p>
<p>Try it without installing anything. The self-test runs offline with demo data:</p>
<pre><code class="language-bash">python3 cvewatch.py selftest
</code></pre>
<h2 id="how-it-works">How it works</h2>
<pre><code> hosts.ini ──► collect ──► OSV.dev ──► KEV + EPSS ──► prioritise ──► SQLite ──► report + alerts
   local        dpkg/rpm/apk   distro      exploited?     P1..P4         history     HTML · CSV · JSON
   SSH          kernel         security    likely?                       resolved?   Prometheus
   file:        reboot flag    data                                                  ntfy · webhook · mail
</code></pre>
<ol>
<li><strong>Collect</strong> the package inventory of each host (read-only).</li>
<li><strong>Match</strong> source packages against OSV.dev distro data. Versions are compared with real dpkg/rpm rules, so backported fixes such as <code>3.0.13-0ubuntu3.4</code> are handled correctly.</li>
<li><strong>Enrich</strong> each CVE with KEV, EPSS and the CVSS vector.</li>
<li><strong>Prioritise</strong> P1 to P4 (see below), apply exceptions.</li>
<li><strong>Remember</strong> in SQLite: new, still open, resolved, reopened.</li>
<li><strong>Report and alert</strong>: rewrite the reports, send one message per channel for new P1/P2 findings and failed hosts.</li>
</ol>
<h2 id="prioritisation">Prioritisation</h2>
<table>
<thead>
<tr>
<th>Priority</th>
<th>Rule</th>
<th>Suggested target</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>P1</strong></td>
<td>(in KEV <strong>or</strong> EPSS ≥ 0.5) <strong>and</strong> host exposure is <code>internet</code> <strong>and</strong> the attack vector is not local/physical</td>
<td>48 hours</td>
</tr>
<tr>
<td><strong>P2</strong></td>
<td>in KEV, <strong>or</strong> EPSS ≥ 0.1, <strong>or</strong> (CVSS ≥ 9 <strong>and</strong> exposed <strong>and</strong> a fix exists)</td>
<td>7 days</td>
</tr>
<tr>
<td><strong>P3</strong></td>
<td>CVSS ≥ 7 <strong>and</strong> a fix exists</td>
<td>30 days</td>
</tr>
<tr>
<td><strong>P4</strong></td>
<td>everything else</td>
<td>next maintenance</td>
</tr>
</tbody>
</table>
<p>Hosts with <code>criticality = high</code> move every finding up one level. The EPSS thresholds are configurable (<code>[priority] p1_epss</code>, <code>p2_epss</code>).</p>
<p>Local privilege-escalation bugs (<code>AV:L</code>) never count as "exposed" on their own, so an exploited kernel EoP on a web server is P2, not P1. On a high-criticality host it becomes P1.</p>
<h2 id="scanning-remote-hosts">Scanning remote hosts</h2>
<p>cvewatch is agentless. In the default <strong>push</strong> mode the scanner pipes the collector to <code>python3 -</code> over SSH, so nothing is installed on the target.</p>
<p><strong>1. On each target</strong>, authorise the scanner's key for one command only:</p>
<pre><code class="language-bash">sudo ./setup-target.sh &quot;$(cat scanner_key.pub)&quot; 192.168.10.5
</code></pre>
<p>This creates a <code>cvewatch</code> user with a locked password and adds the key as:</p>
<pre><code>from=&quot;192.168.10.5&quot;,restrict,command=&quot;/usr/bin/python3 /usr/local/lib/cvewatch/cvewatch.py collect&quot; ssh-ed25519 AAAA...
</code></pre>
<p>The key cannot open a shell, forward ports or run anything else, and it only works from the scanner's address. An Ansible playbook for many hosts is in <a href="examples/ansible-setup-targets.yml"><code>examples/ansible-setup-targets.yml</code></a>.</p>
<p><strong>2. On the scanner</strong>, list the host in <code>/etc/cvewatch/hosts.ini</code>:</p>
<pre><code class="language-ini">[web01]
address = 192.168.10.20
user = cvewatch
exposure = internet      # internet | lan | internal | isolated
criticality = high       # high | medium | low

[nas01]
address = file:/srv/inventories/nas01.json   # offline host
exposure = isolated
</code></pre>
<p><strong>3. Confirm the host key once</strong> (<code>sudo -u cvewatch ssh cvewatch@192.168.10.20</code>) and run a scan.</p>
<h2 id="configuration">Configuration</h2>
<p><code>/etc/cvewatch/cvewatch.ini</code> (print all defaults with <code>cvewatch config</code>):</p>
<pre><code class="language-ini">[general]
data_dir = /var/lib/cvewatch
hosts_file = /etc/cvewatch/hosts.ini
exceptions_file = /etc/cvewatch/exceptions.csv
cache_hours = 20
keep_reports = 30

[priority]
p1_epss = 0.5
p2_epss = 0.1

[alerts]
min_priority = P2
ntfy_url = https://ntfy.sh/your-long-random-topic
webhook_url =
email_to =

[output]
prometheus_file = /var/lib/cvewatch/cvewatch.prom
</code></pre>
<p><strong>Exceptions</strong> (<code>/etc/cvewatch/exceptions.csv</code>) record accepted risks with an end date:</p>
<pre><code># vuln,host,expires,reason
CVE-2023-50495,docker01,2027-03-01,tic is not used on this host; Ubuntu priority low
</code></pre>
<p>Expired exceptions stop applying and the finding alerts again.</p>
<h2 id="commands">Commands</h2>
<table>
<thead>
<tr>
<th>Command</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>cvewatch scan</code></td>
<td>Collect, analyse, store, report, alert (<code>--local-only</code>, <code>--hosts FILE</code>, <code>--no-alerts</code>, <code>--fail-on P1</code>)</td>
</tr>
<tr>
<td><code>cvewatch status</code></td>
<td>Open findings per host and the current P1/P2 list</td>
</tr>
<tr>
<td><code>cvewatch report</code></td>
<td>Rebuild reports from the database</td>
</tr>
<tr>
<td><code>cvewatch collect</code></td>
<td>Print this host's inventory as JSON (used over SSH)</td>
</tr>
<tr>
<td><code>cvewatch selftest</code></td>
<td>Offline test with demo data; writes a demo report</td>
</tr>
<tr>
<td><code>cvewatch config</code></td>
<td>Print the default configuration</td>
</tr>
<tr>
<td><code>cvewatch version</code></td>
<td>Print the version</td>
</tr>
</tbody>
</table>
<p>Global options: <code>-c CONFIG</code> (or <code>CVEWATCH_CONFIG</code>), <code>-q</code> for warnings and errors only.</p>
<p>Run commands as the <code>cvewatch</code> user (<code>sudo -u cvewatch cvewatch status</code>) so the database stays writable for the timer.</p>
<p><strong>Exit codes</strong> of <code>scan</code>: <code>0</code> ok, <code>1</code> at least one host failed, <code>2</code> the <code>--fail-on</code> threshold was reached. Use it as a gate in CI or image pipelines:</p>
<pre><code class="language-bash">cvewatch scan --hosts new-image.ini --no-alerts --fail-on P2 || echo &quot;image has open P1/P2 vulnerabilities&quot;
</code></pre>
<h2 id="supported-systems">Supported systems</h2>
<table>
<thead>
<tr>
<th>Family</th>
<th>Detection</th>
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ubuntu (LTS and interim), Linux Mint and other derivatives</td>
<td>OSV <code>Ubuntu:&lt;version&gt;[:LTS]</code></td>
<td>Source packages; backports handled by Ubuntu data</td>
</tr>
<tr>
<td>Debian, Raspberry Pi OS, Proxmox VE</td>
<td>OSV <code>Debian:&lt;major&gt;</code></td>
<td>Source packages</td>
</tr>
<tr>
<td>AlmaLinux, Rocky Linux</td>
<td>OSV + <code>dnf updateinfo</code></td>
<td>Source RPM names</td>
</tr>
<tr>
<td>RHEL, Fedora, CentOS Stream, Oracle Linux</td>
<td><code>dnf updateinfo --security</code></td>
<td>Advisories, no CVE-level detail</td>
</tr>
<tr>
<td>Alpine</td>
<td>OSV <code>Alpine:v&lt;x.y&gt;</code></td>
<td>Origin packages</td>
</tr>
</tbody>
</table>
<p>Targets need Python 3 (on RHEL 8 set <code>python = /usr/libexec/platform-python</code>) and an SSH server.</p>
<h2 id="files">Files</h2>
<table>
<thead>
<tr>
<th>Path</th>
<th>Content</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>/usr/local/lib/cvewatch/</code></td>
<td>Program, self-test fixtures, README</td>
</tr>
<tr>
<td><code>/etc/cvewatch/cvewatch.ini</code></td>
<td>Configuration</td>
</tr>
<tr>
<td><code>/etc/cvewatch/hosts.ini</code></td>
<td>Hosts to scan</td>
</tr>
<tr>
<td><code>/etc/cvewatch/exceptions.csv</code></td>
<td>Accepted risks with expiry dates</td>
</tr>
<tr>
<td><code>/var/lib/cvewatch/cvewatch.db</code></td>
<td>SQLite history</td>
</tr>
<tr>
<td><code>/var/lib/cvewatch/reports/</code></td>
<td>HTML, CSV, JSON reports and dated archive</td>
</tr>
<tr>
<td><code>/var/lib/cvewatch/cache/</code></td>
<td>OSV, KEV and EPSS cache</td>
</tr>
</tbody>
</table>
<p>Repository layout:</p>
<pre><code>cvewatch.py              the program (single file)
install.sh               install | uninstall | purge on the scanner
setup-target.sh          prepare a remote host (user + restricted key)
systemd/                 hardened service and daily timer (06:15, randomised)
examples/                config, hosts, exceptions, Ansible playbook, nginx for reports
tests/fixtures/          demo data for the self-test
</code></pre>
<h2 id="security-model">Security model</h2>
<ul>
<li><strong>Read-only targets.</strong> The collector only reads the package database and a few files under <code>/proc</code>, <code>/etc</code> and <code>/var/run</code>.</li>
<li><strong>Restricted key.</strong> <code>from=</code>, <code>restrict</code> and a forced <code>command=</code> limit the scanner's key to one action from one address.</li>
<li><strong>Unprivileged scanner.</strong> The systemd service runs as <code>cvewatch</code> with <code>ProtectSystem=strict</code>, <code>ProtectHome</code>, <code>NoNewPrivileges</code> and a single writable path.</li>
<li><strong>Sensitive output.</strong> Reports list unpatched hosts. <code>/var/lib/cvewatch</code> is not world-readable. Put the report behind authentication if you publish it (see <code>examples/nginx-reports.conf</code>).</li>
</ul>
<p>Found a security issue in cvewatch itself? See <a href="SECURITY.md">SECURITY.md</a>.</p>
<h2 id="network-and-privacy">Network and privacy</h2>
<p>The scanner needs HTTPS to <code>api.osv.dev</code>, <code>www.cisa.gov</code> and <code>api.first.org</code>. <code>HTTPS_PROXY</code> and similar variables are honoured. Targets need only an SSH connection from the scanner.</p>
<p>Only <strong>package names and versions</strong> go to OSV.dev and only <strong>CVE IDs</strong> go to FIRST. Host names, IP addresses and findings never leave your network.</p>
<h2 id="limitations">Limitations</h2>
<ul>
<li>cvewatch reports <strong>known vulnerabilities in distro packages</strong>. It does not see software installed outside the package manager (tarballs, <code>pip</code>, <code>npm</code>, container images). Use a container or SBOM scanner for those.</li>
<li>RHEL and Fedora without OSV coverage are reported from <code>dnf</code> security advisories, without per-CVE detail.</li>
<li>The CVSS score comes from OSV data where available; distro severity ratings can differ.</li>
<li>It is not an intrusion detection or configuration-audit tool.</li>
</ul>
<h2 id="faq">FAQ</h2>
<p><strong>Does it install anything on my servers?</strong>
Not in push mode. <code>setup-target.sh</code> only creates a user and an <code>authorized_keys</code> entry. The collector is streamed over SSH at scan time.</p>
<p><strong>How long does a scan take?</strong>
Seconds for one host after the first run. OSV queries are batched (up to 1000 packages per request) and KEV/EPSS are cached for <code>cache_hours</code>.</p>
<p><strong>Why is a CVE I patched still shown?</strong>
Usually the fix is installed but not active: the kernel or a library needs a reboot or a service restart. The report shows <code>reboot</code> in the host state.</p>
<p><strong>Can I use it in CI?</strong>
Yes. <code>--fail-on P1</code> (or <code>P2</code>) returns exit code 2 when such findings are open.</p>
<p><strong>Is there a Windows version?</strong>
A sister project for Windows is described in the guide below.</p>
<h2 id="the-guide">The guide</h2>
<p>cvewatch is the companion toolkit of the guide <strong>"Automate Linux CVE Tracking"</strong> (63 pages, PDF + EPUB, with a 20-slide deck). It explains every design decision, the security model, alerts, exceptions, dashboards, automatic remediation and a daily routine. Available at <strong><a href="https://dargslan.com">dargslan.com</a></strong>.</p>
<h2 id="contributing">Contributing</h2>
<p>Issues and pull requests are welcome. Please read <a href="CONTRIBUTING.md">CONTRIBUTING.md</a> first. In short: keep it one file, standard library only, and make <code>python3 cvewatch.py selftest</code> pass.</p>
<h2 id="licence">Licence</h2>
<p><a href="LICENSE">MIT</a> © 2026 Dargslan · <a href="https://dargslan.com">dargslan.com</a> · YouTube <a href="https://www.youtube.com/@Dargslan">@Dargslan</a></p>
<p>Vulnerability data: OSV.dev (CC-BY 4.0 and source licences), CISA KEV (public domain), FIRST EPSS. cvewatch is not affiliated with these projects.</p>
