class MyFooter extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
<footer class="footer">
        <div class="container">
            <div class="footer-list">
                <div class="footer-item footer-info">
                    <h3 class="footer-title footer-info-title">Tổng đài đặt vé và CSKH</h3>
                    <div class="footer-info-local">
                        <div class="footer-info-phone"><a href="tel:19006067">1900 6067</a></div>
                        <a href="#" class="footer-info-sub">
                            <img src="./../images/home-footer-subscribe.png" alt="" class="footer-info-img">
                        </a>
                    </div>
                    <p class="footer-info-name">CÔNG TY CỔ PHẦN XE KHÁCH PHƯƠNG TRANG FUTA BUS LINES</p>
                    <p class="footer-info-address"> Địa chỉ: 468-468A Lê Văn Lương, P.Tân Phong, Q.7, TP Hồ Chí Minh.
                    </p>
                    <p class="footer-info-mail">Email: <a href="mailto:hotro@futabus.vn">hotro@futabus.vn</a></p>
                    <div class="footer-info-contact">
                        <p class="footer-info-call">Điện thoại: <a href="tel:02838386852">028 3838 6852</a></p>
                        <p class="footer-info-call">Fax: <a href="tel:02838386853">028 3838 6853</a></p>
                    </div>
                </div>
                <div class="footer-item footer-line">
                    <h3 class="footer-title footer-line-title">FUTA Bus Lines</h3>
                    <div class="footer-nav">
                        <ul class="footer-nav-left">
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Về chúng tôi</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Lịch trình</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Tin tức</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Tuyển dụng</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Tra cứu thông tin đặt vé</a>
                            </li>
                        </ul>
                        <ul class="footer-nav-right">
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Điều khoản sử dụng</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Hỏi đáp</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Hướng dẫn đặt vé trên Web</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Hướng dẫn đặt vé trên App</a>
                            </li>
                            <li class="footer-nav-item">
                                <i class='bx bx-chevrons-right footer-nav-icon'></i>
                                <a href="#" class="footer-nav-link">Mạng lưới văn phòng</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="footer-item footer-connect">
                    <div class="footer-connect-item">
                        <h3 class="footer-title footer-connect-title">kết nối với chúng tôi</h3>
                        <div class="footer-connect-link">
                            <a href="#" class="footer-connect-social"><img src="./../images/fb.png" alt=""></a>
                            <a href="#" class="footer-connect-social"><img src="./../images/ytb.png" alt=""></a>
                        </div>
                    </div>
                    <div class="footer-connect-item">
                        <h3 class="footer-title footer-connect-title">tải app futa</h3>
                        <div class="footer-connect-link">
                            <a href="#" class="footer-connect-app"><i class='bx bxl-apple'></i>App Store</a>
                            <a href="#" class="footer-connect-app"><i class='bx bxl-play-store'></i>CH Play</a>
                        </div>
                    </div>
                </div>
                <div class="footer-item footer-feature">
                    <a href="#" class="footer-feature-item">
                        <img src="./../images/home-footer-bottom1.png" alt="" class="footer-feature-img">
                    </a>
                    <a href="#" class="footer-feature-item">
                        <img src="./../images/home-footer-bottom2.png" alt="" class="footer-feature-img">
                    </a>
                    <a href="#" class="footer-feature-item">
                        <img src="./../images/home-footer-bottom3.png" alt="" class="footer-feature-img">
                    </a>
                    <a href="#" class="footer-feature-item">
                        <img src="./../images/home-footer-bottom4.png" alt="" class="footer-feature-img">
                    </a>
                </div>
            </div>
            <div class="footer-end">
                &copy; 2022 | Bản quyền thuộc về Công ty Cổ Phần Xe Khách Phương Trang FUTA Bus Lines | www.futabus.vn |
                Chịu trách nhiệm nội dung: Đinh Văn Huỳnh
            </div>
        </div>
    </footer>
`
    }
}

async function createFooter() {
    await customElements.define('my-footer', MyFooter);
    let newFooter = document.querySelector('my-footer');
    console.log(newFooter);
}
createFooter();