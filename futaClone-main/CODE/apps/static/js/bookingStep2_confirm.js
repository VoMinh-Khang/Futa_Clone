//active floor on responsive screen
let routeSeats = [...document.querySelectorAll('.route-seat')];

routeSeats.forEach((item, index) => {
    let buttonFloorControls = [...item.querySelectorAll('.route-seat-title div')];
    let floors = [...item.querySelectorAll('.route-seat-floor-item')];

    buttonFloorControls.forEach((ele, ind) => {
        ele.onclick = () => {
            if (screen.width <= 767) {
                removeFloorControlActive(buttonFloorControls);
                addFloorNone(floors);

                ele.classList.add('seat-title-active');

                floors[ind].classList.remove('this-floor-not');
            }
        }
    })
})

function removeFloorControlActive(buttons) {
    buttons.forEach(ele => ele.classList.remove('seat-title-active'));
}

function addFloorNone(floors) {
    floors.forEach(ele => ele.classList.add('this-floor-not'));
}

function removeFloorNone(floors) {
    floors.forEach(ele => ele.classList.remove('this-floor-not'));
}

// on edit seat route
let editBtn = document.querySelector('.confirm-seat-btn');
let editSeatRoute = document.querySelector('.confirm-seat');

editBtn.onclick = () => {
    editSeatRoute.classList.toggle('on-edit-active');
}

// on pickup active 
let pickupField = document.querySelector('.confirm-pickup-field');
let pickupBlock = document.querySelector('.confirm-pickup');
let pickupValue = [...document.querySelectorAll('.confirm-pickup-item')];

pickupField.onclick = (e) => {
    // e.stopPropagation();
    pickupBlock.classList.toggle('on-field-active');
}

pickupValue.forEach((item, index) => {
    item.onclick = (e) => {
        // e.stopPropagation();
        pickupBlock.classList.toggle('on-field-active');
        pickupField.querySelector('input[type="text"]').value = item.querySelector('.confirm-pickup-location').innerHTML;
    }
})