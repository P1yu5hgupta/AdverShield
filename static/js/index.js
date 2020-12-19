function initialize() {
	return;
}

function validateEmail(email) {
	const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(String(email).toLowerCase());
}

function showSliderValue(n) {
	var slider = document.getElementById('model' + n + 'Slider');
	var output = document.getElementById('model' + n + 'ShowValue');
	output.innerHTML = slider.value;
}

function formatFGSMResults(response) {
	response['classes'] = response['classes'].split(',');
	final_text = "<div class='col-sm-12'>";
	final_text += "<div class='row'>	<div class='col-sm-6'>";
	final_text +=
		"Best Classification:</div><div class='col-sm-6 base2'>" +
		response['classes'][0] +
		'</div></div>';
	if (response['classes'].length > 1) {
		final_text += "<div class='row'>	<div class='col-sm-6'>";
		final_text +=
			"Other Classifications:</div><div class='col-sm-6 base2'>" +
			'' +
			'</div></div>';
		for (let i = 1; i < response['classes'].length; i++) {
			final_text += "<div class='row'>	<div class='col-sm-6'>";
			final_text +=
				"</div><div class='col-sm-6 base2'>" +
				response['classes'][i] +
				'</div></div>';
		}
	}
	final_text += '</div>';
	document.getElementById('model1Results').innerHTML = final_text;
}

async function fetchFGSMResults() {
	showLoader();
	option_selected = document.getElementById('model1Select').value;
	epsilon_value = document.getElementById('model1Slider').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	endpoint =
		'fetchFGSMAttack?image_name=' +
		option_selected +
		'&epsilon_value=' +
		epsilon_value;
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	if (response['status'] == 'found') formatFGSMResults(response);
	document.getElementById('model1Perturbation').src =
		'static/images/fgsmattack/perbutation.jpg' + '?' + new Date().getTime();
	document.getElementById('model1Adversarial').src =
		'static/images/fgsmattack/fgsmAdversarial.jpg' + '?' + new Date().getTime();

	hideLoader();
	alert(response['message']);
}

async function fetchFGSMExample() {
	showLoader();
	option_selected = document.getElementById('model1Select').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	document.getElementById('model1Image').src =
		'static/images/fgsmattack/' + option_selected;

	endpoint =
		'fetchFGSMAttack?image_name=' + option_selected + '&epsilon_value=0';
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	formatFGSMResults(response);
	document.getElementById('model1Perturbation').src = '';
	document.getElementById('model1Adversarial').src = '';
	hideLoader();
	// alert(response['message']);
}

function formatOnePixelResults(response) {
	final_text = "<div class='col-sm-12'>";
	final_text += "<div class='row'>	<div class='col-sm-6'>";
	final_text +=
		response['classes'] +
		"</div><div class='col-sm-6 base2'>" +
		response['percent'] +
		'%</div></div>';
	final_text +=
		'</div><div class="row"><img class="modelImage" src="" id="model2Adversarial"></div>';

	document.getElementById('model2Results').innerHTML = final_text;
}

async function fetchOnePixelResults() {
	showLoader();
	option_selected = document.getElementById('model2Select').value;
	epsilon_value = document.getElementById('model2Slider').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	endpoint =
		'fetchOnePixelAttack?image_name=' +
		option_selected +
		'&epsilon_value=' +
		epsilon_value;
	// console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	// console.log(response);
	if (response['status'] == 'found') formatOnePixelResults(response);
	document.getElementById('model2Adversarial').src =
		'static/images/onepixelattack/adversarial.jpg' + '?' + new Date().getTime();
	hideLoader();
	alert(response['message']);
}

async function fetchOnePixelExample() {
	showLoader();
	option_selected = document.getElementById('model2Select').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	document.getElementById('model2Image').src =
		'static/images/onepixelattack/' + option_selected;

	endpoint = 'fetchOnePixelAttackPredict?image_name=' + option_selected;
	// console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	formatOnePixelResults(response);
	hideLoader();
	// alert(response['message']);
}

function formatCWResults(response) {
	final_text = "<div class='col-sm-6'>";
	final_text += response['classes'];
	final_text += '</div><img class="model3Image" src="" id="model3Adversarial">';

	document.getElementById('model3Results').innerHTML = final_text;
}

async function fetchCWResults() {
	showLoader();
	option_selected = document.getElementById('model3Select').value;
	epsilon_value = document.getElementById('model3Slider').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	endpoint =
		'fetchCWAttack?image_name=' +
		option_selected +
		'&epsilon_value=' +
		epsilon_value;
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	if (response['status'] == 'found') formatCWResults(response);
	document.getElementById('model3Adversarial').src =
		'static/images/cwattack/adversarial.jpg' + '?' + new Date().getTime();

	hideLoader();
	alert(response['message']);
}

async function fetchCWExample() {
	showLoader();
	option_selected = document.getElementById('model3Select').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	document.getElementById('model3Image').src =
		'static/images/cwattack/' + option_selected;

	endpoint = 'fetchCWAttack?image_name=' + option_selected + '&epsilon_value=0';
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	formatCWResults(response);
	hideLoader();
	// alert(response['message']);
}

function formatBIResults(response) {
	final_text = "<div class='col-sm-12'>";
	final_text += "<div class='row'>	<div class='col-sm-6'>";
	final_text +=
		"Best Classification:</div><div class='col-sm-6 base2'>" +
		response['classes'] +
		'</div></div>';
	final_text += '</div>';
	document.getElementById('model4Results').innerHTML = final_text;
}

async function fetchBIResults() {
	showLoader();
	option_selected = document.getElementById('model4Select').value;
	epsilon_value = document.getElementById('model41Slider').value;
	iteration_count = document.getElementById('model42Slider').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	endpoint =
		'fetchBIAttack?image_name=' +
		option_selected +
		'&epsilon_value=' +
		epsilon_value +
		'&iteration_count=' +
		iteration_count;
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	if (response['status'] == 'found') formatBIResults(response);
	document.getElementById('model4Perturbation').src =
		'static/images/biattack/perbutation.jpg' + '?' + new Date().getTime();
	document.getElementById('model4Adversarial').src =
		'static/images/biattack/adversarial.jpg' + '?' + new Date().getTime();

	hideLoader();
	alert(response['message']);
}

async function fetchBIExample() {
	showLoader();
	option_selected = document.getElementById('model4Select').value;
	if (option_selected == 'None') {
		hideLoader();
		alert('Select an image');
		return;
	}
	document.getElementById('model4Image').src =
		'static/images/biattack/' + option_selected;

	endpoint =
		'fetchBIAttack?image_name=' +
		option_selected +
		'&epsilon_value=0&iteration_count=0';
	console.log(endpoint);
	response = await makeAsyncGetRequest(endpoint);
	console.log(response);
	formatBIResults(response);
	document.getElementById('model4Perturbation').src = '';
	document.getElementById('model4Adversarial').src = '';
	hideLoader();
	// alert(response['message']);
}
