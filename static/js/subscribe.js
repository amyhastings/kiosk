subscribeForm = document.getElementById("subscribe-form");

subscribeForm.addEventListener('input', function(event){
    costPerIssue = Number(document.getElementById("mag_cost").value);
    numIssues = Number(document.getElementById("sub_length").value);
    totalCost = costPerIssue * numIssues / 100;
    overallCost = document.getElementById("overall_cost");
    overallCost.innerHTML = "The total cost of your subscription will be €" + totalCost.toFixed(2);
})