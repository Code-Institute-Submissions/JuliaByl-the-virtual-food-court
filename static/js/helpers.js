$(document).ready(function () {
    add_ingredient();
    add_step();
});

// TODO: edit global python variables when posting new/edited recipe

// Deletes parent of element when trashcan is clicked
function delete_item() {
    $(".fa-trash-alt").click(function() {
        $(this).parent().remove();
    })
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
    })
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
    })
}