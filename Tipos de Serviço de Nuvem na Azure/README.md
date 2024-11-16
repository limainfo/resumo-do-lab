### Tipos de Serviço de Nuvem na Azure - IaaS, PaaS e SaaS na Azure

### Resumo sobre Tipos de Serviço em Nuvem: IaaS, PaaS e SaaS

O vídeo explica os três principais tipos de serviços em nuvem no contexto do modelo de responsabilidade compartilhada: **Infraestrutura como Serviço (IaaS)**, **Plataforma como Serviço (PaaS)** e **Software como Serviço (SaaS)**.

- **Infraestrutura como Serviço (IaaS)**: Oferece maior controle ao cliente, que é responsável por configurar, monitorar e atualizar os recursos. O cliente gerencia a infraestrutura virtual, mas não precisa se preocupar com o hardware físico.

- **Plataforma como Serviço (PaaS)**: Permite que o cliente desenvolva e gerencie aplicações sem lidar com a infraestrutura subjacente, como sistemas operacionais e bancos de dados. Isso reduz o esforço de configuração e manutenção.

- **Software como Serviço (SaaS)**: O cliente acessa uma aplicação completa, como Microsoft Teams, onde o nível de acesso é determinado pela licença adquirida. Nesse modelo, o cliente lida apenas com a configuração de usuários e permissões.

Cada modelo tem suas próprias responsabilidades e casos de uso apropriados. Em IaaS, o cliente realiza mais atividades de monitoramento; em PaaS, a carga de trabalho diminui; e em SaaS, o cliente recebe uma solução pronta para uso.

| Tempo     | Descrição |
|-----------|-----------|
| 00:00:06  | Introdução aos tipos de serviço em nuvem: infraestrutura como serviço (IaaS), plataforma como serviço (PaaS) e software como serviço (SaaS), dentro do modelo de responsabilidade compartilhada. |
| 00:00:33  | Explicação de que IaaS, PaaS e SaaS são conceitos genéricos de nuvem, não específicos da Microsoft. A diferença entre provedores está principalmente nos nomes e produtos específicos. |
| 00:00:59  | Objetivo da aula: entender como cada modelo de serviço funciona, as responsabilidades do cliente e do provedor em cada caso, e os cenários apropriados para uso. |
| 00:01:29  | **Infraestrutura como Serviço (IaaS)**: oferece maior controle ao cliente sobre configurações, monitoramento e manutenção. Exemplo: criação e gerenciamento de máquinas virtuais. |
| 00:01:58  | Explicação sobre a responsabilidade do cliente em IaaS: configurar, monitorar e atualizar recursos. IaaS permite mais liberdade para personalizar a infraestrutura de TI. |
| 00:02:35  | IaaS permite criar uma infraestrutura completa na nuvem, eliminando a necessidade de gerenciar o hardware físico, mas mantendo a responsabilidade pelas configurações. |
| 00:03:04  | **Plataforma como Serviço (PaaS)**: cobre parte da infraestrutura, incluindo sistemas operacionais e bancos de dados, permitindo que o cliente se concentre na aplicação sem se preocupar com o servidor. |
| 00:03:31  | Em PaaS, o cliente não precisa gerenciar o sistema operacional, focando apenas no desenvolvimento e operação da aplicação. |
| 00:04:00  | Exemplo de PaaS: uso de um banco de dados na nuvem sem precisar gerenciar o servidor. Permite ao cliente se concentrar nos dados e na aplicação. |
| 00:04:28  | **Software como Serviço (SaaS)**: o cliente acessa uma aplicação completa, como Microsoft Teams, e o nível de acesso e recursos depende da licença adquirida. |
| 00:05:21  | Explicação sobre como o modelo de licenciamento em SaaS determina os recursos disponíveis para o cliente. Quanto maior a licença, mais funcionalidades estão disponíveis. |
| 00:06:13  | Comparação entre os modelos: IaaS demanda mais trabalho do cliente, PaaS reduz a carga de trabalho ao gerenciar o sistema operacional, e SaaS entrega uma aplicação pronta com configuração mínima. |
| 00:07:02  | Em SaaS, o cliente não precisa se preocupar com detalhes de infraestrutura, apenas com a configuração dos grupos e permissões de usuários. |
| 00:07:17  | Quanto mais se utiliza IaaS, mais atividades e monitoramento são necessários. Em SaaS, as responsabilidades do cliente são mínimas. |
| 00:07:45  | Resumo: identificar o modelo de serviço mais adequado para cada situação, considerando as responsabilidades e o esforço necessário em cada nível. |



