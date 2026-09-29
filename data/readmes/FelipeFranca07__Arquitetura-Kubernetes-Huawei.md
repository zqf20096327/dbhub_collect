# Arquitetura Huawei Cloud — Rede, Kubernetes e Dados de Ponta a Ponta

Do tráfego público até o cluster CCE e os bancos gerenciados: como VPC, firewall, load balancer, Enterprise Router e os serviços de dados da Huawei se encaixam num único ambiente provisionado por código.

![Diagrama de arquitetura](diagrams/architecture.svg)

## Terraform

A pasta [`terraform/`](terraform/) contém os 9 arquivos `.tf` na ordem de apply:

1. `01-network.tf` — VPC
2. `02-subnets.tf` — Subnets (pública e privada)
3. `03-firewall.tf` — Security Group
4. `04-loadbalancer.tf` — ELB
5. `05-router.tf` — Enterprise Router
6. `06-kubernetes.tf` — Cluster CCE
7. `07-database.tf` — RDS (PostgreSQL)
8. `08-storage.tf` — OBS
9. `09-nosql.tf` — GaussDB (Cassandra API)

> O provider Terraform `huaweicloud/huaweicloud` é bem menos maduro e documentado que os da Azure, AWS e GCP — confirme os nomes exatos de argumento na documentação atual antes de aplicar isto de verdade.

## 01. Rede — VPC

A VPC é o contêiner isolado onde todo o resto vive; CIDR próprio, sem sobreposição com as outras nuvens do ambiente.

> Console Huawei Cloud → Network → Virtual Private Cloud → Create VPC

**Passos pelo console:**
1. No canto superior do console, selecione a região `sa-brazil-1`.
2. No menu de serviços, acesse `Network` → `Virtual Private Cloud`.
3. Clique em `Create VPC`.
4. Preencha Name: `vpc-prod`, IPv4 CIDR Block: `10.20.0.0/16`.
5. Se o assistente pedir uma subnet padrão, pode deixar o valor sugerido — as subnets reais serão criadas no próximo passo.
6. Clique em `Create Now` e aguarde o status mudar para `Available`.

## 02. Subnets

Uma subnet pública para o ELB, uma privada para o cluster e os bancos — nada com IP público conversa direto com a internet.

> VPC → vpc-prod → Subnets → Create Subnet

**Passos pelo console:**
1. Abra a VPC `vpc-prod` criada e vá até a aba `Subnets`.
2. Clique `Create Subnet`, nomeie `subnet-public`, CIDR `10.20.1.0/24`, Gateway `10.20.1.1`.
3. Clique `Create Subnet` de novo para a privada: nome `subnet-private`, CIDR `10.20.2.0/24`, Gateway `10.20.2.1`.
4. Mantenha o servidor DNS padrão sugerido pela Huawei nas duas.
5. Confirme que as duas aparecem na lista com status `Normal`.

## 03. Firewall — Security Group

Regra explícita por porta; só HTTPS entra vindo da internet, o resto do tráfego fica restrito ao security group da aplicação.

> Network Console → Access Control → Security Groups → Create Security Group

**Passos pelo console:**
1. Acesse `Network Console` → `Access Control` → `Security Groups`.
2. Clique `Create Security Group`, nomeie `sg-app` e associe à VPC `vpc-prod`.
3. Abra o grupo criado e vá em `Inbound Rules` → `Add Rule`.
4. Protocolo `TCP`, porta `443`, origem `0.0.0.0/0`, ação `Allow`.
5. Salve e confirme a regra na lista de entrada do security group.

## 04. Load Balancer — ELB

Recebe o tráfego na subnet pública e distribui entre os nós do pool via HTTPS.

> Network → Elastic Load Balance → Buy Elastic Load Balancer

**Passos pelo console:**
1. Vá em `Network` → `Elastic Load Balance`.
2. Clique `Buy Elastic Load Balancer`.
3. Tipo `Dedicated`, Network Type `Public network`, associe à subnet `subnet-public`.
4. Nomeie `elb-prod` e confirme a compra.
5. Com o ELB criado, abra a aba `Listeners` → `Add Listener`: protocolo `HTTPS`, porta `443`.
6. Crie o `Backend Server Group` `pool-app` apontando para os nós do CCE (passo 06) e associe ao listener.

