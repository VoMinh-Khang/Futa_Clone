let allEmptySeats = [...document.querySelectorAll('.route-seat-item')];

let allRealSeats = removeNoneSeat(allEmptySeats);

let seatDisplay = document.querySelector('.confirm-seat-list');

let seatCollection = document.querySelector('.route-result-name');

let seatCost = document.querySelector('.route-result-cost-value');

let continueButton = document.querySelector('.step-next-btn');

let seatCount = document.querySelector('.route-result-count-value');

let pickupPlace = document.querySelector('.confirm-pickup-field #pick-up-field');

let errorBox = document.querySelector('.error-list');

let dataBooking = JSON.parse(window.localStorage.getItem('dataBooking'));

let seatsChoosing = dataBooking.seats;

async function activeCurrentSeats() {
    let currentSeats = await findCurrentSeatsChoosing(allRealSeats, seatsChoosing);

    // display all seat
    displayAllCurrentSeats(seatDisplay, currentSeats);

    // display all seat and total cost
    displayCurrentCostAndSeats(seatCollection, currentSeats, seatCost, dataBooking);

    //handle click all case
    handleClickSeat(allRealSeats);

    //handle continue button
    handleContinueButton(continueButton, seatsChoosing);
}

activeCurrentSeats();

function handleClickSeat(allSeats) {
    allSeats.forEach(seat => {
        seat.onclick = () => {
            limitSeatsChoosing(seat, seatsChoosing);
            // addSeatsAndChangeState();
            displaySeatInfoCost(seatCollection, seatCost, seatsChoosing, seatCount, dataBooking.ticketCost);
        }
    })
}

function limitSeatsChoosing(seat, seatsChoosing) {
    if (seat.classList.contains('seat-active')) {
        seat.classList.add('seat-empty');
        seat.classList.remove('seat-active');

        removeSeatFromChoosing(seat, seatsChoosing);
    } else if (seat.classList.contains('seat-empty')) {
        if (seatsChoosing.length === 5) {
            alertSeatChoosingError(false, ['Số lượng ghế tối đa là 5...'], errorBox);
        } else {
            seat.classList.remove('seat-empty');
            seat.classList.add('seat-active');

            seatsChoosing.push(seat.querySelector('text').innerHTML);
        }
    }
}

function removeSeatFromChoosing(seat, seatsChoosing) {
    let index = seatsChoosing.indexOf(seat.querySelector('text').innerHTML);
    if (index > -1) {
        seatsChoosing.splice(index, 1);
    }
}

function displaySeatInfoCost(seatCollection, seatCost, seatsChoosing, seatCount, ticketCost) {
    seatCollection.innerHTML = seatsChoosing.map((seat, index) => {
        if (seatsChoosing.length === 1 || index === seatsChoosing.length - 1) {
            return seat;
        } else {
            return seat + ', ';
        }
    }).join('');
    seatCount.innerHTML = seatsChoosing.length;
    seatCost.innerHTML = `${ticketCost * seatsChoosing.length}.000<span>&#8363;</span>`
}

function handleContinueButton(continueButton, seatsChoosing) {
    continueButton.onclick = () => {
        let { result, errorMessage } = continueValidationSeat(seatsChoosing);
        let { result: pickupResult, errorMessage: PickupMessage } = continueValidationPickup(pickupPlace);

        let errorContain = [errorMessage, PickupMessage];
        alertSeatChoosingError(result, errorContain, errorBox);
        alertSeatChoosingError(pickupResult, errorContain, errorBox);

        if (result && pickupResult) {
            let totalCost = dataBooking.ticketCost * seatsChoosing.length;
            getDataForLocalStorage(seatsChoosing, totalCost, pickupPlace, dataBooking);
        }
    }
}

function continueValidationSeat(seatsChoosing) {
    const state = {
        result: true,
        errorMessage: '',
    };

    if (seatsChoosing.length === 0) {
        state.result = false;
        state.errorMessage = 'Vui lòng chọn ghế...';
    }
    return state;
}

function continueValidationPickup(pickupPlace) {
    const state = {
        result: true,
        errorMessage: '',
    };

    if (pickupPlace.value === '') {
        state.result = false;
        state.errorMessage = 'Vui lòng điểm lên xe...';
    }
    return state;
}

function displayAllCurrentSeats(seatDisplay, currentSeats) {
    seatDisplay.innerHTML = currentSeats.map(seat => {
        seat.classList.add('seat-active');
        return `<span class="confirm-seat-item">${seat.querySelector('text').innerHTML}</span>`
    });
}

function displayCurrentCostAndSeats(seatCollection, currentSeats, seatCost, dataBooking) {
    seatCollection.innerHTML = currentSeats.map(seat => {
        seatCost.innerHTML = `${dataBooking.totalCost}.000 <span>&#8363;</span>`;
        return `<span class="route-result-name-ticket">${seat.querySelector('text').innerHTML}</span>`
    });
}

function removeNoneSeat(allSeats) {
    realSeats = allSeats.filter(seat => {
        return seat.querySelector('svg').style.display !== 'none';
    })

    return realSeats;
}

function findCurrentSeatsChoosing(seats, seatsChoosing) {
    let attachSeats = seats.filter(seat => {
        if (isSeatsMatchData(seat, seatsChoosing)) return seat;
    });

    return attachSeats;
}

function isSeatsMatchData(seat, seatsData) {
    let seatMatch = undefined;

    for (let i = 0; i < seatsData.length; i++) {
        if (seat.querySelector('text').innerHTML === seatsData[i]) {
            seatMatch = seat;
            break;
        }
    }

    return seatMatch;
}

function alertSeatChoosingError(result, errorContain, errorBox) {
    if (result === false) {
        errorBox.innerHTML = errorContain.map(error => {
            return `<li class="error-item">${error}</li>`
        }).join('');

        errorBox.parentElement.classList.add('error-validation-active');

        let timeAdd = setTimeout(() => {
            errorBox.parentElement.classList.remove('error-validation-active');
        }, 5000);
    }
}

function getDataForLocalStorage(seats, totalCost, pickupPlace, dataBooking) {
    let pickup = pickupPlace.value;
    let data = {
        ...dataBooking, ...{
            seats,
            totalCost,
            pickup
        }
    }

    window.localStorage.setItem('dataBooking', JSON.stringify(data));
}