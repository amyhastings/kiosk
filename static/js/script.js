const menuButton = document.querySelector("#hamburger");
const closeMenuButton = document.querySelector("#close-menu");
const menuContainer = document.querySelector(".menu-content");


function show(item) {
    item.classList.remove("inactive");
};

function hide(item) {
    item.classList.add("inactive");
};

function openMenu() {
    show(menuContainer);
    show(closeMenuButton);
    hide(menuButton);
};

function closeMenu() {
    hide(menuContainer);
    hide(closeMenuButton);
    show(menuButton);
};

document.addEventListener('click', function(e){
    const id = e.target.id;
    if (id === "hamburger") {
        openMenu();
    } else if (id === "close-menu") {
        closeMenu();
    } 
});

subscribeForm = document.getElementById("subscribe-form");

subscribeForm.addEventListener('input', function(event){
    costPerIssue = Number(document.getElementById("mag_cost").value);
    numIssues = Number(document.getElementById("sub_length").value);
    totalCost = costPerIssue * numIssues / 100;
    overallCost = document.getElementById("overall_cost");
    overallCost.innerHTML = "The total cost of your subscription will be €" + totalCost.toFixed(2);
})


