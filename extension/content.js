var JSErrorCollector = {
	getSavedErrors: function() {
		var savedErrors = [];
		if (!!localStorage.JSErrors)
				savedErrors = JSON.parse(localStorage.JSErrors);

		return savedErrors;
	},
	saveErrors: function(errors) {
		localStorage.JSErrors = JSON.stringify(errors);
	},
	push: function (jsErrors) {
		var list = this.getSavedErrors();
		list.push(jsErrors);
		this.saveErrors(list);
	},
	pump: function() {
		var list = this.getSavedErrors();
		this.clear();
		return list;
	},
	clear: function() {
		this.saveErrors([]);
	},
	onError: function(errorMessage, sourceName, lineNumber) {
		if(!errorMessage.message) {
			return;
		}
		if(!!errorMessage.filename) {
			sourceName = errorMessage.filename;
		}
		if(!!errorMessage.lineno) {
			lineNumber = errorMessage.lineno;
		}

		if(!!errorMessage.target.chrome && !sourceName && !lineNumber && errorMessage.message != 'Script error.') {
			return;
		}	

		errorMessage = errorMessage.message;
		if(errorMessage == 'Script error.') {
			var error = {
				errorMessage: errorMessage,
				sourceName: '',
				lineNumber: 0,
				pageUrl: document.location.href	
			}
		} else {
			var error = {
				errorMessage: errorMessage.replace(/^Uncaught /g, ''),
				sourceName: sourceName,
				lineNumber: lineNumber,
				pageUrl: document.location.href	
			}
		}

		JSErrorCollector.push(error);
	},
	initialize: function() {
		window.addEventListener('error', JSErrorCollector.onError, false);
		var s = document.createElement('script');
		s.src = chrome.extension.getURL('error_listener.js');
		(document.head||document.documentElement).appendChild(s);
			s.onload = function() {
			s.parentNode.removeChild(s);
		};
	}
};

JSErrorCollector.initialize();