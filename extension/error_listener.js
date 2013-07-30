var JSErrorCollector_errors = {
	getSavedErrors: function() {
		var savedErrors = [];
		if (!!localStorage.JSErrors)
				savedErrors = JSON.parse(localStorage.JSErrors);

		return savedErrors;
	},
	saveErrors: function(pErrors) {
		localStorage.JSErrors = JSON.stringify(pErrors);
	},
	push: function (jsError) {
		var list = this.getSavedErrors();
		list.push(jsError);
		this.saveErrors(list);
	},
	pump: function() {
		var list = this.getSavedErrors();
		this.clear();
		return list;
	},
	clear: function() {
		this.saveErrors([]);
	}
};