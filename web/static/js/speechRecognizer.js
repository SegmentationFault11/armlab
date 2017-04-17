var recognizing;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
reset();
recognition.onend = reset();

recognition.onresult = function (event) {
	console.log('@@@')
	for (var i = event.resultIndex; i < event.results.length; ++i) {
		console.log(event.results[i][0].transcript)
			trans.value += event.results[i][0].transcript;
			trans.value += " ";
	}
}

function reset() {
	recognizing = false;
}

function toggleStartStop() {
	if (recognizing) {
		$("#recbutton").removeClass("playing");
		$("#recbutton").addClass("disabled");
		recognition.stop();
		reset();
	} else {
		$("#recbutton").removeClass("disabled");
		$("#recbutton").addClass("playing");
		recognition.start();
		recognizing = true;
	}
}
