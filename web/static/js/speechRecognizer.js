var recognizing;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
reset();
recognition.onend = reset();

recognition.onresult = function (event) {
	for (var i = event.resultIndex; i < event.results.length; ++i) {
		if (event.results[i].isFinal) {
			trans.value += event.results[i][0].transcript;
			trans.value += " ";
		}
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
