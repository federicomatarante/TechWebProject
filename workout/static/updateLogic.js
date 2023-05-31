function render(template, data) {
    return template.replace(/{{(\w+)}}/g, (_, value) => data[value] || '');
}

function remove(element) {
    element.parentNode.removeChild(element);
}

function getExerciseRow(exercises, index) {
    let exercise_string = Object.keys(exercises).map((id) => {
        return `<option value="${id}">${exercises[id]}</option>`;
    });
    exercise_string = exercise_string.join("");


    if (exercise_string.length === 0) {
        exercise_string = "";
    }

    let data = {
        exercises: exercise_string,
    }

    let body = `
        <tr>
            <td>
                <select class="form-select" id="exerciseSelect">
                    {{exercises}}
                </select>
            </td>
            <td>
                <input id="reps-input" class="form-control" type="number" min="1" max="100" value="6">
            </td>
            <td>
                <input id="sets-input" class="form-control" type="number" min="1" max="100" value="6">
            </td>
            <td>
                <div style="display: flex; justify-content: center">
                    <button onclick="remove(this.parentNode.parentNode.parentNode)" class="btn btn-close""></button>
                </div>
            </td>
        </tr>
    `;
    return render(body, data);
}

function getWorkoutDayTemplate(day_number, exercise_rows_list) {
    let exercise_rows = exercise_rows_list.join("");
    let data = {
        day_number: day_number,
        exercise_rows: exercise_rows
    }
    let body = `
          <div id="{{day_number}}" class="row mb-5">
            <div class="col-md-8 col-xl-6 text-center mx-auto">
                <div style="display: flex;justify-content: center">
                    <button onclick="removeDay({{day_number}})" class="btn btn-close"></button>
                    <h5 id="day-title" class="fw-bold ms-1">Giorno {{day_number}}</h5>
                </div>
            </div>
            <table>
                <thead>
                <tr>
                    <th width="33%" style="text-align: center">Esercizio</th>
                    <th width="33%" style="text-align: center">Ripetizioni</th>
                    <th width="33%" style="text-align: center">Serie</th>
                </tr>
                </thead>
                <tbody id="workoutDayTable-{{day_number}}">
                                {{exercise_rows}}
                <tr id="addExerciseRow-{{day_number}}">
                    <td colspan="3">
                        <div style="display: flex; justify-content: center">
                            <button onclick="addExercise({{day_number}})" class="btn btn-light"> + </button>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    `;
    return render(body, data);
}


function addDay() {
    let day_number = document.getElementById("workoutPlanContent").childElementCount + 1;
    if(day_number === 0 || day_number === undefined || day_number === null){
        day_number = 1;
    }
    let exercise_rows = [getExerciseRow(exercises)];
    let day_template = getWorkoutDayTemplate(day_number, exercise_rows);
    let day = document.createElement("div");
    day.innerHTML = day_template;
    document.getElementById("workoutPlanContent").appendChild(day);
}

function removeDay(day_number) {
    let workoutPlanContent = document.getElementById("workoutPlanContent");
    let child = workoutPlanContent.children[day_number - 1];
    workoutPlanContent.removeChild(child);
    for (i = 1; i < day_number - 1; i++) {
        let day = document.getElementById("day" + i);
        day.id = "day" + i;
        day.getElementById("day-title")[0].innerHTML = "Giorno " + i;
    }
}

function addExercise(day_number) {
    let exercise_row = getExerciseRow(exercises);
    let exercise_tr = document.createElement("tr");
    exercise_tr.innerHTML = exercise_row;
    let last_tr = document.getElementById("addExerciseRow-" + day_number);
    document.getElementById("workoutDayTable-" + day_number).insertBefore(exercise_tr, last_tr)
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

function updateWorkout() {
    let workoutPlanContent = document.getElementById("workoutPlanContent");
    let days = [];
    for (let day_number = 1; day_number < workoutPlanContent.childElementCount + 1; day_number++) {
        let exercise_rows = document.getElementById("workoutDayTable-" + day_number).children;
        let exercises = [];
        for (let j = 0; j < exercise_rows.length - 1; j++) {
            let exercise_row = exercise_rows[j];
            let exercise = exercise_row.querySelector("#exerciseSelect").value;
            let reps = exercise_row.querySelector("#reps-input").value;
            let sets = exercise_row.querySelector("#sets-input").value;
            exercises.push({
                exercise: parseInt(exercise),
                reps: parseInt(reps),
                sets: parseInt(sets)
            });
        }
        days.push({
            day: parseInt(day_number),
            exercises: exercises
        });
    }
    let workoutPlanJson = {
        "id": workoutPlan['id'],
        "days": days,
        "expirationDay": document.getElementById("workoutExpirationDayInput").value
    };
    let token = getCookie('csrftoken');

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/workout/manage/saveWorkout/" + userName, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', token);
    xhr.send(JSON.stringify(workoutPlanJson));
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location.href = "/workout/manage/";
        } else {
            alert("Errore durante il salvataggio del piano di allenamento");
        }
    }

}

function initWorkout() {

    let day_number = 1;
    let exercise_rows = [getExerciseRow(exercises)];
    workoutPlan["days"].forEach(function (day) {
        let exercise_rows = [];
        day["exercises"].forEach(function (exercise) {
            exercise_rows.push(getExerciseRow(exercises, exercise));
        });
        let day_template = getWorkoutDayTemplate(day_number, exercise_rows);
        let dayDiv = document.createElement("div");
        dayDiv.innerHTML = day_template;
        document.getElementById("workoutPlanContent").appendChild(dayDiv);
        day_number++;
    });
    let day_template = getWorkoutDayTemplate(day_number, exercise_rows);
    let day = document.createElement("div");
    day.innerHTML = day_template;
}

document.addEventListener("DOMContentLoaded", function () {
    let endDate = workoutPlan["expected_end_date"]
    let tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    let tomorrow_string = tomorrow.toISOString().split('T')[0];
    let endDate_string = endDate.split('T')[0].split(' ')[0];
    let datePicker = document.getElementById('workoutExpirationDayInput');
    datePicker.min = tomorrow_string;
    datePicker.value = endDate_string;

    initWorkout();
    document.getElementById("addDayButton").addEventListener("click", addDay);
    document.getElementById("saveWorkoutButton").addEventListener("click", updateWorkout);
});