## 05. Enterprise Router

O equivalente da Huawei ao Transit Gateway: liga esta VPC a um hub central, sem participar do caminho de tráfego da aplicação.

> Network → Enterprise Router → Buy Enterprise Router

**Passos pelo console:**
1. Vá em `Network` → `Enterprise Router`.
2. Clique `Buy Enterprise Router`, nomeie `er-hub`, escolha a availability zone.
3. Com o router criado, abra a aba `Attachments` → `Create VPC Attachment`.
4. Selecione a VPC `vpc-prod` e a subnet `subnet-private`, nomeie `attach-prod-vpc`.
5. Em `Default Route Table` do Enterprise Router, adicione uma rota apontando para o attachment recém-criado.

## 06. Kubernetes gerenciado — CCE

O cluster e o node pool ficam inteiramente na subnet privada; nenhum node recebe IP público.

> Containers → Cloud Container Engine → Create Cluster

**Passos pelo console:**
1. Vá em `Containers` → `Cloud Container Engine`.
2. Clique `Create Cluster`, tipo `CCE Standard Cluster`.
3. Nomeie `cce-prod`, associe à VPC `vpc-prod` e subnet `subnet-private`.
4. Escolha o flavor do control plane e confirme a criação.
5. Quando o cluster ficar `Running`, vá em `Node Pools` → `Create Node Pool`.
6. SO `EulerOS 2.9`, flavor `s6.xlarge.2`, quantidade inicial `3`, subnet `subnet-private`.
7. Confirme e aguarde os nós ficarem `Running`.

## 07. Banco relacional — RDS

PostgreSQL gerenciado, na mesma subnet privada do cluster, acessível só pelo security group da aplicação.

> Databases → Relational Database Service → Buy RDS Instance

**Passos pelo console:**
1. Vá em `Databases` → `Relational Database Service`.
2. Clique `Buy RDS Instance`, DB Engine `PostgreSQL`, versão `14`.
3. Flavor `rds.pg.n1.large.2`, storage `Ultra-high I/O`, tamanho `100 GB`.
4. VPC `vpc-prod`, subnet `subnet-private`, security group `sg-app`.
5. Nomeie a instância `rds-app`, defina a senha do administrador e confirme.

## 08. Object Storage — OBS

Bucket privado para artefatos e arquivos estáticos, sem acesso público por padrão.

> Storage → Object Storage Service → Create Bucket

**Passos pelo console:**
1. Vá em `Storage` → `Object Storage Service`.
2. Clique `Create Bucket`.
3. Nomeie `obs-prod-assets`, região `sa-brazil-1`, Storage Class `Standard`.
4. Policy de acesso: `Private`.
5. Confirme a criação e valide o bucket na lista.

## 09. NoSQL — GaussDB (Cassandra API)

O equivalente funcional mais próximo do DynamoDB no catálogo da Huawei: GaussDB para Cassandra (também vendido como GeminiDB), para dados de alta escrita e baixa latência.

> Databases → GaussDB(for Cassandra) → Buy Instance

**Passos pelo console:**
1. Vá em `Databases` → `GaussDB(for Cassandra)` — às vezes listada como `GeminiDB Cassandra`.
2. Clique `Buy Instance`.
3. Flavor `gaussdb.cassandra.xlarge.4`, número de nós `3`.
4. VPC `vpc-prod`, subnet `subnet-private`, security group `sg-app`.
5. Nomeie `gaussdb-cassandra-prod` e confirme a compra.

## Aviso

**O que fica:** a ordem de criação pelo console é a mesma do Terraform — VPC, subnets, firewall, ELB, Enterprise Router, CCE, e só depois os três serviços de dados.

A Huawei Cloud é a nuvem com a interface de console menos padronizada das quatro: nomes de menu, posição de botões e até o nome comercial de um serviço (GaussDB vs. GeminiDB) podem variar entre regiões e datas. Trate este guia como um roteiro confiável, não como um script exato de cliques.