### Tipos de Serviço de Nuvem na Azure - Modelo de Responsabilidade Compartilhada

### Resumo sobre o Modelo de Responsabilidade Compartilhada: IaaS, PaaS e SaaS

O vídeo aborda o modelo de **responsabilidade compartilhada** na nuvem, destacando como as responsabilidades são divididas entre o cliente e o provedor nos três principais tipos de serviços: **IaaS**, **PaaS** e **SaaS**.

- **Infraestrutura como Serviço (IaaS)**: O cliente é responsável pela maior parte da gestão, incluindo sistema operacional e controle de rede, enquanto o provedor cuida da infraestrutura física. Esse modelo oferece maior controle e flexibilidade ao cliente.

- **Plataforma como Serviço (PaaS)**: A responsabilidade é dividida; o provedor gerencia o sistema operacional e parte da infraestrutura, enquanto o cliente gerencia a aplicação e parte da rede. O PaaS permite ao cliente focar mais no desenvolvimento de aplicativos.

- **Software como Serviço (SaaS)**: O provedor assume quase toda a gestão, e o cliente é responsável apenas por dados e identidade. Esse modelo, baseado em licenciamento, reduz a carga de trabalho do cliente, oferecendo menor controle e maior simplicidade.

Esses níveis de serviço ajudam as empresas a escolherem o modelo ideal conforme sua necessidade de controle, custo e carga de trabalho na gestão dos recursos na nuvem.

| Tempo     | Descrição |
|-----------|-----------|
| 00:00:05  | Introdução ao modelo de **responsabilidade compartilhada** na nuvem, explicando que o objetivo não é decorar a tabela, mas entender a divisão de responsabilidades entre cliente e provedor. |
| 00:00:22  | Explicação sobre o modelo **on-premises**, onde toda a responsabilidade é do cliente, incluindo infraestrutura física e manutenção. |
| 00:00:47  | Detalhes sobre a **Infraestrutura como Serviço (IaaS)**: o cliente é responsável por tudo exceto pelo datacenter físico, rede física e hosts físicos, que são de responsabilidade do provedor. |
| 00:01:17  | Explicação sobre **Plataforma como Serviço (PaaS)**: a Microsoft gerencia o sistema operacional, enquanto o cliente gerencia a configuração de aplicativos e controle de rede. |
| 00:01:46  | Em PaaS, a responsabilidade pelo controle de rede, aplicativos e identidade é dividida entre o cliente e a Microsoft. |
| 00:02:16  | **Software como Serviço (SaaS)**: o cliente é responsável apenas por informações e dados, dispositivos e contas, enquanto o provedor gerencia quase tudo, com exceção de identidade e diretório, que é compartilhado. |
| 00:02:40  | Comparação do SaaS com o IaaS, mostrando a inversão de responsabilidades, onde no SaaS a Microsoft assume a maior parte da gestão. |
| 00:03:20  | A carga de trabalho e o custo de gestão aumentam no IaaS, enquanto no SaaS o cliente apenas personaliza e configura contas. |
| 00:04:20  | Comparação dos tipos de serviço: **IaaS** oferece maior flexibilidade, **PaaS** foca no desenvolvimento de aplicativos e **SaaS** opera com um modelo de assinatura para software, com controle reduzido. |
| 00:04:41  | Explicação sobre o modelo de pagamento conforme o uso e o menor controle oferecido pelo **SaaS** em comparação com IaaS e PaaS. |
| 00:05:24  | Observação sobre a escolha entre IaaS, PaaS e SaaS ao criar recursos, enfatizando que IaaS exige maior gestão, PaaS é intermediário e SaaS oferece o menor controle. |
| 00:05:52  | Conclusão sobre os níveis de gestão nos diferentes modelos de serviço e a importância de entender o contexto para criar recursos adequadamente. |
