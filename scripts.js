var Hamburger = document.querySelector(".Hamburger");

Hamburger.addEventListener("click", function(){
    document.querySelector(".container").classList.toggle("show-menu");
});

document.querySelector("#qtde").addEventListener("change", atualizaPreco)
document.querySelector("#JS").addEventListener("change", atualizaPreco)
document.querySelector("#layout-sim").addEventListener("change", atualizaPreco)
document.querySelector("#layout-nao").addEventListener("change", atualizaPreco)
document.querySelector("#prazo").addEventListener("change", function () {
    const prazo = document.querySelector("#prazo").value
    document.querySelector("label[for=prazo]").innerHTML = `Prazo: ${prazo} semanas`
    atualizaPreco()
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

    document.querySelector("#preco").innerHTML = 'R$' + preco.toFixed(2)

}


