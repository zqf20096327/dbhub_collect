# FC Services Core

O FC Services é um aplicativo para uso interno dos colaboradores do Home Center Ferreira Costa, pensado para solucionar um problema de comunicação no que tange aos problemas referentes ao ambiente, infraestrutura da loja e espaço corporativo. Seu principal objetivo é desburocratizar e remover gargalos no processo de gerenciamento de chamados e solicitações, trazendo agilidade e comodide aos usuários. A interface foi pensada para ser simples e de boa usabilidade, considerando o perfil dos usuários

# Pré-requisitos

Certifique-se de ter o seguinte software instalado em sua máquina:

SDK do .NET Core 6.0
Visual Studio Code (opcional)

# Como rodar a aplicação

Abra um terminal ou prompt de comando.

Navegue até a pasta do repositório backend.

Execute o comando a seguir para restaurar as dependências do projeto: `dotnet restore`

Após a restauração das dependências, execute o seguinte comando para compilar o projeto: `dotnet build`

Se a compilação for concluída sem erros, execute o seguinte comando para iniciar a aplicação: `dotnet run`

A aplicação será iniciada e você verá as informações de inicialização no terminal. Aguarde até que a mensagem de sucesso seja exibida.

Agora você pode acessar a web API com Swagger abrindo um navegador e digitando a URL https://localhost:5001/swagger. Certifique-se de que a porta 5001 não esteja sendo usada por outra aplicação. Caso contrário, a porta pode variar.

Observações:

-  Certifique-se de ter o SDK do .NET Core 6.0 instalado em sua máquina.
- Se você preferir usar outra IDE, como o Visual Studio, certifique-se de ter a versão compatível com o .NET Core 6.0.
- Verifique se todas as dependências estão corretamente instaladas e atualizadas.
- Se você encontrar algum problema durante a execução da aplicação, verifique os logs e mensagens de erro exibidos no terminal.
- Certifique-se de configurar corretamente as variáveis de ambiente, se necessário, para a execução adequada da aplicação.

## Artefatos utilizados no projeto

<a href="https://www.figma.com/file/QnStMGzTLxaX0EZZqu4RxM/Main?node-id=0-1&t=wZWNGiKG0Iqy9kSC-0">Figma - Protótipo de Alta Fidelidade</a>

<a href="https://fcservices.pixelsquad.tech/">PWA FC Services</a>

## Equipe

| **Nome**   | Alisson Gabriel | Camyla de Lima | Cleyton Lucas | José Mateus   | Larissa Ferreira | Pedro Mendonça | Wellington Braga | Erika Cibelly     |
| ---------- | --------------- | -------------- | ------------- | ------------- | ---------------- | -------------- | ---------------- | ----------------- |
| **GitHub** | @Alisson-1      | @camyllalima   | @CleytonLu    | @josemateusmz | @imlari          | @Pedromendonc  | @welllucky       | @ErikaCibellySx24 |
