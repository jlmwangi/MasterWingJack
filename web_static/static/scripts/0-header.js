function showSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'flex';
}

function hideSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = 'none';
}

let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    if (window.scrollY < lastScrollY) {
	// scrolling up
	document.querySelector('.header-content').classList.add('stick-on-scroll-up');
    } else {
	// scrolling down
	document.querySelector('.header-content').classList.remove('stick-on-scroll-up');
    }
    lastScrollY = window.scrollY;
});
