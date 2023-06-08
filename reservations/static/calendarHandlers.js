var active_row = null;
var active_day_number = null;

function makeGetRequest(url, year, month, day) {
    return fetch(url + "?year=" + year + "&month=" + month + "&day=" + day)
        .then(response => response.json())
        .then(data => {
            // Estrarre oggetti dall'array JSON
            return data;
        })
        .catch(error => {
            alert("Errore: " + error);
        });
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

async function makeReservation(day, hour) {
    let token = getCookie('csrftoken');
    return fetch('/reservations/makereservation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify({
            'year': parseInt(variables.getAttribute('year')),
            'month': parseInt(variables.getAttribute('month')),
            'day': day,
            'hour': hour,
        }),

    });
}

async function deleteReservation(day, hour) {
    var token = document.getElementById('csrf-token').getAttribute('data-csrf-token');

    return fetch('/reservations/deletereservation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify({
            'year': parseInt(variables.getAttribute('year')),
            'month': parseInt(variables.getAttribute('month')),
            'day': day,
            'hour': hour,
        }),

    });
}

async function generateDayInfo(day) {
    let variables = document.getElementById('variables');
    let year = variables.getAttribute('year');
    let month = variables.getAttribute('month');

    let container = document.createElement('div');
    container.id = 'container';
    container.style.width = '100%';

    let timeline = document.createElement('div');
    timeline.classList = ['timeline'];

    let timeSlots = Array.from({length: 24}, (_, index) => index);
    let dayData = await makeGetRequest('/reservations/dayinfo/', year, month, day);
    let openHours = dayData.openHours;
    let fullHours = dayData.fullHours
    let reservations = dayData.reservations;
    timeSlots.forEach(function (timeSlot) {
        var button = document.createElement('button');
        button.style.padding = '0';
        button.style.margin = '0';

        var slot = document.createElement('div');
        button.appendChild(slot);
        slot.classList = ['time-slot'];
        slot.textContent = timeSlot < 10 ? "0" + timeSlot + ":00" : timeSlot + ":00";
        if (openHours.includes(timeSlot)) {
            slot.title = "Clicca per prenotare"
            slot.style.backgroundColor = "green";
            button.onclick = function () {
                makeReservation(parseInt(day), parseInt(timeSlot)).then(async () => {
                    active_row.children.item(1).innerHTML = '';
                    active_row.children.item(1).appendChild(await generateDayInfo(day));
                }).catch(error => {
                    alert("Errore: " + error);
                })
            }
        } else {
            slot.title = "Palestra chiusa!"
            slot.style.backgroundColor = "red";
        }
        if (fullHours.includes(timeSlot)) {
            slot.title = "Palestra piena!"
            slot.style.backgroundColor = "orange";
        }
        if (reservations.includes(timeSlot)) {
            slot.title = "Clicca per cancellare la prenotazione"
            slot.style.backgroundColor = "blue";
            button.onclick = function () {
                deleteReservation(parseInt(day), parseInt(timeSlot)).then(async () => {
                    active_row.children.item(1).innerHTML = '';
                    active_row.children.item(1).appendChild(await generateDayInfo(day));
                }).catch(error => {
                    alert("Errore: " + error);
                })
            }
        }

        if (openHours.includes(timeSlot) || reservations.includes(timeSlot)) {
            timeline.appendChild(button);
        } else {
            timeline.appendChild(slot);
        }
    });

    container.appendChild(timeline);

    return container;
}

document.addEventListener("DOMContentLoaded", function () {
    let elements = document.getElementsByClassName("calendar-button");
    for (let i = 0; i < elements.length; i++) {
        let calendarDayButton = elements[i];
        let calendarDay = calendarDayButton.getAttribute('day');
        let row = calendarDayButton.getAttribute('row');
        calendarDayButton.addEventListener("click", async function () {
            if (active_row != null) {
                active_row.style.display = 'none';
                let header = active_row.children.item(0);
                header.children.item(0).innerHTML = '';
                active_row.children.item(1).innerHTML = '';
            }
            if (active_day_number === calendarDay) {
                active_row = null;
                active_day_number = null;
                return;
            }
            active_day_number = calendarDay;
            active_row = document.getElementById("day-info-" + row);
            let cardHeader = active_row.children.item(0)
            let headerTitle = cardHeader.children.item(0);
            let headerButton = cardHeader.children.item(1);
            let cardBody = active_row.children.item(1);
            headerTitle.innerHTML = "Orari - " + calendarDay;
            if (headerButton != null) headerButton.href = calendarDay + "-" + variables.getAttribute('month') + "-" + variables.getAttribute('year') + "/openinghours/";
            cardBody.appendChild(await generateDayInfo(calendarDay));
            active_row.style.display = 'block';
        });
    }
});

