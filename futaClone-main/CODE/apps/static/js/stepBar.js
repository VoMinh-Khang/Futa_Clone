class MyBookingStepBar extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <section class="step">
        <div class="mini-container">
            <div class="step-bar">
                <ul class="step-number">
                    <li class="step-number-first step-number-item step-number-processing">
                        <div class="step-number-title">chọn tuyến</div>
                        <div class="step-number-circles">1</div>
                    </li>
                    <li class="step-number-second step-number-item step-number-waiting">
                        <div class="step-number-title">xác nhận lộ trình</div>
                        <div class="step-number-circles">2</div>
                    </li>
                    <li class="step-number-third step-number-item step-number-waiting">
                        <div class="step-number-title">thông tin khách hàng</div>
                        <div class="step-number-circles">3</div>
                    </li>
                    <li class="step-number-fourth step-number-item step-number-waiting">
                        <div class="step-number-title">thanh toán</div>
                        <div class="step-number-circles">4</div>
                    </li>
                </ul>
                <ul class="step-line">
                    <li class="step-line-first step-line-item step-line-item-waiting"></li>
                    <li class="step-line-second step-line-item step-line-item-waiting"></li>
                    <li class="step-line-third step-line-item step-line-item-waiting"></li>
                </ul>
            </div>
        </div>
    </section>
        `
    }
}
class MyBookingStepBarSecond extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <section class="step">
        <div class="mini-container">
            <div class="step-bar">
                <ul class="step-number">
                    <li class="step-number-first step-number-item step-number-completed">
                        <div class="step-number-title">chọn tuyến</div>
                        <div class="step-number-circles">1</div>
                    </li>
                    <li class="step-number-second step-number-item step-number-processing">
                        <div class="step-number-title">xác nhận lộ trình</div>
                        <div class="step-number-circles">2</div>
                    </li>
                    <li class="step-number-third step-number-item step-number-waiting">
                        <div class="step-number-title">thông tin khách hàng</div>
                        <div class="step-number-circles">3</div>
                    </li>
                    <li class="step-number-fourth step-number-item step-number-waiting">
                        <div class="step-number-title">thanh toán</div>
                        <div class="step-number-circles">4</div>
                    </li>
                </ul>
                <ul class="step-line">
                    <li class="step-line-first step-line-item step-line-item-completed"></li>
                    <li class="step-line-second step-line-item step-line-item-waiting"></li>
                    <li class="step-line-third step-line-item step-line-item-waiting"></li>
                </ul>
            </div>
        </div>
    </section>
        `
    }
}
class MyBookingStepBarThird extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <section class="step">
        <div class="mini-container">
            <div class="step-bar">
                <ul class="step-number">
                    <li class="step-number-first step-number-item step-number-completed">
                        <div class="step-number-title">chọn tuyến</div>
                        <div class="step-number-circles">1</div>
                    </li>
                    <li class="step-number-second step-number-item step-number-completed">
                        <div class="step-number-title">xác nhận lộ trình</div>
                        <div class="step-number-circles">2</div>
                    </li>
                    <li class="step-number-third step-number-item step-number-processing">
                        <div class="step-number-title">thông tin khách hàng</div>
                        <div class="step-number-circles">3</div>
                    </li>
                    <li class="step-number-fourth step-number-item step-number-waiting">
                        <div class="step-number-title">thanh toán</div>
                        <div class="step-number-circles">4</div>
                    </li>
                </ul>
                <ul class="step-line">
                    <li class="step-line-first step-line-item step-line-item-completed"></li>
                    <li class="step-line-second step-line-item step-line-item-completed"></li>
                    <li class="step-line-third step-line-item step-line-item-waiting"></li>
                </ul>
            </div>
        </div>
    </section>
        `
    }
}
class MyBookingStepBarFourth extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <section class="step">
        <div class="mini-container">
            <div class="step-bar">
                <ul class="step-number">
                    <li class="step-number-first step-number-item step-number-completed">
                        <div class="step-number-title">chọn tuyến</div>
                        <div class="step-number-circles">1</div>
                    </li>
                    <li class="step-number-second step-number-item step-number-completed">
                        <div class="step-number-title">xác nhận lộ trình</div>
                        <div class="step-number-circles">2</div>
                    </li>
                    <li class="step-number-third step-number-item step-number-completed">
                        <div class="step-number-title">thông tin khách hàng</div>
                        <div class="step-number-circles">3</div>
                    </li>
                    <li class="step-number-fourth step-number-item step-number-processing">
                        <div class="step-number-title">thanh toán</div>
                        <div class="step-number-circles">4</div>
                    </li>
                </ul>
                <ul class="step-line">
                    <li class="step-line-first step-line-item step-line-item-completed"></li>
                    <li class="step-line-second step-line-item step-line-item-completed"></li>
                    <li class="step-line-third step-line-item step-line-item-completed"></li>
                </ul>
            </div>
        </div>
    </section>
        `
    }
}

async function createStepBarFirst() {
    await customElements.define('my-step-bar', MyBookingStepBar);
    let newStepBar = document.querySelector('my-step-bar');
    console.log(newStepBar);
}

async function createStepBarSecond() {
    await customElements.define('my-step-bar-second', MyBookingStepBarSecond);
    let newStepBar = document.querySelector('my-step-bar-second');
    console.log(newStepBar);
}

async function createStepBarThird() {
    await customElements.define('my-step-bar-third', MyBookingStepBarThird);
    let newStepBar = document.querySelector('my-step-bar-third');
    console.log(newStepBar);
}

async function createStepBarFourth() {
    await customElements.define('my-step-bar-fourth', MyBookingStepBarFourth);
    let newStepBar = document.querySelector('my-step-bar-fourth');
    console.log(newStepBar);
}
createStepBarFirst();
createStepBarSecond();
createStepBarThird();
createStepBarFourth();