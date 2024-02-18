var Hamburger = document.querySelector(".Hamburger");
var menu = document.querySelector(".Hamburger");



// Função para abrir o menu hamburguer

Hamburger.addEventListener("click", function(){
    document.querySelector(".container").classList.toggle("show-menu")
});

// Função para fechar o menu ao clicar fora


 document.addEventListener("click", function(event) {
    const isMenuClicado = menu.contains(event.target);
     if (!isMenuClicado && menu.classList.contains("show-menu")) {
         menu.classList.remove("show-menu");
    }
});


//Espera ate que o conteúdo da página seja carregado
document.addEventListener("DOMContentLoaded", function() {
  var infoBox = document.querySelector(".info-box");
  var banner = document.querySelector(".banner");
  var saibaMaisButton = document.getElementById("btn-saiba-mais");

  // Garante que a caixa de informações esteja oculta por padrão
  infoBox.style.display = "none";

  // Define uma variável para controlar o estado do botão
  var isMostrarDetalhes = false;

  // Adiciona um evento de clique ao botão "Saiba mais"
  saibaMaisButton.addEventListener("click", function() {
    // Altera o estado do botão
    isMostrarDetalhes = !isMostrarDetalhes;

    // Altera o texto do botão com base no estado
    if (isMostrarDetalhes) {
      saibaMaisButton.textContent = "Saiba Menos";
    } else {
      saibaMaisButton.textContent = "Saiba Mais";
    }

    // Verifica se o info-box está oculto
    if (infoBox.style.display === "none") {
      infoBox.style.display = "block";

      // Adiciona uma classe ao banner para alterar a posição
      banner.classList.add("info-box-active");
    } else {
      // Oculta o info-box
      infoBox.style.display = "none";

      // Remove a classe do banner para voltar à posição original
      banner.classList.remove("info-box-active");
    }
  });

  // Função para remover o banner de informação da tela ao clicar fora
  document.addEventListener("click", function(event) {
    if (!infoBox.contains(event.target) && !event.target.matches("#btn-saiba-mais")) {
      infoBox.style.display = "none";
      banner.classList.remove("info-box-active");

      // Restaura o texto do botão para "Saiba Mais" quando o info-box é fechado
      saibaMaisButton.textContent = "Saiba Mais";
      isMostrarDetalhes = false;
    }
  });
});


// Obtenha o elemento "card-info" e o elemento "card" pelo ID
const cardInfo = document.getElementById("card-info");
const card = document.getElementById("card");

// Obtenha todos os botões "Saiba Mais" e os parágrafos
const saibaMaisButtons = document.querySelectorAll('.btn');
const descricoes = document.querySelectorAll('.descricao');

// Adicione um evento de clique a cada botão "Saiba Mais"
saibaMaisButtons.forEach((button, index) => {
  button.addEventListener('click', () => {
    // Verifique o estado atual de exibição do parágrafo
    if (descricoes[index].style.display === 'none' || descricoes[index].style.display === '') {
      // Se estiver oculto, mostre o parágrafo
      descricoes[index].style.display = 'block';
      // Oculte o parágrafo dentro de .card-info
      const paragraph = button.parentElement.querySelector('.card-info p');
      
      if (paragraph) {
        paragraph.style.display = 'none';
      }

      // Altere o texto do botão para "Saiba Menos"
      button.textContent = 'Saiba Menos';
    } else {
      // Se estiver visível, oculte o parágrafo
      descricoes[index].style.display = 'none';
      // Mostre o parágrafo dentro de .card-info
      const paragraph = button.parentElement.querySelector('.card-info p');
      if (paragraph) {
        paragraph.style.display = 'block';
      }

      // Altere o texto do botão de volta para "Saiba Mais"
      button.textContent = 'Saiba Mais';
    }
  });
});


document.getElementById('btn-contato').addEventListener('click', function(event) {
  // Rolagem suave para a seção de Orçamento
  console.log('Botão de contato clicado');
  var orcamentoSection = document.querySelector('a[href="#Contato"]');
  if (orcamentoSection) {
      orcamentoSection.scrollIntoView({ 
          behavior: 'smooth' 
      });
  } else {
      console.log('Seção de orçamento não encontrada');
  }
});


document.getElementById('btn-orcamento').addEventListener('click', function(event) {
  // Rolagem suave para a seção de Orçamento
  console.log('Botão de orçamento clicado');
  var orcamentoSection = document.querySelector('a[href="#Orcamento"]');
  if (orcamentoSection) {
      orcamentoSection.scrollIntoView({ 
          behavior: 'smooth' 
      });
  } else {
      console.log('Seção de orçamento não encontrada');
  }
});



document.querySelector("#qtde").addEventListener("change", atualizaPreco)
document.querySelector("#JS").addEventListener("change", atualizaPreco)
document.querySelector("#layout-sim").addEventListener("change", atualizaPreco)
document.querySelector("#layout-nao").addEventListener("change", atualizaPreco)
document.querySelector("#prazo").addEventListener("change", function () {
  const prazo = document.querySelector("#prazo").value;
  const labelPrazo = document.querySelector("label[for=prazo]");
  if (prazo === "1") {
      labelPrazo.innerHTML = `Prazo: ${prazo} semana`;
  } else {
      labelPrazo.innerHTML = `Prazo: ${prazo} semanas`;
  }
  atualizaPreco();
})


function atualizaPreco(){
    const qtde = document.querySelector("#qtde").value
    const temJS = document.querySelector("#JS").checked
    const incluiLayout = document.querySelector("#layout-sim").checked
    const naoincluiLayout = document.querySelector("#layout-nao").checked
    const prazo = document.querySelector("#prazo").value
    
    let preco = qtde * 50;
    if (temJS) {
        preco *= 1.1
    }
    if (incluiLayout) {
        preco += 200
    }

    if (naoincluiLayout){
        preco = preco
    }

    let taxaUrgencia = 1 - prazo*0.1;
    preco *= 1 + taxaUrgencia

    document.querySelector("#preco").innerHTML = "R$" + preco.toFixed(2)
}
