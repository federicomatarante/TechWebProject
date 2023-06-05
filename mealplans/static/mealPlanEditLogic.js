function render(template, data) {
    return template.replace(/{{(\w+)}}/g, (_, value) => data[value] || '');
}

function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function remove(element) {
    element.parentNode.removeChild(element);
}

function getIngredientRow(ingredient_name = "", quantity = "", quantity_type = "") {
    let quantity_types = ['gr', 'kg', 'mg', 'ml', 'l', 'unità']
        .map(quantity_type => `<option value="${quantity_type}">${quantity_type}</option>`)

    let content = {
        quantity_types: quantity_types,
        ingredient_name: ingredient_name,
        ingredient_quantity: quantity,
        ingredient_quantity_type: quantity_type
    }

    let body = `
        <td>
                <input id="ingredientNameInput" placeholder="Inserisci l'ingrediente" class="form-control" type="text" value="{{ingredient_name}}">
            </td>
            <td>
                <input id="quantityInput" placeholder="Inserisci la quantità" class="form-control" type="number" min="1" max="10000" value="{{ingredient_quantity}}">
            </td>
            <td>
                <select id="unitInput" class="form-select" value="{{ingredient_quantity}}">
                    {{quantity_types}}
                </select>
            </td>
            <td>
                <div style="display: flex; justify-content: center">
                    <button onclick="remove(this.parentNode.parentNode.parentNode)" class="btn btn-close""></button>
                </div>
            </td>
    `;
    let rendered_body = render(body, content);
    let tr = document.createElement("tr");
    tr.innerHTML = rendered_body;
    return tr;
}

function getMealTable(day_number, meal_number, ingredient_rows, meal_name = "") {
    let ingredient_row = ingredient_rows.map(function (ingredient_row) {
        return ingredient_row.outerHTML;
    }).join("")
    let data = {
        ingredient_row: ingredient_row,
        meal_number: meal_number,
        day_number: day_number,
        meal_name: meal_name
    }
    let body = `
        <tr>
            <td colspan="3">
                <div style="display: flex; justify-content: center">
                    <input id="mealNameInput" placeholder="Inserisci il pasto" class="form-control" type="text" value="{{meal_name}}">
                </div>
            </td>
            <td>
                <div style="display: flex; justify-content: center">
                    <button onclick="remove(this.parentNode.parentNode.parentNode.parentNode.parentNode)" class="btn btn-close""></button>
                </div>
            </td>
        </tr>
        {{ingredient_row}}
        <tr>
            <td colspan="4">
                <div style="display: flex; justify-content: center;">
                    <button style="width: 20%" onclick="addIngredient({{day_number}},{{meal_number}})" class="btn btn-light"> + </button>
                </div>
            </td>
        </tr>
    `;
    let rendered_body = render(body, data);
    let table = document.createElement("table");
    let table_body = document.createElement("tbody");
    table_body.innerHTML = rendered_body;
    table.appendChild(table_body);
    table.classList.add('mb-2');
    table.id = "meal-" + meal_number;
    return table;
}

function getDayDiv(day_number, meal_tables) {
    let meal_table = meal_tables.map(function (meal_table) {
        return meal_table.outerHTML;
    }).join("")
    let data = {
        day_number: day_number,
        meal_table: meal_table
    }
    let body = `
        <div class="col-md-8 col-xl-6 text-center mx-auto">
                <div style="display: flex;justify-content: center">
                    <button onclick="removeDay({{day_number}})" class="btn btn-close"></button>
                    <h5 id="day-title" class="fw-bold ms-1">Giorno {{day_number}}</h5>
                </div>
        </div>
        <div class="row mb-3">
            {{meal_table}}
        </div>
        <div style="display: flex; justify-content: center">
                <button style="width: 20%; margin-right: 10px" onclick="addMeal({{day_number}})" class="btn btn-light"> + Pasto  </button>
        </div>
    `;
    let rendered_body = render(body, data);
    let day = document.createElement("div");
    day.innerHTML = rendered_body;
    day.id = "day-" + day_number;
    day.classList = ["row mb-5"];
    return day;
}

function addIngredient(day_number, meal_number) {
    let mealPlanContent = document.getElementById("mealPlanContent");
    let day = mealPlanContent.querySelector("#day-" + day_number);
    let mealTable = day.querySelector("#meal-" + meal_number);
    let ingredient_row = getIngredientRow();
    mealTable.querySelector("tbody").insertBefore(ingredient_row, mealTable.querySelector("tbody").children[mealTable.querySelector("tbody").children.length - 1]);

}

function addMeal(day_number) {
    let mealPlanContent = document.getElementById("mealPlanContent");
    let day = mealPlanContent.querySelector("#day-" + day_number);
    let meal_tables = day.querySelectorAll("table");
    let meal_number = meal_tables.length + 1;
    let ingredient_rows = [getIngredientRow()];
    let meal_table = getMealTable(day_number, meal_number, ingredient_rows);
    day.insertBefore(meal_table, day.children[day.children.length - 2]);
}

function addDay() {
    let mealPlanContent = document.getElementById("mealPlanContent");
    let day_number = mealPlanContent.childElementCount + 1;
    let meal_tables = [];
    let day = getDayDiv(day_number, meal_tables);
    mealPlanContent.appendChild(day);
}

