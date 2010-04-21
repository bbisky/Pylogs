tinyMCEPopup.requireLangPack();

var CodeDialog = {
	init : function(ed) {
		tinyMCEPopup.resizeToInnerSize();
	},

	insert : function(file, title) {
		var code_name = document.forms[0].codeSelect.options[document.forms[0].codeSelect.selectedIndex].value;
		var code_content = document.forms[0].codeTextArea.value.replace(/</gi, "&lt;").replace(/\n/gi, "<br />");

		tinyMCEPopup.restoreSelection();
		tinyMCE.execCommand("mceInsertContent", false, ("<pre name=\"code\" class=\"" + code_name + "\">" + code_content + "</pre>"));
		tinyMCEPopup.close();
	}
};

tinyMCEPopup.onInit.add(CodeDialog.init, CodeDialog);