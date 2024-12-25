using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace httpValidaCpf
{
    public static class fnvalidacpf
    {
        [FunctionName("fnvalidacpf")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Iniciando validação do CPF...");

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);
            if (data is null)
            {
                return new BadRequestObjectResult("Informe o CPF");
            }
            String cpf = data?.cpf;
            if (ValidaCpf(cpf) == false)
            {
                return new BadRequestObjectResult("CPF inválido");
            }

            string responseMessage = "CPF atende aos critérios de validação!";

            return new OkObjectResult(responseMessage);
        }

        public static bool ValidaCpf(string cpf)
        {
            if (string.IsNullOrWhiteSpace(cpf))
                return false;

            // Remover formatação
            cpf = cpf.Replace(".", "").Replace("-", "");

            // Verificar se o comprimento é 11
            if (cpf.Length != 11)
                return false;

            // Verificar se todos os dígitos são iguais
            if (new string(cpf[0], cpf.Length) == cpf)
                return false;

            // Calcular o primeiro dígito verificador
            int[] multiplicador1 = new int[9] { 10, 9, 8, 7, 6, 5, 4, 3, 2 };
            int soma = 0;
            for (int i = 0; i < 9; i++)
                soma += int.Parse(cpf[i].ToString()) * multiplicador1[i];

            int resto = soma % 11;
            if (resto < 2)
                resto = 0;
            else
                resto = 11 - resto;

            if (resto != int.Parse(cpf[9].ToString()))
                return false;

            // Calcular o segundo dígito verificador
            int[] multiplicador2 = new int[10] { 11, 10, 9, 8, 7, 6, 5, 4, 3, 2 };
            soma = 0;
            for (int i = 0; i < 10; i++)
                soma += int.Parse(cpf[i].ToString()) * multiplicador2[i];

            resto = soma % 11;
            if (resto < 2)
                resto = 0;
            else
                resto = 11 - resto;

            if (resto != int.Parse(cpf[10].ToString()))
                return false;

            return true;
        }
    }
}
