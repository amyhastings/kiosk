magForm = document.getElementById("mag-form-add");
magCats = document.querySelectorAll(".mag-cats");
magFormButton = document.querySelector(".mag-form-button");

magForm.addEventListener('input', function(event){
    for (let i = 0; i < magCats.length; i++){
        if (magCats[i].checked) {
            magFormButton.disabled = false;
            break;
        } else {
            magFormButton.setAttribute("disabled", "True");
        }
    }
});

