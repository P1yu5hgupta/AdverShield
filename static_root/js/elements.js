window.addEventListener('scroll', (event) => {
	const articleHeight = document.getElementById('models').clientHeight;
	// console.log(articleHeight);

	const bodyTop = document.documentElement.scrollTop;
	// console.log(bodyTop);
	scrolled = 10 + (bodyTop / articleHeight) * 100;
	if (scrolled > 100) scrolled = 100;
	// console.log(scrolled);
	document.documentElement.style.setProperty(
		'--article-read-size',
		`${scrolled}%`
	);
});

function showLoader() {
	document.getElementById('loaderDiv').style.display = 'block';
}

function hideLoader() {
	document.getElementById('loaderDiv').style.display = 'none';
}

function alert(message) {
	document.getElementById('modal-body').innerHTML = message;
	document.getElementById('main-modal').style.display = 'block';
}
function alertClose() {
	document.getElementById('main-modal').style.display = 'none';
}
