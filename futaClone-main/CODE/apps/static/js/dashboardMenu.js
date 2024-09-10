//dashboard menu
let adminSidebar = document.querySelector('.sidebar');
let adminMain = document.querySelector('.main');
let adminToggle = document.querySelector('.header-toggle');

adminToggle.onclick = () => {
    adminMain.classList.toggle('main-move-padding');
    adminSidebar.classList.toggle('sidebar-move-margin');
}

//dashboard header user 
let adminUser = document.querySelector('.header-user');
let userBox = document.querySelector('.header-profile');

adminUser.onclick = (e) => {
    userBox.classList.add('user-visible');

}

window.onclick = (e) => {
    if (!e.target.closest('.header-user') && !e.target.matches('.header-profile')) {
        userBox.classList.remove('user-visible');
    }
    if ((window.screen.width <= 549) && !e.target.closest('.sidebar') && !e.target.closest('.header-toggle')) {
        adminSidebar.classList.remove('sidebar-move-margin');
    }
}