function removeDay(day_number) {
    let mealPlanContent = document.getElementById("mealPlanContent");
    let child = mealPlanContent.children[day_number - 1];
    mealPlanContent.removeChild(child);
    for (let i = 1; i < mealPlanContent.children.length + 2; i++) {
        if (i === day_number) {
            continue;
        }
        let day = document.getElementById("day-" + i);
        if (i >= day_number) {
            day.id = "day-" + (i - 1);
            day.querySelector("#day-title").innerHTML = "Giorno " + (i - 1);
        }
    }
}

function containsOnlyDigits(str) {
    return str.match(/^[0-9]+$/) !== null;
}

function saveMealPlan() {
    let mealPlanContent = document.getElementById("mealPlanContent");
    let days = [];
    if (mealPlanContent.childElementCount === 0) {
        alert("Inserisci almeno un giorno");
        return;
    }

    for (let day_number = 1; day_number < mealPlanContent.childElementCount + 1; day_number++) {
        let meal_tables = document.getElementById("day-" + day_number).querySelectorAll("table");
        if (meal_tables.length === 0) {
            alert("Inserisci almeno un pasto per ogni giorno");
            return;
        }
        let meals = [];
        for (let meal_number = 1; meal_number < meal_tables.length + 1; meal_number++) {
            let mealRows = document.getElementById("meal-" + meal_number).querySelectorAll("tr");
            if (mealRows.length === 2) {
                alert("Inserisci almeno un ingrediente per ogni pasto");
                return;
            }
            let mealName = mealRows[0].querySelector("#mealNameInput").value;
            if (mealName === "") {
                alert("Inserisci il nome di ogni pasto");
                return;
            }
            let ingredients = [];
            for (let j = 1; j < mealRows.length - 1; j++) {
                let ingredient = mealRows[j];
                let name = ingredient.querySelector("#ingredientNameInput").value;
                if (name === "") {
                    alert("Inserisci il nome di ogni ingrediente");
                    return;
                }
                let quantity = ingredient.querySelector("#quantityInput").value;
                if (quantity === "") {
                    alert("Inserisci la quantità di ogni ingrediente");
                    return;
                }

                if (!containsOnlyDigits(quantity)) {
                    alert("Inserisci una quantità valida per ogni ingrediente");
                    return;
                }
                let unit = ingredient.querySelector("#unitInput").value;
                if (unit === "") {
                    alert("Inserisci l'unità di misura di ogni ingrediente");
                    return;
                }
                ingredients.push({
                    name: name,
                    quantity: parseInt(quantity),
                    unit: unit
                });
            }
            meals.push({
                name: mealName,
                ingredients: ingredients
            });
        }
        days.push({
            day: parseInt(day_number),
            meals: meals
        });
    }

    if (document.getElementById("expirationDayInput").value === "") {
        alert("Inserisci una data di scadenza");
        return;
    }


    let mealPlanJson = {
        "id": mealPlan["id"],
        "days": days,
        "expirationDay": document.getElementById("expirationDayInput").value
    };
    let token = getCookie('csrftoken');

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/mealplans/manage/saveMealPlan/" + userName, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', token);
    xhr.send(JSON.stringify(mealPlanJson));
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 400) {
            window.location.href = "/mealplans/manage/";
        } else {
            alert("Errore durante il salvataggio del piano di allenamento: " + xhr.responseText);
        }
    }
}


/**
 * {"expirationDay": "2023-06-03",
 * "days": [{"day": 1,
 * "meals": [{"name": "Carbonara",
 * "ingredients": [{"name": "Pasta", "quantity": 300, "unit": "gr"},
 * {"name": "Uova", "quantity": 2, "unit": "unit\u00e0"}]},
 * {"name": "Matriciana",
 * "ingredients": [{"name": "Pomodoro", "quantity": 100, "unit": "gr"},
 * {"name": "Pecorino", "quantity": 19, "unit": "gr"}]}]},
 * {"day": 2, "meals": [{"name": "Carbonara", "ingredients": [{"name": "Pasta", "quantity": 300, "unit": "gr"}, {"name": "Uova", "quantity": 2, "unit": "unit\u00e0"}]}]}]}
 */

function init() {
    let exirationDay = mealPlan['expirationDay'];
    let expirationDayInput = document.getElementById("expirationDayInput");
    expirationDayInput.value = exirationDay;

    let days = mealPlan['days'];
    days.forEach(day => {
        let day_number = day['day'];
        let meals = day['meals'];
        let meal_tables = [];
        for (let meal_number = 0; meal_number < meals.length; meal_number++) {
            const meal = meals[meal_number];
            let ingredients = meal['ingredients'];
            let ingredient_rows = ingredients.map(ingredient => {
                return getIngredientRow(ingredient['name'], ingredient['quantity'], ingredient['unit']);
            });
            let meal_name = meal['name'];
            let meal_table = getMealTable(day_number, meal_number + 1, ingredient_rows,meal_name);
            meal_tables.push(meal_table);
        }
        let day_div = getDayDiv(day_number, meal_tables);
        let mealPlanContent = document.getElementById("mealPlanContent");
        mealPlanContent.appendChild(day_div);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    let today = new Date();
    let tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    let tomorrow_string = tomorrow.toISOString().split('T')[0];
    let datePicker = document.getElementById('expirationDayInput');
    datePicker.min = tomorrow_string;

    init();

    document.getElementById("addDayButton").addEventListener("click", addDay);
    document.getElementById("saveMealPlanButton").addEventListener("click", saveMealPlan);
});