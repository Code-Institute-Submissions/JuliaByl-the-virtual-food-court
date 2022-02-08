$(document).ready(function () {
    delete_item();
    add_ingredient();
    add_step();
    onsubmit();
    onedit();
    deletedalert();
});

// Deletes parent of element when trashcan is clicked
function delete_item() {
    $(".fa-trash-alt").click(function() {
        $(this).parent().remove();
    });
}

// Moves ingredient from input form to ingredient list
function add_ingredient(){
    $("#add_ingredient").click(function() {
        let new_ingredient = $("#ingredients_amount").val();
        // If button is clicked after entering an ingredient
        if (new_ingredient) {
            $("#ingredients_list").append(`<li class="p-1 text-start">
            ${new_ingredient}
            <button class="fas fa-trash-alt float-end text-danger btn"></button>
        </li>`);
        $("#ingredients_amount").val("");
        delete_item();
        }
    });
}

// Moves how_to section from input form to how_to list
function add_step(){
    $("#add_step").click(function() {
        let new_step = $("#how_to").val();
        // If button is clicked after entering an ingredient
        if (new_step) {
            $("#how_to_list").append(`<li class="p-1 text-start mt-2">
            ${new_step}
            <button class="fas fa-trash-alt float-end text-danger btn"></button>
        </li>`);
        $("#how_to").val("");
        delete_item();
        }
    });
}

// when the user is clicking the "create-recipe" - button (posts the information to python function)
function onsubmit(){
    $("#create_recipe").click(function(){
        let ingredients_amount = grab_ingredients();
        let how_to = grab_steps();
        
        $.post("/create-recipe", JSON.stringify({
            "title": $("#title").val(),
            "time_required": $("#time_required").val(),
            "ingredients_amount": ingredients_amount,
            "portions_amount": $("#portions_amount").val(),
            "food_category": $("#food_category").val(),
            "how_to": how_to
        }));

        alert("Recipe has been successfully created!");
        // TODO: Change this url when reopening workspace until project has bee ndeployed or it won't work
        window.location.replace("https://8080-juliabyl-thevirtualfoodc-hxrzt10w7ru.ws-eu30.gitpod.io/browse-recipes");
    });
}

// when the user is clicking the "edit-recipe" - button (posts the information to python function)
function onedit(){
    $("#update_recipe").click(function(){
        let ingredients_amount = grab_ingredients();
        let how_to = grab_steps();
        let page = window.location.href;
        let recipe_id = page.slice(page.lastIndexOf("/"));
        let url = "/edit_recipe"+recipe_id;
        
        $.post(url, JSON.stringify({
            "title": $("#title").val(),
            "time_required": $("#time_required").val(),
            "ingredients_amount": ingredients_amount,
            "portions_amount": $("#portions_amount").val(),
            "food_category": $("#food_category").val(),
            "how_to": how_to
        }));

        alert("Recipe has been successfully updated!");
        // TODO: Change this url when reopening workspace until project has been deployed or it won't work
        window.location.replace("https://8080-juliabyl-thevirtualfoodc-hxrzt10w7ru.ws-eu30.gitpod.io/browse-recipes"); 
    });
}

// displays an alert showing that the recipe has been deleted when clicking the "delete recipe" - button 
function deletedalert(){
    $("#delete_recipe").click(function(){
        alert("Recipe has been deleted!");
    });
}

// grabs the ingredients listed in the ingredients_list and adds them in a list
function grab_ingredients(){
    let ingredients_list = $("#ingredients_list");
    let ingredients = ingredients_list.children();
    let ingredients_amount = [];

    for (let ingredient of ingredients) {
        ingredients_amount.push(ingredient.innerHTML.replace(
            '<button class="fas fa-trash-alt float-end text-danger btn"></button>', '').trim());
    }

    return ingredients_amount;
}

// grabs the how-to steps listed in the how_to_list and adds them in a list
function grab_steps(){
    let how_to_list = $("#how_to_list");
    let steps = how_to_list.children();
    let how_to = [];

    for (let step of steps) {
        how_to.push(step.innerHTML.replace(
            '<button class="fas fa-trash-alt float-end text-danger btn"></button>', '').trim());
    }

    return how_to;
}